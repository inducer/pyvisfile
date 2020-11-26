import numpy as np
import pytest

from pytools.obj_array import make_obj_array


@pytest.mark.parametrize("ambient_dim", [2, 3])
@pytest.mark.parametrize("dformat", ["xml", "hdf", "binary"])
def test_unstructured_vertex_grid(ambient_dim, dformat, npoints=64):
    """Test constructing a vertex grid with different ways to define the
    points and connectivity.
    """

    cargs = {"dtype": np.dtype(np.uint32), "shape": (npoints,)}
    pargs = {"dtype": np.dtype(np.float), "shape": (ambient_dim, npoints)}

    if dformat == "xml":
        cargs = {}
        pargs = {}
        connectivity = np.arange(npoints, dtype=np.uint32)
        points = np.random.rand(ambient_dim, npoints)
    elif dformat == "hdf":
        connectivity = "geometry.h5:/Grid/Connectivity"
        points = "geometry.h5:/Grid/Points"
    elif dformat == "binary":
        connectivity = "connectivity.out"
        points = "points.out"
    else:
        raise ValueError(f"unknown format: '{dformat}'")

    from pyvisfile.xdmf import DataItemArray
    connectivity = DataItemArray("connectivity", connectivity, **cargs)
    points = DataItemArray("points", points, **pargs)

    from pyvisfile.xdmf import TopologyType
    from pyvisfile.xdmf import XdmfUnstructuredGrid
    grid = XdmfUnstructuredGrid(
            points,
            (TopologyType.Polyvertex, connectivity),
            name="polyvertex")

    from pyvisfile.xdmf import XdmfWriter
    writer = XdmfWriter((grid,))

    filename = f"test_unstructured_vertex_{ambient_dim}d.xmf"
    writer.write_pretty(filename)


@pytest.mark.parametrize("ambient_dim", [2, 3])
def test_unstructured_simplex_grid(ambient_dim, nelements=2):
    """Test constructing a grid with a more complicated topology."""

    from pyvisfile.xdmf import TopologyType
    if ambient_dim == 1:
        topology_type = TopologyType.Polyline
    if ambient_dim == 2:
        topology_type = TopologyType.Triangle
    elif ambient_dim == 3:
        topology_type = TopologyType.Tetrahedron
    else:
        raise ValueError("unsupported dimension")

    # {{{ points

    x = np.linspace(-1.0, 1.0, nelements + 1)

    npoints = len(x)
    points = np.empty((ambient_dim,) + (npoints,) * ambient_dim)
    for idim in range(ambient_dim):
        points[idim] = x.reshape((npoints,) + (1,) * (ambient_dim - 1 - idim))

    from pyvisfile.xdmf import DataItemArray
    points = DataItemArray("points", points.reshape(ambient_dim, -1))

    # }}}

    # {{{ connectivity

    from pyvisfile.xdmf import _XDMF_ELEMENT_NODE_COUNT
    nelements = 2 * nelements**ambient_dim
    nnodes = _XDMF_ELEMENT_NODE_COUNT[topology_type]

    point_indices = np.arange(points.shape[1]).reshape((npoints,) * ambient_dim)
    connectivity = np.empty((nelements, nnodes), dtype=np.uint32)

    ielement = 0
    from itertools import product
    if ambient_dim == 1:
        raise NotImplementedError
    elif ambient_dim == 2:
        for i, j in product(range(npoints - 1), repeat=ambient_dim):
            a = point_indices[i + 0, j + 0]
            b = point_indices[i + 1, j + 0]
            c = point_indices[i + 0, j + 1]
            d = point_indices[i + 1, j + 1]

            connectivity[ielement + 0, :] = (a, b, c)
            connectivity[ielement + 1, :] = (d, c, b)
            ielement += 2
    else:
        raise NotImplementedError

    assert ielement == nelements

    connectivity = DataItemArray("connectivity", connectivity.T)

    # }}}

    from pyvisfile.xdmf import XdmfUnstructuredGrid
    grid = XdmfUnstructuredGrid(
            points,
            (topology_type, connectivity),
            name="simplex")

    from pyvisfile.xdmf import XdmfWriter
    writer = XdmfWriter((grid,))

    filename = f"test_unstructured_simplex_{ambient_dim}d.xmf"
    writer.write_pretty(filename)


def test_structured_grid():
    pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        pytest.main([__file__])

# vim: fdm=marker
