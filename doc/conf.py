from datetime import datetime
from importlib import metadata
from urllib.request import urlopen


_conf_url = \
        "https://raw.githubusercontent.com/inducer/sphinxconfig/main/sphinxconfig.py"
with urlopen(_conf_url) as _inf:
    exec(compile(_inf.read(), _conf_url, "exec"), globals())

copyright = f"2010 - {datetime.today().year}, Andreas Kloeckner"
release = metadata.version("pyvisfile")
version = ".".join(release.split(".")[:2])

intersphinx_mapping = {
        "modepy": ("https://documen.tician.de/modepy", None),
        "numpy": ("https://numpy.org/doc/stable/", None),
        "python": ("https://docs.python.org/3/", None),
        "pytools": ("https://documen.tician.de/pytools", None),
}
