posixfs
=======

posixfs provides context managers and functions to manipulate files on a POSIX file system with atomicity and
durability. The module is intended to be simple and straightforward to use.

The module is written in Python 3 with types annotated and using ``pathlib.Path``.

Related Projects
================
There are many modules and projects which already provide this functionality. We give below a non-exhaustive list:

* https://github.com/abarnert/fatomic
* https://github.com/untitaker/python-atomicwrites
* https://github.com/mitsuhiko/python-atomicfile
* https://github.com/sashka/atomicfile
* https://boltons.readthedocs.io/en/latest/fileutils.html#boltons.fileutils.atomic_save

Unfortunately, none of them provides durable writes (only atomic ones), they lack type annotations and they all use
``str`` instead of ``pathlib.Path`` to deal with file paths.

We particularly found type annotations to be crucial for a
module which is widely used, such as for writing and reading files, in a large code base that requires static checks and
good readability. Moreover, we do not want to give away the manipulation capabilities of ``pathlib`` and be forced to
sprinkle ``.as_posix()`` all over the code.

For more information on atomic and durable writes on POSIX file systems, see
http://blog.httrack.com/blog/2013/11/15/everything-you-always-wanted-to-know-about-fsync

Usage
=====
.. code-block:: python

    import pathlib

    import posixfs

    # write bytes to a file atomically and durably
    pth = pathlib.Path("/some/file.txt")
    posixfs.atomic_write_bytes(path=pth, data=b"hello", durable=True)

    # write text to a file atomically and durably
    posixfs.atomic_write_bytes(path=pth, text="hello", durable=True)

    # use context manager
    with posixfs.AtomicWritingText(path=pth, durable=True) as file:
        file.write('hello\n')
        file.write('how do you do?\n')

Installation
============

* Create a virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate it:

.. code-block:: bash

    source venv3/bin/activate

* Install posixfs with pip:

.. code-block:: bash

    pip3 install posixfs

Development
===========

* Check out the repository.

* In the repository root, create the virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate the virtual environment:

.. code-block:: bash

    source venv3/bin/activate

* Install the development dependencies:

.. code-block:: bash

    pip3 install -e .[dev]

* We use tox for testing and packaging the distribution. Assuming that the virtual environment has been activated and
  the development dependencies have been installed, run:

.. code-block:: bash

    tox

* We also provide a set of pre-commit checks that lint and check code for formatting. Run them locally from an activated
  virtual environment with development dependencies:

.. code-block:: bash

    ./precommit.py

* The pre-commit script can also automatically format the code:

.. code-block:: bash

    ./precommit.py  --overwrite

Versioning
==========
We follow `Semantic Versioning <http://semver.org/spec/v1.0.0.html>`_. The version X.Y.Z indicates:

* X is the major version (backward-incompatible),
* Y is the minor version (backward-compatible), and
* Z is the patch version (backward-compatible bug fix).