.. _include-exclude-patterns:

Include-Exclude Pattern Matching Guide
================================================================================

Introduction
--------------------------------------------------------------------------------

This document explains the pattern matching syntax used in include-exclude patterns, which follows the same syntax as ``.gitignore`` files. These patterns are used to specify which files to include or exclude when creating knowledge bases or other file filtering operations.

The pattern syntax allows for powerful and flexible matching of file paths using wildcards, directory specifiers, and character classes. This guide demonstrates each pattern type with concrete examples to help you understand exactly how they work.

Basic File Pattern Matching
--------------------------------------------------------------------------------

Basic patterns match files regardless of their location in the directory structure.

.. list-table:: Basic File Name Matching
   :widths: 30 30 20 20
   :header-rows: 1

   * - Pattern
     - Description
     - Example Path
     - Matches?
   * - ``README.md``
     - Matches any file named README.md in any directory
     - README.md
     - ✓ Yes
   * - ``README.md``
     - Matches README.md in subdirectories too
     - folder/README.md
     - ✓ Yes
   * - ``README.md``
     - Matches at any depth in the directory structure
     - folder/subfolder/README.md
     - ✓ Yes
   * - ``*.py``
     - Matches any Python file in any directory
     - example.py
     - ✓ Yes
   * - ``*.py``
     - Matches Python files in subdirectories
     - folder/example.py
     - ✓ Yes
   * - ``*.py``
     - Matches Python files at any depth
     - folder/subfolder/example.py
     - ✓ Yes

Directory-Specific Matching
--------------------------------------------------------------------------------

Patterns can be made directory-specific to match files only in certain locations.

.. list-table:: Directory-Specific Matching
   :widths: 30 30 20 20
   :header-rows: 1

   * - Pattern
     - Description
     - Example Path
     - Matches?
   * - ``src/*.py``
     - Matches Python files directly in the src directory
     - src/example.py
     - ✓ Yes
   * - ``src/*.py``
     - Does NOT match Python files in other directories
     - example.py
     - ✗ No
   * - ``src/*.py``
     - Does NOT match Python files in other directories
     - folder/example.py
     - ✗ No
   * - ``src/*.py``
     - Does NOT match Python files in subdirectories of src
     - src/folder/example.py
     - ✗ No

Recursive Directory Matching
--------------------------------------------------------------------------------

The ``**`` pattern allows matching files recursively through directories.

.. list-table:: Recursive Directory Matching
   :widths: 30 30 20 20
   :header-rows: 1

   * - Pattern
     - Description
     - Example Path
     - Matches?
   * - ``src/**/*.py``
     - Matches Python files directly in the src directory
     - src/example.py
     - ✓ Yes
   * - ``src/**/*.py``
     - Matches Python files in subdirectories of src
     - src/folder/example.py
     - ✓ Yes
   * - ``src/**/*.py``
     - Matches Python files at any depth under src
     - src/folder/subfolder/example.py
     - ✓ Yes
   * - ``docs/source/*/**/index.rst``
     - Matches index.rst files at least 2 levels deep under docs/source
     - docs/source/Section-1/index.rst
     - ✓ Yes
   * - ``docs/source/*/**/index.rst``
     - Matches index.rst files at deeper levels
     - docs/source/Section-1/Section-1-1/index.rst
     - ✓ Yes
   * - ``docs/source/*/**/index.rst``
     - Does NOT match index.rst directly in docs/source
     - docs/source/index.rst
     - ✗ No

Directory Name Matching
--------------------------------------------------------------------------------

Patterns can match directories and their contents.

.. list-table:: Directory Name Matching
   :widths: 30 30 20 20
   :header-rows: 1

   * - Pattern
     - Description
     - Example Path
     - Matches?
   * - ``tmp``
     - Matches files inside any directory named tmp
     - tmp/file.txt
     - ✓ Yes
   * - ``tmp``
     - Matches files in subdirectories of tmp
     - tmp/folder/file.txt
     - ✓ Yes
   * - ``tmp``
     - Matches files at any depth under tmp
     - tmp/folder/subfolder/file.txt
     - ✓ Yes
   * - ``tmp``
     - Matches files in tmp directories anywhere in the path
     - tests/tmp/file.txt
     - ✓ Yes
   * - ``tmp``
     - Matches files in nested tmp directories
     - tests/tmp/folder/file.txt
     - ✓ Yes
   * - ``tmp``
     - Matches deeply nested files in tmp directories
     - tests/tmp/subfolder/file.txt
     - ✓ Yes

Directory Contents Matching
--------------------------------------------------------------------------------

Adding a trailing slash focuses on directory contents rather than the directory itself.

.. list-table:: Directory Contents Matching
   :widths: 30 30 20 20
   :header-rows: 1

   * - Pattern
     - Description
     - Example Path
     - Matches?
   * - ``tmp/``
     - Does NOT match the tmp directory itself
     - tmp
     - ✗ No
   * - ``tmp/``
     - Matches files inside any tmp directory
     - tmp/file.txt
     - ✓ Yes
   * - ``tmp/``
     - Matches files in subdirectories of tmp
     - tmp/folder/file.txt
     - ✓ Yes
   * - ``tmp/``
     - Matches files at any depth under tmp
     - tmp/folder/subfolder/file.txt
     - ✓ Yes
   * - ``tmp/``
     - Matches files in tmp directories anywhere in the path
     - tests/tmp/file.txt
     - ✓ Yes
   * - ``tmp/``
     - Matches files in nested tmp directories
     - tests/tmp/folder/file.txt
     - ✓ Yes
   * - ``tmp/``
     - Matches deeply nested files in tmp directories
     - tests/tmp/subfolder/file.txt
     - ✓ Yes

Character Class Matching
--------------------------------------------------------------------------------

Character classes allow matching one character from a set of characters.

.. list-table:: Character Class Matching
   :widths: 30 30 20 20
   :header-rows: 1

   * - Pattern
     - Description
     - Example Path
     - Matches?
   * - ``*.py[cod]``
     - Matches Python bytecode files (.pyc)
     - test.pyc
     - ✓ Yes
   * - ``*.py[cod]``
     - Matches Python optimized bytecode files (.pyo)
     - test.pyo
     - ✓ Yes
   * - ``*.py[cod]``
     - Matches Python dynamic library files (.pyd)
     - test.pyd
     - ✓ Yes

Summary of Pattern Syntax
--------------------------------------------------------------------------------

Here's a quick reference for the pattern syntax demonstrated:

.. list-table:: Pattern Syntax Summary
   :widths: 25 75
   :header-rows: 1

   * - Pattern Element
     - Description
   * - ``*``
     - Matches any sequence of characters within a path segment (not including path separators)
   * - ``**``
     - Matches any sequence of characters spanning multiple path segments (including path separators)
   * - ``/``
     - When used at the end of a pattern, specifies matching directory contents rather than the directory itself
   * - ``[abc]``
     - Character class that matches any single character from the set (a, b, or c)
   * - ``dir/``
     - Specifies a directory prefix, restricting matches to that directory
   * - ``dir/**``
     - Specifies a directory prefix with recursive matching, finding matches in that directory and all its subdirectories

These patterns can be combined to create powerful file selection rules for your knowledge base configuration. Use the examples above as a reference when creating your own patterns to ensure they match exactly the files you intend.