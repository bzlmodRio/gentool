
from bazelrio_gentool.deps.sha256_helper import get_hash

class CppPlatformConfig:
    def __init__(self, os, short_os, ext):
        self.os = os
        self.short_os = short_os
        self.ext = ext

class CppToolchainConfig:
    def __init__(
        self,
        repo_name,
        year,
        version,
        toolchain_version,
        release_version,
        cpp_url,
        cpp_platform_configs,
    ):
        self.repo_name = repo_name
        self.version = version
        self.release_version = release_version
        self.release_version_underscore = release_version.replace("-", "_")
        self.toolchain_version = toolchain_version
        self.year = year

        self.cpp_url = cpp_url

        self.cpp_platform_configs = cpp_platform_configs
        print(self.cpp_platform_configs)

    def get_cpp_url(self, platform_config):
        release_version_hyphen = self.release_version.replace("_", "-")
        return self.cpp_url.format(
            ext=platform_config.ext,
            year=self.year,
            platform_config=platform_config,
            toolchain_version=self.toolchain_version,
            release_version_hyphen=release_version_hyphen,
        )

    def get_cpp_sha256(self, resource):
        return get_hash(self.get_cpp_url(resource), True)
