from pydoc import locate
import json

def train(args):
    # Retrieve arguments
    output = args.output
    dataset_keep = args.dataset_keep
    test_set = args.test_set
    config = args.config
    preview_only = args.preview_only
    dataset_class = args.dataset_class
    dataset_config_path = args.dataset_config

    """
    parser_train.add_argument('-o', '--output', help=HelpReference.TrainReference.output, default='./')
    parser_train.add_argument('-k', '--dataset-keep', type=int, help=HelpReference.TrainReference.dataset_keep, default=0)
    parser_train.add_argument('-t', '--test-set', help=HelpReference.TrainReference.test_set)
    parser_train.add_argument('-c', '--config', help=HelpReference.TrainReference.config)
    parser_train.add_argument('-s', '--synthetic', choices=['random', 'grouped'], help=HelpReference.TrainReference.synthetic, default='grouped')
    parser_train.add_argument('-dc', '--dataset-class', help=HelpReference.TrainReference.dataset_class, default='BananaDataset')
    parser_train.add_argument('--leaf-size-min', type=int, help=HelpReference.TrainReference.leaf_size_min)
    parser_train.add_argument('--leaf-size-max', type=int, help=HelpReference.TrainReference.leaf_size_max)
    parser_train.add_argument('--leaf-number-min', type=int, help=HelpReference.TrainReference.leaf_number_min)
    parser_train.add_argument('--leaf-number-max', type=int, help=HelpReference.TrainReference.leaf_number_max)
    parser_train.add_argument('--preview-only', type=int, help=HelpReference.TrainReference.preview_only)
    """

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
    train_config = 
    model = 

def apply_class_configuration(class_instance, config_dict):
    for key, value in config_dict.items():
        setattr(class_instance, key, value)