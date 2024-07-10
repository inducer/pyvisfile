import pathlib

import numpy as np

from pyvisfile.vtk import (
    VF_LIST_OF_COMPONENTS,
    VF_LIST_OF_VECTORS,
    VTK_VERTEX,
    AppendedDataXMLGenerator,
    DataArray,
    UnstructuredGrid,
)


rng = np.random.default_rng(seed=42)

n = 5000
points = rng.normal(size=(n, 3))
data = [
        ("pressure", rng.normal(size=n)),
        ("velocity", rng.normal(size=(3, n)))]

grid = UnstructuredGrid(
        (n, DataArray("points", points, vector_format=VF_LIST_OF_VECTORS)),
        cells=np.arange(n, dtype=np.uint32),
        cell_types=np.array([VTK_VERTEX] * n, dtype=np.uint8))

for name, field in data:
    grid.add_pointdata(
        DataArray(name, field, vector_format=VF_LIST_OF_COMPONENTS))

file_name = pathlib.Path("points.vtu")
compressor = None

if file_name.exists():
    raise FileExistsError(f"Output file '{file_name}' already exists")

with open(file_name, "w") as outf:
    AppendedDataXMLGenerator(compressor)(grid).write(outf)
