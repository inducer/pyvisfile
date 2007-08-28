#!/usr/bin/env python
# -*- coding: latin-1 -*-

import glob
import os
import os.path
import sys

try:
    execfile("siteconf.py")
except IOError:
    print "*** Please run configure first."
    sys.exit(1)

from distutils.core import setup,Extension

def non_matching_config():
    print "*** The version of your configuration template does not match"
    print "*** the version of the setup script. Please re-run configure."
    sys.exit(1)

try:
    PYLO_CONF_TEMPLATE_VERSION
except NameError:
    non_matching_config()

if PYLO_CONF_TEMPLATE_VERSION != 1:
    non_matching_config()

INCLUDE_DIRS = ["src/silo/include"] \
        + BOOST_INCLUDE_DIRS \
        + BOOST_BINDINGS_INCLUDE_DIRS

LIBRARY_DIRS = BOOST_LIBRARY_DIRS
LIBRARIES = BPL_LIBRARIES

EXTRA_DEFINES = {}
EXTRA_INCLUDE_DIRS = []
EXTRA_LIBRARY_DIRS = []
EXTRA_LIBRARIES = []

setup(name="pylo",
      version="0.90",
      description="A wrapper around libsilo",
      author=u"Andreas Kloeckner",
      author_email="inform@tiker.net",
      license = "BSD",
      url="http://news.tiker.net/software/pylo",
      packages=["pylo"],
      package_dir={"pylo": "src/python"},
      ext_package="pylo",
      ext_modules=[
            Extension("_internal", 
                [ "src/wrapper/wrap_silo.cpp", ],
                include_dirs=INCLUDE_DIRS + EXTRA_INCLUDE_DIRS,
                library_dirs=LIBRARY_DIRS + EXTRA_LIBRARY_DIRS,
                libraries=LIBRARIES + EXTRA_LIBRARIES,
                extra_compile_args=EXTRA_COMPILE_ARGS,
                define_macros=list(EXTRA_DEFINES.iteritems()),
                )],
     )
