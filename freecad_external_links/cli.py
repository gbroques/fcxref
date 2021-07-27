import argparse
import os

from .find import Match, Reference, make_find
from .find_root_by_document_path import find_root_by_document_path

find = make_find(find_root_by_document_path)


def main():
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(
        description='Find cross-document references.')
    parser.add_argument(
        'document', help='Document name or label.')
    parser.add_argument('object', help='Object name or label.')
    parser.add_argument('property_name', help='Name of property.')
    args = parser.parse_args()
    ref = Reference(args.document, args.object, args.property_name)
    matches = find(cwd, ref)

    def format_match(match: Match) -> str:
        beginning_path = cwd + os.path.sep
        return str(match).replace(beginning_path, '')

    if matches:
        num_matches = len(matches)
        word = 'reference' if num_matches == 1 else 'references'
        print('{} {} to {} found:'.format(num_matches, word, ref))
        print('  ' + '\n  '.join(map(format_match, matches)))
    else:
        print('No references to {} found.'.format(ref))


if __name__ == '__main__':
    main()
