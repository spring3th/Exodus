import importlib
import pathlib
from argparse import Namespace, ArgumentParser

from src import __version__
from src.util.default_root import DEFAULT_ROOT_PATH


SUBCOMMANDS = [
    "init",
    "keys",
    "show",
    "start",
    "stop",
    "version",
    "netspace",
    "run_daemon",
]


def create_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        description="Manage exodus blockchain infrastructure (%s)." % __version__,
        epilog="Try 'exodus start node', 'exodus netspace -d 48', or 'exodus show -s'.",
    )

    parser.add_argument(
        "-r",
        "--root-path",
        help="Config file root (defaults to %s)." % DEFAULT_ROOT_PATH,
        type=pathlib.Path,
        default=DEFAULT_ROOT_PATH,
    )

    subparsers = parser.add_subparsers()

    # this magic metaprogramming generalizes:
    #   from src.cmds import version
    #   new_parser = subparsers.add_parser(version)
    #   version.version_parser(new_parser)

    for subcommand in SUBCOMMANDS:
        mod = importlib.import_module("src.cmds.%s" % subcommand)
        mod.make_parser(subparsers.add_parser(subcommand))  # type: ignore

    parser.set_defaults(function=lambda args, parser: parser.print_help())
    return parser


def exodus(args: Namespace, parser: ArgumentParser):
    return args.function(args, parser)


def main():
    parser = create_parser()
    args = parser.parse_args()
    return exodus(args, parser)


if __name__ == "__main__":
    main()
