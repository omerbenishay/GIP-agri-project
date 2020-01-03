from pydoc import locate
import json
from Config import ModelLeafConfig
from mrcnn.model import MaskRCNN
from mrcnn import utils
import numpy as np
from PIL import Image
import os
from DatasetUtils import mask_to_image
from tqdm import tqdm
from datetime import datetime


def train(args):
    # Retrieve arguments
    output = args.output
    samples_number = args.dataset_keep
    # test_set = args.test_set
    preview_only = args.preview_only
    dataset_class_name = args.dataset_class
    dataset_config_path = args.dataset_config
    epochs = args.epochs
    layers = args.layers
    pretrain = args.pretrain

    # Assemble output directories
    train_output_dir = os.path.join(output, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
    model_output_dir = os.path.join(train_output_dir, "model")
    if not os.path.exists(model_output_dir):
        os.makedirs(model_output_dir, exist_ok=True)
    samples_output_dir = os.path.join(train_output_dir, "samples")

    # Create dataset
    dataset_class = locate(dataset_class_name + '.' + dataset_class_name)
    dataset_config = None
    if dataset_config_path is not None:
        with open(dataset_config_path) as dataset_config_file:
            dataset_config = json.load(dataset_config_file).get(dataset_class_name)

    train_config = ModelLeafConfig()
    dataset_train = dataset_class.from_config(dataset_config["train"], train_config.IMAGE_SHAPE[0], train_config.IMAGE_SHAPE[1])
    dataset_valid = dataset_class.from_config(dataset_config["valid"], train_config.IMAGE_SHAPE[0], train_config.IMAGE_SHAPE[1])

    # Save train samples
    if samples_number != 0:
        save_samples(dataset_train, samples_number, path=samples_output_dir)

    if preview_only:
        return  # finish here
    
    # Create model
    model = MaskRCNN(mode="training", config=train_config, model_dir=model_output_dir)

    # Start training from COCO or from previously trained model
    if pretrain == "COCO":
        load_coco_weights(model)
    else:
        model.load_weights(pretrain, by_name=True)

    # Start train
    model.train(dataset_train, dataset_valid, learning_rate=train_config.LEARNING_RATE, epochs=epochs, layers=layers)


def apply_class_configuration(class_instance, config_dict):
    for key, value in config_dict.items():
        setattr(class_instance, key, value)


def save_samples(dataset, n=10, path="./"):
    """
    :params dataset: dataset instance
    :param n: number of samples to create
    :param path: absolute path to store the samples at
    """
    os.makedirs(path, exist_ok=True)
        
    image_ids = np.random.choice(dataset.image_ids, n)
    print("Saving {} samples to {}".format(n, path))
    for image_id in tqdm(image_ids):
        image = dataset.load_image(image_id)
        mask, _ = dataset.load_mask(image_id)
        image_path = os.path.join(path, "{}_image.png".format(image_id))
        Image.fromarray(image).save(image_path)
        mask_path = os.path.join(path, "{}_msk.png".format(image_id))
        Image.fromarray(mask_to_image(mask)).convert("RGB").save(mask_path)


def load_coco_weights(model, dir_path="models"):
    """
    :param model:       MaskRCNN model instance to load model to
    :param dir_path:    Directory to check for existing coco pretrain file
                        or to download it to
    """
    pretrain_file_path = os.path.join(dir_path, "mask_rcnn_coco.h5")
    if not os.path.exists(pretrain_file_path):
        os.makedirs(os.path.dirname(pretrain_file_path), exist_ok=True)
        utils.download_trained_weights(pretrain_file_path)

    model.load_weights(pretrain_file_path, by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])

