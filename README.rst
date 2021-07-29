fcxref
======
Manages **F**\ ree\ **C**\ AD e\ **x**\ ternal **ref**\ erences.

"External references" are also known as external links or cross-document references.

The following operations are supported:

1. *Finding* external references
2. *Renaming* external references
3. and *Removing* external references

Motivation
----------

On `Expressions: Known issues / remaining tasks <https://wiki.freecadweb.org/Expressions#Known_issues_.2F_remaining_tasks>`_, it's mentioned:

    There is no expression manager implemented where all expressions in a document are listed, and can be created, deleted, queried, etc.

Large complex projects in FreeCAD will typically rely on extensive use of cross-document referencing to objects such as aliases in spreadsheets.

When you have dozens of references to the same property, it becomes very difficult to find all the places where references exist to the property or rename the property.

``fcxref`` aims to fill this gap until similiar functionality can be added to FreeCAD core.

See the following related FreeCAD forum discussions for additional motivation:

* `Expression engine - Automatic renaming <https://forum.freecadweb.org/viewtopic.php?t=18049>`_
* `Rename a file containing external links <https://forum.freecadweb.org/viewtopic.php?p=471267>`_

Approach
--------
``fcxref`` relies on parsing the ``Document.xml`` in compressed ``.FCStd`` files.

Python API
----------

find
^^^^

Simple Queries
""""""""""""""

.. code-block:: python

   from fcxref import find, Property
   
   base_path = './base/path/to/freecad/documents'
   references = find(base_path, Property('Master', 'Spreadsheet', 'Value'))
   print(references)

.. code-block::

   [Example.FCStd Spreadsheet.B1 (cells), Example.FCStd Cylinder.Radius (ExpressionEngine)]

The above example represents ``Example.FCStd`` contains two references to ``Master#Spreadsheet.Value``:

1. In B1 of the ``Spreadsheet``.
2. In the expression of ``Cylinder.Radius``.

Regular Expressions
"""""""""""""""""""

You can pass in regular expressions for the document, object, or property name for more powerful expressions.

For example, query all external references to the ``Spreadsheet`` object in ``Master``:

.. code-block:: python

   from fcxref import find, Property
      
   base_path = './base/path/to/freecad/documents'
   references = find(base_path, Property('Master', 'Spreadsheet', '.*'))


Command Line
------------
Upon installing ``fcxref``, the ``fcxref`` command will become globally accessible.

For usage information, pass ``--help`` to each command.

Each command scans for ``*.FCStd`` files recursively from the current working directory.

Thus, you should navigate to a directory where you store your FreeCAD documents before executing ``fcxref`` commands.

.. code-block::

   $ fcxref --help ↵
   usage: fcxref [-h] [--version] {find,rename} ...
   
   Manage cross-document references to properties.
   
   optional arguments:
     -h, --help     show this help message and exit
     --version      show program's version number and exit
   
   Commands:
     {find,rename}
       find         Find cross-document references to a property
       rename       Rename cross-document references to a property

find
^^^^

.. code-block::

   $ fcxref find --help ↵                
   usage: fcxlink find <document> <object> <property>
   
   positional arguments:
     document    Document name or label.
     object      Object name or label.
     property    Property.
   
   optional arguments:
     -h, --help  show this help message and exit

Simple Queries
""""""""""""""

.. code-block::
   
   $ fcxref find Master Spreadsheet Value ↵
   2 references to Master#Spreadsheet.Value found:
     Example.FCStd Spreadsheet.B1 (cells)
     Example.FCStd Cylinder.Radius (ExpressionEngine)

Regular Expressions
"""""""""""""""""""

Regular expressions for more powerful queries are also supported:

.. code-block::

   $ fcxref find Master Spreadsheet ".*" ↵
   3 references to Master#Spreadsheet..* found:
   Example.FCStd Spreadsheet.B1 (cells) -> Master#Spreadsheet.Value
   Example.FCStd Cylinder.Radius (ExpressionEngine) -> Master#Spreadsheet.Value
   AnotherExample.FCStd Spreadsheet.A1 (cells) -> Master#Spreadsheet.AnotherValue

Supported FreeCAD Versions
--------------------------
Currently only FreeCAD 19 and greater is supported.

If changes are minimal, then supporting older versions may be considered.

Contributing
------------
See `Contributing Guidelines <./CONTRIBUTING.rst>`_.
