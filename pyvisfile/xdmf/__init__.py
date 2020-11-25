__copyright__ = "Copyright (C) 2020 Andreas Kloeckner"

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

import enum
from xml.etree.ElementTree import Element

import numpy as np

# {{{ xdmf tags

# {{{ attribute

class AttributeType(enum.Enum):
    Scalar = enum.auto()
    Vector = enum.auto()
    Tensor = enum.auto()
    Tensor6 = enum.auto()
    Matrix = enum.auto()


class AttributeCenter(enum.Enum):
    Node = enum.auto()
    Cell = enum.auto()
    Grid = enum.auto()
    Face = enum.auto()
    Edge = enum.auto()
    Other = enum.auto()


class Attribute(Element):
    def __init__(self, parent: Element, name: str,
            atype: AttributeType,
            acenter: AttributeCenter):
        super().__init__("Attribute", {
            "Name": name,
            "Center": center.name,
            "AttributeType": atype.name,
            })

        parent.append(self)

# }}}


# {{{ data item

class DataItemType(enum.Enum):
    Uniform = enum.auto()
    HyperSlab = enum.auto()
    Function = enum.auto()


class DataItemNumberType(enum.Enum):
    Char = enum.auto()
    UChar = enum.auto()
    Int = enum.auto()
    UInt = enum.auto()
    Float = enum.auto()


class DataItemFormat(enum.Enum):
    XML = enum.auto()
    HDF = enum.auto()
    Binary = enum.auto()
    TIFF = enum.auto()


class DataItemEndian(enum.Enum):
    Native = enum.auto()
    Big = enum.auto()
    Little = enum.auto()


class DataItem(Element):
    def __init__(self, parent: Element, name: str,
            itype: DataItemType,
            dimensions: List[int],
            dtype: DataItemNumberType,
            ntype: DataItemNumberType,
            precision: int,
            reference: str,
            endian: DataItemEndian,
            dformat: DataItemFormat):
        super().__init__("DataItem", {
            "Name": name,
            "ItemType": itype.name,
            "Dimensions": " ".join([str(i) for i in dimensions])
            "NumberType": ntype.name,
            "Precision": precision,
            "Reference": reference,
            "Endian": endian.name,
            "Format": dformat.name,
            })

        parent.append(self)

# }}}


# {{{ grid

class GridType(enum.Enum):
    Uniform = enum.auto()
    Collection = enum.auto()
    Tree = enum.auto()
    SubSet = enum.auto()


class CollectionType(enum.Enum):
    Spatial = enum.auto()
    Temporal = enum.auto()


class Grid(Element):
    def __init__(self, parent: Element, name: str,
            gtype: GridType
            ctype: CollectionType):
        super().__init__("Grid", {
            "GridType": gtype.name,
            "CollectionType": ctype.name
            })

        parent.append(self)

# }}}


# {{{ topology

class TypologyType(enum.Enum):
    # linear elements
    Polyvertex = enum.auto()
    Polyline = enum.auto()
    Polygon = enum.auto()
    Triangle = enum.auto()
    Quadrilateral = enum.auto()
    Tetrahedron = enum.auto()
    Pyramid = enum.auto()
    Wedge = enum.auto()
    Hexahedron = enum.auto()

    # quadratic elements
    Edge_3 = enum.auto()
    Triangle_6 = enum.auto()
    Quadrilateral_8 = enum.auto()
    Tetrahedron_10 = enum.auto()
    Pyramid_13 = enum.auto()
    Wedge_15 = enum.auto()
    Hexahedron_20 = enum.auto()

    Mixed = enum.auto()

    # structured
    2DSMesh = enum.auto()
    2DRectMesh = enum.auto()
    2DCoRectMesh = enum.auto()
    3DSMesh = enum.auto()
    3DRectMesh = enum.auto()
    3DCoRectmesh = enum.auto()

    # TODO: add the high-order elements when supported


class Topology(Element):
    def __init__(self, parent: Element,
            ttype: TopologyType,
            dimensons: List[int]):
        super().__init__("Topology", {
            "TopologyType": ttype.name,
            "Dimensions": " ".join([str(i) for i in dimensions]),
            })

        parent.append(self)

# }}}


# {{{ geometry

class GeometryType(enum.Enum):
    XY = enum.auto()
    XYZ = enum.auto()
    X_Y = enum.auto()
    X_Y_Z = enum.auto()
    VXVY = enum.auto()
    VXVYVZ = enum.auto()
    ORIGIN_DXDY = enum.auto()
    ORIGIN_DXDYDZ = enum.auto()


class Geometry(Element):
    def __init__(self, parent: Element, name: str,
            gtype: GeometryType):
        super().__init__("Geometry", {
            "Name": name,
            "GeometryType": gtype.name
            })

        parent.append(self)

# }}}


# {{{ time

class TimeType(enum.Enum):
    Single = enum.auto()
    HyperSlab = enum.auto()
    List = enum.auto()
    Range = enum.auto()

# }}}


# {{{ domain

class Domain(Element):
    def __init__(self, parent: Element, name: str):
        super().__init__("Domain", {
            "Name": name,
            })

        parent.append(self)

# }}}


# {{{ information

class Information(Element):
    def __init__(self, parent: Element, name: str, value: str):
        super().__init__("Information", {
            "Name": name,
            "Value": str(value),
            })

        parent.append(self)

# }}}

# }}}


# {{{ xdmf writer


# }}}
