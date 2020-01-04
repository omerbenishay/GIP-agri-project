import os
from mrcnn.model import MaskRCNN
from Config import ModelLeafConfig

def infer(args):
    infer_path = args.path
    output = args.output
    pictures_only = args.pictures_only
    contour_only = args.contour_only

    # Retrieve images
    images = generate_images(infer_path)

    # Load model
    inference_config = get_inference_config(ModelLeafConfig)
    model = MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)


def generate_images(infer_path):
    if os.path.isdir(infer_path):
        for _, _, file in os.walk(infer_path):
            if file.split(".")[-1].lower() in ['jpg', 'jpeg', 'png']:
                yield os.path.join(infer_path, file)
    else:
        if infer_path.split(".")[-1].lower() in ['jpg', 'jpeg', 'png']:
            return [os.path.join(infer_path)]


def get_inference_config(config):
    """
    specify here the changes to make to an inference config class
    :param config: the config class
    :return: a modified config class
    """
    config.IMAGES_PER_GPU = 1
    config.GPU_COUNT = 1
    return config()
