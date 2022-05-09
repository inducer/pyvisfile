PyVisfile: Write VTK/Silo Visualization Files Efficiently
---------------------------------------------------------

.. image:: https://gitlab.tiker.net/inducer/pyvisfile/badges/main/pipeline.svg
    :alt: Gitlab Build Status
    :target: https://gitlab.tiker.net/inducer/pyvisfile/commits/main
.. image:: https://github.com/inducer/pyvisfile/workflows/CI/badge.svg?branch=main&event=push
    :alt: Github Build Status
    :target: https://github.com/inducer/pyvisfile/actions?query=branch%3Amain+workflow%3ACI+event%3Apush
.. image:: https://badge.fury.io/py/pyvisfile.png
    :alt: Python Package Index Release Page
    :target: https://pypi.org/project/pyvisfile/
.. image:: https://zenodo.org/badge/1575355.svg
    :alt: Zenodo DOI for latest release
    :target: https://zenodo.org/badge/latestdoi/1575355

Pyvisfile allows you to write a variety of visualization file formats,
including

* `Kitware's <http://www.kitware.com>`_
  `XML-style <http://www.vtk.org/VTK/help/documentation.html>`_
  `VTK <http://vtk.org>`_ data files. VTK files can be written without
  additional software installed (e.g. VTK's Python bindings).

* Silo visualization files, as used by the
  `VisIt <https://wci.llnl.gov/codes/visit/>`_ large-scale visualization program.
  To use pyvisfile to create Silo files, you need `libsilo
  <https://wci.llnl.gov/codes/silo/>`_ as well as `pybind11
  <https://pybind11.readthedocs.io/en/stable>`_.

pyvisfile supports many mesh geometries, such as unstructured
and rectangular structured meshes, particle meshes, as well as
scalar and vector variables on them. In addition, pyvisfile allows the
semi-automatic writing of parallelization-segmented visualization files
in both Silo and VTK formats. For Silo files, pyvisfile also
supports the writing of expressions as visualization variables.

Resources:

* `Documentation <https://documen.tician.de/pyvisfile/>`_.
* `Source Code <https://github.com/inducer/pyvisfile>`_.
