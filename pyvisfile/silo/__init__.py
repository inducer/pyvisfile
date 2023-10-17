__copyright__ = "Copyright (C) 2007,2010 Andreas Kloeckner"

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

__doc__ = """PyVisfile exposes the functionality of libsilo to Python using the
Boost.Python wrapper library.

To use pyvisfile, you would typically create a SiloFile instance and then
write different entities (variables and meshes, for the most part) to
this file.

If you are running on a parallel machine, you might want to use
ParallelSiloFile to automatically create a master file along with your
SiloFile.
"""

try:
    import pyvisfile.silo._internal as _silo
except ImportError:
    from warnings import warn
    warn("Importing the native-code parts of PyVisfile's silo component failed. "
            "By default, PyVisfile is installed without Silo support. If you would "
            "like support for the Silo file format, configure with --use-silo. "
            "This requires the libsilo library.")
    raise


from pyvisfile.silo._internal import (  # noqa: F401; enums; classes
    DB_ABORT, DB_ABUTTING, DB_ALL, DB_ALL_AND_DRVR, DB_APPEND, DB_AREA, DB_BLOCKCENT,
    DB_BNDCENT, DB_CARTESIAN, DB_CLOBBER, DB_COLLINEAR, DB_COLMAJOR, DB_CRAY,
    DB_CURVILINEAR, DB_CYLINDRICAL, DB_DEBUG, DB_EDGECENT, DB_FACECENT, DB_FLOATING,
    DB_GHOSTTYPE_INTDUP, DB_GHOSTTYPE_NOGHOST, DB_HDF5, DB_HDF5X, DB_INTEL, DB_LOCAL,
    DB_NETCDF, DB_NOCLOBBER, DB_NODECENT, DB_NONCOLLINEAR, DB_NONE, DB_NOTCENT,
    DB_NUMERICAL, DB_OFF, DB_ON, DB_OTHER, DB_PDB, DB_PDBP, DB_QUAD_CURV,
    DB_QUAD_RECT, DB_READ, DB_RECTILINEAR, DB_RESUME, DB_ROWMAJOR, DB_RS6000, DB_SGI,
    DB_SPHERICAL, DB_SUN3, DB_SUN4, DB_SUSPEND, DB_TAURUS, DB_TOP, DB_UNKNOWN,
    DB_VARTYPE_ARRAY, DB_VARTYPE_LABEL, DB_VARTYPE_MATERIAL, DB_VARTYPE_SCALAR,
    DB_VARTYPE_SPECIES, DB_VARTYPE_SYMTENSOR, DB_VARTYPE_TENSOR, DB_VARTYPE_VECTOR,
    DB_VOLUME, DB_ZONECENT, DBCSG_ANGLE_PNLA, DBCSG_ANGLE_PPA, DBCSG_BOX_XYXY,
    DBCSG_BOX_XYZXYZ, DBCSG_CIRCLE_PR, DBCSG_COMPLIMENT, DBCSG_CONE_PNLA,
    DBCSG_CONE_PPA, DBCSG_CYLINDER_PNLR, DBCSG_CYLINDER_PPR, DBCSG_DIFF,
    DBCSG_ELLIPSE_PRR, DBCSG_ELLIPSOID_PRRR, DBCSG_HEX_6F, DBCSG_INNER,
    DBCSG_INTERSECT, DBCSG_LINE_G, DBCSG_LINE_PN, DBCSG_LINE_PP, DBCSG_LINE_X,
    DBCSG_LINE_Y, DBCSG_ON, DBCSG_OUTER, DBCSG_PLANE_G, DBCSG_PLANE_PN,
    DBCSG_PLANE_PPP, DBCSG_PLANE_X, DBCSG_PLANE_Y, DBCSG_PLANE_Z, DBCSG_POLYGON_KP,
    DBCSG_POLYHEDRON_KF, DBCSG_PRISM_5F, DBCSG_PYRAMID_5F, DBCSG_QUAD_4P,
    DBCSG_QUADRATIC_G, DBCSG_QUADRIC_G, DBCSG_SPHERE_PR, DBCSG_SWEEP, DBCSG_TET_4F,
    DBCSG_TRI_3P, DBCSG_UNION, DBCSG_XFORM, DBOPT_ALIGN, DBOPT_ALLOWMAT0,
    DBOPT_ALT_NODENUM_VARS, DBOPT_ALT_ZONENUM_VARS, DBOPT_ASCII_LABEL,
    DBOPT_BASEINDEX, DBOPT_BLOCKORIGIN, DBOPT_BNDNAMES, DBOPT_CONSERVED,
    DBOPT_COORDSYS, DBOPT_CYCLE, DBOPT_DISJOINT_MODE, DBOPT_DTIME, DBOPT_EXTENSIVE,
    DBOPT_EXTENTS, DBOPT_EXTENTS_SIZE, DBOPT_FACETYPE, DBOPT_GHOST_NODE_LABELS,
    DBOPT_GHOST_ZONE_LABELS, DBOPT_GROUPINGNAMES, DBOPT_GROUPINGS,
    DBOPT_GROUPINGS_SIZE, DBOPT_GROUPNUM, DBOPT_GROUPORIGIN,
    DBOPT_HAS_EXTERNAL_ZONES, DBOPT_HI_OFFSET, DBOPT_HIDE_FROM_GUI, DBOPT_LABEL,
    DBOPT_LLONGNZNUM, DBOPT_LO_OFFSET, DBOPT_MAJORORDER, DBOPT_MATCOLORS,
    DBOPT_MATCOUNTS, DBOPT_MATLISTS, DBOPT_MATNAME, DBOPT_MATNAMES, DBOPT_MATNOS,
    DBOPT_MB_BLOCK_NS, DBOPT_MB_BLOCK_TYPE, DBOPT_MB_EMPTY_COUNT,
    DBOPT_MB_EMPTY_LIST, DBOPT_MB_FILE_NS, DBOPT_MB_REPR_BLOCK_IDX,
    DBOPT_MISSING_VALUE, DBOPT_MIXLENS, DBOPT_MMESH_NAME, DBOPT_MRGTREE_NAME,
    DBOPT_MRGV_ONAMES, DBOPT_MRGV_RNAMES, DBOPT_NGROUPS, DBOPT_NMAT, DBOPT_NMATNOS,
    DBOPT_NMATSPEC, DBOPT_NODENUM, DBOPT_NSPACE, DBOPT_ORIGIN, DBOPT_PHZONELIST,
    DBOPT_PLANAR, DBOPT_REFERENCE, DBOPT_REGION_PNAMES, DBOPT_REGNAMES,
    DBOPT_SPECCOLORS, DBOPT_SPECNAMES, DBOPT_TENSOR_RANK, DBOPT_TIME, DBOPT_TOPO_DIM,
    DBOPT_TV_CONNECTIVITY, DBOPT_UNITS, DBOPT_USESPECMF, DBOPT_XLABEL, DBOPT_XUNITS,
    DBOPT_XVARNAME, DBOPT_YLABEL, DBOPT_YUNITS, DBOPT_YVARNAME, DBOPT_ZLABEL,
    DBOPT_ZONECOUNTS, DBOPT_ZONENAMES, DBOPT_ZONENUM, DBOPT_ZUNITS, DBOPT_ZVARNAME,
    E_BADARGS, E_BADFTYPE, E_BADOPTCLASS, E_CALLFAIL, E_CHECKSUM, E_COMPRESSION,
    E_CONCURRENT, E_DRVRCANTOPEN, E_EMPTYOBJECT, E_FEXIST, E_FILEISDIR, E_FILENOREAD,
    E_FILENOWRITE, E_GRABBED, E_INTERNAL, E_INVALIDNAME, E_MAXFILEOPTSETS,
    E_MAXFILTERS, E_MAXOPEN, E_MSERVER, E_NOERROR, E_NOFILE, E_NOHDF5, E_NOMEM,
    E_NOOVERWRITE, E_NOTDIR, E_NOTENABLEDINBUILD, E_NOTFILTER, E_NOTFOUND, E_NOTIMP,
    E_NOTREG, E_OBJBUFFULL, E_PROTO, E_SYSTEMERR, E_TAURSTATE, DBCurve, DBdatatype,
    DBObjectType, DBQuadMesh, DBQuadVar, DBToc, IntVector, get_silo_version,
    set_deprecate_warnings)


if get_silo_version() >= (4, 6, 1):
    from pyvisfile.silo._internal import (  # noqa: F401
        DB_HDF5_CORE, DB_HDF5_DIRECT, DB_HDF5_FAMILY, DB_HDF5_LOG, DB_HDF5_MPIO,
        DB_HDF5_MPIOP, DB_HDF5_MPIP, DB_HDF5_SEC2, DB_HDF5_SILO, DB_HDF5_SPLIT,
        DB_HDF5_STDIO, DB_ZONETYPE_BEAM, DB_ZONETYPE_HEX, DB_ZONETYPE_POLYHEDRON,
        DB_ZONETYPE_PRISM, DB_ZONETYPE_PYRAMID, DB_ZONETYPE_QUAD, DB_ZONETYPE_TET,
        DB_ZONETYPE_TRIANGLE)


def _convert_optlist(ol_dict):
    optcount = len(ol_dict) + 1
    ol = _silo.DBOptlist(optcount, optcount * 150)

    for key, value in ol_dict.items():
        if isinstance(value, int):
            ol.add_int_option(key, value)
        elif isinstance(value, tuple):
            for el in value:
                if not isinstance(el, int):
                    raise TypeError("For now only tuples of int are "
                            "implemented as option value!")
            ol.add_option(key, value)
        else:
            ol.add_option(key, value)

    return ol


class SiloFile(_silo.DBFile):
    """This class can be used in a Python 2.5 *with* statement."""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __init__(self, pathname, create=True, mode=None,
            fileinfo="Created using PyVisfile",
            target=DB_LOCAL, filetype=None):
        if create:
            if mode is None:
                mode = DB_NOCLOBBER
            if filetype is None:
                filetype = DB_PDB
            _silo.DBFile.__init__(self, pathname, mode, target,
                    fileinfo, filetype)
        else:
            if mode is None:
                mode = DB_APPEND
            if filetype is None:
                filetype = DB_UNKNOWN
            _silo.DBFile.__init__(self, pathname, filetype, mode)

    def put_zonelist_2(self, names, nzones, ndims, nodelist, lo_offset, hi_offset,
            shapetype, shapesize, shapecounts, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_zonelist_2(self, names, nzones, ndims,
                nodelist, lo_offset, hi_offset,
                shapetype, shapesize, shapecounts, _convert_optlist(optlist))

    def put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name,
            optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name, _convert_optlist(optlist))

    def put_ucdvar1(self, vname, mname, vec, centering, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_ucdvar1(self, vname, mname, vec, centering,
                _convert_optlist(optlist))

    def put_ucdvar(self, vname, mname, varnames, vars,
            centering, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_ucdvar(self, vname, mname, varnames, vars, centering,
                _convert_optlist(optlist))

    def put_defvars(self, vname, vars):
        """Add an defined variable ("expression") to this database.

        The *vars* argument consists of a list of tuples of type
        ``(name, definition)`` or
        ``(name, definition, DB_VARTYPE_SCALAR | DB_VARTYPE_VECTOR)`` or even
        ``(name, definition, DB_VARTYPE_XXX, {options})``
        If the type is not specified, scalar is assumed.
        """

        _silo.DBFile.put_defvars(self, vname, vars)

    def put_pointmesh(self, mname, coords, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_pointmesh(self, mname, coords,
                _convert_optlist(optlist))

    def put_pointvar1(self, vname, mname, var, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_pointvar1(self, vname, mname, var,
                _convert_optlist(optlist))

    def put_pointvar(self, vname, mname, vars, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_pointvar(self, vname, mname, vars,
                _convert_optlist(optlist))

    def put_quadmesh(self, mname, coords, coordtype=DB_COLLINEAR, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_quadmesh(self, mname, coords, coordtype,
                _convert_optlist(optlist))

    def put_quadvar1(self, vname, mname, var, dims, centering, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_quadvar1(self, vname, mname, var, dims, centering,
                _convert_optlist(optlist))

    def put_quadvar(self, vname, mname, varnames, vars, dims, centering,
            optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_quadvar(self, vname, mname,
                varnames, vars, dims, centering,
                _convert_optlist(optlist))

    def put_multimesh(self, mname, mnames_and_types, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_multimesh(self, mname,
                mnames_and_types, _convert_optlist(optlist))

    def put_multivar(self, vname, vnames_and_types, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_multivar(self, vname,
                vnames_and_types, _convert_optlist(optlist))

    def put_curve(self, curvename, xvals, yvals, optlist=None):
        if optlist is None:
            optlist = {}

        _silo.DBFile.put_curve(self, curvename, xvals, yvals,
                _convert_optlist(optlist))


class ParallelSiloFile:
    """A :class:`SiloFile` that automatically creates a parallel master file.

    This class is meant to be instantiated on every rank of an MPI
    computation. It creates one data file per rank, and it
    automatically chooses a rank that writes a master file.

    The contents of the master file is automatically built,
    without any further user intervention.

    A :file:`.silo` extension is automatically appended to *pathname*
    for the master file, as are rank numbers and the extension
    for each individual rank.

    This class can be used as a context manager in ``with`` statement.

    .. automethod:: __init__
    .. automethod:: close
    .. automethod:: put_zonelist
    .. automethod:: put_zonelist_2
    .. automethod:: put_ucdmesh
    .. automethod:: put_ucdvar1
    .. automethod:: put_ucdvar
    .. automethod:: put_defvars
    .. automethod:: put_pointmesh
    .. automethod:: put_pointvar1
    .. automethod:: put_pointvar
    .. automethod:: put_quadmesh
    .. automethod:: put_quadvar1
    .. automethod:: put_quadvar
    """

    def __init__(self, pathname, rank, ranks, *args, **kwargs):
        self.rank = rank
        self.ranks = ranks

        rank_pathname_pattern = "{}-{:05d}.silo"
        rank_pathname = rank_pathname_pattern.format(pathname, rank)

        self.data_file = SiloFile(rank_pathname, *args, **kwargs)

        if self.rank == self.ranks[0]:
            head_pathname = f"{pathname}.silo"
            self.master_file = SiloFile(head_pathname, *args, **kwargs)

            self.rank_filenames = [
                    rank_pathname_pattern.format(pathname, fn_rank)
                    for fn_rank in ranks]
        else:
            self.master_file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.data_file.close()
        if self.master_file:
            self.master_file.close()

    # -------------------------------------------------------------------------
    def put_zonelist(self, *args, **kwargs):
        self.data_file.put_zonelist(*args, **kwargs)

    def put_zonelist_2(self, *args, **kwargs):
        self.data_file.put_zonelist_2(*args, **kwargs)

    def put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name, optlist):
        self.data_file.put_ucdmesh(mname, coordnames, coords,
            nzones, zonel_name, facel_name, optlist)

        self._added_mesh(mname, DBObjectType.DB_UCDMESH, optlist)

    def put_ucdvar1(self, vname, mname, vec, centering, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_ucdvar1(vname, mname, vec, centering, optlist)
        self._added_variable(vname, DBObjectType.DB_UCDVAR, optlist)

    def put_ucdvar(self, vname, mname, varnames, vars,
            centering, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_ucdvar(vname, mname, varnames, vars, centering)
        self._added_variable(vname, DBObjectType.DB_UCDVAR, optlist)

    def put_defvars(self, vname, vars):
        """Add an defined variable ("expression") to this database.

        The *vars* argument consists of a list of tuples of type
        ``(name, definition)``
        or
        ``(name, definition, DB_VARTYPE_SCALAR | DB_VARTYPE_VECTOR)``.
        or even
        ``(name, definition, DB_VARTYPE_XXX, {options})``.
        If the type is not specified, scalar is assumed.
        """
        if self.master_file is not None:
            self.master_file.put_defvars(vname, vars)

    def put_pointmesh(self, mname, coords, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_pointmesh(mname, coords, optlist)
        self._added_mesh(mname, DBObjectType.DB_POINTMESH, optlist)

    def put_pointvar1(self, vname, mname, var, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_pointvar1(vname, mname, var, optlist)
        self._added_variable(vname, DBObjectType.DB_POINTVAR, optlist)

    def put_pointvar(self, vname, mname, vars, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_pointvar(vname, mname, vars, optlist)
        self._added_variable(vname, DBObjectType.DB_POINTVAR, optlist)

    def put_quadmesh(self, mname, coords, coordtype=DB_COLLINEAR, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_quadmesh(mname, coords, coordtype, optlist)
        self._added_mesh(mname, DBObjectType.DB_QUADMESH, optlist)

    def put_quadvar1(self, vname, mname, var, dims, centering, optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_quadvar1(vname, mname, var, dims, centering, optlist)
        self._added_variable(vname, DBObjectType.DB_QUADVAR, optlist)

    def put_quadvar(self, vname, mname, varnames, vars, dims, centering,
            optlist=None):
        if optlist is None:
            optlist = {}

        self.data_file.put_quadvar(vname, mname, varnames, vars,
                dims, centering, optlist)
        self._added_variable(vname, DBObjectType.DB_QUADVAR, optlist)

    def _added_mesh(self, mname, type, optlist):
        if self.master_file:
            self.master_file.put_multimesh(mname,
                    [(f"{rank_fn}:{mname}", type)
                        for rank_fn in self.rank_filenames],
                    optlist)

    def _added_variable(self, vname, type, optlist):
        if self.master_file:
            self.master_file.put_multivar(vname,
                    [(f"{rank_fn}:{vname}", type)
                        for rank_fn in self.rank_filenames],
                    optlist)

# vim: foldmethod=marker
