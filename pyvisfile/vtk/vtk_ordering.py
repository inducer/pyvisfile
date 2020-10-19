__copyright__ = "Copyright (C) 2020 Alexandru Fikl"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from pytools import (
        add_tuples,
        generate_nonnegative_integer_tuples_summing_to_at_most as gnitstam)


__doc__ = """
VTK High-Order Lagrange Elements
--------------------------------

The high-order elements are described in
`this blog post <https://blog.kitware.com/modeling-arbitrary-order-lagrange-finite-elements-in-the-visualization-toolkit/>`_.
The ordering of the element nodes is as follows:

    1. the vertices (in an order that matches the linear elements,
       e.g. :data:`~pyvisfile.vtk.VTK_TRIANGLE`).
    2. the interior edge (or face in 2D) nodes, i.e. without the endpoints
    3. the interior face (3D only) nodes, i.e. without the edge nodes.
    4. the remaining interior nodes.

For simplices, the interior nodes are defined recursively by using the same
rules. However, for box elements the interior nodes are just listed in
order, with the last coordinate moving slowest.

To a large extent, the VTK ordering matches the ordering used by ``gmsh`` and
described `here <https://gmsh.info/doc/texinfo/gmsh.html#Node-ordering>`_.

.. autofunction:: vtk_lagrange_simplex_node_tuples
.. autofunction:: vtk_lagrange_simplex_node_tuples_to_permutation

.. autofunction:: vtk_lagrange_quad_node_tuples
.. autofunction:: vtk_lagrange_quad_node_tuples_to_permutation
"""     # noqa


# {{{

def add_tuple_to_list(ary, x):
    return [add_tuples(x, y) for y in ary]

# }}}


# {{{ VTK_LAGRANGE_${SIMPLEX} (i.e. CURVE/TRIANGLE/TETRAHEDRON)

def vtk_lagrange_curve_node_tuples(order):
    return [(0,), (order,)] + [(i,) for i in range(1, order)]


def vtk_lagrange_triangle_node_tuples(order):
    nodes = []
    offset = (0, 0)

    if order < 0:
        return nodes

    while order >= 0:
        if order == 0:
            nodes += [offset]
            break

        #   y
        #   ^
        #   |
        #   2
        #   |`\
        #   |  `\
        #   |    `\
        #   |      `\
        #   |        `\
        #   0----------1 --> x

        # add vertices
        vertices = [(0, 0), (order, 0), (0, order)]
        nodes += add_tuple_to_list(vertices, offset)
        if order == 1:
            break

        # add faces
        face_ids = range(1, order)
        faces = (
                # vertex 0 -> 1
                [(i, 0) for i in face_ids]
                # vertex 1 -> 2
                + [(order - i, i) for i in face_ids]
                # vertex 2 -> 0
                + [(0, order - i) for i in face_ids])
        nodes += add_tuple_to_list(faces, offset)

        order = order - 3
        offset = add_tuples(offset, (1, 1))

    return nodes


def vtk_lagrange_tetrahedron_node_tuples(order):
    nodes = []
    offset = (0, 0, 0)

    while order >= 0:
        if order == 0:
            nodes += [offset]
            break

        #                  z
        #               ,/
        #              3
        #            ,/|`\
        #          ,/  |  `\
        #        ,/    '.   `\
        #      ,/       |     `\
        #    ,/         |       `\
        #   0-----------'.--------2---> y
        #    `\.         |      ,/
        #       `\.      |    ,/
        #          `\.   '. ,/
        #             `\. |/
        #                `1
        #                  `.
        #                     x

        vertices = [(0, 0, 0), (order, 0, 0), (0, order, 0), (0, 0, order)]
        nodes += add_tuple_to_list(vertices, offset)
        if order == 1:
            break

        # add edges
        edge_ids = range(1, order)
        edges = (
                # vertex 0 -> 1
                [(i, 0, 0) for i in edge_ids]
                # vertex 1 -> 2
                + [(order - i, i, 0) for i in edge_ids]
                # vertex 2 -> 0
                + [(0, order - i, 0) for i in edge_ids]
                # vertex 0 -> 3
                + [(0, 0, i) for i in edge_ids]
                # vertex 1 -> 3
                + [(order - i, 0, i) for i in edge_ids]
                # vertex 2 -> 3
                + [(0, order - i, i) for i in edge_ids])
        nodes += add_tuple_to_list(edges, offset)

        # add faces
        face_ids = add_tuple_to_list(
                vtk_lagrange_triangle_node_tuples(order - 3), (1, 1))
        faces = (
                # face between vertices (0, 2, 3)
                [(i, 0, j) for i, j in face_ids]
                # face between vertices (1, 2, 3)
                + [(j, order - (i + j), i) for i, j in face_ids]
                # face between vertices (0, 1, 3)
                + [(0, j, i) for i, j in face_ids]
                # face between vertices (0, 1, 2)
                + [(j, i, 0) for i, j in face_ids])
        nodes += add_tuple_to_list(faces, offset)

        order = order - 4
        offset = add_tuples(offset, (1, 1, 1))

    return nodes


def vtk_lagrange_simplex_node_tuples(dims, order, vtk_version=(2, 1),
        is_consistent=None):
    """
    :arg dims: dimension of the simplex, i.e. 1 corresponds to a curve, 2 to
        a triangle, etc.
    :arg order: order of the polynomial representation, which also defines
        the number of nodes on the simplex.
    :arg vtk_version: a :class:`tuple` of two elements containing the version
        of the VTK XML file format in use. The ordering of some of the
        high-order elements changed between versions `2.1` and `2.2`.

    :return: a :class:`list` of ``dims``-dimensional tuples of integers
        up to ``order`` in the ordering expected by VTK. This list can be
        passed to :func:`vtk_lagrange_simplex_node_tuples_to_permutation`
        to obtain a permutation from the order used by :mod:`modepy`.
    """
    if dims == 1:
        return vtk_lagrange_curve_node_tuples(order)
    elif dims == 2:
        return vtk_lagrange_triangle_node_tuples(order)
    elif dims == 3:
        return vtk_lagrange_tetrahedron_node_tuples(order)
    else:
        raise ValueError(f"unsupported dimension: {dims}")


def vtk_lagrange_simplex_node_tuples_to_permutation(node_tuples):
    order = max([max(i) for i in node_tuples])
    dims = len(node_tuples[0])

    node_to_index = {
            node_tuple: i
            for i, node_tuple in enumerate(gnitstam(order, dims))
            }

    assert len(node_tuples) == len(node_to_index)
    return [node_to_index[v] for v in node_tuples]

# }}}


# {{{ VTK_LAGRANGE_${QUAD} (i.e. QUADRILATERAL/HEXAHEDRON)

def vtk_lagrange_quadrilateral_node_tuples(order):
    nodes = []

    if order < 0:
        return nodes

    if order == 0:
        return [(0, 0)]

    #   y
    #   ^
    #   |
    #   3----------2
    #   |          |
    #   |          |
    #   |          |
    #   |          |
    #   |          |
    #   0----------1 --> x

    # add vertices
    nodes += [(0, 0), (order, 0), (order, order), (0, order)]
    if order == 1:
        return nodes

    # add faces
    face_ids = range(1, order)
    nodes += (
            # vertex 0 -> 1
            [(i, 0) for i in face_ids]
            # vertex 1 -> 2
            + [(order, i) for i in face_ids]
            # vertex 2 -> 3
            + [(i, order) for i in face_ids]
            # vertex 3 -> 0
            + [(0, i) for i in face_ids])

    # add remaining interior nodes
    from itertools import product
    nodes += [(i, j) for j, i in product(range(1, order), repeat=2)]

    return nodes


def vtk_lagrange_hexahedon_node_tuples(order, vtk_version=(2, 1)):
    nodes = []

    if order < 0:
        return nodes

    if order == 0:
        return [(0, 0, 0)]

    #   z
    #   ^
    #   |
    #   4----------7
    #   |\         |\
    #   | \        | \
    #   |  \       |  \
    #   |   5------+---6
    #   |   |      |   |
    #   0---+------3---|--> y
    #    \  |       \  |
    #     \ |        \ |
    #      \|         \|
    #       1----------2
    #        \
    #         v x

    # add vertices
    nodes += [
            # (0, 1, 2, 3)
            (0, 0, 0), (order, 0, 0),
            (order, order, 0), (0, order, 0),
            # (4, 5, 6, 7)
            (0, 0, order), (order, 0, order),
            (order, order, order), (0, order, order),
            ]
    if order == 1:
        return nodes

    # add edges
    edge_ids = range(1, order)
    nodes += (
            # vertex 0 -> 1
            [(i, 0, 0) for i in edge_ids]
            # vertex 1 -> 2
            + [(order, i, 0) for i in edge_ids]
            # vertex 2 -> 3
            + [(i, order, 0) for i in edge_ids]
            # vertex 3 -> 0
            + [(0, i, 0) for i in edge_ids]

            # vertex 4 -> 5
            + [(i, 0, order) for i in edge_ids]
            # vertex 5 -> 6
            + [(order, i, order) for i in edge_ids]
            # vertex 6 -> 7
            + [(i, order, order) for i in edge_ids]
            # vertex 7 -> 4
            + [(0, i, order) for i in edge_ids]

            # vertex 0 -> 4
            + [(0, 0, i) for i in edge_ids]
            # vertex 1 -> 5
            + [(order, 0, i) for i in edge_ids]
            )

    if vtk_version <= (2, 1):
        nodes += (
            # vertex 3 -> 7
            [(0, order, i) for i in edge_ids]
            # vertex 2 -> 6
            + [(order, order, i) for i in edge_ids]
            )
    else:
        nodes += (
            # vertex 2 -> 6
            [(order, order, i) for i in edge_ids]
            # vertex 3 -> 7
            + [(0, order, i) for i in edge_ids]
            )

    # add faces
    from itertools import product
    nodes += (
            # face between (0, 4, 7, 3)
            [(0, i, j) for j, i in product(range(1, order), repeat=2)]
            # face between (1, 5, 6, 2)
            + [(order, i, j) for j, i in product(range(1, order), repeat=2)]
            # face between (0, 1, 5, 4)
            + [(i, 0, j) for j, i in product(range(1, order), repeat=2)]
            # face between (3, 2, 6, 7)
            + [(i, order, j) for j, i in product(range(1, order), repeat=2)]
            # face between (0, 1, 2, 3)
            + [(i, j, 0) for j, i in product(range(1, order), repeat=2)]
            # face between (4, 5, 6, 7)
            + [(i, j, order) for j, i in product(range(1, order), repeat=2)]
            )

    # add interior
    nodes += [(i, j, k) for k, j, i in product(range(1, order), repeat=3)]

    return nodes


def vtk_lagrange_quad_node_tuples(dims, order, vtk_version=(2, 1)):
    """
    :arg dims: dimension of the box, i.e. 1 corresponds to a curve, 2 to
        a quadrilateral, etc.
    :arg order: order of the polynomial representation, which also defines
        the number of nodes on the box.
    :arg vtk_version: a :class:`tuple` of two elements containing the version
        of the VTK XML file format in use. The ordering of some of the
        high-order elements changed between versions `2.1` and `2.2`.

    :return: a :class:`list` of ``dims``-dimensional tuples of integers
        up to ``order`` in the ordering expected by VTK. This list can be
        passed to :func:`vtk_lagrange_quad_node_tuples_to_permutation`
        to obtain a permutation from the order used by :mod:`modepy`.
    """
    if dims == 1:
        return vtk_lagrange_curve_node_tuples(order)
    elif dims == 2:
        return vtk_lagrange_quadrilateral_node_tuples(order)
    elif dims == 3:
        return vtk_lagrange_hexahedon_node_tuples(order, vtk_version=vtk_version)
    else:
        raise ValueError(f"unsupported dimension: {dims}")


def vtk_lagrange_quad_node_tuples_to_permutation(node_tuples):
    order = max([max(i) for i in node_tuples])
    dims = len(node_tuples[0])

    from itertools import product
    node_to_index = {
            node_tuple: i
            for i, node_tuple in enumerate(product(range(order + 1), repeat=dims))
            }

    assert len(node_tuples) == len(node_to_index)
    return [node_to_index[v] for v in node_tuples]

# }}}
