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

Building blocks
---------------

.. autoclass:: DataArray
.. autoclass:: UnstructuredGrid
.. autoclass:: StructuredGrid

XML elements
^^^^^^^^^^^^^^

.. autoclass:: XMLElement

XML generators
^^^^^^^^^^^^^^

.. autoclass:: InlineXMLGenerator
.. autoclass:: AppendedDataXMLGenerator
.. autoclass:: ParallelXMLGenerator

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
class XMLElementBase:
    def __init__(self):
        self.children = []

    def copy(self, new_children=None):
        result = self.__class__(self.tag, self.attributes)
        if new_children is not None:
            result.children = new_children
        else:
            result.children = self.children
        return result

    def add_child(self, child):
        self.children.append(child)


class XMLElement(XMLElementBase):
    """
    .. automethod:: write
    """

    def __init__(self, tag, **attributes):
        XMLElementBase.__init__(self)
        self.tag = tag
        self.attributes = attributes

    def write(self, file):
        attr_string = "".join(
                f' {key}="{value}"'
                for key, value in self.attributes.items())
        if self.children:
            file.write(f"<{self.tag}{attr_string}>\n")
            for child in self.children:
                if isinstance(child, XMLElement):
                    child.write(file)
                else:
                    # likely a string instance, write it directly
                    file.write(child)
            file.write(f"</{self.tag}>\n")
        else:
            file.write(f"<{self.tag}{attr_string}/>\n")


class XMLRoot(XMLElementBase):
    def __init__(self, child=None):
        XMLElementBase.__init__(self)
        if child:
            self.add_child(child)

    def write(self, file):
        file.write('<?xml version="1.0"?>\n')
        for child in self.children:
            if isinstance(child, XMLElement):
                child.write(file)
            else:
                # likely a string instance, write it directly
                file.write(child)

# }}}


# {{{ encoded buffers

_U32CHAR = np.dtype(np.uint32).char


class EncodedBuffer:
    def encoder(self):
        """Return an identifier for the binary encoding used."""
        raise NotImplementedError

    def compressor(self):
        """Return an identifier for the compressor used, or None."""
        raise NotImplementedError

    def raw_buffer(self):
        """Reobtain the raw buffer string object that was used to
        construct this encoded buffer."""

        raise NotImplementedError

    def add_to_xml_element(self, xml_element):
        """Add encoded buffer to the given *xml_element*
        Return total size of encoded buffer in bytes."""

        raise NotImplementedError


class BinaryEncodedBuffer:
    def __init__(self, buffer):
        self.buffer = buffer

    def encoder(self):
        return "binary"

    def compressor(self):
        return None

    def raw_buffer(self):
        return self.buffer

    def add_to_xml_element(self, xml_element):
        raise NotImplementedError


class Base64EncodedBuffer:
    def __init__(self, buffer):
        from struct import pack
        from base64 import b64encode
        length = buffer.nbytes
        self.b64header = b64encode(
                pack(_U32CHAR, length)).decode()
        self.b64data = b64encode(buffer).decode()

    def encoder(self):
        return "base64"

    def compressor(self):
        return None

    def raw_buffer(self):
        from base64 import b64decode
        return b64decode(self.b64data)

    def add_to_xml_element(self, xml_element):
        """Add encoded buffer to the given *xml_element*.
        Return total size of encoded buffer in bytes."""

        xml_element.add_child(self.b64header)
        xml_element.add_child(self.b64data)

        return len(self.b64header) + len(self.b64data)


class Base64ZLibEncodedBuffer:
    def __init__(self, buffer):
        from struct import pack
        from base64 import b64encode
        from zlib import compress
        comp_buffer = compress(buffer)
        comp_header = [1, len(buffer), len(buffer), len(comp_buffer)]
        self.b64header = b64encode(
                pack(_U32CHAR*len(comp_header), *comp_header))
        self.b64data = b64encode(comp_buffer)

    def encoder(self):
        return "base64"

    def compressor(self):
        return "zlib"

    def raw_buffer(self):
        from base64 import b64decode
        from zlib import decompress
        return decompress(b64decode(self.b64data))

    def add_to_xml_element(self, xml_element):
        """Add encoded buffer to the given *xml_element*.
        Return total size of encoded buffer in bytes."""

        xml_element.add_child(self.b64header)
        xml_element.add_child(self.b64data)

        return len(self.b64header) + len(self.b64data)

# }}}


# {{{ data array

class DataArray:
    def __init__(self, name, container, vector_padding=3,
            vector_format=VF_LIST_OF_COMPONENTS, components=None):
        self.name = name

        if isinstance(container, DataArray):
            self.type = container.type
            self.components = container.components
            self.encoded_buffer = container.encoded_buffer
            return

        if not isinstance(container, np.ndarray):
            raise ValueError(
                f"cannot convert object of type '{type(container)}' to DataArray")

        if container.dtype.char == "O":
            for subvec in container:
                if not isinstance(subvec, np.ndarray):
                    raise TypeError(
                            f"expected numpy array, got '{type(subvec)}' instead")

            container = np.array(list(container))
            assert container.dtype.char != "O"

        if len(container.shape) > 1:
            if vector_format == VF_LIST_OF_COMPONENTS:
                container = container.T.copy()

            assert len(container.shape) == 2, \
                    "numpy vectors of rank >2 are not supported"
            assert container.strides[1] == container.itemsize, \
                    "2D numpy arrays must be row-major"

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
            raise TypeError(f"unsupported vector type: '{container.dtype}'")

        if not container.flags.c_contiguous:
            container = container.copy()

        buf = memoryview(container)
        self.encoded_buffer = BinaryEncodedBuffer(buf)

    def get_encoded_buffer(self, encoder, compressor):
        have_encoder = self.encoded_buffer.encoder()
        have_compressor = self.encoded_buffer.compressor()

        if (encoder, compressor) != (have_encoder, have_compressor):
            raw_buf = self.encoded_buffer.raw_buffer()

            # avoid having three copies of the buffer around temporarily
            del self.encoded_buffer

            if (encoder, compressor) == ("binary", None):
                self.encoded_buffer = BinaryEncodedBuffer(raw_buf)
            elif (encoder, compressor) == ("base64", None):
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

    def encode(self, compressor, xml_element):
        ebuf = self.get_encoded_buffer("base64", compressor)
        return ebuf.add_to_xml_element(xml_element)

    def invoke_visitor(self, visitor):
        return visitor.gen_data_array(self)

# }}}


# {{{ grids

class UnstructuredGrid:
    """
    .. automethod:: add_pointdata
    .. automethod:: add_celldata
    """

    def __init__(self, points, cells, cell_types):
        self.cell_count = len(cells)

        self.point_count, self.points = points
        assert self.points.name == "points"

        try:
            self.cell_count, self.cell_connectivity, self.cell_offsets = cells
        except Exception:
            self.cell_count = len(cell_types)

            offsets = np.cumsum(
                    np.vectorize(CELL_NODE_COUNT.get)(cell_types),
                    dtype=cells.dtype)

            self.cell_connectivity = DataArray("connectivity", cells)
            self.cell_offsets = DataArray("offsets", offsets)

        self.cell_types = DataArray("types", cell_types)

        self.pointdata = []
        self.celldata = []

    def copy(self):
        return UnstructuredGrid(
                (self.point_count, self.points),
                (self.cell_count, self.cell_connectivity, self.cell_offsets),
                self.cell_types)

    def vtk_extension(self):
        return "vtu"

    def invoke_visitor(self, visitor):
        return visitor.gen_unstructured_grid(self)

    def add_pointdata(self, data_array):
        self.pointdata.append(data_array)

    def add_celldata(self, data_array):
        self.celldata.append(data_array)


class StructuredGrid:
    """
    .. automethod:: add_pointdata
    .. automethod:: add_celldata
    """

    def __init__(self, mesh):
        """
        :arg mesh: has shape *(ndims, nx, ny, nz)*
            (ny, nz may be omitted)
        """
        self.mesh = mesh

        self.ndims = mesh.shape[0]
        transpose_arg = tuple(range(1, 1+self.ndims)) + (0,)
        mesh = mesh.transpose(transpose_arg).copy()

        self.shape = mesh.shape[:-1][::-1]
        mesh = mesh.reshape(-1, self.ndims)
        self.points = DataArray(
                "points", mesh,
                vector_format=VF_LIST_OF_VECTORS)

        self.pointdata = []
        self.celldata = []

    def copy(self):
        return StructuredGrid(self.mesh)

    def vtk_extension(self):
        return "vts"

    def invoke_visitor(self, visitor):
        return visitor.gen_structured_grid(self)

    def add_pointdata(self, data_array):
        self.pointdata.append(data_array)

    def add_celldata(self, data_array):
        self.celldata.append(data_array)

# }}}


# {{{ vtk xml writers

def make_vtkfile(filetype, compressor, version="0.1"):
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
    def __init__(self, compressor=None, vtk_file_version=None):
        """
        :arg vtk_file_version: a string ``"x.y"`` with the desired VTK
            XML file format version. Relevant versions are as follows:

            * ``"0.1"`` is the original version.
            * ``"1.0"`` added support for 64-bit indices and offsets, as
              described `here <https://www.paraview.org/Wiki/VTK_XML_Formats>`__.
            * ``"2.0"`` added support for ghost array data, as
              described `here <https://blog.kitware.com/ghost-and-blanking-visibility-changes/>`__.
            * ``"2.1"``: added support for writing additional information
              attached to a :class:`DataArray` using
              `information keys <https://vtk.org/doc/nightly/html/IOXMLInformationFormat.html>`__.
            * ``"2.2"``: changed the node numbering of the hexahedron, as
              described `here <https://gitlab.kitware.com/vtk/vtk/-/merge_requests/6678>`__.
        """     # noqa

        if compressor == "zlib":
            try:
                import zlib  # noqa
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

    def __call__(self, vtkobj):
        """Return an :class:`XMLElement`."""

        child = self.rec(vtkobj)
        vtkf = make_vtkfile(child.tag, self.compressor,
                version=self.vtk_file_version)
        vtkf.add_child(child)
        return XMLRoot(vtkf)

    def rec(self, vtkobj):
        return vtkobj.invoke_visitor(self)


class InlineXMLGenerator(XMLGenerator):
    """
    .. automethod:: __init__
    .. automethod:: __call__
    """

    def gen_unstructured_grid(self, ugrid):
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

    def gen_structured_grid(self, sgrid):
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

    def gen_data_array(self, data):
        el = XMLElement("DataArray", type=data.type, Name=data.name,
                NumberOfComponents=data.components, format="binary")
        data.encode(self.compressor, el)
        el.add_child("\n")
        return el


class AppendedDataXMLGenerator(InlineXMLGenerator):
    """
    .. automethod:: __call__
    """

    def __init__(self, compressor=None, vtk_file_version=None):
        InlineXMLGenerator.__init__(self, compressor, vtk_file_version)

        self.base64_len = 0
        self.app_data = XMLElement("AppendedData", encoding="base64")
        self.app_data.add_child("_")

    def __call__(self, vtkobj):
        """Return an :class:`XMLElement`."""

        xmlroot = XMLGenerator.__call__(self, vtkobj)
        self.app_data.add_child("\n")
        xmlroot.children[0].add_child(self.app_data)
        return xmlroot

    def gen_data_array(self, data):
        el = XMLElement("DataArray", type=data.type, Name=data.name,
                NumberOfComponents=data.components, format="appended",
                offset=self.base64_len)

        self.base64_len += data.encode(self.compressor, self.app_data)

        return el


class ParallelXMLGenerator(XMLGenerator):
    """
    .. automethod:: __call__
    """

    def __init__(self, pathnames):
        XMLGenerator.__init__(self, compressor=None)

        self.pathnames = pathnames

    def gen_unstructured_grid(self, ugrid):
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

    def gen_data_array(self, data):
        el = XMLElement("PDataArray", type=data.type, Name=data.name,
                NumberOfComponents=data.components)
        return el


def write_structured_grid(
        file_name, mesh,
        cell_data=None, point_data=None,
        overwrite=False):
    if cell_data is None:
        cell_data = []

    if point_data is None:
        point_data = []

    grid = StructuredGrid(mesh)

    from pytools.obj_array import obj_array_vectorize

    def do_reshape(fld):
        return fld.T.copy().reshape(-1)

    for name, field in cell_data:
        reshaped_fld = obj_array_vectorize(do_reshape, field)
        grid.add_pointdata(DataArray(name, reshaped_fld))

    for name, field in point_data:
        reshaped_fld = obj_array_vectorize(do_reshape, field)
        grid.add_pointdata(DataArray(name, reshaped_fld))

    import os.path
    if os.path.exists(file_name):
        if overwrite:
            # nothing to do, just overwrite below
            pass
        else:
            raise FileExistsError(f"output file '{file_name}' already exists")

    with open(file_name, "w") as outf:
        AppendedDataXMLGenerator()(grid).write(outf)
