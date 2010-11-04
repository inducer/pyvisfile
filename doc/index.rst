Welcome to :mod:`pyvisfile`'s documentation!
============================================

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

pyvisfiles supports many mesh geometries, such such as unstructured
and rectangular structured meshes, particle meshes, as well as
scalar and vector variables on them. In addition, pyvisfile allows the
semi-automatic writing of parallelization-segmented visualization files
in both Silo and Vtk formats. For Silo files, pyvisfile also
supports the writing of expressions as visualization variables.

pyvisfile can write Vtk files without any extra software installed.

PyVisfile allows you to write `Silo <https://wci.llnl.gov/codes/silo/>`_
and `Vtk <http://www.vtk.org/>`_ (`XML-style <http://www.vtk.org/VTK/help/documentation.html>`_)
visualization files from the `Python <http://www.python.org>`_
programming language, more specifically from data contained in `numpy
<http://www.numpy.org>`_ arrays.

For updates, downloads and support, please visit the `PyVisfile web page
<http://mathema.tician.de/software/pyvisfile>`_.

Table of Contents
-----------------

.. toctree::
    :maxdepth: 2

    installing
    silo
    vtk
    faq

* :ref:`genindex`
