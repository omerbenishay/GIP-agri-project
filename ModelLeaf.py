import argparse
from ModelLeafInfer import infer

def main():
    # top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # parser for infer
    parser_infer = subparsers.add_parser('infer')
    parser_infer.add_argument('-x', type=int, default=1)
    parser_infer.set_defaults(func=infer)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()