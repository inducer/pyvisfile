Usage Reference for :mod:`pyvisfile.silo`
=========================================

.. module:: pyvisfile.silo
.. moduleauthor:: Andreas Kloeckner <inform@tiker.net>

.. function:: get_silo_version()
.. function:: set_deprecate_warnings(max)

    Silo 4.6.1 or newer only.

Database file object
--------------------

.. class:: SiloFile

    .. method:: close()
    .. method:: get_toc()

        Returns a :class:`DBToc` instance.

    .. method:: get_curve(name)

        Returns a :class:`DBCurve` instance.

    .. method:: get_quadmesh(name)

        Returns a :class:`DBQuadMesh` instance.

    .. method:: get_quadvar(name)

        Returns a :class:`DBQuadVar` instance.

    .. automethod:: put_curve
    .. automethod:: put_defvars
    .. automethod:: put_multimesh
    .. automethod:: put_multivar
    .. automethod:: put_pointmesh
    .. automethod:: put_pointvar
    .. automethod:: put_pointvar1
    .. automethod:: put_quadmesh
    .. automethod:: put_quadvar
    .. automethod:: put_quadvar1
    .. automethod:: put_ucdmesh
    .. automethod:: put_ucdvar
    .. automethod:: put_ucdvar1
    .. automethod:: put_zonelist_2

Support for Parallel Computation
--------------------------------

.. autoclass:: ParallelSiloFile
    :members:
    :undoc-members:

Supporting Objects
------------------

.. class:: IntVector

    .. method:: append(val)
    .. method:: extend(iterable)
    .. method:: reserve(count)

Data objects
------------

.. autoclass:: DBToc
    :members:
    :undoc-members:

.. autoclass:: DBCurve
    :members:
    :undoc-members:

.. autoclass:: DBQuadMesh
    :members:
    :undoc-members:

.. autoclass:: DBQuadVar
    :members:
    :undoc-members:

Constants
---------

Drivers
^^^^^^^
.. data:: DB_NETCDF
.. data:: DB_PDB
.. data:: DB_TAURUS
.. data:: DB_UNKNOWN
.. data:: DB_DEBUG
.. data:: DB_HDF5

The below entries only work for Silo 4.6.1 and newer.

.. data:: DB_HDF5_SEC2
.. data:: DB_HDF5_STDIO
.. data:: DB_HDF5_CORE
.. data:: DB_HDF5_MPIO
.. data:: DB_HDF5_MPIOP

Flags for DBCreate
^^^^^^^^^^^^^^^^^^
.. data:: DB_CLOBBER
.. data:: DB_NOCLOBBER

Flags for DBOpen
^^^^^^^^^^^^^^^^

.. data:: DB_READ
.. data:: DB_APPEND

Target machine for DBCreate
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_LOCAL
.. data:: DB_SUN3
.. data:: DB_SUN4
.. data:: DB_SGI
.. data:: DB_RS6000
.. data:: DB_CRAY
.. data:: DB_INTEL

Options
^^^^^^^

.. data:: DBOPT_ALIGN
.. data:: DBOPT_COORDSYS
.. data:: DBOPT_CYCLE
.. data:: DBOPT_FACETYPE
.. data:: DBOPT_HI_OFFSET
.. data:: DBOPT_LO_OFFSET
.. data:: DBOPT_LABEL
.. data:: DBOPT_XLABEL
.. data:: DBOPT_YLABEL
.. data:: DBOPT_ZLABEL
.. data:: DBOPT_MAJORORDER
.. data:: DBOPT_NSPACE
.. data:: DBOPT_ORIGIN
.. data:: DBOPT_PLANAR
.. data:: DBOPT_TIME
.. data:: DBOPT_UNITS
.. data:: DBOPT_XUNITS
.. data:: DBOPT_YUNITS
.. data:: DBOPT_ZUNITS
.. data:: DBOPT_DTIME
.. data:: DBOPT_USESPECMF
.. data:: DBOPT_XVARNAME
.. data:: DBOPT_YVARNAME
.. data:: DBOPT_ZVARNAME
.. data:: DBOPT_ASCII_LABEL
.. data:: DBOPT_MATNOS
.. data:: DBOPT_NMATNOS
.. data:: DBOPT_MATNAME
.. data:: DBOPT_NMAT
.. data:: DBOPT_NMATSPEC
.. data:: DBOPT_BASEINDEX
.. data:: DBOPT_ZONENUM
.. data:: DBOPT_NODENUM
.. data:: DBOPT_BLOCKORIGIN
.. data:: DBOPT_GROUPNUM
.. data:: DBOPT_GROUPORIGIN
.. data:: DBOPT_NGROUPS
.. data:: DBOPT_MATNAMES
.. data:: DBOPT_EXTENTS_SIZE
.. data:: DBOPT_EXTENTS
.. data:: DBOPT_MATCOUNTS
.. data:: DBOPT_MATLISTS
.. data:: DBOPT_MIXLENS
.. data:: DBOPT_ZONECOUNTS
.. data:: DBOPT_HAS_EXTERNAL_ZONES
.. data:: DBOPT_PHZONELIST
.. data:: DBOPT_MATCOLORS
.. data:: DBOPT_BNDNAMES
.. data:: DBOPT_REGNAMES
.. data:: DBOPT_ZONENAMES
.. data:: DBOPT_HIDE_FROM_GUI

Error trapping method
^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_TOP
.. data:: DB_NONE
.. data:: DB_ALL
.. data:: DB_ABORT
.. data:: DB_SUSPEND
.. data:: DB_RESUME

Errors
^^^^^^

.. data:: E_NOERROR
.. data:: E_BADFTYPE
.. data:: E_NOTIMP
.. data:: E_NOFILE
.. data:: E_INTERNAL
.. data:: E_NOMEM
.. data:: E_BADARGS
.. data:: E_CALLFAIL
.. data:: E_NOTFOUND
.. data:: E_TAURSTATE
.. data:: E_MSERVER
.. data:: E_PROTO     
.. data:: E_NOTDIR
.. data:: E_MAXOPEN
.. data:: E_NOTFILTER
.. data:: E_MAXFILTERS
.. data:: E_FEXIST
.. data:: E_FILEISDIR
.. data:: E_FILENOREAD
.. data:: E_SYSTEMERR
.. data:: E_FILENOWRITE
.. data:: E_INVALIDNAME
.. data:: E_NOOVERWRITE
.. data:: E_CHECKSUM
.. data:: E_NERRORS

Definitions for MAJOR_ORDER
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_ROWMAJOR
.. data:: DB_COLMAJOR

Definitions for COORD_TYPE
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_COLLINEAR
.. data:: DB_NONCOLLINEAR
.. data:: DB_QUAD_RECT
.. data:: DB_QUAD_CURV

Definitions for CENTERING
^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_NOTCENT
.. data:: DB_NODECENT
.. data:: DB_ZONECENT
.. data:: DB_FACECENT
.. data:: DB_BNDCENT

Definitions for COORD_SYSTEM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_CARTESIAN
.. data:: DB_CYLINDRICAL
.. data:: DB_SPHERICAL
.. data:: DB_NUMERICAL
.. data:: DB_OTHER

Definitions for ZONE FACE_TYPE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_RECTILINEAR
.. data:: DB_CURVILINEAR

Definitions for PLANAR
^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_AREA
.. data:: DB_VOLUME

Definitions for flag values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_ON
.. data:: DB_OFF

Definitions for derived variable types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DB_VARTYPE_SCALAR
.. data:: DB_VARTYPE_VECTOR
.. data:: DB_VARTYPE_TENSOR
.. data:: DB_VARTYPE_SYMTENSOR
.. data:: DB_VARTYPE_ARRAY
.. data:: DB_VARTYPE_MATERIAL
.. data:: DB_VARTYPE_SPECIES
.. data:: DB_VARTYPE_LABEL

Definitions for CSG boundary types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DBCSG_QUADRIC_G
.. data:: DBCSG_SPHERE_PR
.. data:: DBCSG_ELLIPSOID_PRRR
.. data:: DBCSG_PLANE_G
.. data:: DBCSG_PLANE_X
.. data:: DBCSG_PLANE_Y
.. data:: DBCSG_PLANE_Z
.. data:: DBCSG_PLANE_PN
.. data:: DBCSG_PLANE_PPP
.. data:: DBCSG_CYLINDER_PNLR
.. data:: DBCSG_CYLINDER_PPR
.. data:: DBCSG_BOX_XYZXYZ
.. data:: DBCSG_CONE_PNLA
.. data:: DBCSG_CONE_PPA
.. data:: DBCSG_POLYHEDRON_KF
.. data:: DBCSG_HEX_6F
.. data:: DBCSG_TET_4F
.. data:: DBCSG_PYRAMID_5F
.. data:: DBCSG_PRISM_5F

Definitions for 2D CSG boundary types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DBCSG_QUADRATIC_G
.. data:: DBCSG_CIRCLE_PR
.. data:: DBCSG_ELLIPSE_PRR
.. data:: DBCSG_LINE_G
.. data:: DBCSG_LINE_X
.. data:: DBCSG_LINE_Y
.. data:: DBCSG_LINE_PN
.. data:: DBCSG_LINE_PP
.. data:: DBCSG_BOX_XYXY
.. data:: DBCSG_ANGLE_PNLA
.. data:: DBCSG_ANGLE_PPA
.. data:: DBCSG_POLYGON_KP
.. data:: DBCSG_TRI_3P
.. data:: DBCSG_QUAD_4P

Definitions for CSG Region operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: DBCSG_INNER
.. data:: DBCSG_OUTER
.. data:: DBCSG_ON
.. data:: DBCSG_UNION
.. data:: DBCSG_INTERSECT
.. data:: DBCSG_DIFF
.. data:: DBCSG_COMPLIMENT
.. data:: DBCSG_XFORM
.. data:: DBCSG_SWEEP

Shape types
^^^^^^^^^^^

These constants only work for Silo 4.6.1 and newer.

.. data:: DB_ZONETYPE_BEAM
.. data:: DB_ZONETYPE_TRIANGLE
.. data:: DB_ZONETYPE_QUAD
.. data:: DB_ZONETYPE_POLYHEDRON
.. data:: DB_ZONETYPE_TET
.. data:: DB_ZONETYPE_PYRAMID
.. data:: DB_ZONETYPE_PRISM
.. data:: DB_ZONETYPE_HEX

Data types
^^^^^^^^^^

.. class:: DBdatatype

    .. attribute:: DB_INT
    .. attribute:: DB_SHORT
    .. attribute:: DB_LONG
    .. attribute:: DB_LONG_LONG
    .. attribute:: DB_FLOAT
    .. attribute:: DB_DOUBLE
    .. attribute:: DB_CHAR
    .. attribute:: DB_NOTYPE

Object types
^^^^^^^^^^^^
.. class:: DBObjectType

    .. attribute:: DB_INVALID_OBJECT
    .. attribute:: DB_QUADMESH
    .. attribute:: DB_QUADVAR
    .. attribute:: DB_UCDMESH
    .. attribute:: DB_UCDVAR
    .. attribute:: DB_MULTIMESH
    .. attribute:: DB_MULTIVAR
    .. attribute:: DB_MULTIMAT
    .. attribute:: DB_MULTIMATSPECIES
    .. attribute:: DB_MULTIBLOCKMESH
    .. attribute:: DB_MULTIBLOCKVAR
    .. attribute:: DB_MULTIMESHADJ
    .. attribute:: DB_MATERIAL
    .. attribute:: DB_MATSPECIES
    .. attribute:: DB_FACELIST
    .. attribute:: DB_ZONELIST
    .. attribute:: DB_EDGELIST
    .. attribute:: DB_PHZONELIST
    .. attribute:: DB_CSGZONELIST
    .. attribute:: DB_CSGMESH
    .. attribute:: DB_CSGVAR
    .. attribute:: DB_CURVE
    .. attribute:: DB_DEFVARS
    .. attribute:: DB_POINTMESH
    .. attribute:: DB_POINTVAR
    .. attribute:: DB_ARRAY
    .. attribute:: DB_DIR
    .. attribute:: DB_VARIABLE
    .. attribute:: DB_USERDEF
