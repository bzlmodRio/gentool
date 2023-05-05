from bazelrio_gentool.deps.sha256_helper import get_hash


class CppPlatformConfig:
    def __init__(self, os, short_os, ext, arch):
        self.os = os
        self.short_os = short_os
        self.ext = ext
        self.arch = arch


class CppToolchainConfig:
    def __init__(
        self,
        repo_name,
        short_name,
        year,
        version,
        toolchain_version,
        release_version,
        bin_subfolder,
        bin_prefix,
        sysroot_subfolder,
        cxx_version,
        sysroot_include_folder,
        cpp_url,
        cpp_platform_configs,
    ):
        self.repo_name = repo_name
        self.version = version
        self.short_name = short_name
        self.release_version = release_version
        self.release_version_underscore = release_version.replace("-", "_")
        self.toolchain_version = toolchain_version
        self.year = year

        self.bin_subfolder = bin_subfolder
        self.bin_prefix = bin_prefix
        self.sysroot_subfolder = sysroot_subfolder
        self.cxx_version = cxx_version
        self.sysroot_include_folder = sysroot_include_folder

        self.cpp_url = cpp_url

        self.cpp_platform_configs = cpp_platform_configs

        self.short_name_underscore = short_name.replace("-", "_")
        self.short_name_no_dash = short_name.replace("-", "")

    def get_cpp_url(self, platform_config):
        release_version_hyphen = self.release_version.replace("_", "-")
        return self.cpp_url.format(
            ext=platform_config.ext,
            year=self.year,
            platform_config=platform_config,
            toolchain_version=self.toolchain_version,
            release_version_hyphen=release_version_hyphen,
            arch=platform_config.arch,
        )

    def get_cpp_sha256(self, resource):
        return get_hash(self.get_cpp_url(resource), True)

    def has_any_maven_deps(self):
        return False


class ToolchainDependencyContainer:
    def __init__(self, repo_name, year, version):
        self.repo_name = repo_name
        self.version = version
        self.year = year
        self.configs = []

        self.sanitized_version = self.version.replace("+", "-")
