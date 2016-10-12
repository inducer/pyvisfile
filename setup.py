#!/usr/bin/env python
# -*- coding: latin-1 -*-


def get_config_schema():
    from aksetup_helper import ConfigSchema,  \
            IncludeDir, LibraryDir, Libraries, BoostLibraries, \
            Switch, StringListOption, make_boost_base_options

    return ConfigSchema(make_boost_base_options() + [
        Switch("USE_SILO", False, "Compile libsilo interface"),

        BoostLibraries("python"),

        IncludeDir("SILO", []),
        LibraryDir("SILO", []),
        Libraries("SILO", ["siloh5"]),

        StringListOption("CXXFLAGS", [],
            help="Any extra C++ compiler options to include"),
        ])


def main():
    from setuptools import find_packages
    from aksetup_helper import hack_distutils, get_config, setup, \
            PyUblasExtension

    hack_distutils()
    conf = get_config(get_config_schema())

    INCLUDE_DIRS = conf["BOOST_INC_DIR"] \

    LIBRARY_DIRS = conf["BOOST_LIB_DIR"]
    LIBRARIES = conf["BOOST_PYTHON_LIBNAME"]

    EXTRA_DEFINES = {}
    EXTRA_INCLUDE_DIRS = []
    EXTRA_LIBRARY_DIRS = []
    EXTRA_LIBRARIES = []

    ver_dic = {}
    ver_file_name = "pyvisfile/__init__.py"
    with open(ver_file_name, "r") as inf:
        exec(compile(inf.read(), ver_file_name, 'exec'), ver_dic)

    requirements = []
    ext_modules = []

    if conf["USE_SILO"]:
        EXTRA_DEFINES["USE_SILO"] = 1
        EXTRA_INCLUDE_DIRS.extend(conf["SILO_INC_DIR"])
        EXTRA_LIBRARY_DIRS.extend(conf["SILO_LIB_DIR"])
        EXTRA_LIBRARIES.extend(conf["SILO_LIBNAME"])

        ext_modules.append(PyUblasExtension("_internal",
            ["src/wrapper/wrap_silo.cpp"],
            include_dirs=INCLUDE_DIRS + EXTRA_INCLUDE_DIRS,
            library_dirs=LIBRARY_DIRS + EXTRA_LIBRARY_DIRS,
            libraries=LIBRARIES + EXTRA_LIBRARIES,
            extra_compile_args=conf["CXXFLAGS"],
            define_macros=list(EXTRA_DEFINES.items()),
            ))

        requirements.append("PyUblas>=0.92.1")

    setup(name="pyvisfile",
            version=ver_dic["VERSION_TEXT"],
            description="Large-scale Visualization Data Storage",
            long_description="""
            Pyvisfile allows you to write a variety of visualization file formats,
            including

            * `Kitware's <http://www.kitware.com>`_
              `XML-style <http://www.vtk.org/VTK/help/documentation.html>`_
              `Vtk <http://vtk.org>`_ data files.

            * Silo visualization files, as
              introduced by LLNL's
              `MeshTV <https://wci.llnl.gov/codes/meshtv/>`_ and
              more recently used by the
              `VisIt <https://wci.llnl.gov/codes/visit/>`_
              large-scale visualization program.

            pyvisfiles supports many mesh geometries, such such as unstructured
            and rectangular structured meshes, particle meshes, as well as
            scalar and vector variables on them. In addition, pyvisfile allows the
            semi-automatic writing of parallelization-segmented visualization files
            in both Silo and Vtk formats. For Silo files, pyvisfile also
            supports the writing of expressions as visualization variables.

            pyvisfile can write Vtk files without any extra software installed.

            To use pyvisfile to create Silo files, you need `libsilo
            <https://wci.llnl.gov/codes/silo/>`_ as well as `Boost.Python
            <http://www.boost.org>`_ and `PyUblas
            <http://mathema.tician.de/software/pyublas>`_.  To build
            pyvisfile's Silo support, please refer to the `PyUblas
            documentation <http://tiker.net/doc/pyublas>`_ for build
            instructions first. Check the
            `VisIt source page <https://wci.llnl.gov/codes/visit/source.html>`_
            for the latest Silo source code.
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
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Topic :: Multimedia :: Graphics :: 3D Modeling',
                'Topic :: Scientific/Engineering',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Topic :: Scientific/Engineering :: Physics',
                'Topic :: Scientific/Engineering :: Visualization',
                'Topic :: Software Development :: Libraries',
                ],

            author=u"Andreas Kloeckner",
            author_email="inform@tiker.net",
            license="MIT",
            url="http://mathema.tician.de/software/pyvisfile",

            # dependencies
            setup_requires=requirements,
            install_requires=[
                    "pytools>=2013.2",
                    ] + requirements,

            packages=find_packages(),
            ext_package="pyvisfile.silo",
            ext_modules=ext_modules,

            zip_safe=False)


if __name__ == '__main__':
    main()
