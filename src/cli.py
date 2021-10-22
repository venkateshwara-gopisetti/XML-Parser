"""This module provides the CLI."""

import argparse
import pathlib
import sys
from os.path import splitext

from . import __version__
from .xml_to_json import XmlToJson

def main():
    args = parse_cmd_line_arguments()
    file = pathlib.Path(args.file)
    if not file.is_file():
        print("The specified file doesn't exist")
        sys.exit()
    if splitext(file)[-1] != 'xml':
        print("File provided is not of type XML.")
        sys.exit()
    worker = XmlToJson(file)
    result = worker.generate_json()
    worker.save_json(result)


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="xml-to-json",
        description="XML parser, a program to convert XML to JSON",
        epilog="Thanks for using XML Parser!",
    )
    parser.version = f"XML Parser v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "file",
        metavar="XML_FILE",
        nargs="?",
        default=".",
        help="Name of te XML file",
    )
    return parser.parse_args()
