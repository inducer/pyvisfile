"""
This example can be used to check if the VTK ordering and the ones implemented
in :mod:`pyvisfil.vtk.vtk_ordering` match. It can be useful for debugging
and implementing additional element types.

To facilitate this comparison, and unlike the rest of the package, this example
makes use of the VTK Python bindings.
"""

import numpy as np
import numpy.linalg as la

from distutils.version import LooseVersion
import matplotlib.pyplot as plt

try:
    import vtk
    from vtkmodules.util.numpy_support import vtk_to_numpy
except ImportError:
    raise ImportError("python bindings for vtk cannot be found")

if LooseVersion(vtk.VTK_VERSION) <= LooseVersion("8.2.0"):
    is_consistent = False
else:
    is_consistent = True

VTK_LAGRANGE_SIMPLICES = [
        "VTK_LAGRANGE_CURVE",
        "VTK_LAGRANGE_TRIANGLE",
        "VTK_LAGRANGE_TETRAHEDRON",
        ]

VTK_LAGRANGE_QUADS = [
        "VTK_LAGRANGE_QUADRILATERAL",
        "VTK_LAGRANGE_HEXAHEDRON",
        ]


def plot_node_ordering(filename, points, show=False):
    if points.shape[0] == 1:
        points = np.hstack([points, np.zeros_like(points)])

    if points.shape[0] == 2:
        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.gca()
        ax.plot(points[0], points[1], "o")

        ax.set_xlim([-0.1, 1.1])
        ax.set_xlabel("$x$")
        ax.set_ylim([-0.1, 1.1])
        ax.set_ylabel("$y$")
    elif points.shape[0] == 3:
        from mpl_toolkits.mplot3d import art3d      # noqa: F401

        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.gca(projection="3d")
        ax.plot(points[0], points[1], points[2], "o-")

        ax.set_xlim([-0.1, 1.1])
        ax.set_xlabel("$x$")
        ax.set_ylim([-0.1, 1.1])
        ax.set_ylabel("$y$")
        ax.set_zlim([-0.1, 1.1])
        ax.set_zlabel("$z$")

        ax.view_init(15, 45)
    else:
        raise ValueError("dimension not supported: %d" % points.shape[0])

    ax.grid()
    for i, p in enumerate(points.T):
        ax.text(*p, str(i), color="k", fontsize=12)

    print("output: %s.png" % filename)
    fig.savefig(filename)
    if show:
        plt.show(block=True)


def create_sample_element(cell_type, order=3, visualize=True):
    cell_type = cell_type.upper()
    vtk_cell_type = getattr(vtk, cell_type, None)
    if vtk_cell_type is None:
        raise ValueError("unknown cell type: '%s'" % cell_type)

    source = vtk.vtkCellTypeSource()
    source.SetCellType(vtk_cell_type)
    source.SetBlocksDimensions(1, 1, 1)
    # 0 - single precision; 1 - double precision
    source.SetOutputPrecision(1)

    if "LAGRANGE" in cell_type:
        source.SetCellOrder(order)
    source.Update()
    grid = source.GetOutput()

    basename = f"sample_{cell_type.lower()}"
    if visualize:
        filename = f"{basename}.vtu"
        print("cell type: %s" % cell_type)
        print("output: %s" % filename)

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(filename)
        writer.SetCompressorTypeToNone()
        writer.SetDataModeToAscii()
        writer.SetInputData(grid)
        writer.Write()

    cell = grid.GetCell(0)
    points = vtk_to_numpy(cell.GetPoints().GetData()).T

    dim = cell.GetCellDimension()
    points = points[0:dim]

    if cell_type in VTK_LAGRANGE_SIMPLICES:
        from pyvisfile.vtk.vtk_ordering import vtk_lagrange_simplex_node_tuples
        node_tuples = vtk_lagrange_simplex_node_tuples(dim, order,
            is_consistent=is_consistent)

        from pyvisfile.vtk.vtk_ordering import \
                vtk_lagrange_simplex_node_tuples_to_permutation
        vtk_lagrange_simplex_node_tuples_to_permutation(node_tuples)

        nodes = np.array(node_tuples) / order
        error = la.norm(nodes - points.T)
    elif cell_type in VTK_LAGRANGE_QUADS:
        from pyvisfile.vtk.vtk_ordering import vtk_lagrange_quad_node_tuples
        node_tuples = vtk_lagrange_quad_node_tuples(dim, order,
            is_consistent=is_consistent)

        from pyvisfile.vtk.vtk_ordering import \
                vtk_lagrange_quad_node_tuples_to_permutation
        vtk_lagrange_quad_node_tuples_to_permutation(node_tuples)

        nodes = np.array(node_tuples) / order
        error = la.norm(nodes - points.T)

    if error < 5.0e-15:
        print(f"\033[92merror[{order}]: {error:.5e}\033[0m")
    else:
        print(f"\033[91merror[{order}]: {error:.5e}\033[0m")

    if not visualize:
        return

    filename = f"{basename}_vtk"
    plot_node_ordering(filename, points, show=False)

    if cell_type in (VTK_LAGRANGE_SIMPLICES + VTK_LAGRANGE_QUADS):
        filename = f"{basename}_pyvisfile"
        plot_node_ordering(filename, nodes.T, show=False)


def test_order():
    for cell_type in VTK_LAGRANGE_SIMPLICES:
        print("cell_type:", cell_type)
        for order in range(1, 11):
            create_sample_element(cell_type, order=order, visualize=False)

    for cell_type in VTK_LAGRANGE_QUADS:
        print("cell_type:", cell_type)
        for order in range(1, 11):
            create_sample_element(cell_type, order=order, visualize=False)


if __name__ == "__main__":
    test_order()
    create_sample_element("VTK_LAGRANGE_HEXAHEDRON", order=3)
