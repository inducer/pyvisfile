from __future__ import annotations

from datetime import datetime
from importlib import metadata
from typing import TYPE_CHECKING
from urllib.request import urlopen


if TYPE_CHECKING:
    from sphinx.application import Sphinx


_conf_url = "https://tiker.net/sphinxconfig-v0.py"
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


sphinxconfig_missing_reference_aliases: dict[str, str] = {
    "np.dtype": "class:numpy.dtype",
    "np.ndarray": "class:numpy.ndarray",
}


def setup(app: Sphinx) -> None:
    app.connect("missing-reference", process_autodoc_missing_reference)  # noqa: F821
