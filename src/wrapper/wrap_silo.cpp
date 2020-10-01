// PyVisfile - A Python wrapper around Silo
// Copyright (C) 2007 Andreas Kloeckner

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <numpy/arrayobject.h>

#include <vector>
#include <stdexcept>
#include <iostream>

#include <silo.h>

#ifdef SILO_VERS_MAJ
#define PYVISFILE_SILO_VERSION_GE(Maj, Min, Rel)  \
        (((SILO_VERS_MAJ == Maj) && (SILO_VERS_MIN == Min) && (SILO_VERS_PAT >= Rel)) || \
         ((SILO_VERS_MAJ == Maj) && (SILO_VERS_MIN > Min)) || \
         (SILO_VERS_MAJ > Maj))
#else
#define PYVISFILE_SILO_VERSION_GE(Maj, Min, Rel) 0
#endif

// {{{ macros

#define PYTHON_ERROR(TYPE, REASON) \
{ \
  PyErr_SetString(PyExc_##TYPE, REASON); \
  throw py::error_already_set(); \
}

#define ENUM_VALUE(NAME) \
  value(#NAME, NAME)

#define DEF_SIMPLE_FUNCTION(NAME) \
  m.def(#NAME, &NAME)

#define DEF_SIMPLE_METHOD(NAME) \
  def(#NAME, &cl::NAME)

#define DEF_SIMPLE_METHOD_WITH_ARGS(NAME, ARGS) \
  def(#NAME, &cl::NAME, args ARGS)

#define DEF_SIMPLE_RO_MEMBER(NAME) \
  def_readonly(#NAME, &cl::NAME)

#define DEF_SIMPLE_RO_PROPERTY(NAME) \
  def_property_readonly(#NAME, &cl::get##NAME)

#define CALL_GUARDED(NAME, ARGLIST) \
  if (NAME ARGLIST) \
    throw std::runtime_error(#NAME " failed");

#define COPY_PY_LIST(TYPE, NAME) \
    std::vector<TYPE> NAME; \
    for (auto it: py_##NAME) \
      NAME.push_back(it.cast<TYPE>()); \

#define MAKE_STRING_POINTER_VECTOR(NAME) \
  std::vector<const char *> NAME##_ptrs; \
  for(const std::string &s: NAME) \
    NAME##_ptrs.push_back(s.data()); \

// }}}

namespace py = pybind11;

// NOTE: for IntVector
PYBIND11_MAKE_OPAQUE(std::vector<int>);

namespace
{
  // {{{ helpers

  // https://stackoverflow.com/a/44175911
  class noncopyable {
  public:
    noncopyable() = default;
    ~noncopyable() = default;

  private:
    noncopyable(const noncopyable&) = delete;
    noncopyable& operator=(const noncopyable&) = delete;
  };

  py::tuple get_silo_version()
  {
#if PYVISFILE_SILO_VERSION_GE(4, 6, 1)
    return py::make_tuple(SILO_VERS_MAJ, SILO_VERS_MIN, SILO_VERS_PAT);
#else
    return py::make_tuple(4, 5, 1);
#endif
  }

#if !PYVISFILE_SILO_VERSION_GE(4, 6, 1)
  int set_dep_warning_dummy(int)
  {
    return 0;
  }
#endif

  // }}}

  // {{{ constants

  void silo_expose_symbols(py::module &m)
  {
#define EXPORT_CONSTANT(NAME) \
    m.attr(#NAME) = NAME

    /* Drivers */
    EXPORT_CONSTANT(DB_NETCDF);
    EXPORT_CONSTANT(DB_PDB);
    EXPORT_CONSTANT(DB_TAURUS);
    EXPORT_CONSTANT(DB_UNKNOWN);
    EXPORT_CONSTANT(DB_DEBUG);
    EXPORT_CONSTANT(DB_HDF5);

#if PYVISFILE_SILO_VERSION_GE(4,6,1)
    EXPORT_CONSTANT(DB_HDF5_SEC2);
    EXPORT_CONSTANT(DB_HDF5_STDIO);
    EXPORT_CONSTANT(DB_HDF5_CORE);
    EXPORT_CONSTANT(DB_HDF5_MPIO);
    EXPORT_CONSTANT(DB_HDF5_MPIOP);
#endif

    /* Flags for DBCreate */
    EXPORT_CONSTANT(DB_CLOBBER);
    EXPORT_CONSTANT(DB_NOCLOBBER);

    /* Flags for DBOpen */
    EXPORT_CONSTANT(DB_READ);
    EXPORT_CONSTANT(DB_APPEND);

    /* Target machine for DBCreate */
    EXPORT_CONSTANT(DB_LOCAL);
    EXPORT_CONSTANT(DB_SUN3);
    EXPORT_CONSTANT(DB_SUN4);
    EXPORT_CONSTANT(DB_SGI);
    EXPORT_CONSTANT(DB_RS6000);
    EXPORT_CONSTANT(DB_CRAY);
    EXPORT_CONSTANT(DB_INTEL);

    /* Options */
    EXPORT_CONSTANT(DBOPT_ALIGN);
    EXPORT_CONSTANT(DBOPT_COORDSYS);
    EXPORT_CONSTANT(DBOPT_CYCLE);
    EXPORT_CONSTANT(DBOPT_FACETYPE);
    EXPORT_CONSTANT(DBOPT_HI_OFFSET);
    EXPORT_CONSTANT(DBOPT_LO_OFFSET);
    EXPORT_CONSTANT(DBOPT_LABEL);
    EXPORT_CONSTANT(DBOPT_XLABEL);
    EXPORT_CONSTANT(DBOPT_YLABEL);
    EXPORT_CONSTANT(DBOPT_ZLABEL);
    EXPORT_CONSTANT(DBOPT_MAJORORDER);
    EXPORT_CONSTANT(DBOPT_NSPACE);
    EXPORT_CONSTANT(DBOPT_ORIGIN);
    EXPORT_CONSTANT(DBOPT_PLANAR);
    EXPORT_CONSTANT(DBOPT_TIME);
    EXPORT_CONSTANT(DBOPT_UNITS);
    EXPORT_CONSTANT(DBOPT_XUNITS);
    EXPORT_CONSTANT(DBOPT_YUNITS);
    EXPORT_CONSTANT(DBOPT_ZUNITS);
    EXPORT_CONSTANT(DBOPT_DTIME);
    EXPORT_CONSTANT(DBOPT_USESPECMF);
    EXPORT_CONSTANT(DBOPT_XVARNAME);
    EXPORT_CONSTANT(DBOPT_YVARNAME);
    EXPORT_CONSTANT(DBOPT_ZVARNAME);
    EXPORT_CONSTANT(DBOPT_ASCII_LABEL);
    EXPORT_CONSTANT(DBOPT_MATNOS);
    EXPORT_CONSTANT(DBOPT_NMATNOS);
    EXPORT_CONSTANT(DBOPT_MATNAME);
    EXPORT_CONSTANT(DBOPT_NMAT);
    EXPORT_CONSTANT(DBOPT_NMATSPEC);
    EXPORT_CONSTANT(DBOPT_BASEINDEX);
    EXPORT_CONSTANT(DBOPT_ZONENUM);
    EXPORT_CONSTANT(DBOPT_NODENUM);
    EXPORT_CONSTANT(DBOPT_BLOCKORIGIN);
    EXPORT_CONSTANT(DBOPT_GROUPNUM);
    EXPORT_CONSTANT(DBOPT_GROUPORIGIN);
    EXPORT_CONSTANT(DBOPT_NGROUPS);
    EXPORT_CONSTANT(DBOPT_MATNAMES);
    EXPORT_CONSTANT(DBOPT_EXTENTS_SIZE);
    EXPORT_CONSTANT(DBOPT_EXTENTS);
    EXPORT_CONSTANT(DBOPT_MATCOUNTS);
    EXPORT_CONSTANT(DBOPT_MATLISTS);
    EXPORT_CONSTANT(DBOPT_MIXLENS);
    EXPORT_CONSTANT(DBOPT_ZONECOUNTS);
    EXPORT_CONSTANT(DBOPT_HAS_EXTERNAL_ZONES);
    EXPORT_CONSTANT(DBOPT_PHZONELIST);
    EXPORT_CONSTANT(DBOPT_MATCOLORS);
    EXPORT_CONSTANT(DBOPT_BNDNAMES);
    EXPORT_CONSTANT(DBOPT_REGNAMES);
    EXPORT_CONSTANT(DBOPT_ZONENAMES);
    EXPORT_CONSTANT(DBOPT_HIDE_FROM_GUI);

    /* Error trapping method */
    EXPORT_CONSTANT(DB_TOP);
    EXPORT_CONSTANT(DB_NONE);
    EXPORT_CONSTANT(DB_ALL);
    EXPORT_CONSTANT(DB_ABORT);
    EXPORT_CONSTANT(DB_SUSPEND);
    EXPORT_CONSTANT(DB_RESUME);

    /* Errors */
    EXPORT_CONSTANT(E_NOERROR);
    EXPORT_CONSTANT(E_BADFTYPE);
    EXPORT_CONSTANT(E_NOTIMP);
    EXPORT_CONSTANT(E_NOFILE);
    EXPORT_CONSTANT(E_INTERNAL);
    EXPORT_CONSTANT(E_NOMEM);
    EXPORT_CONSTANT(E_BADARGS);
    EXPORT_CONSTANT(E_CALLFAIL);
    EXPORT_CONSTANT(E_NOTFOUND);
    EXPORT_CONSTANT(E_TAURSTATE);
    EXPORT_CONSTANT(E_MSERVER);
    EXPORT_CONSTANT(E_PROTO     );
    EXPORT_CONSTANT(E_NOTDIR);
    EXPORT_CONSTANT(E_MAXOPEN);
    EXPORT_CONSTANT(E_NOTFILTER);
    EXPORT_CONSTANT(E_MAXFILTERS);
    EXPORT_CONSTANT(E_FEXIST);
    EXPORT_CONSTANT(E_FILEISDIR);
    EXPORT_CONSTANT(E_FILENOREAD);
    EXPORT_CONSTANT(E_SYSTEMERR);
    EXPORT_CONSTANT(E_FILENOWRITE);
    EXPORT_CONSTANT(E_INVALIDNAME);
    EXPORT_CONSTANT(E_NOOVERWRITE);
    EXPORT_CONSTANT(E_CHECKSUM);
    EXPORT_CONSTANT(E_NERRORS);

    /* Definitions for MAJOR_ORDER */
    EXPORT_CONSTANT(DB_ROWMAJOR);
    EXPORT_CONSTANT(DB_COLMAJOR);

    /* Definitions for COORD_TYPE */
    EXPORT_CONSTANT(DB_COLLINEAR);
    EXPORT_CONSTANT(DB_NONCOLLINEAR);
    EXPORT_CONSTANT(DB_QUAD_RECT);
    EXPORT_CONSTANT(DB_QUAD_CURV);

    /* Definitions for CENTERING */
    EXPORT_CONSTANT(DB_NOTCENT);
    EXPORT_CONSTANT(DB_NODECENT);
    EXPORT_CONSTANT(DB_ZONECENT);
    EXPORT_CONSTANT(DB_FACECENT);
    EXPORT_CONSTANT(DB_BNDCENT);

    /* Definitions for COORD_SYSTEM */
    EXPORT_CONSTANT(DB_CARTESIAN);
    EXPORT_CONSTANT(DB_CYLINDRICAL);
    EXPORT_CONSTANT(DB_SPHERICAL);
    EXPORT_CONSTANT(DB_NUMERICAL);
    EXPORT_CONSTANT(DB_OTHER);

    /* Definitions for ZONE FACE_TYPE */
    EXPORT_CONSTANT(DB_RECTILINEAR);
    EXPORT_CONSTANT(DB_CURVILINEAR);

    /* Definitions for PLANAR */
    EXPORT_CONSTANT(DB_AREA);
    EXPORT_CONSTANT(DB_VOLUME);
    /* Definitions for flag values */
    EXPORT_CONSTANT(DB_ON);
    EXPORT_CONSTANT(DB_OFF);

    /* Definitions for derived variable types */
    EXPORT_CONSTANT(DB_VARTYPE_SCALAR);
    EXPORT_CONSTANT(DB_VARTYPE_VECTOR);
    EXPORT_CONSTANT(DB_VARTYPE_TENSOR);
    EXPORT_CONSTANT(DB_VARTYPE_SYMTENSOR);
    EXPORT_CONSTANT(DB_VARTYPE_ARRAY);
    EXPORT_CONSTANT(DB_VARTYPE_MATERIAL);
    EXPORT_CONSTANT(DB_VARTYPE_SPECIES);
    EXPORT_CONSTANT(DB_VARTYPE_LABEL);

    /* Definitions for CSG boundary types */
    EXPORT_CONSTANT(DBCSG_QUADRIC_G);
    EXPORT_CONSTANT(DBCSG_SPHERE_PR);
    EXPORT_CONSTANT(DBCSG_ELLIPSOID_PRRR);
    EXPORT_CONSTANT(DBCSG_PLANE_G);
    EXPORT_CONSTANT(DBCSG_PLANE_X);
    EXPORT_CONSTANT(DBCSG_PLANE_Y);
    EXPORT_CONSTANT(DBCSG_PLANE_Z);
    EXPORT_CONSTANT(DBCSG_PLANE_PN);
    EXPORT_CONSTANT(DBCSG_PLANE_PPP);
    EXPORT_CONSTANT(DBCSG_CYLINDER_PNLR);
    EXPORT_CONSTANT(DBCSG_CYLINDER_PPR);
    EXPORT_CONSTANT(DBCSG_BOX_XYZXYZ);
    EXPORT_CONSTANT(DBCSG_CONE_PNLA);
    EXPORT_CONSTANT(DBCSG_CONE_PPA);
    EXPORT_CONSTANT(DBCSG_POLYHEDRON_KF);
    EXPORT_CONSTANT(DBCSG_HEX_6F);
    EXPORT_CONSTANT(DBCSG_TET_4F);
    EXPORT_CONSTANT(DBCSG_PYRAMID_5F);
    EXPORT_CONSTANT(DBCSG_PRISM_5F);

    /* Definitions for 2D CSG boundary types */
    EXPORT_CONSTANT(DBCSG_QUADRATIC_G);
    EXPORT_CONSTANT(DBCSG_CIRCLE_PR);
    EXPORT_CONSTANT(DBCSG_ELLIPSE_PRR);
    EXPORT_CONSTANT(DBCSG_LINE_G);
    EXPORT_CONSTANT(DBCSG_LINE_X);
    EXPORT_CONSTANT(DBCSG_LINE_Y);
    EXPORT_CONSTANT(DBCSG_LINE_PN);
    EXPORT_CONSTANT(DBCSG_LINE_PP);
    EXPORT_CONSTANT(DBCSG_BOX_XYXY);
    EXPORT_CONSTANT(DBCSG_ANGLE_PNLA);
    EXPORT_CONSTANT(DBCSG_ANGLE_PPA);
    EXPORT_CONSTANT(DBCSG_POLYGON_KP);
    EXPORT_CONSTANT(DBCSG_TRI_3P);
    EXPORT_CONSTANT(DBCSG_QUAD_4P);

    /* Definitions for CSG Region operators */
    EXPORT_CONSTANT(DBCSG_INNER);
    EXPORT_CONSTANT(DBCSG_OUTER);
    EXPORT_CONSTANT(DBCSG_ON);
    EXPORT_CONSTANT(DBCSG_UNION);
    EXPORT_CONSTANT(DBCSG_INTERSECT);
    EXPORT_CONSTANT(DBCSG_DIFF);
    EXPORT_CONSTANT(DBCSG_COMPLIMENT);
    EXPORT_CONSTANT(DBCSG_XFORM);
    EXPORT_CONSTANT(DBCSG_SWEEP);

#if PYVISFILE_SILO_VERSION_GE(4,6,1)
    /* Shape types */
    EXPORT_CONSTANT(DB_ZONETYPE_BEAM);
    EXPORT_CONSTANT(DB_ZONETYPE_TRIANGLE);
    EXPORT_CONSTANT(DB_ZONETYPE_QUAD);
    EXPORT_CONSTANT(DB_ZONETYPE_POLYHEDRON);
    EXPORT_CONSTANT(DB_ZONETYPE_TET);
    EXPORT_CONSTANT(DB_ZONETYPE_PYRAMID);
    EXPORT_CONSTANT(DB_ZONETYPE_PRISM);
    EXPORT_CONSTANT(DB_ZONETYPE_HEX);
#endif

#undef EXPORT_CONSTANT
  }

  // }}}

  NPY_TYPES get_varlist_dtype(py::sequence varlist)
  {
    bool first = true;
    NPY_TYPES result = NPY_NOTYPE;

    for(py::object var: varlist)
    {
      if (!PyArray_Check(var.ptr()))
        PYTHON_ERROR(TypeError, "component of variable list is not numpy array");

      if (first)
      {
        result = (NPY_TYPES) PyArray_TYPE(var.ptr());
        first = false;
      }
      else if (result != PyArray_TYPE(var.ptr()))
        PYTHON_ERROR(TypeError, "components of variable list have non-matching types");
    }

    return result;
  }

  // {{{ DBoptlist wrapper

  class DBoptlistWrapper: noncopyable
  {
    private:
      DBoptlist *m_optlist;
      char *m_option_storage;
      unsigned m_option_storage_size;
      unsigned m_option_storage_occupied;

    public:
      DBoptlistWrapper(unsigned maxsize, unsigned storage_size)
        : m_optlist(DBMakeOptlist(maxsize)),
        m_option_storage(new char[storage_size]),
        m_option_storage_size(storage_size),
        m_option_storage_occupied(0)
      {
        if (m_optlist == NULL)
          throw std::runtime_error("DBMakeOptlist failed");
      }
      ~DBoptlistWrapper()
      {
        DBFreeOptlist(m_optlist);
      }

      void add_option(int option, int value)
      {
        CALL_GUARDED(DBAddOption,(m_optlist, option,
              add_storage_data((void *) &value, sizeof(value))
              ));
      }

      void add_option(int option, double value)
      {
        switch (option)
        {
          case DBOPT_DTIME:
            {
              CALL_GUARDED(DBAddOption,(m_optlist, option,
                    add_storage_data((void *) &value, sizeof(value))
                    ));
              break;
            }
          default:
            {
              float cast_val = value;
              CALL_GUARDED(DBAddOption,(m_optlist, option,
                    add_storage_data((void *) &cast_val, sizeof(cast_val))
                    ));
              break;
            }
        }
      }

      void add_option(int option, const std::string &value)
      {
        CALL_GUARDED(DBAddOption,(m_optlist, option,
              add_storage_data((void *) value.data(), value.size()+1)
              ));
      }

      void add_option(int option, py::tuple py_values)
      {
        std::vector<int> values;

        for(size_t i = 0; i < py::len(py_values); ++i)
        {
          values.push_back(py_values[i].cast<int>());
        }

        CALL_GUARDED(DBAddOption,(m_optlist, option,
              add_storage_data((void *) &values.front(), values.size()*sizeof(int))
              ));
      }

      DBoptlist *get_optlist()
      {
        return m_optlist;
      }

    protected:
      void *add_storage_data(void *data, unsigned size)
      {
        if (m_option_storage_occupied + size > m_option_storage_size)
          throw std::runtime_error("silo option list storage exhausted"
              "--specify bigger storage size");

        void *dest = m_option_storage + m_option_storage_occupied;
        memcpy(dest, data, size);
        m_option_storage_occupied += size;
        return dest;
      }

  };

  // }}}

  int get_datatype(int) { return DB_INT; }
  int get_datatype(short) { return DB_SHORT; }
  int get_datatype(long) { return DB_LONG; }
  int get_datatype(float) { return DB_FLOAT; }
  int get_datatype(double) { return DB_DOUBLE; }
  int get_datatype(char) { return DB_CHAR; }

  int silo_typenum_to_numpy_typenum(int silo_tp)
  {
    switch (silo_tp)
    {
      case DB_INT:
        return NPY_INT;
      case DB_SHORT:
        return NPY_SHORT;
      case DB_LONG:
        return NPY_LONG;
      case DB_FLOAT:
          return NPY_FLOAT;
      case DB_DOUBLE:
          return NPY_DOUBLE;
      case DB_CHAR:
          return NPY_STRING;
#if SILO_VERSION_GE(4, 7, 2)
      case DB_LONG_LONG:
          return NPY_LONGLONG;
#endif
      default:
          throw std::runtime_error("invalid silo type code");
    }
  }

  // {{{ data wrappers

  // {{{ data wrapper helpers
#define PYVISFILE_TYPED_ACCESSOR(TYPE,NAME) \
  TYPE get##NAME() const { return m_data->NAME; }

#define PYVISFILE_STRING_ACCESSOR(NAME) \
  py::object get##NAME() const \
  { \
    if (m_data) \
      return py::cast(std::string(m_data->NAME)); \
    else \
      return py::none(); \
  }

#define PYVISFILE_TYPED_ARRAY_ACCESSOR(CAST_TO, NAME, SIZE) \
  py::object get##NAME() const \
  { \
    py::list py_list_result; \
    for (unsigned i = 0; i < SIZE; ++i) \
      py_list_result.append(CAST_TO(m_data->NAME[i])); \
    return py::make_tuple(py_list_result); \
  }

  // }}}

  // {{{ curve wrapper

  class DBcurveWrapper: noncopyable
  {
    public:
      DBcurve   *m_data;

      DBcurveWrapper(DBcurve *data)
        : m_data(data)
      { }
      ~DBcurveWrapper()
      {
        DBFreeCurve(m_data);
      }

      PYVISFILE_TYPED_ACCESSOR(int, id);
      PYVISFILE_TYPED_ACCESSOR(int, origin);
      PYVISFILE_STRING_ACCESSOR(title);
      PYVISFILE_STRING_ACCESSOR(xvarname);
      PYVISFILE_STRING_ACCESSOR(yvarname);
      PYVISFILE_STRING_ACCESSOR(xlabel);
      PYVISFILE_STRING_ACCESSOR(ylabel);
      PYVISFILE_STRING_ACCESSOR(xunits);
      PYVISFILE_STRING_ACCESSOR(yunits);
      PYVISFILE_STRING_ACCESSOR(reference);
  };

#define PYVISFILE_CURVE_DATA_GETTER(COORD) \
  py::handle curve_##COORD(py::object py_curve) \
  { \
    DBcurveWrapper &curve(py_curve.cast<DBcurveWrapper &>()); \
    npy_intp dims[] = { curve.m_data->npts }; \
    py::handle result(PyArray_SimpleNewFromData(1, dims, \
          silo_typenum_to_numpy_typenum(curve.m_data->datatype), \
          curve.m_data->COORD)); \
    PyArray_BASE(result.ptr()) = py_curve.ptr(); \
    Py_INCREF(PyArray_BASE(result.ptr())); \
    return result; \
  }

  PYVISFILE_CURVE_DATA_GETTER(x);
  PYVISFILE_CURVE_DATA_GETTER(y);

  // }}}

  // {{{ quad mesh wrapper

  class DBquadmeshWrapper: noncopyable
  {
    public:
      DBquadmesh   *m_data;

      DBquadmeshWrapper(DBquadmesh *data)
        : m_data(data)
      { }
      ~DBquadmeshWrapper()
      {
        DBFreeQuadmesh(m_data);
      }

      PYVISFILE_TYPED_ACCESSOR(int, id);
      PYVISFILE_TYPED_ACCESSOR(int, block_no);
      PYVISFILE_TYPED_ACCESSOR(int, group_no);
      PYVISFILE_STRING_ACCESSOR(name);
      PYVISFILE_TYPED_ACCESSOR(int, cycle);
      PYVISFILE_TYPED_ACCESSOR(int, coord_sys);
      PYVISFILE_TYPED_ACCESSOR(int, major_order);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, stride, 3);
      PYVISFILE_TYPED_ACCESSOR(int, coordtype);
      PYVISFILE_TYPED_ACCESSOR(int, facetype);
      PYVISFILE_TYPED_ACCESSOR(int, planar);
      // not wrapped: datatype
      PYVISFILE_TYPED_ACCESSOR(float, time);
      PYVISFILE_TYPED_ACCESSOR(double, dtime);

      PYVISFILE_TYPED_ARRAY_ACCESSOR(float, min_extents, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(float, max_extents, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(std::string, labels, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(std::string, units, 3);
      PYVISFILE_TYPED_ACCESSOR(int, ndims);
      PYVISFILE_TYPED_ACCESSOR(int, nspace);
      PYVISFILE_TYPED_ACCESSOR(int, nnodes);
      // not wrapped: dims
      PYVISFILE_TYPED_ACCESSOR(int, origin);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, min_index, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, max_index, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, base_index, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, start_index, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, size_index, 3);
      PYVISFILE_TYPED_ACCESSOR(int, guihide);
      PYVISFILE_STRING_ACCESSOR(mrgtree_name);
  };

  py::object quadmesh_coords(py::object py_quadmesh)
  {
    DBquadmeshWrapper &quadmesh(py_quadmesh.cast<DBquadmeshWrapper &>());

    py::list result;
    for (int i = 0; i < quadmesh.m_data->ndims; ++i)
    {
      npy_intp dims[] = { quadmesh.m_data->dims[i] };
      py::handle coord_array(PyArray_SimpleNewFromData(1, dims,
            silo_typenum_to_numpy_typenum(quadmesh.m_data->datatype),
            quadmesh.m_data->coords[i]));
      PyArray_BASE(coord_array.ptr()) = py_quadmesh.ptr();
      Py_INCREF(PyArray_BASE(coord_array.ptr()));
      result.append(coord_array);
    }

    return py::make_tuple(result);
  }

  // }}}

  // {{{ quad var wrapper

  class DBquadvarWrapper: noncopyable
  {
    public:
      DBquadvar   *m_data;

      DBquadvarWrapper(DBquadvar *data)
        : m_data(data)
      { }
      ~DBquadvarWrapper()
      {
        DBFreeQuadvar(m_data);
      }

      PYVISFILE_TYPED_ACCESSOR(int, id);
      PYVISFILE_STRING_ACCESSOR(name);
      PYVISFILE_STRING_ACCESSOR(units);
      PYVISFILE_STRING_ACCESSOR(label);

      PYVISFILE_TYPED_ACCESSOR(int, cycle);
      PYVISFILE_TYPED_ACCESSOR(int, meshid);
      // not wrapped: datatype

      PYVISFILE_TYPED_ACCESSOR(int, nels);
      PYVISFILE_TYPED_ACCESSOR(int, nvals);
      PYVISFILE_TYPED_ACCESSOR(int, ndims);
      PYVISFILE_TYPED_ACCESSOR(int, major_order);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, stride, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, min_index, 3);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(int, max_index, 3);
      PYVISFILE_TYPED_ACCESSOR(int, origin);
      PYVISFILE_TYPED_ACCESSOR(float, time);
      PYVISFILE_TYPED_ACCESSOR(float, dtime);
      PYVISFILE_TYPED_ARRAY_ACCESSOR(float, align, 3);
      // TODO: mixvals
      PYVISFILE_TYPED_ACCESSOR(float, mixlen);

      PYVISFILE_TYPED_ACCESSOR(float, use_specmf);
      PYVISFILE_TYPED_ACCESSOR(float, ascii_labels);

      PYVISFILE_STRING_ACCESSOR(meshname);
      PYVISFILE_TYPED_ACCESSOR(int, guihide);
      // TODO: region_pnames
  };

  py::object quadvar_vals(py::object py_quadvar)
  {
    DBquadvarWrapper &quadvar(py_quadvar.cast<DBquadvarWrapper &>());

    npy_intp dims[3];

    for (int i = 0; i < quadvar.m_data->ndims; ++i)
      dims[i] = quadvar.m_data->dims[i];

    int ary_flags = 0;
    if (quadvar.m_data->major_order)
      ary_flags |= NPY_CARRAY;
    else
      ary_flags |= NPY_FARRAY;

    py::list result;
    for (int i = 0; i < quadvar.m_data->nvals; ++i)
    {
      PyArray_Descr *tp_descr;
      tp_descr = PyArray_DescrNewFromType(
          silo_typenum_to_numpy_typenum(quadvar.m_data->datatype));
      if (tp_descr == 0)
        throw py::error_already_set();

      py::handle val_array(PyArray_NewFromDescr(
          &PyArray_Type, tp_descr,
          quadvar.m_data->ndims, dims, /*strides*/ NULL,
          quadvar.m_data->vals[i], ary_flags, /*obj*/NULL));

      PyArray_BASE(val_array.ptr()) = py_quadvar.ptr();
      Py_INCREF(PyArray_BASE(val_array.ptr()));
      result.append(val_array);
    }

    return py::make_tuple(result);
  }

  // }}}

  // }}}

  // {{{ DBtoc copy

  struct DBtocCopy : noncopyable
  {
    py::list curve_names;
    py::list multimesh_names;
    py::list multimeshadj_names;
    py::list multivar_names;
    py::list multimat_names;
    py::list multimatspecies_names;
    py::list csgmesh_names;
    py::list csgvar_names;
    py::list defvars_names;
    py::list qmesh_names;
    py::list qvar_names;
    py::list ucdmesh_names;
    py::list ucdvar_names;
    py::list ptmesh_names;
    py::list ptvar_names;
    py::list mat_names;
    py::list matspecies_names;
    py::list var_names;
    py::list obj_names;
    py::list dir_names;
    py::list array_names;
    py::list mrgtree_names;
    py::list groupelmap_names;
    py::list mrgvar_names;
  };

  // }}}

  // {{{ DBfile wrapper

#define PYVISFILE_DBFILE_GET_WRAPPER(LOWER_TYPE, CAMEL_TYPE) \
  DB##LOWER_TYPE##Wrapper *get_##LOWER_TYPE(const char *name) \
  { \
    DB##LOWER_TYPE *obj = DBGet##CAMEL_TYPE(m_dbfile, name); \
    if (!obj) \
      throw std::runtime_error("DBGet" #CAMEL_TYPE " failed"); \
    return new DB##LOWER_TYPE##Wrapper(obj); \
  }

  class DBfileWrapper: noncopyable
  {
    public:
      // {{{ construction and administrativa
      DBfileWrapper(const char *name, int target, int mode)
        : m_db_is_open(false),
        m_dbfile(DBOpen(name, target, mode))
      {
        if (m_dbfile == NULL)
          throw std::runtime_error("DBOpen failed");
        m_db_is_open = true;
      }

      DBfileWrapper(const char *name, int mode, int target, const char *info, int type)
        : m_db_is_open(false),
        m_dbfile(DBCreate(name, mode, target, info, type))
      {
        if (m_dbfile == NULL)
          throw std::runtime_error("DBCreate failed");
        m_db_is_open = true;
      }

      ~DBfileWrapper()
      {
        if (m_db_is_open)
          close();
      }

      void ensure_db_open()
      {
        if (!m_db_is_open)
          throw std::runtime_error("silo db is already closed");
      }

      void close()
      {
        ensure_db_open();
        CALL_GUARDED(DBClose, (m_dbfile));
        m_db_is_open = false;
      }

      operator DBfile *()
      {
        ensure_db_open();
        return m_dbfile;
      }

      // }}}

      // {{{ zone lists
      void put_zonelist(const char *name, int nzones, int ndims,
          const std::vector<int> &nodelist,
          const std::vector<int> &shapesize,
          const std::vector<int> &shapecounts)
      {
        ensure_db_open();

        CALL_GUARDED(DBPutZonelist, (m_dbfile, name, nzones, ndims,
              const_cast<int *>(&nodelist.front()),
              nodelist.size(), 0,
              const_cast<int *>(&shapesize.front()),
              const_cast<int *>(&shapecounts.front()),
              shapesize.size()
            ));
      }

#if PYVISFILE_SILO_VERSION_GE(4, 6, 1)
      void put_zonelist_2(const char *name, int nzones, int ndims,
          const std::vector<int> &nodelist, int lo_offset, int hi_offset,
          const std::vector<int> &shapetype,
          const std::vector<int> &shapesize,
          const std::vector<int> &shapecounts,
          DBoptlistWrapper &optlist
          )
      {
        ensure_db_open();

        CALL_GUARDED(DBPutZonelist2, (m_dbfile, name, nzones, ndims,
              const_cast<int *>(&nodelist.front()), nodelist.size(),
              0, lo_offset, hi_offset,
              const_cast<int *>(&shapetype.front()),
              const_cast<int *>(&shapesize.front()),
              const_cast<int *>(&shapecounts.front()),
              shapesize.size(),
              optlist.get_optlist()
            ));
      }
#endif

      // }}}

      // {{{ ucd mesh/var
      template <class T>
      void put_ucdmesh(const char *name,
             py::sequence py_coordnames, py::array_t<T> coords,
             int nzones, const char *zonel_name, const char *facel_name,
             DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        if (coords.ndim() != 2)
          throw std::invalid_argument("need 2d array");

        int ndims = coords.shape(0);
        int nnodes = coords.shape(1);

        auto coords_unchecked = coords.unchecked();
        std::vector<const T *> coord_starts;
        for (int d = 0; d < ndims; d++)
          coord_starts.push_back(&coords_unchecked(d, 0));

        CALL_GUARDED(DBPutUcdmesh, (m_dbfile, name, ndims,
            /* coordnames*/ NULL,
            (float **) &coord_starts.front(), nnodes,
            nzones, zonel_name, facel_name,
            get_datatype(T()), optlist.get_optlist()));
      }

      template <class T>
      void put_ucdvar1(const char *vname, const char *mname,
          const py::array_t<T> &v,
          /*float *mixvar, int mixlen, */int centering,
          DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        CALL_GUARDED(DBPutUcdvar1, (m_dbfile, vname, mname,
            (float *) v.data(),
            v.size(),
            /* mixvar */ NULL, /* mixlen */ 0,
            get_datatype(T()), centering,
            optlist.get_optlist()));
      }

      template<class T>
      void put_ucdvar_backend(const char *vname, const char *mname,
          py::sequence py_varnames, py::sequence py_vars,
          /*float *mixvars[], int mixlen,*/
          int centering, DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        if (py::len(py_varnames) != py::len(py_vars))
          PYTHON_ERROR(ValueError, "varnames and vars must have the same length");

        COPY_PY_LIST(std::string, varnames);
        MAKE_STRING_POINTER_VECTOR(varnames);

        std::vector<float *> vars;
        bool first = true;
        int vlength = 0;

        for(py::object py_var: py_vars)
        {
          py::array_t<T> v = py_var.cast<py::array_t<T>>();
          if (first)
          {
            vlength = v.size();
            first = false;
          }
          else if (vlength != int(v.size()))
            PYTHON_ERROR(ValueError, "field components need to have matching lengths");
          vars.push_back((float *) v.data());
        }

        CALL_GUARDED(DBPutUcdvar, (m_dbfile, vname, mname,
            py::len(py_vars),
            const_cast<char **>(&varnames_ptrs.front()),
            &vars.front(),
            vlength,
            /* mixvar */ NULL, /* mixlen */ 0,
            get_datatype(T()), centering, optlist.get_optlist()));
      }

      void put_ucdvar(const char *vname, const char *mname,
          py::object py_varnames, py::object py_vars,
          /*float *mixvars[], int mixlen,*/
          int centering, DBoptlistWrapper &optlist)
      {
        switch (get_varlist_dtype(py_vars))
        {
          case NPY_FLOAT:
            put_ucdvar_backend<float>(vname, mname, py_varnames, py_vars,
                centering, optlist);
            break;
          case NPY_DOUBLE:
            put_ucdvar_backend<double>(vname, mname, py_varnames, py_vars,
                centering, optlist);
            break;
          default:
            PYTHON_ERROR(TypeError, "unsupported variable type");
        }
      }

      // }}}

      // {{{ defvars

      void put_defvars(std::string id, py::sequence py_vars)
      {
        ensure_db_open();

        std::vector<std::string> varnames_container;
        std::vector<const char *> varnames;
        std::vector<std::string> vardefs_container;
        std::vector<const char *> vardefs;
        std::vector<int> vartypes;
        std::vector<DBoptlist *> varopts;

        for(py::object py_entry: py_vars)
        {
          py::tuple entry = py_entry.cast<py::tuple>();
          varnames_container.push_back(entry[0].cast<std::string>());
          vardefs_container.push_back(entry[1].cast<std::string>());
          if (py::len(entry) == 2)
          {
            vartypes.push_back(DB_VARTYPE_SCALAR);
            varopts.push_back(NULL);
          }
          else
          {
            vartypes.push_back(entry[2].cast<int>());
            if (py::len(entry) == 4)
              varopts.push_back(entry[3].cast<DBoptlistWrapper *>()->get_optlist());
            else
              varopts.push_back(NULL);
          }
        }

        for (size_t i = 0; i < py::len(py_vars); i++)
        {
          varnames.push_back(varnames_container[i].data());
          vardefs.push_back(vardefs_container[i].data());
        }

#if PYVISFILE_SILO_VERSION_GE(4, 6, 1)
        CALL_GUARDED(DBPutDefvars, (m_dbfile, id.data(), py::len(py_vars),
            const_cast<char **>(&varnames.front()),
            &vartypes.front(),
            const_cast<char **>(&vardefs.front()), &varopts.front()));
#else
        CALL_GUARDED(DBPutDefvars, (m_dbfile, id.data(), py::len(py_vars),
            &varnames.front(), &vartypes.front(),
            &vardefs.front(), &varopts.front()));
#endif
      }

      // }}}

      // {{{ point mesh/var

      template <class T>
      void put_pointmesh(const char *id, const py::array_t<T> &coords,
          DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        if (coords.ndim() != 2)
          throw std::invalid_argument("need 2d array");

        int ndims = coords.shape(0);
        int npoints = coords.shape(1);

        auto coords_unchecked = coords.unchecked();
        std::vector<float *> coord_starts;
        for (int d = 0; d < ndims; d++)
          coord_starts.push_back((float *) &coords_unchecked(d, 0));

        CALL_GUARDED(DBPutPointmesh, (m_dbfile, id,
              ndims, &coord_starts.front(), npoints,
              get_datatype(T()), optlist.get_optlist()));
      }

      template <class T>
      void put_pointvar1(const char *vname, const char *mname,
          const py::array_t<T> &v, DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        CALL_GUARDED(DBPutPointvar1, (m_dbfile, vname, mname,
              (float *) v.data(), v.size(),
              get_datatype(T()), optlist.get_optlist()));
      }

      template <class T>
      void put_pointvar_backend(const char *vname, const char *mname,
          py::sequence py_vars,
          DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        std::vector<float *> vars;
        bool first = true;
        int vlength = 0;

        for(py::object py_var: py_vars)
        {
          py::array_t<T> v = py_var.cast<py::array_t<T>>();
          if (first)
          {
            vlength = v.size();
            first = false;
          }
          else if (vlength != int(v.size()))
            PYTHON_ERROR(ValueError, "field components need to have matching lengths");

          vars.push_back((float *) v.data());
        }

        CALL_GUARDED(DBPutPointvar, (m_dbfile, vname, mname,
              py::len(py_vars), &vars.front(), vlength,
              get_datatype(T()),
              optlist.get_optlist()));
      }

      void put_pointvar(const char *vname, const char *mname,
          py::object py_vars, DBoptlistWrapper &optlist)
      {
        switch (get_varlist_dtype(py_vars))
        {
          case NPY_FLOAT:
            put_pointvar_backend<float>(vname, mname, py_vars, optlist);
            break;
          case NPY_DOUBLE:
            put_pointvar_backend<double>(vname, mname, py_vars, optlist);
            break;
          default:
            PYTHON_ERROR(TypeError, "unsupported variable type");
        }
      }

      // }}}

      // {{{ quad mesh/var

      template <class T>
      void put_quadmesh_backend(const char *name, py::sequence py_coords,
          int coordtype, DBoptlistWrapper &optlist)
      {
        std::vector<int> dims;
        std::vector<float *> coords;

        for(py::object py_coord_dim: py_coords)
        {
          py::array_t<T> coord_dim = py_coord_dim.cast<py::array_t<T>>();
          dims.push_back(coord_dim.size());
          coords.push_back((float *) coord_dim.data());
        }

        CALL_GUARDED(DBPutQuadmesh, (m_dbfile, name,
              /* coordnames */ NULL,
              &coords.front(),
              &dims.front(),
              dims.size(),
              get_datatype(T()),
              coordtype,
              optlist.get_optlist()));
      }

      void put_quadmesh(const char *name, py::object py_coords,
          int coordtype, DBoptlistWrapper &optlist)
      {
        switch (get_varlist_dtype(py_coords))
        {
          case NPY_FLOAT:
            put_quadmesh_backend<float>(name, py_coords, coordtype, optlist);
            break;
          case NPY_DOUBLE:
            put_quadmesh_backend<double>(name, py_coords, coordtype, optlist);
            break;
          default:
            PYTHON_ERROR(TypeError, "unsupported variable type");
        }
      }

      template <class T>
      void put_quadvar_backend(const char *vname, const char *mname,
          py::sequence py_varnames, py::sequence py_vars, py::sequence py_dims,
          /* float *mixvar, int mixlen, */ int centering,
          DBoptlistWrapper &optlist)
      {
        COPY_PY_LIST(int, dims);

        if (py::len(py_varnames) != py::len(py_vars))
          PYTHON_ERROR(ValueError, "varnames and vars must have the same length");

        COPY_PY_LIST(std::string, varnames);
        MAKE_STRING_POINTER_VECTOR(varnames);

        std::vector<float *> vars;
        bool first = true;
        int vlength = 0;

        for(py::object py_var: py_vars)
        {
          py::array_t<T> v = py_var.cast<py::array_t<T>>();
          if (first)
          {
            vlength = v.size();
            first = false;
          }
          else if (vlength != int(v.size()))
            PYTHON_ERROR(ValueError, "field components need to have matching lengths");
          vars.push_back((float *) v.data());
        }

        CALL_GUARDED(DBPutQuadvar, (m_dbfile, vname, mname,
              vars.size(),
              const_cast<char **>(&varnames_ptrs.front()),
              &vars.front(),
              &dims.front(),
              dims.size(),
              /* mix stuff */ NULL, 0,
              get_datatype(T()),
              centering,
              optlist.get_optlist()));
      }

      void put_quadvar(const char *vname, const char *mname,
          py::object py_varnames, py::object py_vars, py::object py_dims,
          /*float *mixvar, int mixlen, */int centering,
          DBoptlistWrapper &optlist)
      {
        switch (get_varlist_dtype(py_vars))
        {
          case NPY_FLOAT:
            put_quadvar_backend<float>(vname, mname, py_varnames, py_vars,
                py_dims, centering, optlist);
            break;
          case NPY_DOUBLE:
            put_quadvar_backend<double>(vname, mname, py_varnames, py_vars,
                py_dims, centering, optlist);
            break;
          default:
            PYTHON_ERROR(TypeError, "unsupported variable type");
        }
      }

      template <class T>
      void put_quadvar1(const char *vname, const char *mname,
          py::array_t<T> var, py::sequence py_dims,
          /*float *mixvar, int mixlen, */int centering,
          DBoptlistWrapper &optlist)
      {
        COPY_PY_LIST(int, dims);

        CALL_GUARDED(DBPutQuadvar1, (m_dbfile, vname, mname,
              (float *) var.data(),
              &dims.front(),
              dims.size(),
              /* mix stuff */ NULL, 0,
              get_datatype(T()),
              centering,
              optlist.get_optlist()));
      }

      PYVISFILE_DBFILE_GET_WRAPPER(quadmesh, Quadmesh);
      PYVISFILE_DBFILE_GET_WRAPPER(quadvar, Quadvar);

      // }}}

      // {{{ multi mesh/var

      void put_multimesh(const char *name, py::sequence py_names_and_types,
          DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        std::vector<std::string> meshnames;
        std::vector<int> meshtypes;

        for(py::object py_name_and_type: py_names_and_types)
        {
          py::tuple name_and_type = py_name_and_type.cast<py::tuple>();
          meshnames.push_back(name_and_type[0].cast<std::string>());
          meshtypes.push_back(name_and_type[1].cast<int>());
        }
        MAKE_STRING_POINTER_VECTOR(meshnames)

        CALL_GUARDED(DBPutMultimesh, (m_dbfile, name,
              meshnames.size(),
              const_cast<char **>(&meshnames_ptrs.front()),
              &meshtypes.front(),
              optlist.get_optlist()));
      }

      void put_multivar(const char *name, py::sequence py_names_and_types,
          DBoptlistWrapper &optlist)
      {
        ensure_db_open();

        std::vector<std::string> varnames;
        std::vector<int> vartypes;

        for(py::object py_name_and_type: py_names_and_types)
        {
          py::tuple name_and_type = py_name_and_type.cast<py::tuple>();
          varnames.push_back(name_and_type[0].cast<std::string>());
          vartypes.push_back(name_and_type[1].cast<int>());
        }

        MAKE_STRING_POINTER_VECTOR(varnames)

        CALL_GUARDED(DBPutMultivar, (m_dbfile, name,
              varnames.size(),
              const_cast<char **>(&varnames_ptrs.front()),
              &vartypes.front(),
              optlist.get_optlist()));
      }

      // }}}

      // {{{ curve

      template <class T>
      void put_curve(const char *curvename,
          const py::array_t<T> &xvals,
          const py::array_t<T> &yvals,
          DBoptlistWrapper &optlist)
      {
        if (xvals.size() != yvals.size())
          PYTHON_ERROR(ValueError, "xvals and yvals must have the same length");
        int npoints = xvals.size();
        CALL_GUARDED(DBPutCurve, (m_dbfile, curvename,
              const_cast<void *>(reinterpret_cast<const void *>(xvals.data())),
              const_cast<void *>(reinterpret_cast<const void *>(yvals.data())),
              get_datatype(T()),
              npoints,
              optlist.get_optlist()));
      }

      PYVISFILE_DBFILE_GET_WRAPPER(curve, Curve);

      // }}}

      // {{{ toc

      DBtocCopy *get_toc()
      {
        DBtoc *toc = DBGetToc(m_dbfile);
        std::unique_ptr<DBtocCopy> result(new DBtocCopy());

#define PYVISFILE_COPY_TOC_LIST(NAME, CNT) \
        for (int i = 0; i < toc->CNT; ++i) \
          result->NAME.append(std::string(toc->NAME[i]));

        PYVISFILE_COPY_TOC_LIST(curve_names, ncurve);
        PYVISFILE_COPY_TOC_LIST(multimesh_names, nmultimesh);
        PYVISFILE_COPY_TOC_LIST(multimeshadj_names, nmultimeshadj);
        PYVISFILE_COPY_TOC_LIST(multivar_names, nmultivar);
        PYVISFILE_COPY_TOC_LIST(multimat_names, nmultimat);
        PYVISFILE_COPY_TOC_LIST(multimatspecies_names, nmultimatspecies);
        PYVISFILE_COPY_TOC_LIST(csgmesh_names, ncsgmesh);
        PYVISFILE_COPY_TOC_LIST(csgvar_names, ncsgvar);
        PYVISFILE_COPY_TOC_LIST(defvars_names, ndefvars);
        PYVISFILE_COPY_TOC_LIST(qmesh_names, nqmesh);
        PYVISFILE_COPY_TOC_LIST(qvar_names, nqvar);
        PYVISFILE_COPY_TOC_LIST(ucdmesh_names, nucdmesh);
        PYVISFILE_COPY_TOC_LIST(ucdvar_names, nucdvar);
        PYVISFILE_COPY_TOC_LIST(ptmesh_names, nptmesh);
        PYVISFILE_COPY_TOC_LIST(ptvar_names, nptvar);
        PYVISFILE_COPY_TOC_LIST(mat_names, nmat);
        PYVISFILE_COPY_TOC_LIST(matspecies_names, nmatspecies);
        PYVISFILE_COPY_TOC_LIST(var_names, nvar);
        PYVISFILE_COPY_TOC_LIST(obj_names, nobj);
        PYVISFILE_COPY_TOC_LIST(dir_names, ndir);
#if PYVISFILE_SILO_VERSION_GE(4,9,0)
        PYVISFILE_COPY_TOC_LIST(array_names, narray);
        PYVISFILE_COPY_TOC_LIST(mrgtree_names, nmrgtree);
        PYVISFILE_COPY_TOC_LIST(groupelmap_names, ngroupelmap);
        PYVISFILE_COPY_TOC_LIST(mrgvar_names, nmrgvar);
#else
        PYVISFILE_COPY_TOC_LIST(array_names, narrays);
        PYVISFILE_COPY_TOC_LIST(mrgtree_names, nmrgtrees);
        PYVISFILE_COPY_TOC_LIST(groupelmap_names, ngroupelmaps);
        PYVISFILE_COPY_TOC_LIST(mrgvar_names, nmrgvars);
#endif
        return result.release();
      }

      // }}}

    private:
      bool m_db_is_open;
      DBfile *m_dbfile;
  };
  // }}}

}

// {{{ main wrapper function

static bool import_numpy_helper()
{
  import_array1(false);
  return true;
}

PYBIND11_MODULE(_internal, m)
{
  if (!import_numpy_helper())
    throw py::error_already_set();

  silo_expose_symbols(m);

  py::enum_<DBdatatype>(m, "DBdatatype")
    .ENUM_VALUE(DB_INT)
    .ENUM_VALUE(DB_SHORT)
    .ENUM_VALUE(DB_LONG)
    .ENUM_VALUE(DB_FLOAT)
    .ENUM_VALUE(DB_DOUBLE)
    .ENUM_VALUE(DB_CHAR)
    .ENUM_VALUE(DB_NOTYPE)
#if SILO_VERSION_GE(4,7,2)
    .ENUM_VALUE(DB_LONG_LONG)
#endif
    ;

  py::enum_<DBObjectType>(m, "DBObjectType")
    .ENUM_VALUE(DB_INVALID_OBJECT)
    .ENUM_VALUE(DB_QUADMESH)
    .ENUM_VALUE(DB_QUADVAR)
    .ENUM_VALUE(DB_UCDMESH)
    .ENUM_VALUE(DB_UCDVAR)
    .ENUM_VALUE(DB_MULTIMESH)
    .ENUM_VALUE(DB_MULTIVAR)
    .ENUM_VALUE(DB_MULTIMAT)
    .ENUM_VALUE(DB_MULTIMATSPECIES)
    .ENUM_VALUE(DB_MULTIBLOCKMESH)
    .ENUM_VALUE(DB_MULTIBLOCKVAR)
    .ENUM_VALUE(DB_MULTIMESHADJ)
    .ENUM_VALUE(DB_MATERIAL)
    .ENUM_VALUE(DB_MATSPECIES)
    .ENUM_VALUE(DB_FACELIST)
    .ENUM_VALUE(DB_ZONELIST)
    .ENUM_VALUE(DB_EDGELIST)
    .ENUM_VALUE(DB_PHZONELIST)
    .ENUM_VALUE(DB_CSGZONELIST)
    .ENUM_VALUE(DB_CSGMESH)
    .ENUM_VALUE(DB_CSGVAR)
    .ENUM_VALUE(DB_CURVE)
    .ENUM_VALUE(DB_DEFVARS)
    .ENUM_VALUE(DB_POINTMESH)
    .ENUM_VALUE(DB_POINTVAR)
    .ENUM_VALUE(DB_ARRAY)
    .ENUM_VALUE(DB_DIR)
    .ENUM_VALUE(DB_VARIABLE)
    .ENUM_VALUE(DB_USERDEF)
    ;

  {
    typedef DBfileWrapper cl;
    py::class_<cl>(m, "DBFile")
      .def(py::init<const char *, int, int>())
      .def(py::init<const char *, int, int, const char *, int>())
      .DEF_SIMPLE_METHOD(close)
      .DEF_SIMPLE_METHOD(put_zonelist)

#if PYVISFILE_SILO_VERSION_GE(4,6,1)
      .DEF_SIMPLE_METHOD(put_zonelist_2)
#endif

      .def("put_ucdmesh", &cl::put_ucdmesh<float>)
      .def("put_ucdmesh", &cl::put_ucdmesh<double>)
      .def("put_ucdvar1", &cl::put_ucdvar1<float>)
      .def("put_ucdvar1", &cl::put_ucdvar1<double>)
      .DEF_SIMPLE_METHOD(put_ucdvar)

      .DEF_SIMPLE_METHOD(put_defvars)

      .def("put_pointmesh", &cl::put_pointmesh<float>)
      .def("put_pointmesh", &cl::put_pointmesh<double>)
      .def("put_pointvar1", &cl::put_pointvar1<float>)
      .def("put_pointvar1", &cl::put_pointvar1<double>)
      .DEF_SIMPLE_METHOD(put_pointvar)

      .DEF_SIMPLE_METHOD(put_quadmesh)
      .def("put_quadvar1", &cl::put_quadvar1<float>)
      .def("put_quadvar1", &cl::put_quadvar1<double>)
      .DEF_SIMPLE_METHOD(put_quadvar)

      .DEF_SIMPLE_METHOD(put_multimesh)
      .DEF_SIMPLE_METHOD(put_multivar)

      .def("put_curve", &cl::put_curve<float>)
      .def("put_curve", &cl::put_curve<double>)
      .def("get_curve", &cl::get_curve,
          py::return_value_policy::take_ownership)
      .def("get_quadmesh", &cl::get_quadmesh,
          py::return_value_policy::take_ownership)
      .def("get_quadvar", &cl::get_quadvar,
          py::return_value_policy::take_ownership)

      .def("get_toc", &cl::get_toc,
          py::return_value_policy::take_ownership)
      ;
  }

  {
    typedef DBoptlistWrapper cl;
    py::class_<cl>(m, "DBOptlist")
      .def(py::init<unsigned, unsigned>())
      .def("add_int_option", (void (cl::*)(int, int)) &cl::add_option)
      .def("add_option", (void (cl::*)(int, double)) &cl::add_option)
      .def("add_option", (void (cl::*)(int, const std::string &)) &cl::add_option)
      .def("add_option", (void (cl::*)(int, py::tuple)) &cl::add_option)
      ;
  }

  {
    typedef DBcurveWrapper cl;
    py::class_<cl>(m, "DBCurve")
      .DEF_SIMPLE_RO_PROPERTY(id)
      .DEF_SIMPLE_RO_PROPERTY(origin)
      .DEF_SIMPLE_RO_PROPERTY(title)
      .DEF_SIMPLE_RO_PROPERTY(xvarname)
      .DEF_SIMPLE_RO_PROPERTY(yvarname)
      .DEF_SIMPLE_RO_PROPERTY(xlabel)
      .DEF_SIMPLE_RO_PROPERTY(ylabel)
      .DEF_SIMPLE_RO_PROPERTY(xunits)
      .DEF_SIMPLE_RO_PROPERTY(yunits)
      .DEF_SIMPLE_RO_PROPERTY(reference)
      .def_property_readonly("x", &curve_x)
      .def_property_readonly("y", &curve_y)
      ;
  }

  {
    typedef DBquadmeshWrapper cl;
    py::class_<cl>(m, "DBQuadMesh")
      .DEF_SIMPLE_RO_PROPERTY(id)
      .DEF_SIMPLE_RO_PROPERTY(block_no)
      .DEF_SIMPLE_RO_PROPERTY(group_no)
      .DEF_SIMPLE_RO_PROPERTY(name)
      .DEF_SIMPLE_RO_PROPERTY(cycle)
      .DEF_SIMPLE_RO_PROPERTY(coord_sys)
      .DEF_SIMPLE_RO_PROPERTY(major_order)
      .DEF_SIMPLE_RO_PROPERTY(stride)
      .DEF_SIMPLE_RO_PROPERTY(coordtype)
      .DEF_SIMPLE_RO_PROPERTY(facetype)
      .DEF_SIMPLE_RO_PROPERTY(planar)
      .DEF_SIMPLE_RO_PROPERTY(time)
      .DEF_SIMPLE_RO_PROPERTY(dtime)
      .DEF_SIMPLE_RO_PROPERTY(min_extents)
      .DEF_SIMPLE_RO_PROPERTY(max_extents)
      .DEF_SIMPLE_RO_PROPERTY(labels)
      .DEF_SIMPLE_RO_PROPERTY(units)
      .DEF_SIMPLE_RO_PROPERTY(ndims)
      .DEF_SIMPLE_RO_PROPERTY(nspace)
      .DEF_SIMPLE_RO_PROPERTY(nnodes)
      .DEF_SIMPLE_RO_PROPERTY(origin)
      .DEF_SIMPLE_RO_PROPERTY(min_index)
      .DEF_SIMPLE_RO_PROPERTY(max_index)
      .DEF_SIMPLE_RO_PROPERTY(base_index)
      .DEF_SIMPLE_RO_PROPERTY(start_index)
      .DEF_SIMPLE_RO_PROPERTY(size_index)
      .DEF_SIMPLE_RO_PROPERTY(guihide)
      .DEF_SIMPLE_RO_PROPERTY(mrgtree_name)
      .def_property_readonly("coords", &quadmesh_coords)
      ;
  }

  {
    typedef DBquadvarWrapper cl;
    py::class_<cl>(m, "DBQuadVar")
      .DEF_SIMPLE_RO_PROPERTY(id)
      .DEF_SIMPLE_RO_PROPERTY(name)
      .DEF_SIMPLE_RO_PROPERTY(units)
      .DEF_SIMPLE_RO_PROPERTY(label)

      .DEF_SIMPLE_RO_PROPERTY(cycle)
      .DEF_SIMPLE_RO_PROPERTY(meshid)

      .DEF_SIMPLE_RO_PROPERTY(nels)
      .DEF_SIMPLE_RO_PROPERTY(nvals)
      .DEF_SIMPLE_RO_PROPERTY(ndims)
      .DEF_SIMPLE_RO_PROPERTY(major_order)
      .DEF_SIMPLE_RO_PROPERTY(stride)
      .DEF_SIMPLE_RO_PROPERTY(min_index)
      .DEF_SIMPLE_RO_PROPERTY(max_index)
      .DEF_SIMPLE_RO_PROPERTY(origin)
      .DEF_SIMPLE_RO_PROPERTY(time)
      .DEF_SIMPLE_RO_PROPERTY(dtime)
      .DEF_SIMPLE_RO_PROPERTY(align)
      .DEF_SIMPLE_RO_PROPERTY(mixlen)

      .DEF_SIMPLE_RO_PROPERTY(use_specmf)
      .DEF_SIMPLE_RO_PROPERTY(ascii_labels)
      .DEF_SIMPLE_RO_PROPERTY(meshname)
      .DEF_SIMPLE_RO_PROPERTY(guihide)
      .def_property_readonly("vals", &quadvar_vals)
      ;
  }

  {
    typedef DBtocCopy cl;
    py::class_<cl>(m, "DBToc")
      .DEF_SIMPLE_RO_MEMBER(curve_names)
      .DEF_SIMPLE_RO_MEMBER(multimesh_names)
      .DEF_SIMPLE_RO_MEMBER(multimeshadj_names)
      .DEF_SIMPLE_RO_MEMBER(multivar_names)
      .DEF_SIMPLE_RO_MEMBER(multimat_names)
      .DEF_SIMPLE_RO_MEMBER(multimatspecies_names)
      .DEF_SIMPLE_RO_MEMBER(csgmesh_names)
      .DEF_SIMPLE_RO_MEMBER(csgvar_names)
      .DEF_SIMPLE_RO_MEMBER(defvars_names)
      .DEF_SIMPLE_RO_MEMBER(qmesh_names)
      .DEF_SIMPLE_RO_MEMBER(qvar_names)
      .DEF_SIMPLE_RO_MEMBER(ucdmesh_names)
      .DEF_SIMPLE_RO_MEMBER(ucdvar_names)
      .DEF_SIMPLE_RO_MEMBER(ptmesh_names)
      .DEF_SIMPLE_RO_MEMBER(ptvar_names)
      .DEF_SIMPLE_RO_MEMBER(mat_names)
      .DEF_SIMPLE_RO_MEMBER(matspecies_names)
      .DEF_SIMPLE_RO_MEMBER(var_names)
      .DEF_SIMPLE_RO_MEMBER(obj_names)
      .DEF_SIMPLE_RO_MEMBER(dir_names)
      .DEF_SIMPLE_RO_MEMBER(array_names)
      .DEF_SIMPLE_RO_MEMBER(mrgtree_names)
      .DEF_SIMPLE_RO_MEMBER(groupelmap_names)
      .DEF_SIMPLE_RO_MEMBER(mrgvar_names)
      ;
  }

  {
    typedef std::vector<int> cl;
    py::class_<cl>(m, "IntVector")
      .def(py::init<>())
      .def("reserve", &cl::reserve,
          py::arg("advised_size"))
      .def("__len__", &cl::size)
      .def("append", (void (std::vector<int>::*)(const int &)) &cl::push_back,
          py::arg("value"))
      .def("extend", [](std::vector<int> &self, const py::iterable &py_other)
          {
            for(const py::handle &item: py_other)
              self.push_back(item.cast<int>());
          },
          py::arg("iterable"))
      ;
  }

#if PYVISFILE_SILO_VERSION_GE(4,6,1)
  m.def("set_deprecate_warnings", DBSetDeprecateWarnings);
#else
  m.def("set_deprecate_warnings", set_dep_warning_dummy);
#endif
  DEF_SIMPLE_FUNCTION(get_silo_version);
}

// }}}

// vim: ts=2:sw=2:foldmethod=marker
