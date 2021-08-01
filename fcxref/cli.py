import argparse
import os

from ._version import __version__
from .find import Property, Reference, make_find
from .group_references_by_document_path import \
    group_references_by_document_path
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
                                        help='Find cross-document references to a property',
                                        description='Surround arguments containing special characters in quotes (e.g. "<<My Label>>").',
                                        usage='fcxlink find <document> <object> <property>')

    find_parser.add_argument(
        'document', help='Document name or label.')
    find_parser.add_argument('object', help='Object name or label.')
    find_parser.add_argument('property', help='Property.')

    rename_parser = subparsers.add_parser('rename',
                                          help='Rename cross-document references to a property',
                                          description='Surround arguments containing special characters in quotes (e.g. "<<My Label>>").',
                                          usage='fcxlink rename <document> <object> <from_property> <to_property>')

    rename_parser.add_argument(
        'document', help='Document name or label of reference to rename.')
    rename_parser.add_argument(
        'object', help='Object name or label of reference to rename.')
    rename_parser.add_argument(
        'from_property', help='Property of reference before renaming.')
    rename_parser.add_argument(
        'to_property', help='Property of reference after renaming.')

    cwd = os.getcwd()
    args = parser.parse_args()

    args = vars(parser.parse_args())
    command = args.pop('command')
    if command == 'find':
        property = Property(args['document'], args['object'], args['property'])
        references = find(cwd, property)

        def format_reference(reference: Reference) -> str:
            formatted_reference = str(reference)
            word = 'direct' if str(property) == reference.match else 'indirect'
            formatted_reference += ' [{}]'.format(word)
            return formatted_reference

        num_references = len(references)
        if num_references > 0:
            references_by_document_path = group_references_by_document_path(
                references)
            for document_path, references in references_by_document_path.items():
                beginning_path = cwd + os.path.sep
                formatted_path = str(document_path).replace(beginning_path, '')
                print(formatted_path)
                print('  ' + '\n  '.join(map(format_reference, references)))
                print('')
            num_documents = len(references_by_document_path.items())
            word = 'reference' if num_references == 1 else 'references'
            print('{} {} to {} across {} document(s) found.'.format(
                num_references, word, property, num_documents))
        else:
            print('No references to {} found.'.format(property))
    elif command == 'rename':
        renamed_root_by_document_path = rename(cwd,
                                               args['document'],
                                               args['object'],
                                               (args['from_property'], args['to_property']))
        from_property = Property(
            args['document'], args['object'], args['from_property'])
        to_property = Property(
            args['document'], args['object'], args['to_property'])
        document_paths = renamed_root_by_document_path.keys()
        num_documents = len(document_paths)
        if num_documents == 0:
            print('No documents contain references to {}.'.format(from_property))
        else:
            print('The following {} document(s) reference {}:'.format(
                num_documents, from_property))

            def format_document_path(document_path: str) -> str:
                beginning_path = cwd + os.path.sep
                return document_path.replace(beginning_path, '')
            print('  ' + '\n  '.join(map(format_document_path, document_paths)) + '\n')
            question = 'Do you wish to rename references to {}?'.format(
                to_property)
            answer = query_yes_no(question, 'no')
            if answer:
                write_root_by_document_path(renamed_root_by_document_path)
                print('{} document(s) updated.'.format(num_documents))


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
