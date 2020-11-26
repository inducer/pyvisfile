import numpy as np


def test_unstructed_grid(ambient_dim=3, npoints=100):
    from pyvisfile.xdmf import DataItemArray
    points = DataItemArray("points",
            np.random.rand(ambient_dim, npoints))
    connectivity = DataItemArray("connectivity",
            np.arange(npoints, dtype=np.uint32))

    from pyvisfile.xdmf import TopologyType
    from pyvisfile.xdmf import XdmfUnstructuredGrid, XdmfWriter
    grid = XdmfUnstructuredGrid(points, (TopologyType.Polyvertex, connectivity))

    writer = XdmfWriter((grid,))
    writer.write_pretty("test_unstructured_grid.xmf")


def test_structured_grid():
    pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])

# vim: fdm=marker
