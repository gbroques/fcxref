import argparse
import os

from .find import Property, Reference, make_find
from .find_root_by_document_path import find_root_by_document_path

find = make_find(find_root_by_document_path)


def main():
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(
        description='Find cross-document references to a property.')
    parser.add_argument(
        'document', help='Document name or label.')
    parser.add_argument('object', help='Object name or label.')
    parser.add_argument('property_name', help='Name of property.')
    args = parser.parse_args()
    property = Property(args.document, args.object, args.property_name)
    references = find(cwd, property)

    def format_reference(reference: Reference) -> str:
        beginning_path = cwd + os.path.sep
        formatted_reference = str(reference).replace(beginning_path, '')
        if str(property) != reference.match:
            formatted_reference += ' -> ' + reference.match
        return formatted_reference

    if references:
        num_references = len(references)
        word = 'reference' if num_references == 1 else 'references'
        print('{} {} to {} found:'.format(num_references, word, property))
        print('  ' + '\n  '.join(map(format_reference, references)))
    else:
        print('No references to {} found.'.format(property))


if __name__ == '__main__':
    main()
