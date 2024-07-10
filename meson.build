project('pyvisfile', 'cpp',
  license: 'MIT',
  meson_version: '>=1.0.0',
  default_options : ['warning_level=2', 'cpp_std=c++14'],
)

# {{{ gather includes

py_mod = import('python')
py = py_mod.find_installation(pure: false)
pybind11_dep = dependency('pybind11')

# NOTE: meson does not like absolute paths, so we dance around it
incdir_numpy = run_command(py,
  [
    '-c',
    '''import os
import numpy as np
try:
  incdir = os.path.relpath(np.get_include())
except Exception:
  incdir = np.get_include()
print(incdir)
  '''], check: true).stdout().strip()
inc_numpy = include_directories(incdir_numpy)

# get SILO includes as well
if get_option('use-silo')
  cpp = meson.get_compiler('cpp')
  silo_dep = dependency(['silo', 'siloh5'], required: false)

  if not silo_dep.found()
    silo_dep = cpp.find_library('silo', required: false)
  endif

  if not silo_dep.found()
    silo_dep = cpp.find_library('siloh5', required: true)
  endif

  silo_dep = [silo_dep]
else
  silo_dep = []
endif

# }}}

# {{{ wrapper

if silo_dep.length() == 1
  py.extension_module(
    '_internal',
    ['src/wrapper/wrap_silo.cpp'],
    dependencies : [pybind11_dep, silo_dep],
    include_directories: [incdir_numpy],
    subdir: 'pyvisfile/silo',
    install: true,
  )
endif

py.install_sources([
  'pyvisfile/__init__.py',
  'pyvisfile/py.typed',
  'pyvisfile/silo/__init__.py',
  'pyvisfile/vtk/__init__.py',
  'pyvisfile/vtk/vtk_ordering.py',
  'pyvisfile/xdmf/__init__.py',
  ],
  preserve_path: true)

# }}}
