from pyvisfile.silo import SiloFile, DB_READ
db = SiloFile("qmesh.silo", create=False, mode=DB_READ)
print db.get_toc().qmesh_names
print db.get_toc().qvar_names

qmesh = db.get_quadmesh("meshxy")
print qmesh.coords
qvar = db.get_quadvar("value")
print qvar.vals

