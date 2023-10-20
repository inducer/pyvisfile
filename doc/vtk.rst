Usage Reference for :mod:`pyvisfile.vtk`
========================================

.. automodule:: pyvisfile.vtk
.. moduleauthor:: Andreas Kloeckner <inform@tiker.net>

.. automodule:: pyvisfile.vtk.vtk_ordering

Examples
--------

Writing a structured mesh
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/vtk-structured-2d-plain.py

(You can find this example as
:download:`examples/vtk-structured-2d-plain.py <../examples/vtk-structured-2d-plain.py>` in the PyVisfile
source distribution.)

Writing a collection of points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   Observe that this is written as a 'unstructured grid', even though there
   is not much grid here. However, by supplying connectivity data, it is
   possible to generalize from this to actual unstructured meshes.

.. literalinclude:: ../examples/vtk-unstructured-points.py

(You can find this example as
:download:`examples/vtk-unstructured-points.py <../examples/vtk-unstructured-points.py>` in the PyVisfile
source distribution.)
