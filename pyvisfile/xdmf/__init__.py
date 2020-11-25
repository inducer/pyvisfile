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
from typing import Tuple, Optional, Union
from xml.etree.ElementTree import Element, ElementTree

import numpy as np

# {{{ xdmf tags

class XdmfElement(Element):
    def __init__(self, parent, tag, attrib):
        super().__init__(tag,
                {k: v for k, v in attrib.items() if v is not None}
                )
        parent.append(self)


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


class Attribute(XdmfElement):
    def __init__(self, parent: Element, *,
            atype: AttributeType = AttributeType.Scalar,
            acenter: AttributeCenter = AttributeCenter.Node,
            name: Optional[str] = None,
            ):
        super().__init__(parent, "Attribute", {
            "Name": name,
            "Center": center.name,
            "AttributeType": atype.name,
            })

# }}}


# {{{ data item

def _numpy_to_xdmf_number_type(dtype):
    if dtype.type in (np.int8, np.int16, np.int32, np.int64, np.int):
        return DataItemNumberType.Int
    elif dtype.type in (np.uint8, np.uint16, np.uint32, np.uint64, np.uint):
        return DataItemNumberType.UInt
    elif dtype.type in (np.float16, np.float32, np.float64, np.float128):
        return DataItemNumberType.Float
    else:
        raise ValueError(f"unsupported dtype: '{dtype}'")


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


class DataItem(XdmfElement):
    def __init__(self, parent: Element, *,
            dimensions: Tuple[int],
            name: Optional[str] = None,
            itype: DataItemType = DataItemType.Uniform,
            ntype: DataItemNumberType = DataItemNumberType.Float,
            precision: int = 4,
            reference: Optional[str] = None,
            endian: DataItemEndian = DataItemEndian.Native,
            dformat: DataItemFormat = DataItemFormat.XML):
        super().__init__(parent, "DataItem", {
            "Name": name,
            "ItemType": itype.name,
            "Dimensions": " ".join([str(i) for i in dimensions]),
            "NumberType": ntype.name,
            "Precision": precision,
            "Reference": reference,
            "Endian": endian.name,
            "Format": dformat.name,
            })

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


class Grid(XdmfElement):
    def __init__(self, parent: Element, *,
            name: Optional[str] = None,
            gtype: GridType = GridType.Uniform,
            ctype: CollectionType = CollectionType.Spatial):
        super().__init__(parent, "Grid", {
            "Name": name,
            "GridType": gtype.name,
            "CollectionType": ctype.name
            })

# }}}


# {{{ topology

class TopologyType(enum.IntEnum):
    NoTopology = 0x0
    Mixed = 0x70

    # linear elements from XdmfTopologyType.cpp
    Polyvertex = 0x1
    Polyline = 0x2
    Polygon = 0x3
    Triangle = 0x4
    Quadrilateral = 0x5
    Tetrahedron = 0x6
    Pyramid = 0x7
    Wedge = 0x8
    Hexahedron = 0x9
    Polyhedron = 0x10
    # quadratic elements from XdmfTopologyType.cpp
    Edge_3 = 0x22
    Triangle_6 = 0x24
    Quadrilateral_8 = 0x25
    Tetrahedron_10 = 0x26
    Pyramid_13 = 0x27
    Wedge_15 = 0x28
    Wedge_18 = 0x29
    Hexahedron_20 = 0x30
    # TODO: add the high-order elements when supported

    # structured from XdmfCurvilinearGrid.cpp
    SMesh2D = 0x1110        # Curvilinear mesh
    SMesh3D = 0x1110
    # structured from XdfmRectilinearGrid.cpp
    RectMesh2D = 0x1101     # Mesh with perpendicular axes
    RectMesh3D = 0x1101
    # stuctured from XdmfRegularGrid.cpp
    CoRectMesh2D = 0x1102   # Mesh with equally spaced perpendicular axes
    CoRectMesh3D = 0x1102


class Topology(XdmfElement):
    def __init__(self, parent: Element, *,
            ttype: TopologyType,
            dimensons: Tuple[int]):
        super().__init__("Topology", {
            "TopologyType": _XDMF_TOPOLOGY_TYPE_TO_NAME.get(ttype, ttype.name),
            "Dimensions": " ".join([str(i) for i in dimensions]),
            })

        parent.append(self)


_XDMF_ELEMENT_NODE_COUNT = {
        TopologyType.Polyvertex: 1,
        # TopologyType.Polyline: user-defined
        # TopologyType.Polygon: user-defined
        TopologyType.Triangle: 3,
        TopologyType.Quadrilateral: 4,
        TopologyType.Tetrahedron: 4,
        TopologyType.Pyramid: 5,
        TopologyType.Wedge: 6,
        TopologyType.Hexahedron: 8,
        # TopologyType.Polyhedron: user-defined
        TopologyType.Edge_3: 3,
        TopologyType.Triangle_6: 6,
        TopologyType.Quadrilateral_8: 8,
        TopologyType.Tetrahedron_10: 10,
        TopologyType.Pyramid_13: 13,
        TopologyType.Wedge_15: 15,
        TopologyType.Wedge_18: 18,
        TopologyType.Hexahedron_20: 20,
        }


# NOTE: the names in TopologyType are weird because python identifiers cannot
# start with a number, so 2DSMesh is not allowed
_XDMF_TOPOLOGY_TYPE_TO_NAME = {
        TopologyType.SMesh2D: "2DSMesh",
        TopologyType.SMesh3D: "3DSMesh",
        TopologyType.RectMesh2D: "2DRectMesh",
        TopologyType.RectMesh3D: "3DRectMesh",
        TopologyType.CoRectMesh2D: "2DCoRectMesh",
        TopologyType.CoRectMesh3D: "3DCoRectMesh",
        }


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


class Geometry(XdmfElement):
    def __init__(self, parent: Element, *,
            name: Optional[str],
            gtype: GeometryType = GeometryType.XYZ):
        super().__init__(parent, "Geometry", {
            "Name": name,
            "GeometryType": gtype.name,
            })

# }}}


# {{{ time

class TimeType(enum.Enum):
    Single = enum.auto()
    HyperSlab = enum.auto()
    List = enum.auto()
    Range = enum.auto()


class Time(XdmfElement):
    def __init__(self, parent: Element, *, value: str):
        super().__init__(parent, "Time", {
            "Value": value,
            })

# }}}


# {{{ domain

class Domain(XdmfElement):
    def __init__(self, parent: Element, *,
            name: Optional[str] = None):
        super().__init__(parent, "Domain", {
            "Name": name,
            })

# }}}


# {{{ information

class Information(XdmfElement):
    def __init__(self, parent: Element, name: str, value: str):
        super().__init__(parent, "Information", {
            "Name": name,
            "Value": str(value),
            })

# }}}

# }}}


# {{{ xdmf writer

class DataItemArray:
    def __init__(self, name: str, data: Union[str, np.ndarray], *,
            dtype: Optional[np.dtype] = None,
            shape: Optional[Tuple[int]] = None):
        if dtype is None:
            if not isinstance(data, np.ndarray):
                raise ValueError("'dtype' not provided for non-array data")

            dtype = data.dtype

        if shape is None:
            if not isinstance(data, np.ndarray):
                raise ValueError("'shape' not provided for non-array data")

            shape = data.shape

        self.name = name
        self.dtype = dtype
        self.shape = shape
        self.data = data

    def as_data_item(self, parent):
        if isinstance(data, str):
            dformat = DataItemFormat.HDF
        else:
            dformat = DataItemFormat.XML

        import sys
        if sys.byteorder == "little":
            endian = DataItemEndian.Little
        elif sys.byteorder == "big":
            endian = DataItemEndian.Big
        else:
            endian = DataItemEndian.Native

        item = DataItem(parent, self.name,
                itype=DataItemType.Uniform,
                dimensions=self.shape,
                ntype=_numpy_to_xdmf_number_type(self.dtype),
                precision=self.dtype.itemsize,
                endian=endian,
                dformat=dformat)

        item.text = self.data
        return item


class XdmfElementTree(ElementTree):
    def __init__(self):
        root = Element("Xdmf", {
            "Version": "3.0",
            })
        super().__init__(root)

    def add_attribute(self, attr):
        pass

    def write_pretty(self, filename):
        from xml.etree.ElementTree import tostring
        from xml.dom import minidom
        dom = minidom.parseString(tostring(
            self.getroot(),
            encoding="utf-8",
            short_empty_elements=False,
            ))

        with open(filename, "wb") as fd:
            fd.write(dom.toprettyxml(indent="  ", encoding="utf-8"))

    def write(self, filename):
        super().write(filename,
                encoding="utf-8",
                xml_declaration=True,
                short_empty_elements=False,
                )


class XdmfUnstructuredGrid(XdmfElementTree):
    def __init__(self):
        super().__init__()

        domain = Domain(self.getroot())
        grid = Grid(domain)


class XdmfStructuredGrid(XdmfElementTree):
    def __init__(self):
        super().__init__()


# }}}
