import argparse
import os

from ._version import __version__
from .find import Property, Reference, make_find
from .rename import make_rename
from .root_by_document_path import (find_root_by_document_path,
                                    write_root_by_document_path)

find = make_find(find_root_by_document_path)
rename = make_rename(find_root_by_document_path)


def main():
    parser = argparse.ArgumentParser(
        description='Manage cross-document references to properties.')
    parser.add_argument('--version', action='version', version=__version__)
    subparsers = parser.add_subparsers(title='Commands',
                                       dest='command',
                                       required=True)

    find_parser = subparsers.add_parser('find',
                                        help='Find cross-document refrences to a property',
                                        usage='fcxlink find <document> <object> <property>')

    find_parser.add_argument(
        'document', help='Document name or label.')
    find_parser.add_argument('object', help='Object name or label.')
    find_parser.add_argument('property', help='Property.')

    rename_parser = subparsers.add_parser('rename',
                                          help='Rename cross-document refrences to a property',
                                          usage='fcxlink rename <from_document> <from_object> <from_property> <to_document> <to_object> <to_property>')

    rename_parser.add_argument(
        'from_document', help='Document name or label of reference to rename.')
    rename_parser.add_argument(
        'from_object', help='Object name or label of reference to rename.')
    rename_parser.add_argument(
        'from_property', help='Property of reference to rename.')
    rename_parser.add_argument(
        'to_document', help='Document name or label of reference to rename to.')
    rename_parser.add_argument(
        'to_object', help='Object name or label of reference to rename to.')
    rename_parser.add_argument(
        'to_property', help='Property of reference to rename to.')

    cwd = os.getcwd()
    args = parser.parse_args()

    args = vars(parser.parse_args())
    command = args.pop('command')
    if command == 'find':
        property = Property(args['document'], args['object'], args['property'])
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
    elif command == 'rename':
        from_property = Property(
            args['from_document'], args['from_object'], args['from_property'])
        to_property = Property(args['to_document'],
                               args['to_object'], args['to_property'])
        renamed_root_by_document_path = rename(cwd, from_property, to_property)
        document_paths = renamed_root_by_document_path.keys()
        num_documents = len(document_paths)
        if num_documents == 0:
            print('No documents contain references to {}.'.format(from_property))
        else:
            word = 'document' if num_documents == 1 else 'documents'
            print('The following {} {} references {}:'.format(
                num_documents, word, from_property))

            def format_document_path(document_path: str) -> str:
                beginning_path = cwd + os.path.sep
                return document_path.replace(beginning_path, '')
            print('  ' + '\n  '.join(map(format_document_path, document_paths)) + '\n')
            question = 'Do you wish to rename the references to {}?'.format(
                to_property)
            answer = query_yes_no(question, 'no')
            if answer:
                write_root_by_document_path(renamed_root_by_document_path)
                print('{} {} updated.'.format(num_documents, word))


def query_yes_no(question, default: str = 'yes'):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
    It must be "yes" (the default), "no" or None (meaning
    an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {'yes': True, 'y': True, 'ye': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('Invalid default answer "%s".' % default)

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print('Please respond with "yes" or "no" (or "y" or "n").\n')


if __name__ == '__main__':
    main()