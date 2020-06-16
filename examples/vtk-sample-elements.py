"""
This example can be used to check if the VTK ordering and the ones implemented
in :mod:`pyvisfil.vtk.vtk_ordering` match. It can be useful for debugging
and implementing additional element types.

To facilitate this comparison, and unlike the rest of the package, this example
makes use of the Vtk Python bindings.
"""

import numpy as np
import numpy.linalg as la

import matplotlib.pyplot as plt


VTK_LAGRANGE_SIMPLICES = [
        "VTK_LAGRANGE_CURVE",
        "VTK_LAGRANGE_TRIANGLE",
        "VTK_LAGRANGE_TETRAHEDRON",
        ]


def plot_node_ordering(filename, points, show=False):
    if points.shape[0] == 1:
        points = np.hstack([points, np.zeros_like(points)])

    if points.shape[0] == 2:
        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.gca()
        ax.plot(points[0], points[1], "o")
    elif points.shape[0] == 3:
        from mpl_toolkits.mplot3d import art3d      # noqa: F401

        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.gca(projection="3d")
        ax.plot(points[0], points[1], points[2], "o")

        ax.view_init(0, 90)
    else:
        raise ValueError("dimension not supported: %d" % points.shape[0])

    ax.grid()
    for i, p in enumerate(points.T):
        if abs(p[1]) < 1.0e-14:
            ax.text(*p, str(i), color="k", fontsize=12)

    print("output: %s.png" % filename)
    fig.savefig(filename)
    if show:
        plt.show(block=True)


def create_sample_element(cell_type, order=3, visualize=True):
    try:
        import vtk
        from vtkmodules.util.numpy_support import vtk_to_numpy
    except ImportError:
        raise ImportError("python bindings for vtk cannot be found")

    cell_type = cell_type.upper()
    vtk_cell_type = getattr(vtk, cell_type, None)
    if vtk_cell_type is None:
        raise ValueError("unknown cell type: '%s'" % cell_type)

    source = vtk.vtkCellTypeSource()
    source.SetCellType(vtk_cell_type)
    source.SetBlocksDimensions(1, 1, 1)
    if "LAGRANGE" in cell_type:
        source.SetCellOrder(order)
    source.Update()
    grid = source.GetOutput()

    if visualize:
        filename = "sample_%s.vtu" % cell_type.lower()
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
        nodes = np.array(vtk_lagrange_simplex_node_tuples(dim, order))

        error = la.norm(nodes/order - points.T)
        print("error[%d]: %.5e" % (order, error))
        assert error < 5.0e-7

    if visualize:
        filename = "sample_%s" % cell_type.lower()
        plot_node_ordering(filename, points, show=False)

        if cell_type in VTK_LAGRANGE_SIMPLICES:
            filename = "sample_%s_new" % cell_type.lower()
            plot_node_ordering(filename, nodes.T, show=False)


if __name__ == "__main__":
    for cell_type in VTK_LAGRANGE_SIMPLICES:
        print("cell_type: ", cell_type)
        for order in range(1, 11):
            create_sample_element(
                        cell_type, order=order, visualize=False)

    create_sample_element("VTK_LAGRANGE_TETRAHEDRON", order=4)
