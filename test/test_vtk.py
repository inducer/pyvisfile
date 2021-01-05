import numpy as np
from pyvisfile.vtk import (
    UnstructuredGrid, DataArray,
    AppendedDataXMLGenerator,
    VTK_VERTEX, VF_LIST_OF_VECTORS, VF_LIST_OF_COMPONENTS)

from pyvisfile.vtk import write_structured_grid


def test_vtk_unstructured_points():
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


def test_vtk_structured_grid():
    angle_mesh = np.mgrid[1:2:10j, 0:2*np.pi:20j, 0:np.pi:30j]

    r = angle_mesh[0, np.newaxis]
    phi = angle_mesh[1, np.newaxis]
    theta = angle_mesh[2, np.newaxis]
    mesh = np.vstack((
        r*np.sin(theta)*np.cos(phi),
        r*np.sin(theta)*np.sin(phi),
        r*np.cos(theta),
        ))

    from pytools.obj_array import make_obj_array
    vec = make_obj_array([
        np.sin(theta)*np.cos(phi),
        np.sin(theta)*np.sin(phi),
        np.cos(theta),
        ])

    write_structured_grid("yo.vts", mesh,
            point_data=[("phi", phi), ("vec", vec)])


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])

# vim: fdm=marker
