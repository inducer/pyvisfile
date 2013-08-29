# PyVisfile Copyright (C) 2007,2010 Andreas Kloeckner
#
# Python wrapper around libsilo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division


"""PyVisfile exposes the functionality of libsilo to Python using the
Boost.Python wrapper library.

To use pyvisfile, you would typically create a SiloFile instance and then
write different entities (variables and meshes, for the most part) to
this file.

If you are running on a parallel machine, you might want to use
ParallelSiloFile to automatically create a master file along with your
SiloFile.
"""


def _ignore_extra_int_vector_warning():
    from warnings import filterwarnings
    filterwarnings("ignore", module="pyvisfile.silo",
            category=RuntimeWarning, lineno=43)
_ignore_extra_int_vector_warning()


import sys
import pyublas  # noqa
try:
    import pyvisfile.silo._internal  # noqa
except ImportError:
    from warnings import warn
    warn("Importing the native-code parts of PyVisfile's silo component failed. "
            "By default, PyVisfile is installed without Silo support. If you would "
            "like support for the Silo file format, configure with --use-silo. "
            "This requires the libsilo library.")
    raise

# hackety hack -- not sure why this is needed
_intnl = sys.modules["pyvisfile.silo._internal"]


def _export_symbols():
    for name, value in _intnl.symbols().iteritems():
        globals()[name] = value
_export_symbols()

DBObjectType = _intnl.DBObjectType
DBdatatype = _intnl.DBdatatype

DBToc = _intnl.DBToc
DBCurve = _intnl.DBCurve
DBQuadMesh = _intnl.DBQuadMesh
DBQuadVar = _intnl.DBQuadVar

IntVector = _intnl.IntVector
get_silo_version = _intnl.get_silo_version
set_deprecate_warnings = _intnl.set_deprecate_warnings


def _convert_optlist(ol_dict):
    optcount = len(ol_dict) + 1
    ol = _intnl.DBOptlist(optcount, optcount * 150)

    for key, value in ol_dict.iteritems():
        if isinstance(value, int):
            ol.add_int_option(key, value)
        elif isinstance(value, tuple):
            for el in value:
                if not isinstance(el, int):
                    raise TypeError('For now only tuples of int are implemented as option value!')
            ol.add_option(key, value)
        else:
            ol.add_option(key, value)

    return ol


class SiloFile(_intnl.DBFile):
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
            _intnl.DBFile.__init__(self, pathname, mode, target,
                    fileinfo, filetype)
        else:
            if mode is None:
                mode = DB_APPEND
            if filetype is None:
                filetype = DB_UNKNOWN
            _intnl.DBFile.__init__(self, pathname, filetype, mode)

    def put_zonelist_2(self, names, nzones, ndims, nodelist, lo_offset, hi_offset,
            shapetype, shapesize, shapecounts, optlist={}):
        _intnl.DBFile.put_zonelist_2(self, names, nzones, ndims,
                nodelist, lo_offset, hi_offset,
                shapetype, shapesize, shapecounts, _convert_optlist(optlist))

    def put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name,
            optlist={}):
        _intnl.DBFile.put_ucdmesh(self, mname, coordnames, coords,
            nzones, zonel_name, facel_name, _convert_optlist(optlist))

    def put_ucdvar1(self, vname, mname, vec, centering, optlist={}):
        _intnl.DBFile.put_ucdvar1(self, vname, mname, vec, centering,
                _convert_optlist(optlist))

    def put_ucdvar(self, vname, mname, varnames, vars,
            centering, optlist={}):
        _intnl.DBFile.put_ucdvar(self, vname, mname, varnames, vars, centering,
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

        _intnl.DBFile.put_defvars(self, vname, vars)

    def put_pointmesh(self, mname, coords, optlist={}):
        _intnl.DBFile.put_pointmesh(self, mname, coords,
                _convert_optlist(optlist))

    def put_pointvar1(self, vname, mname, var, optlist={}):
        _intnl.DBFile.put_pointvar1(self, vname, mname, var,
                _convert_optlist(optlist))

    def put_pointvar(self, vname, mname, vars, optlist={}):
        _intnl.DBFile.put_pointvar(self, vname, mname, vars,
                _convert_optlist(optlist))

    def put_quadmesh(self, mname, coords, coordtype=DB_COLLINEAR, optlist={}):
        _intnl.DBFile.put_quadmesh(self, mname, coords, coordtype,
                _convert_optlist(optlist))

    def put_quadvar1(self, vname, mname, var, dims, centering, optlist={}):
        _intnl.DBFile.put_quadvar1(self, vname, mname, var, dims, centering,
                _convert_optlist(optlist))

    def put_quadvar(self, vname, mname, varnames, vars, dims, centering, optlist={}):
        _intnl.DBFile.put_quadvar(self, vname, mname,
                varnames, vars, dims, centering,
                _convert_optlist(optlist))

    def put_multimesh(self, mname, mnames_and_types, optlist={}):
        _intnl.DBFile.put_multimesh(self, mname,
                mnames_and_types, _convert_optlist(optlist))

    def put_multivar(self, vname, vnames_and_types, optlist={}):
        _intnl.DBFile.put_multivar(self, vname,
                vnames_and_types, _convert_optlist(optlist))

    def put_curve(self, curvename, xvals, yvals, optlist={}):
        _intnl.DBFile.put_curve(self, curvename, xvals, yvals,
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

        rank_pathname_pattern = "%s-%05d.silo"
        rank_pathname = rank_pathname_pattern % (pathname, rank)

        self.data_file = SiloFile(rank_pathname, *args, **kwargs)

        if self.rank == self.ranks[0]:
            head_pathname = "%s.silo" % pathname
            self.master_file = SiloFile(head_pathname, *args, **kwargs)

            self.rank_filenames = [rank_pathname_pattern % (pathname, fn_rank)
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
                    [("%s:%s" % (rank_fn, mname), type)
                        for rank_fn in self.rank_filenames],
                    optlist)

    def _added_variable(self, vname, type, optlist):
        if self.master_file:
            self.master_file.put_multivar(vname,
                    [("%s:%s" % (rank_fn, vname), type)
                        for rank_fn in self.rank_filenames],
                    optlist)
