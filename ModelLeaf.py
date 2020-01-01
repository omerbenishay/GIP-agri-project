import argparse
from ModelLeafInfer import infer
from ModelLeafTrain import train
from ModelLeafCut import cut
from ModelLeafInfo import info
from Reference import HelpReference


def main():
    # top level parser
    parser = argparse.ArgumentParser(description=HelpReference.description, add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help=HelpReference.help_description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')


    subparsers = parser.add_subparsers()
    # parser for train
    parser_train = subparsers.add_parser('train', help=HelpReference.TrainReference.description)
    parser_train.set_defaults(func=train)
    parser_train.add_argument('-o', '--output', help=HelpReference.TrainReference.output, default='./')
    parser_train.add_argument('-k', '--dataset-keep', type=int, help=HelpReference.TrainReference.dataset_keep, default=0)
    parser_train.add_argument('-t', '--test-set', help=HelpReference.TrainReference.test_set)
    parser_train.add_argument('-mc', '--model-config', help=HelpReference.TrainReference.config)
    parser_train.add_argument('-s', '--synthetic', choices=['random', 'grouped'], help=HelpReference.TrainReference.synthetic, default='grouped')
    parser_train.add_argument('-d', '--dataset-class', help=HelpReference.TrainReference.dataset_class, default='BananaDataset')
    parser_train.add_argument('-dc', '--dataset-config', help=HelpReference.TrainReference.dataset_config)
    parser_train.add_argument('--preview-only', type=int, help=HelpReference.TrainReference.preview_only)

    # parser for infer
    parser_infer = subparsers.add_parser('infer', help=HelpReference.InferReference.description)
    parser_infer.set_defaults(func=infer)
    parser_infer.add_argument('-o', '--output', help=HelpReference.InferReference.output, default='./')
    parser_infer.add_argument('--pictures-only', help=HelpReference.InferReference.pictures_only, action='store_true')
    parser_infer.add_argument('--contour-only', help=HelpReference.InferReference.contour_only, action='store_true')

    # parser for cut
    parser_cut = subparsers.add_parser('cut', help=HelpReference.CutReference.description)
    parser_cut.set_defaults(func=cut)
    parser_cut.add_argument('path', help=HelpReference.CutReference.path)
    parser_cut.add_argument('-o', '--output', help=HelpReference.CutReference.output)
    parser_cut.add_argument('-l', '--limit', type=int, help=HelpReference.CutReference.limit)
    parser_cut.add_argument('-n', '--normalize', type=int, help=HelpReference.CutReference.normalize)
    parser_cut.add_argument('-b', '--background', choices=['black', 'white', 'original', 'transparent'], help=HelpReference.CutReference.background, default='transparent')

    # parser for info
    parser_info = subparsers.add_parser('info', help=HelpReference.InfoReference.description)
    parser_info.add_argument('model_path', help=HelpReference.InfoReference.model_path)
    parser_info.set_defaults(func=info)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()