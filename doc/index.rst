Welcome to :mod:`pyvisfile`'s documentation!
============================================

Pyvisfile allows you to write a variety of visualization file formats,
including

* `Kitware's <https://www.kitware.com>`__
  `XML-style <https://vtk.org/documentation>`__
  `VTK <https://vtk.org>`__ data files.

* Silo visualization files, as used by the
  `VisIt <https://visit-dav.github.io/visit-website/>`__
  large-scale visualization program.

* `XDMF <https://www.xdmf.org/index.php/Main_Page>`__ data files.

pyvisfile supports many mesh geometries, such such as unstructured
and rectangular structured meshes, particle meshes, as well as
scalar and vector variables on them. In addition, pyvisfile allows the
semi-automatic writing of parallelization-segmented visualization files
in both Silo and VTK formats. For Silo files, pyvisfile also
supports the writing of expressions as visualization variables.

pyvisfile can write VTK files without any extra software installed.

PyVisfile allows you to write `Silo <https://software.llnl.gov/Silo/>`__
and `VTK <https://vtk.org/>`__ (`XML-style <https://vtk.org/documentation>`__)
visualization files from the `Python <https://www.python.org>`__
programming language, more specifically from data contained in :mod:`numpy`
arrays.

For updates, downloads and support, please visit the `PyVisfile web page
<https://github.com/inducer/pyvisfile>`__.

.. module:: pyvisfile

Table of Contents
-----------------

.. toctree::
    :maxdepth: 2

    installing
    silo
    vtk
    xdmf
    faq
    🚀 Github <https://github.com/inducer/pyvisfile>
    💾 Download Releases <https://pypi.org/project/pyvisfile>

* :ref:`genindex`
