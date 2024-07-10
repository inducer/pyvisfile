"""Generic support for new-style (XML) VTK visualization data files."""

__copyright__ = "Copyright (C) 2007 Andreas Kloeckner"

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

import pathlib
from abc import ABC, abstractmethod
from typing import Any, ByteString, ClassVar, List, Optional, TextIO, Tuple, Union, cast

import numpy as np


__doc__ = """

Constants
---------

Vector formats
^^^^^^^^^^^^^^

.. data:: VF_LIST_OF_COMPONENTS

    ``[[x0, y0, z0], [x1, y1, z1]]``

.. data:: VF_LIST_OF_VECTORS

    ``[[x0, x1], [y0, y1], [z0, z1]]``

Element types
^^^^^^^^^^^^^

.. data:: VTK_VERTEX
.. data:: VTK_POLY_VERTEX
.. data:: VTK_LINE
.. data:: VTK_POLY_LINE
.. data:: VTK_TRIANGLE
.. data:: VTK_TRIANGLE_STRIP
.. data:: VTK_POLYGON
.. data:: VTK_PIXEL
.. data:: VTK_QUAD
.. data:: VTK_TETRA
.. data:: VTK_VOXEL
.. data:: VTK_HEXAHEDRON
.. data:: VTK_WEDGE
.. data:: VTK_PYRAMID

.. data:: VTK_LAGRANGE_CURVE
.. data:: VTK_LAGRANGE_TRIANGLE
.. data:: VTK_LAGRANGE_QUADRILATERAL
.. data:: VTK_LAGRANGE_TETRAHEDRON
.. data:: VTK_LAGRANGE_HEXAHEDRON
.. data:: VTK_LAGRANGE_WEDGE

XML elements
^^^^^^^^^^^^^^

.. autoclass:: XMLElementBase
.. autoclass:: XMLElement
    :show-inheritance:
.. autoclass:: XMLRoot
    :show-inheritance:

Binary encoders
^^^^^^^^^^^^^^^

.. autoclass:: EncodedBuffer
.. autoclass:: BinaryEncodedBuffer
    :show-inheritance:
.. autoclass:: Base64EncodedBuffer
    :show-inheritance:
.. autoclass:: Base64ZLibEncodedBuffer
    :show-inheritance:

Building blocks
---------------

.. autoclass:: Visitable
.. autoclass:: DataArray
    :show-inheritance:
.. autoclass:: UnstructuredGrid
    :show-inheritance:
.. autoclass:: StructuredGrid
    :show-inheritance:

XML generators
^^^^^^^^^^^^^^

.. autoclass:: XMLGenerator
.. autoclass:: InlineXMLGenerator
    :show-inheritance:
.. autoclass:: AppendedDataXMLGenerator
    :show-inheritance:
.. autoclass:: ParallelXMLGenerator
    :show-inheritance:

Convenience functions
---------------------

.. autofunction:: write_structured_grid
"""

# {{{ types

VTK_INT8 = "Int8"
VTK_UINT8 = "UInt8"
VTK_INT16 = "Int16"
VTK_UINT16 = "UInt16"
VTK_INT32 = "Int32"
VTK_UINT32 = "UInt32"
VTK_INT64 = "Int64"
VTK_UINT64 = "UInt64"
VTK_FLOAT32 = "Float32"
VTK_FLOAT64 = "Float64"


NUMPY_TO_VTK_TYPES = {
        np.int8: VTK_INT8,
        np.uint8: VTK_UINT8,
        np.int16: VTK_INT16,
        np.uint16: VTK_UINT16,
        np.int32: VTK_INT32,
        np.uint32: VTK_UINT32,
        np.int64: VTK_INT64,
        np.uint64: VTK_UINT64,
        np.float32: VTK_FLOAT32,
        np.float64: VTK_FLOAT64,
        }

# }}}


# {{{ cell types

# NOTE: should keep in sync with
# https://gitlab.kitware.com/vtk/vtk/-/blob/master/Common/DataModel/vtkCellType.h

# linear cells
VTK_VERTEX = 1
VTK_POLY_VERTEX = 2
VTK_LINE = 3
VTK_POLY_LINE = 4
VTK_TRIANGLE = 5
VTK_TRIANGLE_STRIP = 6
VTK_POLYGON = 7
VTK_PIXEL = 8
VTK_QUAD = 9
VTK_TETRA = 10
VTK_VOXEL = 11
VTK_HEXAHEDRON = 12
VTK_WEDGE = 13
VTK_PYRAMID = 14

# NOTE: these were added in VTK 8.1 as part of the commit
# https://gitlab.kitware.com/vtk/vtk/-/commit/cc5101a805386f205631357bba782b2a7d17531a

# high-order Lagrange cells
VTK_LAGRANGE_CURVE = 68
VTK_LAGRANGE_TRIANGLE = 69
VTK_LAGRANGE_QUADRILATERAL = 70
VTK_LAGRANGE_TETRAHEDRON = 71
VTK_LAGRANGE_HEXAHEDRON = 72
VTK_LAGRANGE_WEDGE = 73

# }}}


# {{{ cell node counts

CELL_NODE_COUNT = {
        VTK_VERTEX: 1,
        # VTK_POLY_VERTEX: no a-priori size
        VTK_LINE: 2,
        # VTK_POLY_LINE: no a-priori size
        VTK_TRIANGLE: 3,
        # VTK_TRIANGLE_STRIP: no a-priori size
        # VTK_POLYGON: no a-priori size
        VTK_PIXEL: 4,
        VTK_QUAD: 4,
        VTK_TETRA: 4,
        VTK_VOXEL: 8,
        VTK_HEXAHEDRON: 8,
        VTK_WEDGE: 6,
        VTK_PYRAMID: 5,
        # VTK_LAGRANGE_CURVE: no a-priori size
        # VTK_LAGRANGE_TRIANGLE: no a-priori size
        # VTK_LAGRANGE_QUADRILATERAL: no a-priori size
        # VTK_LAGRANGE_TETRAHEDRON: no a-priori size
        # VTK_LAGRANGE_HEXAHEDRON: no a-priori size
        # VTK_LAGRANGE_WEDGE: no a-priori size
        }

# }}}


# {{{ vector format

# e.g. [[x0, y0, z0], [x1, y1, z1]]
VF_LIST_OF_COMPONENTS = 0
# e.g. [[x0, x1], [y0, y1], [z0, z1]]
VF_LIST_OF_VECTORS = 1

# }}}


# {{{ xml

# Ah, the joys of home-baked non-compliant XML goodness.

Child = Union[str, "XMLElement"]


class XMLElementBase:
    """Base type for XML elements.

    .. attribute:: children
        :type: List[Union[str, XMLElement]]

    .. automethod:: add_child
    """

    def __init__(self) -> None:
        self.children: List[Child] = []

    def add_child(self, child: Child) -> None:
        """Append a new child to the current element."""
        self.children.append(child)


class XMLElement(XMLElementBase):
    """
    .. automethod:: __init__
    .. automethod:: copy
    .. automethod:: write
    """

    def __init__(self, tag: str, **attributes: Any) -> None:
        super().__init__()
        self.tag = tag
        self.attributes = attributes

    def copy(self, children: Optional[List[Child]] = None) -> "XMLElement":
        """Make a copy of the element with new children."""
        if children is None:
            children = self.children

        result = type(self)(self.tag, **self.attributes)
        for child in children:
            result.add_child(child)

        return result

    def write(self, fd: TextIO) -> None:
        """Write the current element and all of its children to a file.

        :arg fd: a file descriptor or another object exposing the required methods.
        """
        attr_string = "".join(
                f' {key}="{value}"'
                for key, value in self.attributes.items())

        if self.children:
            fd.write(f"<{self.tag}{attr_string}>\n")
            for child in self.children:
                if isinstance(child, XMLElement):
                    child.write(fd)
                else:
                    # likely a string instance, write it directly
                    fd.write(child)
            fd.write(f"</{self.tag}>\n")
        else:
            # NOTE: this one has an extra /> at the end
            fd.write(f"<{self.tag}{attr_string}/>\n")


class XMLRoot(XMLElementBase):
    """
    .. automethod:: __init__
    .. automethod:: write
    """

    def __init__(self, child: Optional[Child] = None) -> None:
        super().__init__()
        if child:
            self.add_child(child)

    def write(self, fd: TextIO) -> None:
        """Write the current root and all of its children to a file.

        :arg fd: a file descriptor or another object exposing the required methods.
        """
        fd.write('<?xml version="1.0"?>\n')

        for child in self.children:
            if isinstance(child, XMLElement):
                child.write(fd)
            else:
                # likely a string instance, write it directly
                fd.write(child)

# }}}


# {{{ encoded buffers

_U32CHAR = np.dtype(np.uint32).char


class EncodedBuffer(ABC):
    """An interface for binary buffers for XML data (inline and appended).

    .. automethod:: encoder
    .. automethod:: compressor
    .. automethod:: raw_buffer
    .. automethod:: add_to_xml_element
    """

    @abstractmethod
    def encoder(self) -> str:
        """An identifier for the binary encoding used."""

    @abstractmethod
    def compressor(self) -> Optional[str]:
        """An identifier for the compressor used or *None*."""

    @abstractmethod
    def raw_buffer(self) -> ByteString:
        """The raw buffer object that was used to construct this encoded buffer."""

    @abstractmethod
    def add_to_xml_element(self, xml_element: XMLElement) -> int:
        """Add encoded buffer to the given *xml_element*.

        :returns: total size of encoded buffer in bytes.
        """


class BinaryEncodedBuffer(EncodedBuffer):
    """An encoded buffer that uses raw uncompressed binary data.

    .. automethod:: __init__
    """

    def __init__(self, buffer: ByteString) -> None:
        self.buffer = buffer

    def encoder(self) -> str:
        return "binary"

    def compressor(self) -> Optional[str]:
        return None

    def raw_buffer(self) -> ByteString:
        return self.buffer

    def add_to_xml_element(self, xml_element: XMLElement) -> int:
        raise NotImplementedError


class Base64EncodedBuffer(EncodedBuffer):
    """An encoded buffer that uses :mod:`base64` data.

    .. automethod:: __init__
    """

    def __init__(self, buffer: memoryview) -> None:
        from base64 import b64encode
        from struct import pack

        length = buffer.nbytes
        self.b64header = b64encode(pack(_U32CHAR, length)).decode()
        self.b64data = b64encode(buffer).decode()

    def encoder(self) -> str:
        return "base64"

    def compressor(self) -> Optional[str]:
        return None

    def raw_buffer(self) -> ByteString:
        from base64 import b64decode
        return b64decode(self.b64data)

    def add_to_xml_element(self, xml_element: XMLElement) -> int:
        xml_element.add_child(self.b64header)
        xml_element.add_child(self.b64data)

        return len(self.b64header) + len(self.b64data)


class Base64ZLibEncodedBuffer(EncodedBuffer):
    """An encoded buffer that uses :mod:`base64` and :mod:`zlib` compression.

    .. automethod:: __init__
    """

    def __init__(self, buffer: ByteString) -> None:
        from base64 import b64encode
        from struct import pack
        from zlib import compress

        comp_buffer = compress(buffer)
        comp_header = [1, len(buffer), len(buffer), len(comp_buffer)]

        self.b64header = b64encode(pack(_U32CHAR*len(comp_header), *comp_header))
        self.b64data = b64encode(comp_buffer)

    def encoder(self) -> str:
        return "base64"

    def compressor(self) -> Optional[str]:
        return "zlib"

    def raw_buffer(self) -> ByteString:
        from base64 import b64decode
        from zlib import decompress
        return decompress(b64decode(self.b64data))

    def add_to_xml_element(self, xml_element: XMLElement) -> int:
        xml_element.add_child(self.b64header.decode())
        xml_element.add_child(self.b64data.decode())

        return len(self.b64header) + len(self.b64data)

# }}}


# {{{ data array

class Visitable:
    """A generic class for objects that can be mapped to XML elements.

    .. autoattribute:: generator_method
    .. automethod:: invoke_visitor
    """

    #: Name of the method called in :meth:`invoke_visitor`.
    generator_method: ClassVar[str]

    def invoke_visitor(self, visitor: "XMLGenerator") -> XMLElement:
        """Visit the current object with the given *visitor* and generate the
        corresponding XML element.
        """
        method = getattr(visitor, self.generator_method, None)
        if method is None:
            raise TypeError(
                f"{type(visitor).__name__} does not support {type(self)}"
                )

        return cast(XMLElement, method(self))


class DataArray(Visitable):
    """A representation of a generic VTK DataArray.

    The storage format (inline or appended) is determined by the
    :class:`XMLGenerator` at writing time.

    .. automethod:: __init__
    .. automethod:: get_encoded_buffer
    .. automethod:: encode
    """

    generator_method = "gen_data_array"

    def __init__(self,
                 name: str,
                 container: Any,
                 vector_padding: int = 3,
                 vector_format: int = VF_LIST_OF_COMPONENTS,
                 components: Optional[int] = None) -> None:
        """
        :arg name: name of the data array.
        :arg container: a :class:`numpy.ndarray` or another :class:`DataArray`.
        :arg vector_padding: pad any :class:`~numpy.ndarray` with additional
            zeros given by this variable.
        :arg vector_format: :data:`VF_LIST_OF_COMPONENTS` or
            :data:`VF_LIST_OF_VECTORS`.
        :arg components: number of components in the container (not used).
        """
        self.name = name

        if isinstance(container, DataArray):
            self.type: Optional[str] = container.type
            self.components: int = container.components
            self.encoded_buffer: EncodedBuffer = container.encoded_buffer
            return
        elif isinstance(container, np.ndarray):
            # NOTE: handled below
            pass
        else:
            raise ValueError(
                f"Cannot convert object of type '{type(container)}' to DataArray")

        if vector_format not in (VF_LIST_OF_COMPONENTS, VF_LIST_OF_VECTORS):
            raise ValueError(f"Unknown vector format: {vector_format}")

        if container.dtype.char == "O":
            for subvec in container:
                if not isinstance(subvec, np.ndarray):
                    raise TypeError(
                            f"Expected a numpy array, got '{type(subvec)}' instead")

            container = np.array(list(container))
            assert container.dtype.char != "O"

        if len(container.shape) > 1:
            if vector_format == VF_LIST_OF_COMPONENTS:
                container = container.T.copy()

            if len(container.shape) != 2:
                raise ValueError("numpy vectors of rank>2 are not supported")
            if container.size and container.strides[1] != container.itemsize:
                raise ValueError("2D numpy arrays must be row-major")

            if vector_padding > container.shape[1]:
                container = np.asarray(np.hstack((
                        container,
                        np.zeros((
                            container.shape[0],
                            vector_padding-container.shape[1],
                            ),
                            container.dtype))), order="C")
            self.components = container.shape[1]
        else:
            self.components = 1

        self.type = NUMPY_TO_VTK_TYPES.get(container.dtype.type, None)
        if self.type is None:
            raise TypeError(f"Unsupported array dtype: '{container.dtype}'")

        if not container.flags.c_contiguous:
            container = container.copy()

        buf = memoryview(container)
        self.encoded_buffer = BinaryEncodedBuffer(buf)

    def get_encoded_buffer(self,
                           encoder: str,
                           compressor: Optional[str] = None) -> EncodedBuffer:
        """Re-encode the underlying buffer of the current :class:`DataArray`.

        :arg encoder: new encoder name.
        :arg compressor: new compressor name.
        """
        have_encoder = self.encoded_buffer.encoder()
        have_compressor = self.encoded_buffer.compressor()

        if (encoder, compressor) != (have_encoder, have_compressor):
            raw_buf = self.encoded_buffer.raw_buffer()

            # avoid having three copies of the buffer around temporarily
            del self.encoded_buffer

            if (encoder, compressor) == ("binary", None):
                self.encoded_buffer = BinaryEncodedBuffer(raw_buf)
            elif (encoder, compressor) == ("base64", None):
                assert isinstance(raw_buf, memoryview)
                self.encoded_buffer = Base64EncodedBuffer(raw_buf)
            elif (encoder, compressor) == ("base64", "zlib"):
                self.encoded_buffer = Base64ZLibEncodedBuffer(raw_buf)
            else:
                self.encoded_buffer = BinaryEncodedBuffer(raw_buf)
                raise ValueError("invalid encoder/compressor pair")

            have_encoder = self.encoded_buffer.encoder()
            have_compressor = self.encoded_buffer.compressor()

            assert (encoder, compressor) == (have_encoder, have_compressor)

        return self.encoded_buffer

    def encode(self, compressor: Optional[str], xml_element: "XMLElement") -> int:
        """Encode the underlying buffer with the given compressor and add it
        to the *xml_element*.

        The re-encoding is performed using :meth:`get_encoded_buffer` and the
        result is added to the element using
        :meth:`EncodedBuffer.add_to_xml_element`. The encoding is always done
        in :mod:`base64`.
        """

        ebuf = self.get_encoded_buffer("base64", compressor)
        return ebuf.add_to_xml_element(xml_element)

# }}}


# {{{ grids

class UnstructuredGrid(Visitable):
    """
    .. automethod:: __init__

    .. automethod:: vtk_extension
    .. automethod:: add_pointdata
    .. automethod:: add_celldata
    """

    generator_method = "gen_unstructured_grid"

    def __init__(self,
                 points: Tuple[int, DataArray],
                 cells: Union[
                     "np.ndarray[Any, Any]",
                     Tuple[int, DataArray, DataArray]],
                 cell_types: Union["np.ndarray[Any, Any]", DataArray]) -> None:
        """
        :arg points: a tuple containing the point count and a :class:`DataArray`
            with the actual coordinates.
        :arg cells: if it is only an :class:`~numpy.ndarray`, then it is assumed
            that all the cells in the grid are uniform and have a fixed number
            of vertices. Otherwise, a tuple of ``(ncells, connectivity, offsets)``
            should be provided.
        :arg cell_types: a :class:`DataArray` or :class:`~numpy.ndarray` of
            cell types.
        """
        self.point_count, self.points = points
        assert self.points.name == "points"

        if isinstance(cells, tuple) and len(cells) == 3:
            self.cell_count, self.cell_connectivity, self.cell_offsets = cells
        elif isinstance(cells, np.ndarray):
            assert not isinstance(cell_types, DataArray)
            self.cell_count = len(cell_types)

            if self.cell_count > 0:
                offsets = np.cumsum(
                        np.vectorize(CELL_NODE_COUNT.get)(cell_types),
                        dtype=cells.dtype)
            else:
                offsets = np.empty((0,), dtype=cells.dtype)

            self.cell_connectivity = DataArray("connectivity", cells)
            self.cell_offsets = DataArray("offsets", offsets)
        else:
            raise TypeError(f"Unsupported 'cells' type: {type(cells)}")

        self.cell_types = DataArray("types", cell_types)

        self.pointdata: List[DataArray] = []
        self.celldata: List[DataArray] = []

    def copy(self) -> "UnstructuredGrid":
        return UnstructuredGrid(
                (self.point_count, self.points),
                (self.cell_count, self.cell_connectivity, self.cell_offsets),
                self.cell_types)

    def vtk_extension(self) -> str:
        """Recommended extension for unstructured VTK grids."""
        return "vtu"

    def add_pointdata(self, data_array: DataArray) -> None:
        """Add point data to the grid."""
        self.pointdata.append(data_array)

    def add_celldata(self, data_array: DataArray) -> None:
        """Add cell data to the grid."""
        self.celldata.append(data_array)


class StructuredGrid(Visitable):
    """
    .. automethod:: __init__

    .. automethod:: vtk_extension
    .. automethod:: add_pointdata
    .. automethod:: add_celldata
    """

    generator_method = "gen_structured_grid"

    def __init__(self, mesh: "np.ndarray[Any, Any]") -> None:
        """
        :arg mesh: has shape ``(ndims, nx, ny, nz)``, depending on the dimension.
        """
        self.mesh = mesh

        self.ndims = mesh.shape[0]
        transpose_arg = (*range(1, 1 + self.ndims), 0)
        mesh = mesh.transpose(transpose_arg).copy()

        self.shape = mesh.shape[:-1][::-1]
        mesh = mesh.reshape(-1, self.ndims)
        self.points = DataArray(
                "points", mesh,
                vector_format=VF_LIST_OF_VECTORS)

        self.pointdata: List[DataArray] = []
        self.celldata: List[DataArray] = []

    def copy(self) -> "StructuredGrid":
        return StructuredGrid(self.mesh)

    def vtk_extension(self) -> str:
        """Recommended extension for structured VTK grids."""
        return "vts"

    def add_pointdata(self, data_array: DataArray) -> None:
        """Add point data to the grid."""
        self.pointdata.append(data_array)

    def add_celldata(self, data_array: DataArray) -> None:
        """Add cell data to the grid."""
        self.celldata.append(data_array)

# }}}


# {{{ vtk xml writers

def make_vtkfile(filetype: str,
                 compressor: Optional[str] = None,
                 version: str = "0.1") -> XMLElement:
    import sys
    if sys.byteorder == "little":
        bo = "LittleEndian"
    else:
        bo = "BigEndian"

    kwargs = {}
    if compressor == "zlib":
        kwargs["compressor"] = "vtkZLibDataCompressor"

    return XMLElement("VTKFile",
            type=filetype, version=version, byte_order=bo, **kwargs)


class XMLGenerator:
    """
    .. automethod:: __init__
    .. automethod:: __call__
    """
    def __init__(self,
                 compressor: Optional[str] = None,
                 vtk_file_version: Optional[str] = None) -> None:
        """
        :arg vtk_file_version: a string ``"x.y"`` with the desired VTK
            XML file format version. Relevant versions are as follows:

            * ``"0.1"`` is the original version.
            * ``"1.0"`` added support for 64-bit indices and offsets, as
              described `here <https://www.paraview.org/Wiki/VTK_XML_Formats>`__.
            * ``"2.0"`` added support for ghost array data, as
              described `here <https://www.kitware.com//ghost-and-blanking-visibility-changes/>`__.
            * ``"2.1"``: added support for writing additional information
              attached to a :class:`DataArray` using
              `information keys <https://docs.vtk.org/en/latest/design_documents/IOXMLInformationFormat.html>`__.
            * ``"2.2"``: changed the node numbering of the hexahedron, as
              described `here <https://gitlab.kitware.com/vtk/vtk/-/merge_requests/6678>`__.
        """

        if compressor == "zlib":
            try:
                import zlib  # noqa: F401
            except ImportError:
                compressor = None
        elif compressor is None:
            pass
        else:
            raise ValueError(f"invalid compressor name '{compressor}'")

        if vtk_file_version is None:
            # https://www.paraview.org/Wiki/VTK_XML_Formats
            vtk_file_version = "0.1"

        self.vtk_file_version = vtk_file_version
        self.compressor = compressor

    def __call__(self, vtkobj: Visitable) -> XMLRoot:
        """Generate an XML tree from the given *vtkobj*."""

        child = self.rec(vtkobj)
        vtkf = make_vtkfile(child.tag, self.compressor,
                version=self.vtk_file_version)
        vtkf.add_child(child)

        return XMLRoot(vtkf)

    def rec(self, vtkobj: Visitable) -> XMLElement:
        """Recursively visit all the children of *vtkobj*."""
        return vtkobj.invoke_visitor(self)


class InlineXMLGenerator(XMLGenerator):
    """An XML generator that uses inline :class:`DataArray` entries."""

    def gen_unstructured_grid(self, ugrid: UnstructuredGrid) -> XMLElement:
        el = XMLElement("UnstructuredGrid")
        piece = XMLElement("Piece",
                NumberOfPoints=ugrid.point_count, NumberOfCells=ugrid.cell_count)
        el.add_child(piece)

        if ugrid.pointdata:
            data_el = XMLElement("PointData")
            piece.add_child(data_el)
            for data_array in ugrid.pointdata:
                data_el.add_child(self.rec(data_array))

        if ugrid.celldata:
            data_el = XMLElement("CellData")
            piece.add_child(data_el)
            for data_array in ugrid.celldata:
                data_el.add_child(self.rec(data_array))

        points = XMLElement("Points")
        piece.add_child(points)
        points.add_child(self.rec(ugrid.points))

        cells = XMLElement("Cells")
        piece.add_child(cells)
        cells.add_child(self.rec(ugrid.cell_connectivity))
        cells.add_child(self.rec(ugrid.cell_offsets))
        cells.add_child(self.rec(ugrid.cell_types))

        return el

    def gen_structured_grid(self, sgrid: StructuredGrid) -> XMLElement:
        extent = []
        for dim in range(3):
            extent.append(0)
            if dim < sgrid.ndims:
                extent.append(sgrid.shape[dim]-1)
            else:
                extent.append(0)
        extent_str = " ".join(str(i) for i in extent)

        el = XMLElement("StructuredGrid", WholeExtent=extent_str)
        piece = XMLElement("Piece", Extent=extent_str)
        el.add_child(piece)

        if sgrid.pointdata:
            data_el = XMLElement("PointData")
            piece.add_child(data_el)
            for data_array in sgrid.pointdata:
                data_el.add_child(self.rec(data_array))

        if sgrid.celldata:
            data_el = XMLElement("CellData")
            piece.add_child(data_el)
            for data_array in sgrid.celldata:
                data_el.add_child(self.rec(data_array))

        points = XMLElement("Points")
        piece.add_child(points)
        points.add_child(self.rec(sgrid.points))
        return el

    def gen_data_array(self, data: DataArray) -> XMLElement:
        el = XMLElement("DataArray", type=data.type, Name=data.name,
                NumberOfComponents=data.components, format="binary")

        data.encode(self.compressor, el)
        el.add_child("\n")

        return el


class AppendedDataXMLGenerator(InlineXMLGenerator):
    """An XML generator that uses appended data for :class:`DataArray` entries.

    This creates a special element called ``AppendedData`` and each data array
    will index into it. Additional compression can be added to the appended data.
    """

    def __init__(self, compressor: Optional[str] = None,
                 vtk_file_version: Optional[str] = None) -> None:
        super().__init__(compressor=compressor, vtk_file_version=vtk_file_version)

        self.base64_len = 0
        self.app_data = XMLElement("AppendedData", encoding="base64")
        self.app_data.add_child("_")

    def __call__(self, vtkobj: Visitable) -> XMLRoot:
        xmlroot = super().__call__(vtkobj)

        self.app_data.add_child("\n")
        child = xmlroot.children[0]

        assert isinstance(child, XMLElement)
        child.add_child(self.app_data)

        return xmlroot

    def gen_data_array(self, data: DataArray) -> XMLElement:
        el = XMLElement("DataArray", type=data.type, Name=data.name,
                NumberOfComponents=data.components, format="appended",
                offset=self.base64_len)

        self.base64_len += data.encode(self.compressor, self.app_data)

        return el


class ParallelXMLGenerator(XMLGenerator):
    """An XML generator for parallel unstructured grids.

    .. automethod:: __init__
    """

    def __init__(self, pathnames: List[Union[str, pathlib.Path]]) -> None:
        """
        :arg pathnames: a list of paths to indivitual VTK files containing
            different pieces of a grid.
        """
        super().__init__()
        self.pathnames = [str(p) for p in pathnames]

    def gen_unstructured_grid(self, ugrid: UnstructuredGrid) -> XMLElement:
        el = XMLElement("PUnstructuredGrid")

        pointdata = XMLElement("PPointData")
        el.add_child(pointdata)
        for data_array in ugrid.pointdata:
            pointdata.add_child(self.rec(data_array))

        points = XMLElement("PPoints")
        el.add_child(points)
        points.add_child(self.rec(ugrid.points))

        cells = XMLElement("PCells")
        el.add_child(cells)
        cells.add_child(self.rec(ugrid.cell_connectivity))
        cells.add_child(self.rec(ugrid.cell_offsets))
        cells.add_child(self.rec(ugrid.cell_types))

        for pn in self.pathnames:
            el.add_child(XMLElement("Piece", Source=pn))

        return el

    def gen_data_array(self, data: DataArray) -> XMLElement:
        el = XMLElement("PDataArray", type=data.type, Name=data.name,
                NumberOfComponents=data.components)
        return el


def write_structured_grid(
        file_name: Union[str, pathlib.Path],
        mesh: "np.ndarray[Any, Any]",
        cell_data: Optional[List[Tuple[str, "np.ndarray[Any, Any]"]]] = None,
        point_data: Optional[List[Tuple[str, "np.ndarray[Any, Any]"]]] = None,
        overwrite: bool = False) -> None:
    """Write a structure grid to *filename*.

    This constructs a :class:`StructuredGrid` and adds the relevant point and
    cell data, as necessary. The data is all flattened to one dimensional
    arrays.

    :arg overwrite: if *True*, existing files are overwritten, otherwise an
        exception is raised.
    """
    file_name = pathlib.Path(file_name)

    if cell_data is None:
        cell_data = []

    if point_data is None:
        point_data = []

    grid = StructuredGrid(mesh)

    from pytools.obj_array import obj_array_vectorize

    def do_reshape(fld: "np.ndarray[Any, Any]") -> "np.ndarray[Any, Any]":
        return fld.T.copy().reshape(-1)

    for name, field in cell_data:
        reshaped_fld = obj_array_vectorize(do_reshape, field)
        grid.add_pointdata(DataArray(name, reshaped_fld))

    for name, field in point_data:
        reshaped_fld = obj_array_vectorize(do_reshape, field)
        grid.add_pointdata(DataArray(name, reshaped_fld))

    if not overwrite and file_name.exists():
        raise FileExistsError(f"Output file '{file_name}' already exists")

    with open(file_name, "w") as outf:
        AppendedDataXMLGenerator()(grid).write(outf)

# }}}
