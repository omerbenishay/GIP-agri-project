from ModelLeafUtils import prompt_model, get_metadata_dict_from_h5
from ModelLeafTrain import CONFIG_METADATA_NAME


def info(args):
    model_path = args.model_path
    model_path = prompt_model(model_path)

    resulted_dict = get_metadata_dict_from_h5(model_path, CONFIG_METADATA_NAME)
    print(resulted_dict)


if __name__ == "__main__":
    info()
