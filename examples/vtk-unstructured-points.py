import numpy as np
from pyvisfile.vtk import (
    UnstructuredGrid, DataArray,
    AppendedDataXMLGenerator,
    VTK_VERTEX, VF_LIST_OF_VECTORS, VF_LIST_OF_COMPONENTS)

n = 5000
points = np.random.randn(n, 3)

data = [
        ("p", np.random.randn(n)),
        ("vel", np.random.randn(3, n)),
]
file_name = "points.vtu"
compressor = None

grid = UnstructuredGrid(
        (n, DataArray("points", points, vector_format=VF_LIST_OF_VECTORS)),
        cells=np.arange(n, dtype=np.uint32),
        cell_types=np.asarray([VTK_VERTEX] * n, dtype=np.uint8))

for name, field in data:
    grid.add_pointdata(DataArray(name, field,
        vector_format=VF_LIST_OF_COMPONENTS))

from os.path import exists
if exists(file_name):
    raise RuntimeError("output file '%s' already exists"
        % file_name)

outf = open(file_name, "w")
AppendedDataXMLGenerator(compressor)(grid).write(outf)
outf.close()
