PyVisfile: Write Vtk/Silo Visualization Files Efficiently
---------------------------------------------------------

.. image:: https://gitlab.tiker.net/inducer/pyvisfile/badges/master/pipeline.svg
    :alt: Gitlab Build Status
    :target: https://gitlab.tiker.net/inducer/pyvisfile/commits/master
.. image:: https://github.com/inducer/pyvisfile/workflows/CI/badge.svg?branch=master&event=push
    :alt: Github Build Status
    :target: https://github.com/inducer/pyvisfile/actions?query=branch%3Amaster+workflow%3ACI+event%3Apush
.. image:: https://badge.fury.io/py/pyvisfile.png
    :alt: Python Package Index Release Page
    :target: https://pypi.org/project/pyvisfile/

Pyvisfile allows you to write a variety of visualization file formats,
including

* `Kitware's <http://www.kitware.com>`_
  `XML-style <http://www.vtk.org/VTK/help/documentation.html>`_
  `Vtk <http://vtk.org>`_ data files.

* Silo visualization files, as
  introduced by LLNL's
  `MeshTV <https://wci.llnl.gov/codes/meshtv/>`_ and
  more recently used by the
  `VisIt <https://wci.llnl.gov/codes/visit/>`_
  large-scale visualization program.

pyvisfile supports many mesh geometries, such such as unstructured
and rectangular structured meshes, particle meshes, as well as
scalar and vector variables on them. In addition, pyvisfile allows the
semi-automatic writing of parallelization-segmented visualization files
in both Silo and Vtk formats. For Silo files, pyvisfile also
supports the writing of expressions as visualization variables.

pyvisfile can write Vtk files without any extra software installed.

To use pyvisfile to create Silo files, you need `libsilo
<https://wci.llnl.gov/codes/silo/>`_ as well as `Boost.Python
<http://www.boost.org>`_ and `PyUblas
<http://mathema.tician.de/software/pyublas>`_.  To build
pyvisfile's Silo support, please refer to the `PyUblas
documentation <http://tiker.net/doc/pyublas>`_ for build
instructions first. Check the
`VisIt source page <https://wci.llnl.gov/codes/visit/source.html>`_
for the latest Silo source code.
