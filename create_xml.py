#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path
from typing import List
import xml.etree.ElementTree as et

import submissions
# import collaborations
# import organizations
# import people
from builder import AuthorListXMLBuilder
from xml_utils import pretty_print

__author__ = 'Zane Gerber'
__maintainer__ = 'Zane Gerber'
__email__ = 'zane.gerber@utah.edu'
__status__ = 'Development'


def parse_user_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='create_xml.py',
        description="Convert author list CSV to XML using INSPIRE HEP standards.",
        epilog="Report bugs to Z. Gerber (zane.gerber@utah.edu)")
    parser.add_argument('infile', type=str, help="Full path to authorlist.csv")
    parser.add_argument('publication_reference', type=str, help="Internal report, arXiv ID, DOI, or title")
    parser.add_argument('-m', '--multi-collab', action="store_true", help="Support for multi-collab (not yet implemented)")
    parser.add_argument('-p', '--pretty', action="store_false", help="Disable pretty-printing of output XML")
    return parser.parse_args()


def load_author_csv_list(filename: Path) -> List[dict]:
    try:
        with open(filename, newline='') as csvfile:
            return list(csv.DictReader(csvfile))
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []


def save_xml(tree: et.ElementTree, output_file: Path, pretty: bool) -> None:
    with open(output_file, "wb") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE collaborationauthorlist SYSTEM "author.dtd">'.encode('utf8'))
        if pretty:
            pretty_print(tree.getroot())
        tree.write(f, 'utf-8')


def main():
    args = parse_user_args()
    author_list = load_author_csv_list(Path(args.infile))
    if not author_list:
        return

    builder = AuthorListXMLBuilder(author_list, args.publication_reference)
    tree = builder.build_tree()
    date_str = submissions.Submission(args.publication_reference).creation_date_str.replace('-', '')
    out_dir = Path(__file__).resolve().parent / date_str
    out_dir.mkdir(exist_ok=True)
    output_file = out_dir / f"{args.publication_reference.replace(' ', '')}.{date_str}.authorlist.xml"
    save_xml(tree, output_file, args.pretty)


if __name__ == "__main__":
    main()
