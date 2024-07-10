import pathlib

import numpy as np
import pytest

from pyvisfile.vtk import (
    VF_LIST_OF_COMPONENTS,
    VF_LIST_OF_VECTORS,
    VTK_VERTEX,
    AppendedDataXMLGenerator,
    DataArray,
    ParallelXMLGenerator,
    UnstructuredGrid,
    write_structured_grid,
)


def make_unstructured_grid(n: int) -> UnstructuredGrid:
    rng = np.random.default_rng(seed=42)
    points = rng.normal(size=(n, 3))

    data = [
            ("pressure", rng.normal(size=n)),
            ("velocity", rng.normal(size=(3, n))),
    ]

    grid = UnstructuredGrid(
            (n, DataArray("points", points, vector_format=VF_LIST_OF_VECTORS)),
            cells=np.arange(n, dtype=np.uint32),
            cell_types=np.asarray([VTK_VERTEX] * n, dtype=np.uint8))

    for name, field in data:
        grid.add_pointdata(
            DataArray(name, field, vector_format=VF_LIST_OF_COMPONENTS))

    return grid


@pytest.mark.parametrize("n", [5000, 0])
def test_vtk_unstructured_points(n: int) -> None:
    grid = make_unstructured_grid(n)
    file_name = pathlib.Path(f"vtk-unstructured-{n:04d}.vtu")
    compressor = None

    if file_name.exists():
        raise FileExistsError(f"Output file '{file_name}' already exists")

    with open(file_name, "w") as outf:
        AppendedDataXMLGenerator(compressor)(grid).write(outf)


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

    write_structured_grid(
        "vtk-structured.vts",
        mesh,
        point_data=[("phi", phi), ("vec", vec)])


def test_vtk_parallel():
    cwd = pathlib.Path(__file__).parent
    file_name = cwd / "vtk-parallel.pvtu"

    grid = make_unstructured_grid(1024)
    pathnames = [f"vtk-parallel-piece-{i}.vtu" for i in range(5)]

    if file_name.exists():
        raise FileExistsError(f"Output file '{file_name}' already exists")

    with open(file_name, "w") as outf:
        ParallelXMLGenerator(pathnames)(grid).write(outf)

    import filecmp
    assert filecmp.cmp(file_name, cwd / "ref-vtk-parallel.pvtu")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])

# vim: fdm=marker
