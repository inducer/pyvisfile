from __future__ import annotations

import numpy as np

from pytools import obj_array

from pyvisfile.vtk import write_structured_grid


angle_mesh = np.mgrid[1:2:10j, 0:2*np.pi:20j]

r = angle_mesh[0, np.newaxis]
phi = angle_mesh[1, np.newaxis]
mesh = np.vstack([r*np.cos(phi), r*np.sin(phi)])

vec = obj_array.new_1d([np.cos(phi), np.sin(phi)])
write_structured_grid(
    "yo-2d.vts",
    mesh,
    point_data=[("phi", phi), ("vec", vec)])
