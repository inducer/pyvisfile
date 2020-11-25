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

import numpy as np


# {{{ type enums

class XdmfNumberType(enum.Enum):
    Float = enum.auto()
    Int = enum.auto()
    UInt = enum.auto()
    Char = enum.auto()
    UChar = enum.auto()


class XdmfFormat(enum.Enum):
    XML = enum.auto()
    HDF = enum.auto()
    Binary = enum.auto()


class XdmfEndian(enum.Enum):
    Native = enum.auto()
    Big = enum.auto()
    Little = enum.auto()


class XdmfCompression(enum.Enum):
    Raw = enum.auto()
    Zlib = enum.auto()
    BZip2 = enum.auto()


class XdmfItemType(enum.Enum):
    Uniform = enum.auto()
    Collection = enum.auto()
    Tree = enum.auto()
    HyperSlab = enum.auto()
    Coordinates = enum.auto()
    Function = enum.auto()


class XdmfGridType(enum.Enum):
    Uniform = enum.auto()
    Collection = enum.auto()
    Tree = enum.auto()
    SubSet = enum.auto()


class XdmfTypologyType(enum.Enum):
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


class XdmfGeometryType(enum.Enum):
    XYZ = enum.auto()
    XY = enum.auto()
    X_Y_Z = enum.auto()
    VxVyVz = enum.auto()
    Origin_DxDyDz = enum.auto()
    Origin_DxDy = enum.auto()


class XdmfTimeType(enum.Enum):
    Single = enum.auto()
    HyperSlab = enum.auto()
    List = enum.auto()
    Range = enum.auto()

# }}}
