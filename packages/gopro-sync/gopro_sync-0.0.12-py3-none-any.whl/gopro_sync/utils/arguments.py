from argparse import ArgumentParser


def argparsing():
    parser = ArgumentParser(
        prog="gopro-sync",
        description="Syncronize your GoPro videos easly.",
        usage="gopro-sync PROJECT [-i IN_FOLDER] [-o OUT_FOLDER]",
        epilog="Example: gopro-sync Summer23 -o Videos --no-lrv --save-thm",
    )
    parser.add_argument("name", type=str, help="project name", metavar=("PROJECT"))
    parser.add_argument(
        "-i",
        type=str,
        help="input folder. Default: current folder",
        metavar=("IN_FOLDER"),
    )
    parser.add_argument(
        "-o",
        type=str,
        help="output folder. Default: current folder",
        metavar=("OUT_FOLDER"),
    )
    parser.add_argument(
        "--no-lrv",
        action="store_true",
        help="do NOT save .LRV (Low Resolution Video) files",
    )
    parser.add_argument(
        "--save-thm",
        action="store_true",
        help="save .THM (video thumbnails) files",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="test run to check if everything is correct",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="script version",
        action="version",
        version="gopro-sync v0.0.12",
    )
    return parser.parse_args()
