#!/usr/bin/env python


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

    INCLUDE_DIRS = conf["BOOST_INC_DIR"]  # noqa

    LIBRARY_DIRS = conf["BOOST_LIB_DIR"]  # noqa
    LIBRARIES = conf["BOOST_PYTHON_LIBNAME"]  # noqa

    EXTRA_DEFINES = {}  # noqa
    EXTRA_INCLUDE_DIRS = []  # noqa
    EXTRA_LIBRARY_DIRS = []  # noqa
    EXTRA_LIBRARIES = []  # noqa

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

    setup(name="pyvisfile",
            version=ver_dic["VERSION_TEXT"],
            description="Large-scale Visualization Data Storage",
            long_description=open("README.rst", "rt").read(),
            classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Intended Audience :: Other Audience',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: MIT License',
                'Natural Language :: English',
                'Programming Language :: C++',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
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
            python_requires="~=3.6",
            install_requires=[
                    "pytools>=2013.2",
                    "six",
                    ] + requirements,

            packages=find_packages(),
            ext_package="pyvisfile.silo",
            ext_modules=ext_modules,

            zip_safe=False)


if __name__ == '__main__':
    main()
