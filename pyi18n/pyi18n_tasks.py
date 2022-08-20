from argparse import ArgumentParser

try:
    from pyi18n.tasks import normalize
except ImportError:
    from tasks import normalize


def cli() -> None:
    parser = ArgumentParser()
    parser.add_argument("normalize", help="Sort locales in alphabetical order")
    parser.add_argument("-p", "--path", help="Path to locales",
                        default="locales", type=str, required=False)

    args = parser.parse_args()
    if args.normalize:
        normalize.normalize_locales(args.path)
