from pydoc import locate
import json
from Config import ModelLeafConfig
from mrcnn.model import MaskRCNN

def train(args):
    # Retrieve arguments
    output = args.output
    dataset_keep = args.dataset_keep
    test_set = args.test_set
    config = args.config
    preview_only = args.preview_only
    dataset_class = args.dataset_class
    dataset_config_path = args.dataset_config
    epochs = args.epochs
    layers = args.layers

    # Create dataset
    DatasetClass = locate(dataset_class + '.' + dataset_class)
    dataset_config = None
    if dataset_config_path is not None:
        with open(dataset_config_path) as dataset_config_file:
            dataset_config = json.load(dataset_config_file).get(dataset_class)

    dataset_train = DatasetClass.from_config(dataset_config["train"])
    dataset_valid = DatasetClass.from_config(dataset_config["valid"])

    # todo: save dataset samples

    # Create model
    model = MaskRCNN(mode="training", config=ModelLeafConfig, model_dir=output)

    # Start training from
    # 1. COCO
    # 2. h5 pretrained
    # 3. scratch ? probably never

    # Start train
    model.train(dataset_train, dataset_valid, learning_rate=ModelLeafConfig.LEARNING_RATE, epochs=epochs, layers=layers)

def apply_class_configuration(class_instance, config_dict):
    for key, value in config_dict.items():
        setattr(class_instance, key, value)