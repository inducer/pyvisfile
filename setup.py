#!/usr/bin/env python

from aksetup_helper import NumpyExtension


class PyUblasExtension(NumpyExtension):
    def get_module_include_path(self, name):
        from pkg_resources import Requirement, resource_filename
        return resource_filename(Requirement.parse(name), "%s/include" % name)

    def get_additional_include_dirs(self):
        return (NumpyExtension.get_additional_include_dirs(self)
                + [self.get_module_include_path("pyublas")])


def get_config_schema():
    from aksetup_helper import (ConfigSchema,
            IncludeDir, LibraryDir, Libraries,
            Switch, StringListOption, make_boost_base_options)

    return ConfigSchema(make_boost_base_options() + [
        Switch("USE_SILO", False, "Compile libsilo interface"),

        IncludeDir("SILO", []),
        LibraryDir("SILO", []),
        Libraries("SILO", ["siloh5"]),

        StringListOption("CXXFLAGS", [],
            help="Any extra C++ compiler options to include"),
        ])


def main():
    from setuptools import find_packages
    from aksetup_helper import (hack_distutils, get_config, setup,
            ExtensionUsingNumpy, check_pybind11, PybindBuildExtCommand,
            get_pybind_include)

    hack_distutils()
    conf = get_config(get_config_schema(),
            warn_about_no_config=False)

    extra_defines = {}
    extra_include_dirs = []
    extra_library_dirs = []
    extra_libraries = []

    ver_dic = {}
    ver_file_name = "pyvisfile/__init__.py"
    with open(ver_file_name) as inf:
        exec(compile(inf.read(), ver_file_name, "exec"), ver_dic)

    requirements = []
    ext_modules = []

    if conf["USE_SILO"]:
        check_pybind11()

        extra_defines["USE_SILO"] = 1
        extra_include_dirs.extend(conf["SILO_INC_DIR"])
        extra_library_dirs.extend(conf["SILO_LIB_DIR"])
        extra_libraries.extend(conf["SILO_LIBNAME"])

        ext_modules.append(ExtensionUsingNumpy("_internal",
            ["src/wrapper/wrap_silo.cpp"],
            include_dirs=[get_pybind_include()] + extra_include_dirs,
            library_dirs=extra_library_dirs,
            libraries=extra_libraries,
            extra_compile_args=conf["CXXFLAGS"],
            define_macros=list(extra_defines.items()),
            language="c++",
            ))
        requirements.append("pybind11>=2.5.0")

    setup(name="pyvisfile",
            version=ver_dic["VERSION_TEXT"],
            description="Large-scale Visualization Data Storage",
            long_description=open("README.rst").read(),
            classifiers=[
                "Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "Intended Audience :: Other Audience",
                "Intended Audience :: Science/Research",
                "License :: OSI Approved :: MIT License",
                "Natural Language :: English",
                "Programming Language :: C++",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Topic :: Multimedia :: Graphics :: 3D Modeling",
                "Topic :: Scientific/Engineering",
                "Topic :: Scientific/Engineering :: Mathematics",
                "Topic :: Scientific/Engineering :: Physics",
                "Topic :: Scientific/Engineering :: Visualization",
                "Topic :: Software Development :: Libraries",
                ],

            author="Andreas Kloeckner",
            author_email="inform@tiker.net",
            license="MIT",
            url="http://mathema.tician.de/software/pyvisfile",

            # dependencies
            setup_requires=requirements,
            python_requires="~=3.6",
            install_requires=[
                    "pytools>=2013.2",
                    ] + requirements,

            packages=find_packages(),
            ext_package="pyvisfile.silo",
            ext_modules=ext_modules,

            cmdclass={"build_ext": PybindBuildExtCommand},
            zip_safe=False)


if __name__ == "__main__":
    main()
