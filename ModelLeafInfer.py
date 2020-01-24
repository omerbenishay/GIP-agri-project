import os
from mrcnn.model import MaskRCNN
from Config import ModelLeafConfig
from questionary import select
from PIL import Image
import numpy as np
from tqdm import tqdm
from mrcnn import visualize
from skimage import measure
from matplotlib import cm

COLOR_MAP = "Blues"


def infer(args):
    infer_path = args.path
    output = args.output
    do_pictures = args.pictures_only  # todo: change to negate
    do_contours = args.contour_only  # todo: change to negate
    model_path = args.model

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
    for image_path in tqdm(list(images)):
        inference_dict[image_path] = []
        image_name = os.path.basename(image_path)
        image = np.array(Image.open(image_path))
        r = model.detect([image])[0]
        save_masks(r, output_dir, image_name)  # todo: implement
        # display_top_masks(image, mask, class_ids, class_names, limit=4):
        if do_pictures:
            output_file_path = os.path.join(output_dir, image_name)
            visualize.save_instances(image, r['rois'], r['masks'], r['class_ids'],
                                     ['BG', 'leaf'], r['scores'], save_to=output_file_path)
        if do_contours:
            inference_dict[image_path].append(get_contours(r))


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


def get_contours(r, output_dir, image_name):
    contours = {}
    for i in range(r['masks'].shape[-1]):
        mask = r[..., i]
        contours[str(i)] = list(measure.find_contours(mask, 0.5))

    return contours


def get_contour_from_mask(mask_array):
    return []


def prompt_model(path):
    """
    Generate a correct .h5 model path. If the path is a directory, prompts the user for
    a correct path.
    This function recursively calls itself until a .h5 file is returned
    :param path: The specified path
    :return: the resulting path from prompt
    """
    if path.split('.')[-1] == "h5":
        return path
    if os.path.isfile(path):
        return '..'

    choices = os.listdir(path) + ['..']
    my_question = 'Select the model you want to use for inference'
    response = None
    while response is None or response == '..':
        next_dir = select(my_question, choices).ask()
        if next_dir == '..':
            return '..'
        response = prompt_model(os.path.join(path, next_dir))
    return response


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


if __name__ == "__main__":
    prompt_model("/home/nomios/Documents/Projects")
