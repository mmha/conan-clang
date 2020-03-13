from conans import ConanFile, python_requires, tools
import os

base = python_requires("llvm-project/0.1@mmha/testing")

class IntelClangConan(base.llvm_base_project()):
    name = "clang"
    version = "10.0.0-20190903"
    description = "The Clang C++ compiler"
    url = "https://llvm.org"
    license = "Apache-2.0"
    author = "LLVM"
    topics = ("llvm", "clang", "compiler", "c++", "c")

    scm = {
        "type": "git",
        "url": "https://github.com/llvm/llvm-project.git",
        "revision": "ea366122d28f7756008543e495f1899b64f4060a"
    }

    @property
    def source_subfolder(self):
        return "clang"

    llvm_cmake_options = {
        "build_docs": [True, False],
        "build_examples": [True, False],
        "build_tests": [True, False],
        "build_tools": [True, False],
        "default_cxx_stdlib": "ANY",
        "default_linker": "ANY",
        "default_objcopy": "ANY",
        "default_openmp_runtime": "ANY",
        "default_rtlib": "ANY",
        "default_std_c": "ANY",
        "default_std_cxx": "ANY",
        "default_unwindlib": "ANY",
        "enable_arcmt": [True, False],
        "enable_bootstrap": [True, False],
        "enable_proto_fuzzer": [True, False],
        "enable_static_analyzer": [True, False],
        "link_clang_dylib": [True, False],
        "openmp_nvptx_default_arch": "ANY",
        "order_file": "ANY",
        "python_bindings_versions": "ANY",
        "repository_string": "ANY",
        "resource_dir": "ANY",
        "vendor": "ANY",
        "vendor_uti": "ANY",
    }

    default_llvm_cmake_options = {
        "build_docs": False,
        "build_examples": False,
        "build_tests": False,
        "build_tools": True,
        "default_cxx_stdlib": "",
        "default_linker": "",
        "default_objcopy": "",
        "default_openmp_runtime": "",
        "default_rtlib": "",
        "default_std_c": "",
        "default_std_cxx": "",
        "default_unwindlib": "",
        "enable_arcmt": False,
        "enable_bootstrap": False,
        "enable_proto_fuzzer": False,
        "enable_static_analyzer": False,
        "link_clang_dylib": False,
        "openmp_nvptx_default_arch": "",
        "order_file": "",
        "python_bindings_versions": "",
        "repository_string": "",
        "resource_dir": "",
        "vendor": "",
        "vendor_uti": "",
    }

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        **llvm_cmake_options
    }

    default_options = {
        "shared": False,
        "fPIC": False,
        **default_llvm_cmake_options
    }

    @property
    def custom_cmake_definitions(self):
        return {
            "CLANG_INCLUDE_DOCS": self.options.build_docs,
            "CLANG_INCLUDE_TESTS": self.options.build_tests,
        }

    def requirements(self):
        self.requires(f"llvm/{self.version}@mmha/testing")

    def package_info(self):
        super().package_info()
        bindir = os.path.join(self.package_folder, "bin")
        if self.settings.os == "Windows":
            if hasattr(self.settings.os, "subsystem") and self.settings.os.subsystem not in ["cygwin", "msys", "msys2", "wsl"]:
                self.env_info.CC = os.path.join(bindir, "clang-cl")
                self.env_info.CXX = os.path.join(bindir, "clang-cl")
        else:
            self.env_info.CC = os.path.join(bindir, "clang")
            self.env_info.CXX = os.path.join(bindir, "clang++")

    def package_id(self):
        del self.info.options.build_examples
        del self.info.options.build_tests
