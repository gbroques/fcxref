Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

`[Unreleased]`__
----------------

`[0.4.0]`__ - 2025-01-01
------------------------

Changed
^^^^^^^
* Renamed ``Property`` class to ``Query`` (**breaking change**).

  * The 3rd argument, ``property_name``, is now optional.

* Simplify ``find`` CLI output.
* ``find`` usages within the same spreadsheet (see `#4 <https://github.com/gbroques/fcxref/issues/4>`_).

Added
^^^^^
* Ability to remove ``XLink`` references to a specified document name.
* Ability to find cross-document references to objects.
* Add `--debug` flag to CLI for debug logging.

`[0.3.1]`__ - 2021-08-09
------------------------
Fixed
^^^^^
* Fixed *not* including all packages in PyPI installation (see `#3 <https://github.com/gbroques/fcxref/issues/3>`_).

`[0.3.0]`__ - 2021-08-01
------------------------

Fixed
^^^^^
* Fixed renaming ``.FCStd`` files and losing all files besides ``Document.xml``.

  * Examples of files being lost include ``GuiDocument.xml``, ``*.brp`` files, and others.
  * The net-effect of this was that objects were hidden upon opening in FreeCAD after renaming.

`[0.2.0]`__ - 2021-08-01
------------------------

Added
^^^^^
* Ability to find "indirect" text references to properties.

  * When a spreadsheet cell or alias contains the property name separated by word boundaries.

Removed
^^^^^^^
* Support for regular expressions when finding references.

Fixed
^^^^^
* Rename all references to alias in owner document.
* Fixed ``AttributeError`` when renaming and unable to find owner document
  
  * ``AttributeError: 'NoneType' object has no attribute 'items'``

* Fixed finding owner document when name contains spaces.

Changed
^^^^^^^
* find command CLI output.

`[0.1.0]`__ - 2021-07-31
------------------------

Added
^^^^^
* Ability to **find** external references.
* Ability to **rename** exterenal references.

__ https://github.com/gbroques/fcxref/compare/v0.4.0...HEAD
__ https://github.com/gbroques/fcxref/compare/v0.3.1...v0.4.0
__ https://github.com/gbroques/fcxref/compare/v0.3.0...v0.3.1
__ https://github.com/gbroques/fcxref/compare/v0.2.0...v0.3.0
__ https://github.com/gbroques/fcxref/compare/v0.1.0...v0.2.0
__ https://github.com/gbroques/fcxref/releases/tag/v0.1.0
