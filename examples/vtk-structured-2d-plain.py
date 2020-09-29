# contributed by Luke Olson

import numpy as np

n = 50
x, y = np.meshgrid(np.linspace(-1, 1, n),
np.linspace(-1, 1, n))

u = np.exp(-50 * (x**2 + y**2))

from pyvisfile.vtk import write_structured_grid
mesh = np.rollaxis(np.dstack((x, y)), 2)
write_structured_grid("test.vts", mesh,
        point_data=[("u", u[np.newaxis, :, :])])
