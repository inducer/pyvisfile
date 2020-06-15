from pytools import (
        add_tuples,
        generate_nonnegative_integer_tuples_summing_to_at_most as gnitstam)


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


# {{{ VTK_LAGRANGE_QUADS (i.e. QUADRILATERAL/HEXAHEDRON)

# }}}
