# modified from original code by Matthieu Haefele (IPP, Max-Planck-Gesellschaft)

import numpy

try:
    from pyvisfile import silo
except ImportError as exc:
    print(f"Failed to import 'pyvisfile.silo': {exc}")
    raise SystemExit(0) from None


# {{{ write mesh

f = silo.SiloFile("qmesh.silo", mode=silo.DB_CLOBBER)
coord = [
        numpy.linspace(-1.0, 1.0, 50),
        numpy.linspace(-2.0, 2.0, 100)
        ]

f.put_quadmesh("meshxy", coord)

value = coord[0][:, numpy.newaxis] * coord[1][numpy.newaxis, :]

f.put_quadvar1("value", "meshxy", numpy.asarray(value, order="F"), value.shape,
        centering=silo.DB_NODECENT)

f.close()

# }}}


# {{{ read mesh

db = silo.SiloFile("qmesh.silo", create=False, mode=silo.DB_READ)
print(db.get_toc().qmesh_names)
print(db.get_toc().qvar_names)

qmesh = db.get_quadmesh("meshxy")
print(qmesh.coords)

qvar = db.get_quadvar("value")
print(qvar.vals)

# }}}
