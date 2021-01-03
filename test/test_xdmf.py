import numpy as np
import pytest

from pytools.obj_array import make_obj_array


# {{{ test_unstructured_vertex_grid

@pytest.mark.parametrize("ambient_dim", [2, 3])
@pytest.mark.parametrize("dformat", ["xml", "hdf", "binary"])
def test_unstructured_vertex_grid(ambient_dim, dformat, npoints=64):
    """Test constructing a vertex grid with different ways to define the
    points and connectivity.
    """

    # {{{ set up connectivity

    from pyvisfile.xdmf import NumpyDataArray, DataArray, _data_item_from_numpy
    connectivity = np.arange(npoints, dtype=np.uint32)
    points = np.random.rand(ambient_dim, npoints)

    if dformat == "xml":
        connectivity = NumpyDataArray(connectivity, name="connectivity")
        points = NumpyDataArray(points.T, name="points")
    elif dformat in ["hdf", "binary"]:
        if dformat == "hdf":
            cdata = "geometry.h5:/Grid/Connectivity"
            pdata = "geometry.h5:/Grid/Points"
        else:
            cdata = "connectivity.out"
            pdata = "points.out"

        connectivity = DataArray((
            _data_item_from_numpy(connectivity,
                name="connectivity",
                data=cdata),
            ))
        points = DataArray((
            _data_item_from_numpy(points.T,
                name="points",
                data=pdata),
            ))
    else:
        raise ValueError(f"unknown format: '{dformat}'")

    # }}}

    # {{{ set up grids

    from pyvisfile.xdmf import TopologyType
    from pyvisfile.xdmf import XdmfUnstructuredGrid
    grid = XdmfUnstructuredGrid(
            points, connectivity,
            topology_type=TopologyType.Polyvertex,
            name="polyvertex")

    # }}}

    from pyvisfile.xdmf import XdmfWriter
    writer = XdmfWriter((grid,))

    filename = f"test_unstructured_vertex_{dformat}_{ambient_dim}d.xmf"
    writer.write_pretty(filename)

# }}}


# {{{ test_unstructured_simplex_grid

def _simplex_box_connectivity(*, npoints, nelements, nvertices):
    # NOTE: largely copied from meshmode/mesh/generation.py::generate_box_mesh
    ambient_dim = len(npoints)

    point_indices = np.arange(np.prod(npoints)).reshape(npoints)
    connectivity = np.empty((nelements, nvertices), dtype=np.uint32)

    ielement = 0
    from itertools import product
    if ambient_dim == 1:
        raise NotImplementedError
    elif ambient_dim == 2:
        for i, j in product(range(npoints[0] - 1), repeat=ambient_dim):
            a = point_indices[i + 0, j + 0]
            b = point_indices[i + 1, j + 0]
            c = point_indices[i + 0, j + 1]
            d = point_indices[i + 1, j + 1]

            connectivity[ielement + 0, :] = (a, b, c)
            connectivity[ielement + 1, :] = (d, c, b)
            ielement += 2
    elif ambient_dim == 3:
        for i, j, k in product(range(npoints[0] - 1), repeat=ambient_dim):
            a000 = point_indices[i, j, k]
            a001 = point_indices[i, j, k+1]
            a010 = point_indices[i, j+1, k]
            a011 = point_indices[i, j+1, k+1]

            a100 = point_indices[i+1, j, k]
            a101 = point_indices[i+1, j, k+1]
            a110 = point_indices[i+1, j+1, k]
            a111 = point_indices[i+1, j+1, k+1]

            connectivity[ielement + 0, :] = (a000, a100, a010, a001)
            connectivity[ielement + 1, :] = (a101, a100, a001, a010)
            connectivity[ielement + 2, :] = (a101, a011, a010, a001)

            connectivity[ielement + 3, :] = (a100, a010, a101, a110)
            connectivity[ielement + 4, :] = (a011, a010, a110, a101)
            connectivity[ielement + 5, :] = (a011, a111, a101, a110)
            ielement += 6
    else:
        raise NotImplementedError

    assert ielement == nelements

    from pyvisfile.xdmf import NumpyDataArray
    return NumpyDataArray(connectivity, name="connectivity")


@pytest.mark.parametrize("ambient_dim", [2, 3])
def test_unstructured_simplex_grid(ambient_dim, nelements=16):
    """Test constructing a grid with a more complicated topology."""

    from pyvisfile.xdmf import TopologyType
    if ambient_dim == 1:
        topology_type = TopologyType.Polyline
        simplices_per_quad = 1
    if ambient_dim == 2:
        topology_type = TopologyType.Triangle
        simplices_per_quad = 2
    elif ambient_dim == 3:
        topology_type = TopologyType.Tetrahedron
        simplices_per_quad = 6
    else:
        raise ValueError("unsupported dimension")

    # {{{ points and connectivity

    x = np.linspace(-1.0, 1.0, nelements + 1)

    npoints = len(x)
    points = np.empty((ambient_dim,) + (npoints,) * ambient_dim)
    for idim in range(ambient_dim):
        points[idim] = x.reshape((npoints,) + (1,) * (ambient_dim - 1 - idim))

    from pyvisfile.xdmf import NumpyDataArray
    points = NumpyDataArray(points.reshape(ambient_dim, -1).T, name="points")

    from pyvisfile.xdmf import _XDMF_ELEMENT_NODE_COUNT
    connectivity = _simplex_box_connectivity(
            npoints=(npoints,) * ambient_dim,
            nelements=simplices_per_quad * nelements**ambient_dim,
            nvertices=_XDMF_ELEMENT_NODE_COUNT[topology_type]
            )

    # }}}

    # {{{ attributes

    temperature = np.sin(2.0 * np.pi * points.ary[:, 0]) \
            + np.cos(2.0 * np.pi * points.ary[:, 1])
    temperature = NumpyDataArray(temperature, name="temperature")

    velocity = points.ary + np.array([0, 1, 2][:ambient_dim]).reshape(1, -1)
    velocity = NumpyDataArray(velocity, name="velocity")
    vorticity = NumpyDataArray(make_obj_array(velocity.ary), name="vorticity")

    # }}}

    # {{{ write grids

    from pyvisfile.xdmf import XdmfUnstructuredGrid
    grid = XdmfUnstructuredGrid(
            points, connectivity,
            topology_type=topology_type,
            name="simplex")

    grid.add_attribute(temperature)
    grid.add_attribute(velocity)
    grid.add_attribute(vorticity)

    from pyvisfile.xdmf import XdmfWriter
    writer = XdmfWriter((grid,))

    filename = f"test_unstructured_simplex_{ambient_dim}d.xmf"
    writer.write_pretty(filename)

    # }}}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        pytest.main([__file__])

# vim: fdm=marker
