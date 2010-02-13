# modified from original code by Matthieu Haefele (IPP, Max-Planck-Gesellschaft)

import numpy
import pylo

f = pylo.SiloFile("qmesh.silo", mode=pylo.DB_CLOBBER)
coord = [
        numpy.linspace(-1.0,1.0,50),
        numpy.linspace(-2.0,2.0,100)
        ]

f.put_quadmesh("meshxy", coord)

value = coord[0][:,numpy.newaxis]* coord[1][numpy.newaxis,:]

f.put_quadvar1("value", "meshxy", numpy.asarray(value, order="F"), value.shape,
        centering=pylo.DB_NODECENT)

f.close()
