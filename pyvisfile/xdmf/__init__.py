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

import os
import enum

from typing import Any, Dict, Optional, Tuple, Union
from xml.etree.ElementTree import Element, ElementTree

import numpy as np

__doc__ = """
Xdmf Tags
---------

DataItem
^^^^^^^^

.. autoclass:: DataItemType
    :show-inheritance:
    :members:
    :undoc-members:

.. autoclass:: DataItemNumberType
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: DataItemFormat
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: DataItemEndian
    :show-inheritance:
    :members:
    :undoc-members:

.. autoclass:: DataItem

Domain
^^^^^^

.. autoclass:: Domain

Grid
^^^^

.. autoclass:: GridType
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: CollectionType
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: Grid


Topology
^^^^^^^^

.. autoclass:: TopologyType
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: Topology

Geometry
^^^^^^^^

.. autoclass:: GeometryType
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: Geometry

Attribute
^^^^^^^^^

.. autoclass:: AttributeType
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: AttributeCenter
    :show-inheritance:
    :members:
    :undoc-members:
.. autoclass:: Attribute

Time
^^^^

.. autoclass:: Time
    :members:

Information
^^^^^^^^^^^

.. autoclass:: Information
    :members:

XInclude
^^^^^^^^

.. autoclass:: XInclude
    :members:

Writing
-------

.. autoclass:: DataArray
.. autoclass:: NumpyDataArray

.. autoclass:: XdmfGrid
.. autoclass:: XdmfUnstructuredGrid
    :show-inheritance:

.. autoclass:: XdmfWriter
"""


# {{{ utils

def _stringify(obj):
    if isinstance(obj, (list, tuple)):
        return " ".join(str(c) for c in obj)
    return str(obj)


class XdmfElement(Element):
    """Base class for all the XDMF tags.

    .. attribute:: name

        The ``Name`` attribute the tags. This attribute is optional, so
        it can return *None* if not set.

    .. automethod:: replace
    """

    def __init__(self,
            parent: Optional[Element],
            tag: str,
            attrib: Dict[str, Optional[Any]]):
        super().__init__(tag, attrib={
            k: _stringify(v) for k, v in attrib.items() if v is not None
            })

        self.parent = parent
        if parent is not None:
            parent.append(self)

    @property
    def name(self):
        return self.get("Name")

    def replace(self, **kwargs):
        """Duplicate the current tag with updated attributes from *kwargs*."""
        parent = kwargs.pop("parent", self.parent)
        tag = kwargs.pop("tag", self.tag)

        attrib = self.attrib.copy()
        attrib.update(kwargs)

        return XdmfElement.__init__(self, parent, tag, attrib=attrib)

# }}}


# {{{ xdmf tags

# {{{ attribute

# {{{ unsupported

# NOTE: these are taken from VTK source in
#
#   https://gitlab.kitware.com/vtk/vtk/-/blob/c138bfae93f570b467e7f4fdc0c42d974cd684f4/IO/Xdmf3/vtkXdmf3DataSet.cxx#L2278
#
# and are currently unsupported here (someone needs to figure out how to write
# them). They were introduced in
#
#   https://gitlab.kitware.com/xdmf/xdmf/-/merge_requests/41
#   https://gitlab.kitware.com/vtk/vtk/-/merge_requests/3194

class AttributeElementFamily(enum.Enum):
    """High-order element families for ``FiniteElementFunction``."""
    DG = enum.auto()    #: Discontinuous Galerkin elements for simplices.
    CG = enum.auto()    #: Continuous Galerkin elements for simplices.
    Q = enum.auto()     #: Continuous Galerkin elements for quadrilaterals.
    DQ = enum.auto()    #: Discontinuous Galerkin elements for quadrilaterals.
    RT = enum.auto()    #: Raviart-Thomas elements on triangles.


class AttributeElementCell(enum.Enum):
    """Reference element types for ``FiniteElementFunction``."""
    interval = enum.auto()
    triangle = enum.auto()
    tetrahedron = enum.auto()
    quadrilateral = enum.auto()
    hexahedron = enum.auto()

# }}}


class AttributeType(enum.Enum):
    """Rank of the attribute stored on the mesh."""
    # NOTE: integer ids taken from
    # https://gitlab.kitware.com/xdmf/xdmf/-/blob/04a84bab0eb1568e0f1a27c8fb60c6931efda003/XdmfAttributeType.hpp#L129
    Scalar = 200
    Vector = 201
    Tensor = 202
    Matrix = 203
    Tensor6 = 204
    GlobalId = 205

    @staticmethod
    def from_shape(shape: Tuple[int, ...]) -> "AttributeType":
        # https://github.com/nschloe/meshio/blob/37673c8fb938ad73d92fb3171dee3eb193b5e7ac/meshio/xdmf/common.py#L162
        if len(shape) == 1 or (len(shape) == 2 and shape[1] == 1):
            return AttributeType.Scalar
        elif len(shape) == 2 and shape[0] in [2, 3]:
            return AttributeType.Vector
        elif len(shape) == 2 and shape[0] in [4, 9]:
            return AttributeType.Tensor
        elif len(shape) == 2 and shape[0] == 6:
            return AttributeType.Tensor6
        elif len(shape) == 3:
            return AttributeType.Matrix
        else:
            raise ValueError(f"cannot determine attribute type from shape '{shape}'")


class AttributeCenter(enum.Enum):
    """Center of the attribute stored on the mesh."""
    # NOTE: integer ids taken from
    # https://gitlab.kitware.com/xdmf/xdmf/-/blob/04a84bab0eb1568e0f1a27c8fb60c6931efda003/XdmfAttributeCenter.hpp#L126
    Grid = 100
    Cell = 101
    Face = 102
    Edge = 103
    Node = 104
    # NOTE: only for `FiniteElementFunction` attributes, which are not supported
    Other = 105


class Attribute(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            name: Optional[str] = None,
            atype: AttributeType = AttributeType.Scalar,
            acenter: AttributeCenter = AttributeCenter.Node,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        super().__init__(parent, "Attribute", {
            "Name": name,
            "Center": acenter.name,
            "AttributeType": atype.name,
            })

# }}}


# {{{ data item

class DataItemType(enum.Enum):
    """Data layout of an item."""
    Uniform = enum.auto()
    HyperSlab = enum.auto()
    Function = enum.auto()


class DataItemNumberType(enum.Enum):
    """Basic number types for an item."""
    Char = enum.auto()
    UChar = enum.auto()
    Int = enum.auto()
    UInt = enum.auto()
    Float = enum.auto()

    @staticmethod
    def from_dtype(dtype: np.dtype) -> "DataItemNumberType":
        if dtype.kind == "i":
            return DataItemNumberType.Int
        elif dtype.kind == "u":
            return DataItemNumberType.UInt
        elif dtype.kind == "f":
            return DataItemNumberType.Float
        else:
            raise ValueError(f"unsupported dtype: '{dtype}'")


class DataItemFormat(enum.Enum):
    """Format in which the item is stored."""
    XML = enum.auto()
    HDF = enum.auto()
    Binary = enum.auto()
    # NOTE: unsupported as it's pretty much undocumented
    TIFF = enum.auto()


class DataItemEndian(enum.Enum):
    """Endianess of the data stored in the item."""
    # NOTE: integer ids taken from
    # https://gitlab.kitware.com/xdmf/xdmf/-/blob/04a84bab0eb1568e0f1a27c8fb60c6931efda003/core/XdmfBinaryController.hpp#L211
    Big = 50
    Little = 51
    Native = 52

    @staticmethod
    def from_system() -> "DataItemEndian":
        import sys
        if sys.byteorder == "little":
            return DataItemEndian.Little
        elif sys.byteorder == "big":
            return DataItemEndian.Big
        else:
            return DataItemEndian.Native


class DataItem(XdmfElement):
    """A :class:`DataItem` describes the storage of actual values in an
    XDMF file. This can be inline ASCII data, the path to a binary file
    or a reference to another :class:`DataItem`.

    .. attribute:: dimensions

        Analogous to :attr:`numpy.ndarray.shape`.

    .. automethod:: __init__
    .. automethod:: as_reference
    """

    def __init__(
            self, *,
            dimensions: Optional[Tuple[int, ...]] = None,
            name: Optional[str] = None,
            itype: Optional[DataItemType] = DataItemType.Uniform,
            ntype: Optional[DataItemNumberType] = DataItemNumberType.Float,
            precision: Optional[int] = 4,
            reference: Optional[str] = None,
            function: Optional[str] = None,
            endian: Optional[DataItemEndian] = DataItemEndian.Native,
            dformat: Optional[DataItemFormat] = DataItemFormat.XML,
            parent: Optional[Element] = None,
            data: Optional[str] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        :param reference: path to another :class:`DataItem`.
            Use :meth:`as_reference` to populate.
        :param data: data contained inside the :class:`DataItem`. This is
            usually a path to a binary file.
        """

        self._dimensions = dimensions

        super().__init__(parent, "DataItem", {
            "Name": name,
            "ItemType": itype.name if itype is not None else itype,
            "Dimensions": dimensions,
            "NumberType": ntype.name if ntype is not None else ntype,
            "Precision": precision,
            "Reference": reference,
            "Function": function,
            "Endian": endian.name if endian is not None else endian,
            "Format": dformat.name if dformat is not None else dformat,
            })

        if data is not None:
            self.text = data

    @property
    def dimensions(self):
        if self._dimensions is None:
            raise AttributeError

        return self._dimensions

    @classmethod
    def as_reference(cls, reference_name: str, *,
            parent: Optional[Element] = None) -> "DataItem":
        """
        :param reference_name: a name or an absolute reference to another
            :class:`DataItem`. The name is just the ``Name`` attribute of
            the item, which is assumed to be in the top :class:`Domain`. If
            another :class:`DataItem` needs to be references, or there are
            multiple domains, use an absolute reference path, as defined
            in the `XDMF docs <https://www.xdmf.org/index.php/XDMF_Model_and_Format>`__.
        """     # noqa: E501

        if not reference_name.startswith("/"):
            reference = f"/Xdmf/Domain/DataItem[@Name='{reference_name}']"
        else:
            reference = reference_name

        return cls(
                reference="XML",
                data=reference,
                itype=None, ntype=None, precision=None,
                endian=None, dformat=None,
                parent=parent)


def _data_item_format_from_str(text: str) -> DataItemFormat:
    # NOTE: this handles two cases (not meant to be too smart about it)
    # 1. if the text is just `some_file.bin` or `some_file.out`, we assume it's
    #    a custom binary file.
    # 2. if the text is `some_file.h5:/group/dataset`, we assume it's an HDF5
    #    file.
    if ":" not in text:
        return DataItemFormat.Binary

    try:
        filename, _ = text.split(":")
    except ValueError as exc:
        raise ValueError("cannot determine format from text") from exc

    if filename.endswith(".h5"):
        return DataItemFormat.HDF
    else:
        raise ValueError("cannot determine format from text")


def _data_item_from_numpy(
        ary: np.ndarray, *,
        name: Optional[str] = None,
        parent: Optional[Element] = None,
        data: Optional[str] = None,
        dformat: Optional[DataItemFormat] = None) -> DataItem:
    """Create a :class:`DataItem` from a given :class:`~numpy.ndarray`.

    .. note::

        This is meant for internal use only. Use :class:`NumpyDataArray` instead.
    """

    if dformat is None:
        if data is None:
            dformat = DataItemFormat.XML
        else:
            dformat = _data_item_format_from_str(data)

    return DataItem(
            name=name,
            dimensions=ary.shape,
            itype=DataItemType.Uniform,
            ntype=DataItemNumberType.from_dtype(ary.dtype),
            precision=ary.dtype.itemsize,
            endian=DataItemEndian.from_system(),
            dformat=dformat,
            parent=parent,
            data=data,
            )


def _join_data_items(
        items: Tuple[DataItem, ...], *,
        parent: Optional[Element] = None) -> DataItem:
    r"""Joins several :class:`DataItem`\ s using a :attr:`DataItemType.Function`
    as::

        JOIN($0, $1, ...)

    (Used for describing vectors from scalar data.)
    See the `Xdmf Function docs <https://www.xdmf.org/index.php/XDMF_Model_and_Format#Function>`__
    for more information.

    :returns: the newly created :class:`DataItem` that joins the input items.
    """     # noqa: E501

    if len(items) == 1:
        item = items[0]
    else:
        from pytools import is_single_valued
        if not is_single_valued(item.dimensions for item in items):
            raise ValueError("items must have the same dimension")

        dimensions = (len(items),) + items[0].dimensions
        ids = ", ".join(f"${i}" for i in range(dimensions[0]))

        item = DataItem(
                dimensions=dimensions,
                itype=DataItemType.Function,
                ntype=None,
                precision=None,
                function=f"JOIN({ids})",
                endian=None,
                dformat=None,
                )

        for subitem in items:
            item.append(subitem)

    if parent is not None:
        parent.append(item)

    return item

# }}}


# {{{ grid

class GridType(enum.Enum):
    """General structure of the connectivity."""
    Uniform = enum.auto()
    Collection = enum.auto()
    Tree = enum.auto()
    SubSet = enum.auto()


class CollectionType(enum.Enum):
    Spatial = enum.auto()
    Temporal = enum.auto()


class Grid(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            name: Optional[str] = None,
            gtype: GridType = GridType.Uniform,
            ctype: Optional[CollectionType] = None,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        if gtype == GridType.Collection and ctype is None:
            ctype = CollectionType.Spatial

        super().__init__(parent, "Grid", {
            "Name": name,
            "GridType": gtype.name,
            "CollectionType": ctype.name if ctype is not None else ctype,
            })

# }}}


# {{{ topology

class TopologyType(enum.IntEnum):
    """Element and mesh layouts."""
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
    # high-order elements from XdmfTopologyType.cpp
    Hexahedron_24 = 0x31
    Hexahedron_27 = 0x32
    Hexahedron_64 = 0x33
    Hexahedron_125 = 0x34
    Hexahedron_216 = 0x35
    Hexahedron_343 = 0x36
    Hexahedron_512 = 0x37
    Hexahedron_729 = 0x38
    Hexahedron_1000 = 0x39
    Hexahedron_1331 = 0x40
    # spectral elements from XdmfTopologyType.cpp
    Hexahedron_Spectral_64 = 0x41
    Hexahedron_Spectral_125 = 0x42
    Hexahedron_Spectral_216 = 0x43
    Hexahedron_Spectral_343 = 0x44
    Hexahedron_Spectral_512 = 0x45
    Hexahedron_Spectral_729 = 0x46
    Hexahedron_Spectral_1000 = 0x47
    Hexahedron_Spectral_1331 = 0x48

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
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            ttype: TopologyType,
            nodes_per_element: Optional[int] = None,
            number_of_elements: Optional[int] = None,
            dimensions: Optional[Tuple[int, ...]] = None,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        ttype_name = _XDMF_TOPOLOGY_TYPE_TO_NAME.get(ttype, ttype.name)
        if ttype in _XDMF_ELEMENT_NODE_COUNT or ttype in _XDMF_STRUCTURED_GRIDS:
            if nodes_per_element is not None:
                raise ValueError(f"cannot set 'nodes_per_element' for {ttype_name}")
        else:
            if nodes_per_element is None:
                raise ValueError(f"'nodes_per_element' required for {ttype_name}")

        super().__init__(parent, "Topology", {
            "TopologyType": ttype_name,
            "Dimensions": dimensions,
            "NodesPerElement": nodes_per_element,
            "NumberOfElements": number_of_elements,
            })


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
        TopologyType.Hexahedron_24: 24,
        TopologyType.Hexahedron_27: 27,
        TopologyType.Hexahedron_64: 64,
        TopologyType.Hexahedron_125: 125,
        TopologyType.Hexahedron_216: 216,
        TopologyType.Hexahedron_343: 343,
        TopologyType.Hexahedron_512: 512,
        TopologyType.Hexahedron_729: 729,
        TopologyType.Hexahedron_1000: 1000,
        TopologyType.Hexahedron_1331: 1331,
        TopologyType.Hexahedron_Spectral_64: 64,
        TopologyType.Hexahedron_Spectral_125: 125,
        TopologyType.Hexahedron_Spectral_216: 216,
        TopologyType.Hexahedron_Spectral_343: 343,
        TopologyType.Hexahedron_Spectral_512: 512,
        TopologyType.Hexahedron_Spectral_729: 729,
        TopologyType.Hexahedron_Spectral_1000: 1000,
        TopologyType.Hexahedron_Spectral_1331: 1331,
        }


_XDMF_STRUCTURED_GRIDS = {
        TopologyType.SMesh2D,
        TopologyType.SMesh3D,
        TopologyType.RectMesh2D,
        TopologyType.RectMesh3D,
        TopologyType.CoRectMesh2D,
        TopologyType.CoRectMesh3D,
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
    """Data layout of the node coordinates."""
    XY = enum.auto()
    XYZ = enum.auto()
    # NOTE: all of these don't seem to be supported in VTK/Paraview with
    # XDMF3 for some reason, but are still mentioned in the XDMF source
    VXVY = enum.auto()
    VXVYVZ = enum.auto()
    ORIGIN_DXDY = enum.auto()
    ORIGIN_DXDYDZ = enum.auto()


class Geometry(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            name: Optional[str] = None,
            gtype: GeometryType = GeometryType.XYZ,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        super().__init__(parent, "Geometry", {
            "Name": name,
            "GeometryType": gtype.name,
            })

# }}}


# {{{ time

class Time(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            value: str,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        super().__init__(parent, "Time", {
            "Value": value,
            })

# }}}


# {{{ domain

class Domain(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            name: Optional[str] = None,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        super().__init__(parent, "Domain", {
            "Name": name,
            })

# }}}


# {{{ information

class Information(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            name: str,
            value: str,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        """

        super().__init__(parent, "Information", {
            "Name": name,
            "Value": value,
            })

# }}}


# {{{ include

class XInclude(XdmfElement):
    """
    .. automethod:: __init__
    """

    def __init__(
            self, *,
            href: Optional[str],
            xpointer: Optional[str] = None,
            parent: Optional[Element] = None,
            ):
        """
        :param parent: if provided, *self* is appended to the element.
        :param xpointer: path inside the file represented by *href*.
        """
        if xpointer is not None:
            xpointer = f"xpointer({xpointer})"

        super().__init__(parent, "xi:include", {
            "href": href,
            "xpointer": xpointer,
            })

# }}}

# }}}


# {{{ data arrays

def _ndarray_to_string(ary):
    if not isinstance(ary, np.ndarray):
        raise TypeError(f"expected an 'ndarray', got '{type(ary).__name__}'")

    ntype = DataItemNumberType.from_dtype(ary.dtype)
    if ntype == DataItemNumberType.Int or ntype == DataItemNumberType.UInt:
        fmt = "%d"
    elif ntype == DataItemNumberType.Float:
        if ary.dtype.itemsize == 8:
            fmt = "%.16e"
        elif ary.dtype.itemsize == 4:
            fmt = "%.8e"
        else:
            raise ValueError(f"unsupported dtype item size: {ary.dtype.itemsize}")
    else:
        raise ValueError(f"unsupported dtype: '{ary.dtype}'")

    import io
    bio = io.BytesIO()
    np.savetxt(bio, ary, fmt=fmt)

    return "\n" + bio.getvalue().decode()


def _geometry_type_from_points(points):
    dims = points.shape[-1]

    if len(points.components) == 1:
        if dims == 2:
            return GeometryType.XY
        elif dims == 3:
            return GeometryType.XYZ
        else:
            raise ValueError(f"unsupported dimension: '{dims}'")
    else:
        if dims == 2:
            return GeometryType.VXVY
        elif dims == 3:
            return GeometryType.VXVYVZ
        else:
            raise ValueError(f"unsupported dimension: '{dims}'")


class DataArray:
    r"""An array represented as a list of :class:`DataItem`\ s.

    .. automethod:: __init__
    .. automethod:: as_data_item
    """

    def __init__(
            self,
            components: Tuple[DataItem, ...], *,
            name: Optional[str] = None,
            acenter: Optional[AttributeCenter] = None,
            atype: Optional[AttributeType] = None,
            ):
        r"""
        :param components: a description of each component of an array.
        :param name: name of the array. This name will be used if the array
            is added as an attribute, otherwise the names of the *components*
            are used.
        """
        if not isinstance(components, tuple):
            raise TypeError("'components' should be a tuple")

        if name is None:
            if len(components) == 1:
                name = components[0].name
            else:
                # NOTE: assumes component names are {name}_{suffix}
                name = os.path.commonprefix([
                    c.name for c in components
                    ]).strip("_")

        self.components = components

        self.name = name
        self.acenter = acenter
        self.atype = atype

    @property
    def shape(self):
        if len(self.components) == 1:
            return self.components[0].dimensions
        else:
            return (len(self.components),) + self.components[0].dimensions

    def as_data_item(self, *,
            parent: Optional[Element] = None) -> Tuple[DataItem, ...]:
        r"""Finalize the :class:`DataArray` and construct :class:`DataItem`\ s
        to be written to a file.
        """

        items = self.components[:]
        if parent is not None:
            for item in items:
                if parent.tag != "Attribute":
                    item.set("Name", self.name)

                parent.append(item)

        return items

    @classmethod
    def from_dataset(cls, dset,
            acenter: AttributeCenter = AttributeCenter.Node,
            atype: Optional[AttributeType] = None) -> "DataArray":
        filename = dset.file.filename
        data = f"{filename}:{dset.name}"
        name = dset.name.split("/")[-1]

        item = _data_item_from_numpy(dset,
                data=data,
                dformat=DataItemFormat.HDF)

        return cls(
                components=(item,),
                name=name,
                acenter=acenter,
                atype=atype)


class NumpyDataArray(DataArray):
    """
    .. automethod:: __init__
    """

    def __init__(
            self,
            ary: np.ndarray, *,
            acenter: Optional[AttributeCenter] = None,
            name: Optional[str] = None,
            ):
        """
        :param ary: if this is an :class:`object` array, each entry is considered
            a different component and will consist of a separate
            :class:`DataItem`.
        """

        if ary.dtype.char == "O":
            from pytools import is_single_valued
            if not is_single_valued(iary.shape for iary in ary):
                raise ValueError("'ary' components must have the same size")

            items = tuple([
                    _data_item_from_numpy(iary, name=f"{name}_{i}")
                    for i, iary in enumerate(ary)
                    ])
        else:
            items = (_data_item_from_numpy(ary, name=name),)

        super().__init__(items, name=name, acenter=acenter)
        self.ary = ary

    def as_data_item(self, *,
            parent: Optional[Element] = None) -> Tuple[DataItem, ...]:
        items = super().as_data_item(parent=parent)

        if self.ary.dtype.char == "O":
            ary = tuple(self.ary)
        else:
            ary = (self.ary,)

        for item, iary in zip(items, ary):
            item.text = _ndarray_to_string(iary)

        return items

# }}}


# {{{ grids

class XdmfGrid:
    """
    .. automethod:: __init__
    .. automethod:: add_attribute
    """

    def __init__(self, root: Grid):
        self.root = root

    def getroot(self):
        return self.root

    def add_attribute(self, ary: DataArray, *, join: bool = True) -> Attribute:
        """
        :param ary:
        :param join: If *True* and *ary* has multiple components, they are
            joined using an XDMF Function.
        """

        acenter = ary.acenter
        if acenter is None:
            acenter = AttributeCenter.Node

        atype = ary.atype
        if atype is None:
            atype = AttributeType.from_shape(ary.shape[::-1])

        attr = Attribute(
                name=ary.name,
                atype=atype,
                acenter=acenter,
                parent=self.getroot(),
                )

        if join:
            items = ary.as_data_item()
            _join_data_items(items, parent=attr)
        else:
            ary.as_data_item(parent=attr)

        return attr


class XdmfUnstructuredGrid(XdmfGrid):
    """
    .. automethod:: __init__
    """

    def __init__(self,
            points: DataArray,
            connectivity: DataArray, *,
            topology_type: Union[Topology, TopologyType],
            name: Optional[str] = None,
            geometry_type: Optional[GeometryType] = None):
        if geometry_type is None:
            geometry_type = _geometry_type_from_points(points)

        if geometry_type not in (GeometryType.XY, GeometryType.XYZ):
            # NOTE: Paraview 5.8 seems confused when using VXVY geometry types
            raise ValueError(f"unsupported geometry type: '{geometry_type}'")

        grid = Grid(parent=None, name=name)

        nelements = np.prod(connectivity.shape[:-1])
        if isinstance(topology_type, TopologyType):
            if topology_type == TopologyType.Polyline:
                nodes_per_element = 2
            else:
                nodes_per_element = None

            topology = Topology(
                    parent=grid,
                    ttype=topology_type,
                    nodes_per_element=nodes_per_element,
                    number_of_elements=nelements)
        elif isinstance(topology, Topology):
            topology = topology_type.replace({
                "parent": grid,
                "number_of_elements": nelements
                })
        else:
            raise TypeError(f"unsupported type: {type(topology_type).__name__}")

        connectivity.as_data_item(parent=topology)

        geometry = Geometry(parent=grid, gtype=geometry_type)
        points.as_data_item(parent=geometry)

        super().__init__(grid)

# }}}


# {{{ writer

class XdmfWriter(ElementTree):
    """
    .. automethod:: __init__
    .. automethod:: write
    .. automethod:: write_pretty
    """

    def __init__(self,
            grids: Tuple[XdmfGrid, ...], *,
            arrays: Optional[Tuple[DataArray, ...]] = None,
            tags: Optional[Tuple[Element, ...]] = None):
        r"""
        :param grids: a :class:`tuple` of grids to be added to the
            top :class:`Domain`. Currently only a single domain is supported.
        :param arrays: additional :class:`DataArray`\ s to be added to the
            top :class:`Domain`, as opposed to as attribute on the grids.
        """
        root = Element("Xdmf", {
            "xmlns:xi": "http://www.w3.org/2001/XInclude",
            "Version": "3.0",
            })

        domain = Domain(parent=root)
        if arrays is not None:
            for ary in arrays:
                ary.as_data_item(parent=domain)

        if tags is not None:
            for tag in tags:
                domain.append(tag)

        for grid in grids:
            domain.append(grid.getroot())

        super().__init__(root)

    def write_pretty(self, filename):
        """Produces a nicer-looking XML file with clean indentation."""
        # https://stackoverflow.com/a/1206856
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
        """Write the the XDMF file."""
        super().write(
                filename,
                encoding="utf-8",
                xml_declaration=True,
                short_empty_elements=False,
                )

# }}}
