#!/usr/bin/env python
# -*- coding: latin-1 -*-




def get_config_schema():
    from aksetup_helper import ConfigSchema, Option, \
            IncludeDir, LibraryDir, Libraries, \
            Switch, StringListOption

    return ConfigSchema([
        IncludeDir("BOOST", []),
        LibraryDir("BOOST", []),
        Libraries("BOOST_PYTHON", ["boost_python-gcc42-mt"]),

        IncludeDir("NUMPY"),

        IncludeDir("BOOST_BINDINGS", []),

        IncludeDir("SILO", []),
        LibraryDir("SILO", []),
        Libraries("SILO", ["silo"]),

        StringListOption("CXXFLAGS", [], 
            help="Any extra C++ compiler options to include"),
        ])




def main():
    from aksetup_helper import hack_distutils, get_config, setup, Extension

    hack_distutils()
    conf = get_config()

    if conf["NUMPY_INC_DIR"] is None:
        try:
            import numpy
            from os.path import join
            conf["NUMPY_INC_DIR"] = [join(numpy.__path__[0], "core", "include")]
        except:
            pass

    INCLUDE_DIRS = ["src/silo/include"] \
            + conf["BOOST_INC_DIR"] \
            + conf["BOOST_BINDINGS_INC_DIR"] \
            + conf["NUMPY_INC_DIR"]

    LIBRARY_DIRS = conf["BOOST_LIB_DIR"]
    LIBRARIES = conf["BOOST_PYTHON_LIBNAME"]

    EXTRA_DEFINES = {}
    EXTRA_INCLUDE_DIRS = []
    EXTRA_LIBRARY_DIRS = []
    EXTRA_LIBRARIES = []

    def handle_component(comp):
        if conf["USE_"+comp]:
            EXTRA_DEFINES["USE_"+comp] = 1
            EXTRA_INCLUDE_DIRS.extend(conf[comp+"_INC_DIR"])
            EXTRA_LIBRARY_DIRS.extend(conf[comp+"_LIB_DIR"])
            EXTRA_LIBRARIES.extend(conf[comp+"_LIBNAME"])

    conf["USE_SILO"] = True
    handle_component("SILO")

    setup(name="pylo",
            version="0.90",
            description="A wrapper around libsilo",
            author=u"Andreas Kloeckner",
            author_email="inform@tiker.net",
            license = "BSD",
            url="http://news.tiker.net/software/pylo",

            # dependencies
            setup_requires=[
                "PyUblas>=0.92",
                ],
            zip_safe=False,

            packages=["pylo"],
            package_dir={"pylo": "src/python"},
            ext_package="pylo",
            ext_modules=[
                Extension("_internal", 
                    [ "src/wrapper/wrap_silo.cpp", ],
                    include_dirs=INCLUDE_DIRS + EXTRA_INCLUDE_DIRS,
                    library_dirs=LIBRARY_DIRS + EXTRA_LIBRARY_DIRS,
                    libraries=LIBRARIES + EXTRA_LIBRARIES,
                    extra_compile_args=conf["CXXFLAGS"],
                    define_macros=list(EXTRA_DEFINES.iteritems()),
                    )],
         )




if __name__ == '__main__':
    main()
