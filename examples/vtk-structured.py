from pyvisfile.vtk import write_structured_grid

import numpy as np

angle_mesh = np.mgrid[1:2:10j, 0:2*np.pi:20j, 0:np.pi:30j]

r = angle_mesh[0, np.newaxis]
phi = angle_mesh[1, np.newaxis]
theta = angle_mesh[2, np.newaxis]
mesh = np.vstack((
    r*np.sin(theta)*np.cos(phi),
    r*np.sin(theta)*np.sin(phi),
    r*np.cos(theta),
    ))

from pytools.obj_array import make_obj_array
vec = make_obj_array([
    np.sin(theta)*np.cos(phi),
    np.sin(theta)*np.sin(phi),
    np.cos(theta),
    ])

write_structured_grid("yo.vts", mesh,
        point_data=[("phi", phi), ("vec", vec)])
