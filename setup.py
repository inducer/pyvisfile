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
    from aksetup_helper import (
        ConfigSchema, IncludeDir, Libraries, LibraryDir, StringListOption, Switch,
        make_boost_base_options)

    return ConfigSchema(make_boost_base_options() + [
        Switch("USE_SILO", False, "Compile libsilo interface"),

        IncludeDir("SILO", []),
        LibraryDir("SILO", []),
        Libraries("SILO", ["siloh5"]),

        StringListOption("CXXFLAGS", [],
            help="Any extra C++ compiler options to include"),
        ])


def main():
    from aksetup_helper import (
        ExtensionUsingNumpy, PybindBuildExtCommand, check_pybind11, get_config,
        get_pybind_include, hack_distutils, setup)

    hack_distutils()
    conf = get_config(get_config_schema(),
            warn_about_no_config=False)

    extra_defines = {}
    extra_include_dirs = []
    extra_library_dirs = []
    extra_libraries = []

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

    setup(
        ext_modules=ext_modules,
        cmdclass={"build_ext": PybindBuildExtCommand}
    )


if __name__ == "__main__":
    main()
