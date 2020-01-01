from pydoc import locate

def train(args):
    # Retrieve arguments
    dataset_class = args.dataset_class
    DatasetClass = locate(dataset_class + '.' + dataset_class)
    
    dataset_train = DatasetClass(TRAIN_DIR_OBJECTS, TRAIN_DIR_BACKGROUNDS, MINIMUM_NUMBER_OF_LEAVES,
                                 MAXIMUM_NUMBER_OF_LEAVES)
    dataset_train.load_shapes(NUMBER_TRAIN_IMAGES, train_config.IMAGE_SHAPE[0], train_config.IMAGE_SHAPE[1])
    dataset_train.prepare()
    print("train {}".format(args.y))

def apply_class_configuration(class_instance, config_dict):
    for key, value in config_dict.items():
        setattr(class_instance, key, value)