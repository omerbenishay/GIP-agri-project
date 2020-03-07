import os
from Config import ModelLeafConfig
from PIL import Image
import numpy as np
from tqdm import tqdm
from mrcnn import visualize
from skimage import measure
from matplotlib import cm
import json
from ModelLeafUtils import prompt_model

COLOR_MAP = "Blues"
CONTOUR_FILE_NAME = "contours.json"


def infer(args):
    from mrcnn.model import MaskRCNN
    infer_path = args.path
    output = args.output
    do_pictures = not args.no_pictures
    do_contours = not args.no_contours
    model_path = args.model
    should_save_masks = not args.no_masks
    compare_to_gt = args.gt != ""
    gt_dir = args.gt

    # Retrieve images
    images = generate_images(infer_path)

    # Retrieve model path
    model_path = prompt_model(model_path)

    # Load model
    inference_config = get_inference_config(ModelLeafConfig)
    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)
    model = MaskRCNN(mode="inference", config=inference_config, model_dir=output)
    model.load_weights(model_path, by_name=True)
    output_dir = os.path.join(model.log_dir, "inference")
    os.makedirs(output_dir, exist_ok=True)

    # Infer
    inference_dict = {}
    IoU_dict = {}
    for image_path in tqdm(list(images)):
        inference_dict[image_path] = []
        image_name = os.path.basename(image_path)
        image = np.array(Image.open(image_path))
        r = model.detect([image])[0]
        if should_save_masks:
            save_masks(r, output_dir, image_name)
        
        if do_pictures:
            output_file_path = os.path.join(output_dir, image_name)
            visualize.save_instances(image, r['rois'], r['masks'], r['class_ids'],
                                     ['BG', 'leave'], r['scores'], save_to=output_file_path,)
        
        if do_contours:
            inference_dict[image_path] = get_contours(r)
        
        if compare_to_gt:
            IoU_dict[image_path] = calculate_IoU(image_name, r['masks'], gt_dir)


    if do_contours:
        with open(os.path.join(output_dir, CONTOUR_FILE_NAME), 'w') as f:
            f.write(json.dumps(inference_dict, indent=2))


def save_masks(r, output_dir, image_name):
    masks_shape = r['masks'].shape
    image = np.zeros(masks_shape[:2], dtype='uint8')
    for i in range(masks_shape[-1]):
        mask = r['masks'][..., i]
        image += mask.astype('uint8') * i

    my_cm = cm.get_cmap(COLOR_MAP, masks_shape[-1] + 1)
    my_cm.set_bad(color='black')
    image = np.ma.masked_where(image == 0, image)
    image = np.uint8(my_cm(image) * 255)
    mask_image_name = ".".join(image_name.split('.')[:-1]) + "_mask.png"
    Image.fromarray(image).save(os.path.join(output_dir, mask_image_name))


def get_contours(r):
    contours = {}
    for i in range(r['masks'].shape[-1]):
        mask = r['masks'][..., i]
        # A mask might have multiple polygons
        mask_contours = measure.find_contours(mask, 0.5)
        # reshape in numpy then convert to list
        contours["leaf_{}".format(i)] = [np.reshape(c, (-1,)).tolist() for c in mask_contours]

    return contours


def generate_images(infer_path):
    if os.path.isdir(infer_path):
        for _, _, files in os.walk(infer_path):
            for file in files:
                if file.split(".")[-1].lower() in ['jpg', 'jpeg', 'png']:
                    yield os.path.join(infer_path, file)
    else:
        if infer_path.split(".")[-1].lower() in ['jpg', 'jpeg', 'png']:
            return [os.path.join(infer_path)]


def get_inference_config(config):
    """
    Alters a config class to make it suited for inference
    Alterations are not mandatory for the inference to work
    :param config: the config class
    :return: a modified config class
    """
    config.IMAGES_PER_GPU = 1
    config.GPU_COUNT = 1
    return config()


GROUND_TRUTH_MIN_SIZE_COEFF = 0.05  # 0.03    0.05
def calculate_IoU(image_name, detected_masks, ground_truth_dir, single_mask=True):
    # AZ start validation of single image
    # TODO - log/results file

    # get ground truth masks for this image
    # note: this should be done only once for each validation image (if train, do it once at the beginning, not after each epoch).
    image_name_prefix = image_name.split(".")[0] + "_GT_"
    num_gt_masks = 0
    h = detected_masks.shape[0]
    w = detected_masks.shape[1]
    gt_min_size = GROUND_TRUTH_MIN_SIZE_COEFF * GROUND_TRUTH_MIN_SIZE_COEFF * h * w
    gt_file_names = []
    gt_masks = np.zeros([h,w,num_gt_masks])
    for root, dirs, files in os.walk(ground_truth_dir):
        for i, file in enumerate(files):
            if file.startswith(image_name_prefix):
                # read GT file, and use the GT only if num_pixels in mask > Threshold
                tmp = np.array(Image.open(ground_truth_dir + file))
                tmp_size = np.count_nonzero(tmp)
                if tmp_size > gt_min_size:
                    num_gt_masks = num_gt_masks + 1
                    curr_gt_file = ground_truth_dir + file
                    curr_mask = np.array(Image.open(curr_gt_file))
                    gt_masks[:,:,i] = curr_mask

    
    # create empty IoU matrix M (num_ground_truth_masks x num detected_masks)
    # note: if validation during training - this should be done after each epoch.
    num_of_detected_masks = detected_masks.shape[2]
    all_iou = np.zeros(shape=[num_gt_masks, num_of_detected_masks])

    # fill IoU matrix
    # for each mask m1 in ground truth
    #   for each mask m2 in detected
    #       M(m1,m2) = IoU(m1,m2)
    for i in range(num_gt_masks):
        mask_i = gt_masks[:,:,i]
        for j in range(num_of_detected_masks):
            mask_j = detected_masks[:,:,j]
            intersection = np.logical_and(mask_i,mask_j)
            union = np.logical_or(mask_i,mask_j)
            numI = np.count_nonzero(intersection)
            numU = np.count_nonzero(union)
            all_iou[i,j] = numI/numU

    # calculate total (or average) IoU
    curr_score = 0
    for i in range(num_gt_masks):
        # find max value and indices of max value
        max_iou = np.amax(all_iou)
        curr_score = curr_score + max_iou
        max_idx = np.argmax(all_iou)
        max_idx_row, max_idx_col = divmod(max_idx, all_iou.shape[1])

        # remove row/col of max value (set zeros)
        for j in range(all_iou.shape[1]):
            all_iou[max_idx_row,j] = 0
        for j in range(all_iou.shape[0]):
            all_iou[j,max_idx_col] = 0

    if num_gt_masks > 0:
        curr_score = curr_score / num_gt_masks
    else:
        curr_score = 1

    return curr_score
    # AZ end validation of single image


if __name__ == "__main__":
    print(prompt_model("/home/nomios/Documents/Projects"))
