import numpy as np


def test_unstructed_grid():
    from pyvisfile.xdmf import XdmfUnstructuredGrid
    grid = XdmfUnstructuredGrid()
    grid.write_pretty("test_unstructured_grid.xmf")


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
