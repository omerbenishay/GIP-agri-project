import argparse
from ModelLeafInfer import infer
from ModelLeafTrain import train
from Reference import HelpReference

def main():
    # top level parser
    parser = argparse.ArgumentParser(description=HelpReference.description, add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help=HelpReference.help_description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')


    subparsers = parser.add_subparsers()
    # parser for train
    parser_train = subparsers.add_parser('train')
    parser_train.add_argument('-o', '--output', help=HelpReference.TrainReference.output, default='./')
    parser_train.add_argument('-k', '--dataset-keep', type=int, help=HelpReference.TrainReference.dataset_keep, default=0)
    parser_train.add_argument('-t', '--test-set', help=HelpReference.TrainReference.test_set)
    parser_train.add_argument('-c', '--config', help=HelpReference.TrainReference.config)
    parser_train.add_argument('-s', '--synthetic', choices=['random', 'grouped'], help=HelpReference.TrainReference.synthetic)
    parser_train.add_argument('--leaf-size-min', type=int, help=HelpReference.TrainReference.leaf_size_min)
    parser_train.add_argument('--leaf-size-max', type=int, help=HelpReference.TrainReference.leaf_size_max)
    parser_train.add_argument('--leaf-number-min', type=int, help=HelpReference.TrainReference.leaf_number_min)
    parser_train.add_argument('--leaf-number-max', type=int, help=HelpReference.TrainReference.leaf_number_max)
    parser_train.add_argument('--preview-only', type=int, help=HelpReference.TrainReference.preview_only)
    parser_train.set_defaults(func=train)

    # parser for infer
    parser_infer = subparsers.add_parser('infer')
    parser_infer.add_argument('-x', type=int, default=1)
    parser_infer.set_defaults(func=infer)

    # parser for cut
    parser_train = subparsers.add_parser('cut')
    # parser_train.add_argument('-y', type=int, default=2)
    parser_train.set_defaults(func=train)

    # parser for info
    parser_train = subparsers.add_parser('info')
    # parser_train.add_argument('-y', type=int, default=2)
    parser_train.set_defaults(func=train)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()