.. highlight:: sh

Installation
============

This tutorial will walk you through the process of installing PyVisfile. If
you'd like to only use PyVisfile's VTK writing capability, you may skip to
:ref:`download-and-unpack`. Or, even easier, this command should install
:mod:`pyvisfile`::

    pip install pyvisfile

If you'd also like to write `Silo <https://software.llnl.gov/Silo/>`__ files,
you need to follow the entire set of instructions for now. These days, the Silo
library has its own Python bindings (with a nice BSD-3 license) that you may
want to use.

To follow, you need basic things:

* A UNIX-like machine with web access.
* A working `Python <https://www.python.org>`__ installation.
* A recent C++ compiler. We use `pybind11 <https://pybind11.readthedocs.io/en/stable>`__
  to create the wrappers, so see their documentation for minimal required versions
  if in doubt.
* `meson-python <https://meson-python.readthedocs.io/en/latest/>`__ and
  `ninja <https://ninja-build.org/>`__, which are used to build the wrapper.
  See the `[buildsystem]` section in `pyproject.toml` for an up to date list.

You may adapt the file and directory names in this tutorial to suit
your liking, just be sure to be consistent in your changes.

.. note::

    Whenever you see the "``$``" dollar sign in this tutorial, this
    means you should enter the subsequent text at your shell prompt.
    You don't have to be ``root``. A few spots are marked with "sudo" to
    show that these *do* require root privileges *if* you are using a
    Python interpreter that is installed globally.

With Silo capability
--------------------

Step 1: Download and build libsilo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the `Silo source code
<https://software.llnl.gov/Silo/ghpages/releases/releases.html>`_, version 4.6.1 or
newer. Then unpack, build and install it::

    $ tar xfz ~/download/silo-N.N.N.tar.gz
    $ cd silo-N.N.N
    $ ./configure --prefix=$HOME/pool --enable-shared=yes --enable-static=no
    $ make install

If possible, install the Silo library from your Linux distribution, Homebrew or
Conda repositories. This should make it a lot easier to get started.

.. _download-and-unpack:

Common installation
-------------------

Step 2: Download and unpack PyVisfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Download PyVisfile <http://pypi.python.org/pypi/pyvisfile>`_ and unpack it::

    $ tar xfz pyvisfile-VERSION.tar.gz

You can also get it directly from ``git`` using::

    $ git clone https://github.com/inducer/pyvisfile.git

Step 3a: Build :mod:`pyvisfile` without Silo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Building PyVisfile without Silo is quite easy, since it doesn't require any
form of compilation for the binary extension. If you want to make a source
distribution of wheel for PyVisfile, you can just go::

    $ python -m pip wheel --no-deps .

Otherwise, to install it in editable mode for development, run::

    $ python -m pip install --no-build-isolation --editable .

(the ``--no-build-isolation`` flag is very important!)

Step 3b: Build :mod:`pyvisfile` with Silo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build with Silo, you need to tell the build system to use it. This can be done
as follows::

    $ python -m pip install \
        --config-settings setup-args=-Duse-silo=true \
        --no-build-isolation --editable .

The ``setup-args=...`` is the official clunky way to pass arguments to the
underlying build system, which is based on `Meson <https://mesonbuild.com>`__.
For some more example of how this can work, e.g. to compile in debug mode,
see the `official docs <https://meson-python.readthedocs.io/en/latest/how-to-guides/meson-args.html>`__.

.. warning::

    By default, we do not compile with Silo support, even if it is available on
    the system. You need to pass ``-Duse-silo=true`` as above to enable it.

.. note::

    The build system looks for the ``siloh5`` or the ``silo`` library names.
    If these are not in the standard locations, the usual way to work around it
    is to update ``LIBRARY_PATH``::

        $ export LIBRARY_PATH=/my/custom/Silo/lib
        $ export C_INCLUDE_PATH=/my/custom/Silo/include
