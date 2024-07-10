try:
    from pyvisfile.silo import DB_READ, SiloFile
except ImportError as exc:
    print(f"Failed to import 'pyvisfile.silo': {exc}")
    raise SystemExit(0) from None


db = SiloFile("qmesh.silo", create=False, mode=DB_READ)
print(db.get_toc().qmesh_names)
print(db.get_toc().qvar_names)

qmesh = db.get_quadmesh("meshxy")
print(qmesh.coords)

qvar = db.get_quadvar("value")
print(qvar.vals)
