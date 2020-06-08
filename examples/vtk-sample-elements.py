import numpy as np
import matplotlib.pyplot as plt


def plot_node_ordering(filename, points):
    if points.shape[0] == 2:
        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.gca()
        ax.plot(points[0], points[1], "o")
    elif points.shape[0] == 3:
        from mpl_toolkits.mplot3d import art3d

        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.gca(projection="3d")
        ax.plot(points[0], points[1], points[2], "o")
    else:
        raise ValueError("dimension not supported")

    ax.grid()
    for i, p in enumerate(points.T):
        ax.text(*p, str(i), color="k")

    print("output: %s.png" % filename)
    fig.savefig(filename)
    if 0:
        plt.show(block=True)


def create_sample_element(cell_type, order=3):
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

    filename = "sample_%s.vtu" % cell_type.lower()
    print("cell type: %s" % cell_type)
    print("output: %s" % filename)

    grid = source.GetOutput()

    # write vtk file
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetCompressorTypeToNone()
    writer.SetDataModeToAscii()
    writer.SetInputData(grid)
    writer.Write()

    # write numbered matplotlib file
    cell = grid.GetCell(0)
    points = vtk_to_numpy(cell.GetPoints().GetData()).T

    dim = cell.GetCellDimension()
    points = points[0:max(dim, 2)]

    filename = "sample_%s" % cell_type.lower()
    plot_node_ordering(filename, points)


if __name__ == "__main__":
    create_sample_element("VTK_LAGRANGE_TRIANGLE", order=5)
