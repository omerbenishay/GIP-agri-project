from ModelLeafUtils import prompt_model, get_metadata_dict_from_h5, add_metadata_dict_to_h5


def info(args):
    model_path = args.model_path
    model_path = prompt_model(model_path)

    my_dict = {
        "yossi": "super",
        "hello": "world"
    }
    add_metadata_dict_to_h5(model_path, "my_dict", my_dict)
    resulted_dict = get_metadata_dict_from_h5(model_path, "my_dict")
    print(resulted_dict)


if __name__ == "__main__":
    info()
