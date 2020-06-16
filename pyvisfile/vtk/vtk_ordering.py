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
`this blog post <https://blog.kitware.com/modeling-arbitrary-order-lagrange-finite-elements-in-the-visualization-toolkit/>`_. The ordering in the new elements is as
follows:

    1. vertices of the element (in an order that matches the linear elements,
       e.g. :data:`~pyvisfile.vtk.VTK_TRIANGLE`)
    2. Edge (or face in 2D) nodes in sequence.
    3. Face (3D only) nodes. These are only the nodes interior to the face,
       i.e. without the edges, and they are reported by the same rules
       recursively.
    4. Interior nodes are also defined recursively.

To a large extent, matches the order used by ``gmsh`` and described
`here <https://gmsh.info/doc/texinfo/gmsh.html#Node-ordering>`_.

.. autofunction:: vtk_lagrange_simplex_node_tuples
.. autofunction:: vtk_lagrange_simplex_node_tuples_to_permutation
"""     # noqa


# {{{

def add_tuple_to_list(ary, x):
    return [add_tuples(x, y) for y in ary]

# }}}


# {{{ VTK_LAGRANGE_${SIMPLEX} (i.e. CURVE/TRIANGLE/TETRAHEDRON)

def vtk_lagrange_curve_node_tuples(order, is_consistent=False):
    if is_consistent:
        node_tuples = [(0,), (order,)] + [(i,) for i in range(1, order)]
    else:
        node_tuples = [(i,) for i in range(order + 1)]

    return node_tuples


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


def vtk_lagrange_simplex_node_tuples(dims, order, is_consistent=False):
    """
    :arg dims: dimension of the simplex, i.e. 1 corresponds to a curve, 2 to
        a triangle, etc.
    :arg order: order of the polynomial representation, which also defines
        the number of nodes on the simplex.
    :arg is_consistent: If *True*, 1D curve node ordering will follow the
        same rules as the higher-dimensional simplices by putting the
        vertices first. This is not the default in VTK as of version 8.1,
        when the higher-order elements were introduced.

    :return: a :class:`list` of ``dims``-dimensional tuples of integers
        up to ``order`` in the ordering expected by VTK. This list can be
        passed to :func:`vtk_lagrange_simplex_node_tuples_to_permutation`
        to obtain a permutation from the order used by :mod:`modepy`.
    """

    if dims == 1:
        return vtk_lagrange_curve_node_tuples(order, is_consistent=is_consistent)
    elif dims == 2:
        return vtk_lagrange_triangle_node_tuples(order)
    elif dims == 3:
        return vtk_lagrange_tetrahedron_node_tuples(order)
    else:
        raise ValueError("unsupported dimension: %d" % dims)


def vtk_lagrange_simplex_node_tuples_to_permutation(node_tuples):
    order = max([sum(i) for i in node_tuples])
    dims = len(node_tuples[0])

    node_to_index = dict(
            (node_tuple, i)
            for i, node_tuple in enumerate(gnitstam(order, dims))
            )

    assert len(node_tuples) == len(node_to_index)
    return [node_to_index[v] for v in node_tuples]

# }}}


# {{{ VTK_LAGRANGE_${QUAD} (i.e. QUADRILATERAL/HEXAHEDRON)

# }}}
