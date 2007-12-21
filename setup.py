#!/usr/bin/env python
# -*- coding: latin-1 -*-

import glob
import os
import os.path
import sys

def main():
    try:
        conf = {}
        execfile("siteconf.py", conf)
    except IOError:
        print "*** Please run configure first."
        sys.exit(1)

    from distutils.core import setup,Extension

    def non_matching_config():
        print "*** The version of your configuration template does not match"
        print "*** the version of the setup script. Please re-run configure."
        sys.exit(1)

    if "PYLO_CONF_TEMPLATE_VERSION" not in conf:
        non_matching_config()

    if conf["PYLO_CONF_TEMPLATE_VERSION"] != 1:
        non_matching_config()

    INCLUDE_DIRS = ["src/silo/include"] \
            + conf["BOOST_INCLUDE_DIRS"] \
            + conf["BOOST_BINDINGS_INCLUDE_DIRS"]

    LIBRARY_DIRS = conf["BOOST_LIBRARY_DIRS"]
    LIBRARIES = conf["BPL_LIBRARIES"]

    EXTRA_DEFINES = {}
    EXTRA_INCLUDE_DIRS = []
    EXTRA_LIBRARY_DIRS = []
    EXTRA_LIBRARIES = []

    def handle_component(comp):
        if conf["USE_"+comp]:
            EXTRA_DEFINES["USE_"+comp] = 1
            EXTRA_INCLUDE_DIRS.extend(conf[comp+"_INCLUDE_DIRS"])
            EXTRA_LIBRARY_DIRS.extend(conf[comp+"_LIBRARY_DIRS"])
            EXTRA_LIBRARIES.extend(conf[comp+"_LIBRARIES"])

    conf["USE_SILO"] = True
    handle_component("SILO")

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
                    extra_compile_args=conf["EXTRA_COMPILE_ARGS"],
                    define_macros=list(EXTRA_DEFINES.iteritems()),
                    )],
         )




if __name__ == '__main__':
    # hack distutils.sysconfig to eliminate debug flags
    # stolen from mpi4py
    import sys
    if not sys.platform.lower().startswith("win"):
        from distutils import sysconfig

        cvars = sysconfig.get_config_vars()
        cflags = cvars.get('OPT')
        if cflags:
            cflags = cflags.split()
            for bad_prefix in ('-g', '-O', '-Wstrict-prototypes'):
                for i, flag in enumerate(cflags):
                    if flag.startswith(bad_prefix):
                        cflags.pop(i)
                        break
                if flag in cflags:
                    cflags.remove(flag)
            cflags.append("-O3")
            cvars['OPT'] = str.join(' ', cflags)
            cvars["CFLAGS"] = cvars["BASECFLAGS"] + " " + cvars["OPT"]
    # and now call main
    main()
