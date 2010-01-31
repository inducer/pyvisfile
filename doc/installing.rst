.. highlight:: sh

Installation
============

This tutorial will walk you through the process of installing Pylo. To
follow, you really only need three basic things:

* A UNIX-like machine with web access.
* A C++ compiler, preferably a Version 4.x gcc.
* A working `Python <http://www.python.org>`_ installation, Version 2.4 or newer.

You may adapt the file and directory names in this tutorial to suit
your liking, just be sure to be consistent in your changes.

.. note:: 

    Whenever you see the "`$`" dollar sign in this tutorial, this
    means you should enter the subsequent text at your shell prompt.
    You don't have to be `root`. A few spots are marked with "sudo" to
    show that these *do* require root privileges *if* you are using a
    Python interpreter that is installed globally.

Step 1: Install :mod:`pyublas`
------------------------------

.. note::

    If you have already installed :mod:`hedge`, then you automatically
    also already have :mod:`pyublas`, and you can skip this step.

The first step in this installation is to install PyUblas. To achieve
this, please follow `PyUblas's installation instructions
<http://documen.tician.de/pyublas/installing.html>`_.

Step 2: Download and build libsilo
----------------------------------

Download the `Silo source code
<https://wci.llnl.gov/codes/silo/downloads.html>`_, version 4.6.1 or
newer. Then unpack, build and install it::

    $ tar xfz ~/download/silo-N.N.N.tar.gz
    $ cd silo-N.N.N
    $ ./configure.py --prefix=$HOME/pool --enable-shared=yes --enable-static=no
    $ make install

Step 3: Update your build configuration file
--------------------------------------------

During prior steps of this installation, you will have created
a file called :file:`.aksetup-defaults.py`  in your home directory. 
Now add the following lines to this file::

    SILO_INC_DIR = ['/home/andreas/pool/include']
    SILO_LIB_DIR = ['/home/andreas/pool/lib']

You will need to adapt the above path names to the location where you installed 
the Silo software, of course.

.. note::

    Make sure not to miss the initial dot in the configuration file name, 
    it's important.

.. note::

    The order of the entries in the build configuration file does not
    matter.

Step 4: Download and unpack Pylo
--------------------------------

`Download Pylo <http://pypi.python.org/pypi/pylo>`_ and unpack it::

    $ tar xfz pylo-VERSION.tar.gz

Step 5: Build :mod:`pylo`
-------------------------

Just type::

    $ cd pylo-VERSION # if you're not there already
    $ sudo python setup.py install

Once that works, congratulations! You've successfully built :mod:`pylo`.