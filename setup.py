#!/usr/bin/env python
# -*- coding: latin-1 -*-




def get_config_schema():
    from aksetup_helper import ConfigSchema, Option, \
            IncludeDir, LibraryDir, Libraries, BoostLibraries, \
            Switch, StringListOption, make_boost_base_options

    return ConfigSchema(make_boost_base_options() + [
        BoostLibraries("python"),

        IncludeDir("SILO", []),
        LibraryDir("SILO", []),
        Libraries("SILO", ["silo"]),

        StringListOption("CXXFLAGS", [], 
            help="Any extra C++ compiler options to include"),
        ])




def main():
    from aksetup_helper import hack_distutils, get_config, setup, \
            PyUblasExtension

    hack_distutils()
    conf = get_config(get_config_schema())

    INCLUDE_DIRS = conf["BOOST_INC_DIR"] \

    LIBRARY_DIRS = conf["BOOST_LIB_DIR"]
    LIBRARIES = conf["BOOST_PYTHON_LIBNAME"]

    EXTRA_DEFINES = { }
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
            version="0.91.2",
            description="Large-scale Visualization Data Storage",
            long_description="""
            Pylo allows you to write Silo visualization files, as
            introduced by LLNL's 
            `MeshTV <https://wci.llnl.gov/codes/meshtv/>`_ and
            more recently used by the 
            `VisIt <https://wci.llnl.gov/codes/visit/>`_ 
            large-scale visualization program. Check the
            `VisIt source page <https://wci.llnl.gov/codes/visit/source.html>`_
            for the latest Silo source code.

            Pylo supports the majority of datatypes allowed in 
            Silo files, such as unstructured and rectangular
            structured meshes, particle meshes, as well as 
            scalar and vector variables on them. In addition,
            Pylo supports expressions of scalar variables and
            semi-automatic writing of parallelization-segmented
            Silo files.

            Pylo uses `Boost.Python <http://www.boost.org>`_ and `PyUblas
            <http://mathema.tician.de/software/pyublas>`_.  To build it, please
            refer to the `PyUblas documentation <http://tiker.net/doc/pyublas>`_
            for build instructions first. After that, building pylo should be
            straightforward.
            """,
            classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'Intended Audience :: Other Audience',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: MIT License',
              'Natural Language :: English',
              'Programming Language :: C++',
              'Programming Language :: Python',
              'Topic :: Multimedia :: Graphics :: 3D Modeling',
              'Topic :: Scientific/Engineering',
              'Topic :: Scientific/Engineering :: Mathematics',
              'Topic :: Scientific/Engineering :: Physics',
              'Topic :: Scientific/Engineering :: Visualization',
              'Topic :: Software Development :: Libraries',
              ],

            author=u"Andreas Kloeckner",
            author_email="inform@tiker.net",
            license = "MIT",
            url="http://mathema.tician.de/software/pylo",

            # dependencies
            setup_requires=[
                "PyUblas>=0.92.1",
                ],
            install_requires=[
                "PyUblas>=0.92.1",
                ],

            packages=["pylo"],
            ext_package="pylo",
            ext_modules=[
                PyUblasExtension("_internal", 
                    [ "src/wrapper/wrap_silo.cpp", ],
                    include_dirs=INCLUDE_DIRS + EXTRA_INCLUDE_DIRS,
                    library_dirs=LIBRARY_DIRS + EXTRA_LIBRARY_DIRS,
                    libraries=LIBRARIES + EXTRA_LIBRARIES,
                    extra_compile_args=conf["CXXFLAGS"],
                    define_macros=list(EXTRA_DEFINES.iteritems()),
                    )],

            zip_safe=False)




if __name__ == '__main__':
    main()
