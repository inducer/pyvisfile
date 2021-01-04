Welcome to :mod:`pyvisfile`'s documentation!
============================================

Pyvisfile allows you to write a variety of visualization file formats,
including

* `Kitware's <http://www.kitware.com>`__
  `XML-style <http://www.vtk.org/VTK/help/documentation.html>`__
  `Vtk <http://vtk.org>`__ data files.

* Silo visualization files, as
  introduced by LLNL's
  `MeshTV <https://wci.llnl.gov/codes/meshtv/>`__ and
  more recently used by the
  `VisIt <https://wci.llnl.gov/codes/visit/>`__
  large-scale visualization program.

pyvisfiles supports many mesh geometries, such such as unstructured
and rectangular structured meshes, particle meshes, as well as
scalar and vector variables on them. In addition, pyvisfile allows the
semi-automatic writing of parallelization-segmented visualization files
in both Silo and Vtk formats. For Silo files, pyvisfile also
supports the writing of expressions as visualization variables.

pyvisfile can write Vtk files without any extra software installed.

PyVisfile allows you to write `Silo <https://wci.llnl.gov/codes/silo/>`__
and `Vtk <http://www.vtk.org/>`_ (`XML-style <http://www.vtk.org/VTK/help/documentation.html>`__)
visualization files from the `Python <http://www.python.org>`__
programming language, more specifically from data contained in :mod:`numpy`
arrays.

For updates, downloads and support, please visit the `PyVisfile web page
<http://github.com/inducer/pyvisfile>`__.

.. module:: pyvisfile

Table of Contents
-----------------

.. toctree::
    :maxdepth: 2

    installing
    silo
    vtk
    faq
    🚀 Github <https://github.com/inducer/pyvisfile>
    💾 Download Releases <https://pypi.org/project/pyvisfile>

* :ref:`genindex`
