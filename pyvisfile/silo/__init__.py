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


import sys
try:
    import pyvisfile.silo._internal as _silo
except ImportError:
    from warnings import warn
    warn("Importing the native-code parts of PyVisfile's silo component failed. "
            "By default, PyVisfile is installed without Silo support. If you would "
            "like support for the Silo file format, configure with --use-silo. "
            "This requires the libsilo library.")
    raise


from pyvisfile.silo._internal import (
        # types
        DBObjectType, DBdatatype,

        # classes
        DBToc, DBCurve, DBQuadMesh, DBQuadVar, IntVector,
        get_silo_version, set_deprecate_warnings,

        # constants
        DB_LOCAL, DB_COLLINEAR, DB_CLOBBER, DB_NOCLOBBER, DB_PDB, DB_NODECENT,
        DB_HDF5, DB_READ, DB_UNKNOWN,
        DB_ZONETYPE_TRIANGLE, DB_ZONECENT,

        DBOPT_CYCLE, DBOPT_DTIME, DBOPT_XUNITS, DBOPT_YUNITS, DBOPT_ZUNITS,
        DBOPT_XLABEL, DBOPT_YLABEL, DBOPT_ZLABEL,
        DBOPT_UNITS, DBOPT_HI_OFFSET, DBOPT_LO_OFFSET
        )


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
            shapetype, shapesize, shapecounts, optlist={}):
        _silo.DBFile.put_zonelist_2(self, names, nzones, ndims,
                nodelist, lo_offset, hi_offset,
                shapetype, shapesize, shapecounts, _convert_optlist(optlist))

    def put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name,
            optlist={}):
        _silo.DBFile.put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name, _convert_optlist(optlist))

    def put_ucdvar1(self, vname, mname, vec, centering, optlist={}):
        _silo.DBFile.put_ucdvar1(self, vname, mname, vec, centering,
                _convert_optlist(optlist))

    def put_ucdvar(self, vname, mname, varnames, vars,
            centering, optlist={}):
        _silo.DBFile.put_ucdvar(self, vname, mname, varnames, vars, centering,
                _convert_optlist(optlist))

    def put_defvars(self, vname, vars):
        """Add an defined variable ("expression") to this database.

        The *vars* argument consists of a list of tuples of type
          *(name, definition)*
        or
          *(name, definition, DB_VARTYPE_SCALAR | DB_VARTYPE_VECTOR)*
        or even
          *(name, definition, DB_VARTYPE_XXX, {options})*.
        If the type is not specified, scalar is assumed.
        """

        _silo.DBFile.put_defvars(self, vname, vars)

    def put_pointmesh(self, mname, coords, optlist={}):
        _silo.DBFile.put_pointmesh(self, mname, coords,
                _convert_optlist(optlist))

    def put_pointvar1(self, vname, mname, var, optlist={}):
        _silo.DBFile.put_pointvar1(self, vname, mname, var,
                _convert_optlist(optlist))

    def put_pointvar(self, vname, mname, vars, optlist={}):
        _silo.DBFile.put_pointvar(self, vname, mname, vars,
                _convert_optlist(optlist))

    def put_quadmesh(self, mname, coords, coordtype=DB_COLLINEAR, optlist={}):
        _silo.DBFile.put_quadmesh(self, mname, coords, coordtype,
                _convert_optlist(optlist))

    def put_quadvar1(self, vname, mname, var, dims, centering, optlist={}):
        _silo.DBFile.put_quadvar1(self, vname, mname, var, dims, centering,
                _convert_optlist(optlist))

    def put_quadvar(self, vname, mname, varnames, vars, dims, centering, optlist={}):
        _silo.DBFile.put_quadvar(self, vname, mname,
                varnames, vars, dims, centering,
                _convert_optlist(optlist))

    def put_multimesh(self, mname, mnames_and_types, optlist={}):
        _silo.DBFile.put_multimesh(self, mname,
                mnames_and_types, _convert_optlist(optlist))

    def put_multivar(self, vname, vnames_and_types, optlist={}):
        _silo.DBFile.put_multivar(self, vname,
                vnames_and_types, _convert_optlist(optlist))

    def put_curve(self, curvename, xvals, yvals, optlist={}):
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

    This class can be used in a Python 2.5 *with* statement.
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

    def put_ucdvar1(self, vname, mname, vec, centering, optlist={}):
        self.data_file.put_ucdvar1(vname, mname, vec, centering, optlist)
        self._added_variable(vname, DBObjectType.DB_UCDVAR, optlist)

    def put_ucdvar(self, vname, mname, varnames, vars,
            centering, optlist={}):
        self.data_file.put_ucdvar(vname, mname, varnames, vars,
            centering, optlist={})
        self._added_variable(vname, DBObjectType.DB_UCDVAR, optlist)

    def put_defvars(self, vname, vars):
        """Add an defined variable ("expression") to this database.

        The *vars* argument consists of a list of tuples of type
          *(name, definition)*
        or
          *(name, definition, DB_VARTYPE_SCALAR | DB_VARTYPE_VECTOR)*.
        or even
          *(name, definition, DB_VARTYPE_XXX, {options})*.
        If the type is not specified, scalar is assumed.
        """
        if self.master_file is not None:
            self.master_file.put_defvars(vname, vars)

    def put_pointmesh(self, mname, coords, optlist={}):
        self.data_file.put_pointmesh(mname, coords, optlist)
        self._added_mesh(mname, DBObjectType.DB_POINTMESH, optlist)

    def put_pointvar1(self, vname, mname, var, optlist={}):
        self.data_file.put_pointvar1(vname, mname, var, optlist)
        self._added_variable(vname, DBObjectType.DB_POINTVAR, optlist)

    def put_pointvar(self, vname, mname, vars, optlist={}):
        self.data_file.put_pointvar(vname, mname, vars, optlist)
        self._added_variable(vname, DBObjectType.DB_POINTVAR, optlist)

    def put_quadmesh(self, mname, coords, coordtype=DB_COLLINEAR, optlist={}):
        self.data_file.put_quadmesh(mname, coords, coordtype, optlist)
        self._added_mesh(mname, DBObjectType.DB_QUADMESH, optlist)

    def put_quadvar1(self, vname, mname, var, dims, centering, optlist={}):
        self.data_file.put_quadvar1(vname, mname, var, dims, centering, optlist)
        self._added_variable(vname, DBObjectType.DB_QUADVAR, optlist)

    def put_quadvar(self, vname, mname, varnames, vars, dims, centering, optlist={}):
        self.data_file.put_quadvar(vname, mname, varnames, vars,
                dims, centering, optlist)
        self._added_variable(vname, DBObjectType.DB_QUADVAR, optlist)

    # -------------------------------------------------------------------------
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
