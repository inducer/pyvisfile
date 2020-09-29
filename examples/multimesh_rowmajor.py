__author__ = "Christoph Statz, christoph.statz <at> tu-dresden.de"

import numpy as np

from pyvisfile.silo import SiloFile, \
        DB_HDF5, DB_CLOBBER, DBOPT_CYCLE, DBOPT_DTIME, DB_COLLINEAR, \
        DBOPT_XUNITS, DBOPT_YUNITS, DBOPT_XLABEL, DBOPT_YLABEL, \
        DBOPT_UNITS, DB_NODECENT, DBObjectType, DB_LOCAL, \
        DBOPT_HI_OFFSET


x_len = 50
y_len = 40
x = np.linspace(-10., 20., x_len)
y = np.linspace(20., 40., y_len)

# Funny, but in row-major y comes first.
data_global = np.zeros((y_len, x_len), dtype=np.float64, order="C")

x_from = [0, 19, 0, 19]
x_to = [21, 50, 21, 50]
y_from = [0, 0, 19, 19]
y_to = [21, 21, 40, 40]

# Mark the Ghostzones (at least in one direction).
hi_offset = [(1, 1), (0, 1), (1, 0), (0, 0)]

data_global[:20, :20] = 0.
data_global[20:, :20] = 1.
data_global[:20, 20:] = 2.
data_global[20:, 20:] = 3.

mesh_names = []
var_names = []

for i in range(4):

    file_name = "example_%05d.silo" % i
    s = SiloFile(file_name,
            mode=DB_CLOBBER,
            filetype=DB_HDF5,
            target=DB_LOCAL,
            fileinfo=f"Example Silo {i:05d}.")

    axes = (x[x_from[i]:x_to[i]], y[y_from[i]:y_to[i]])

    # Copy necessary due to slicing!
    data = data_global[y_from[i]:y_to[i], x_from[i]:x_to[i]].copy()

    options = dict()
    options[DBOPT_CYCLE] = 99
    options[DBOPT_DTIME] = 0.99
    options[DBOPT_XLABEL] = "X"
    options[DBOPT_YLABEL] = "Y"
    options[DBOPT_XUNITS] = "a"
    options[DBOPT_YUNITS] = "b"
    options[DBOPT_HI_OFFSET] = hi_offset[i]

    mesh_name = "mesh"
    s.put_quadmesh(mesh_name, axes, coordtype=DB_COLLINEAR, optlist=options)
    mesh_names.append((f"{file_name}:{mesh_name}", DB_COLLINEAR))

    options = dict()
    options[DBOPT_UNITS] = "unit"

    var_name = "variable"
    s.put_quadvar1(var_name, mesh_name, data, data.shape,
            centering=DB_NODECENT, optlist=options)
    var_names.append((f"{file_name}:{mesh_name}", DBObjectType.DB_QUADVAR))

options = dict()
options[DBOPT_CYCLE] = 99
options[DBOPT_DTIME] = 0.99
options[DBOPT_XLABEL] = "xx"
options[DBOPT_YLABEL] = "yy"
options[DBOPT_XUNITS] = "a"
options[DBOPT_YUNITS] = "b"

s = SiloFile("example.silo",
        mode=DB_CLOBBER,
        filetype=DB_HDF5,
        target=DB_LOCAL,
        fileinfo="Example Metadata.")

s.put_multimesh("mesh", mesh_names, optlist=options)
s.put_multivar("scalar", var_names, optlist=options)
