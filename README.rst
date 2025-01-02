fcxref
======

|version badge| |downloads badge|

.. |version badge| image:: https://badge.fury.io/py/fcxref.svg
   :alt: PyPI version
   :target: https://badge.fury.io/py/fcxref

.. |downloads badge| image:: https://img.shields.io/pypi/dm/fcxref
   :alt: PyPI - Downloads

----

* `Introduction`_
* `Motivation`_
* `Approach`_
* `Installation`_
* `Usage`_
* `Python API`_
* `Command Line`_
* `Supported FreeCAD Versions`_
* `Changelog`_
* `Contributing`_

Introduction
------------

Manages **F**\ ree\ **C**\ AD e\ **x**\ ternal **ref**\ erences.

"External references" are also known as external links or cross-document references.

The following operations are supported:

1. *Finding* external references
2. *Renaming* external references
3. and *Removing* external references (i.e. ``XLinks``)

Motivation
----------

On `Expressions: Known issues / remaining tasks <https://wiki.freecadweb.org/Expressions#Known_issues_.2F_remaining_tasks>`_, it's mentioned:

    There is no expression manager implemented where all expressions in a document are listed, and can be created, deleted, queried, etc.

Large complex FreeCAD projects typically rely on extensive use of cross-document referencing to properties such as aliases in spreadsheets.

When you have dozens of references to the same property, it becomes very difficult to find all the places where references exist or rename the property.

``fcxref`` aims to fill this gap until similiar functionality can be added to FreeCAD core.

See the following related FreeCAD forum discussions for additional motivation:

* `Expression engine - Automatic renaming <https://forum.freecadweb.org/viewtopic.php?t=18049>`_
* `Rename a file containing external links <https://forum.freecadweb.org/viewtopic.php?p=471267>`_

Approach
--------
``fcxref`` relies on parsing the ``Document.xml`` in compressed ``.FCStd`` files.

Installation
------------

Available on the `Python Package Index (PyPI) <https://pypi.org/project/fcxref/>`_.

.. code-block::

   pip install fcxref

Usage
-----
There are two ways to use ``fcxref``:

1. via the Python API
2. vai the Command Line

The following 2 sections cover these 2 usage methods with documents in the ``example/`` directory.

Consider you have a ``MainDocument.FCStd`` containing a spreadsheet that drives your model,
and ``ExampleDocument.FCStd`` that references aliases in that spreadsheet.

Python API
----------

find
^^^^

.. code-block:: python

   from fcxref import find, Query
   
   base_path = './example'
   references = find(base_path, Query('MainDocument', 'Spreadsheet', 'Value'))
   print('\n'.join(map(str, references)))

.. code-block::

   MainDocument Spreadsheet.A1 'Value content indirect
   MainDocument Spreadsheet.B1 Value alias source
   MainDocument Spreadsheet.B2 =Value content indirect
   MainDocument Box.Height Cylinder.Value expression indirect
   MainDocument Box.Length Spreadsheet.Value expression indirect
   MainDocument Box.Width <<Spreadsheet>>.Value expression indirect
   ExampleDocument Spreadsheet.B1 =MainDocument#Spreadsheet.Value content direct
   ExampleDocument Spreadsheet.A1 'Value content indirect
   ExampleDocument Spreadsheet.B1 Value alias indirect
   ExampleDocument Box.Length Spreadsheet.Value expression indirect


rename
^^^^^^

The ``rename`` function takes:

1. the base path to look for FreeCAD documents in
2. the name or label of the document
3. the name or label of the object
4. and a 2-element tuple containing the property before and after renaming. 

It returns a dictionary where keys are filepaths to updated ``.FCStd`` files,
and values are XML `Element`_ objects representing updated ``Document.xml`` files.

.. _Element: https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element

.. code-block:: python

   from fcxref import rename
   
   base_path = './example'
   root_by_document_path = rename(base_path, 'MainDocument', 'Spreadsheet', ('Value', 'RenamedValue'))
   print(root_by_document_path)

.. code-block::

   {'ExampleDocument.FCStd': <Element 'Document' at 0x7efcd281cc20>, 'MainDocument.FCStd': <Element 'Document' at 0x7f4d13c39270>}

remove
^^^^^^

The ``remove`` function takes:

1. the base path to look for FreeCAD documents in
2. the name of the document (**label is not supported**)

It returns a dictionary where keys are filepaths to updated ``.FCStd`` files,
and values are XML `Element`_ objects representing updated ``Document.xml`` files.

.. code-block:: python

   from fcxref import remove
   
   base_path = './example'
   root_by_document_path = remove(base_path, 'MainDocument')
   print(root_by_document_path)

.. code-block::

   {'ExampleDocument.FCStd': <Element 'Document' at 0x7efcd281cc20>}

Command Line
------------
Upon `installing <#installation>`_ ``fcxref``, the ``fcxref`` command will become globally accessible.

For usage information, pass ``--help`` to each command.

Each command scans for ``*.FCStd`` files recursively from the current working directory.

Thus, you should navigate to a directory where you store your FreeCAD documents before executing ``fcxref`` commands.

.. code-block::

   $ fcxref --help ↵
   usage: fcxref [-h] [--version] {find,rename,remove} ...
   
   Manage cross-document references to properties.
   
   optional arguments:
     -h, --help            show this help message and exit
     --version             show program's version number and exit
   
   Commands:
     {find,rename,remove}
       find                Find cross-document references to an object or property
       rename              Rename cross-document references to a property
       remove              Remove XLinks to specified document

find
^^^^

.. code-block::

   $ fcxref find --help ↵                
   usage: fcxref find <document> <object> [property]
   
   Surround arguments containing special characters in quotes (e.g. "<<My Label>>").
   
   positional arguments:
     document    Document name or label.
     object      Object name or label.
     property    Property.
   
   optional arguments:
     -h, --help  show this help message and exit

Simple Queries
""""""""""""""

.. code-block::
   
   $ fcxref find MainDocument Spreadsheet Value ↵
   MainDocument Spreadsheet.A1 'Value content indirect
   MainDocument Spreadsheet.B1 Value alias source
   MainDocument Spreadsheet.B2 =Value content indirect
   MainDocument Box.Height Cylinder.Value expression indirect
   MainDocument Box.Length Spreadsheet.Value expression indirect
   MainDocument Box.Width <<Spreadsheet>>.Value expression indirect
   ExampleDocument Spreadsheet.B1 =MainDocument#Spreadsheet.Value content direct
   ExampleDocument Spreadsheet.A1 'Value content indirect
   ExampleDocument Spreadsheet.B1 Value alias indirect
   ExampleDocument Box.Length Spreadsheet.Value expression indirect

💡 **TIP:** When using special characters on the command line such as ``<`` and ``>`` for label names, surround the argument in double-quotes.

rename
^^^^^^

.. code-block::

   $ fcxref rename --help ↵
   usage: fcxref rename <document> <object> <from_property> <to_property>
   
   Surround arguments containing special characters in quotes (e.g. "<<My Label>>").
   
   positional arguments:
     document       Document name or label of reference to rename.
     object         Object name or label of reference to rename.
     from_property  Property of reference before renaming.
     to_property    Property of reference after renaming.
   
   optional arguments:
     -h, --help     show this help message and exit


Simple Renames
""""""""""""""

The ``rename`` command will prompt users for confirmation before modifying any files,
and defaults to "No" if an explicit "Yes" is not provided.

.. code-block::

   $ fcxref rename MainDocument Spreadsheet Value RenamedValue ↵
   The following 2 document(s) reference MainDocument#Spreadsheet.Value:
     ExampleDocument.FCStd
     MainDocument.FCStd
   
   Do you wish to rename references to MainDocument#Spreadsheet.RenamedValue? [y/N] 
   y ↵
   2 document(s) updated.

remove
^^^^^^

.. code-block::

   $ fcxref remove --help ↵
   usage: fcxref remove <document>
   
   Surround arguments containing special characters in quotes (e.g. "<<My Label>>").
   
   positional arguments:
     document    Document name of XLinks to remove.
   
   optional arguments:
     -h, --help  show this help message and exit

Simple Removals
"""""""""""""""

The ``remove`` command will prompt users for confirmation before modifying any files,
and defaults to "No" if an explicit "Yes" is not provided.

.. code-block::

   $ fcxref remove MainDocument ↵
   The following 1 document(s) contain XLinks to MainDocument:
     example/ExampleDocument.FCStd

   Do you wish to remove XLinks to MainDocument? (this will break document linking) [y/N] 
   y ↵
   1 document(s) updated.

Supported FreeCAD Versions
--------------------------
Currently only FreeCAD 1.0 and greater is supported.

If changes are minimal, then supporting older versions may be considered.

Changelog
---------
See `Changelog <./CHANGELOG.rst>`__.

Contributing
------------
See `Contributing Guidelines <./CONTRIBUTING.rst>`_.
