import re
from bazelrio_gentool.deps.multi_resource_dependency import MultiResourceDependency


class CcDependency(MultiResourceDependency):
    def __init__(
        self,
        artifact_name,
        maven_url,
        group_id,
        version,
        parent_folder,
        dependencies,
        resources,
        headers,
        sources,
        has_jni,
        repo_name,
        fail_on_hash_miss=True,
    ):
        MultiResourceDependency.__init__(
            self,
            artifact_name=artifact_name,
            group_id=group_id,
            maven_url=maven_url,
            version=version,
            file_extension=".zip",
            resources=resources,
            repo_name=repo_name,
            fail_on_hash_miss=fail_on_hash_miss,
        )
        self.name = artifact_name
        self.parent_folder = parent_folder
        self.has_jni = has_jni
        self.headers = headers
        self.sources = sources
        self.dependencies = dependencies

    def get_header_archive_name(self):
        return self.get_archive_name("headers")

    def __repr__(self):
        return f"CcDependency: name={self.name}"

    def get_build_file_content(self, resource):
        if resource == "headers":
            return "cc_library_headers"
        elif resource == "sources":
            return "cc_library_sources"
        elif "static" not in resource:
            return "cc_library_shared"
        else:
            return "cc_library_static"

    # CONDITIONS_LOOKUP = {
    #     "@bazel_tools//src/conditions:windows": ["windowsx86-64"],
    #     "@bazel_tools//src/conditions:linux_x86_64": ["linuxx86-64"],
    #     "@bazel_tools//src/conditions:darwin": ["osxx86-64", "osxuniversal"],
    #     "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["linuxathena"],
    # }

    CONDITIONS_LOOKUP = {
        "windowsx86-64": "@rules_bazelrio//conditions:windows",
        "windowsx86-64debug": "@rules_bazelrio//conditions:windows_debug",
        "windowsx86-64static": "@rules_bazelrio//conditions:windows",
        "windowsx86-64staticdebug": "@rules_bazelrio//conditions:windows_debug",
        "linuxx86-64": "@rules_bazelrio//conditions:linux_x86_64",
        "linuxx86-64debug": "@rules_bazelrio//conditions:linux_x86_64_debug",
        "linuxx86-64static": "@rules_bazelrio//conditions:linux_x86_64",
        "linuxx86-64staticdebug": "@rules_bazelrio//conditions:linux_x86_64_debug",
        "osxx86-64": "@rules_bazelrio//conditions:osx",
        "osxx86-64debug": "@rules_bazelrio//conditions:osx_debug",
        "osxx86-64static": "@rules_bazelrio//conditions:osx",
        "osxx86-64staticdebug": "@rules_bazelrio//conditions:osx_debug",
        "osxuniversal": "@rules_bazelrio//conditions:osx",
        "osxuniversaldebug": "@rules_bazelrio//conditions:osx_debug",
        "osxuniversalstatic": "@rules_bazelrio//conditions:osx",
        "osxuniversalstaticdebug": "@rules_bazelrio//conditions:osx_debug",
        # Cross Compilers
        "linuxathena"             : "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio",
        "linuxathenadebug"        : "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio_debug",
        "linuxathenastatic"       : "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio",
        "linuxathenastaticdebug"  : "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio_debug",
        
        "linuxarm32"             : "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32",
        "linuxarm32debug"        : "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32_debug",
        "linuxarm32static"       : "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32",
        "linuxarm32staticdebug"  : "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32_debug",
        
        "linuxarm64"             : "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64",
        "linuxarm64debug"        : "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64_debug",
        "linuxarm64static"       : "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64",
        "linuxarm64staticdebug"  : "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64_debug",
    }

    def __make_ignored_platforms(base_platform):
        return [
            base_platform,
            base_platform + "static",
            base_platform + "staticdebug",
            base_platform + "debug",
        ]

    IGNORED_PLATFORMS = __make_ignored_platforms(
        "windowsx86"
    ) + __make_ignored_platforms("osxarm64")

    def __get_select(self, resources, library_build):
        lines = []
        for res in resources:
            full_res = res
            if full_res in self.CONDITIONS_LOOKUP:
                lines.append(
                    f'        "{self.CONDITIONS_LOOKUP[full_res]}": ["@{self.get_archive_name(res)}//:{library_build}"]'
                )
            elif full_res not in self.IGNORED_PLATFORMS:
                print("Unknown", full_res)
            # condition = self.__resource_type_to_condition(res)
            # if condition:
            #     lines.append(f'        "{condition}": ["@{self.get_archive_name(res)}//:shared_libs"]')

        return ",\n".join(lines) + ","

    def get_shared_library_select(self):
        shared_resources = []
        for res in self.resources:
            if res.endswith("staticdebug") or res.endswith("static"):
                pass
            else:
                shared_resources.append(res)

        return self.__get_select(shared_resources, "shared_libs")

    def get_static_library_select(self):
        shared_resources = []
        for res in self.resources:
            if res.endswith("static") or res.endswith("staticdebug"):
                shared_resources.append(res)
        return self.__get_select(shared_resources, "static_libs")

    # def get_static_debug_library_select(self):
    #     shared_resources = []
    #     for res in self.resources:
    #         if res.endswith("staticdebug"):
    #             shared_resources.append(res)
    #     return self.__get_select(shared_resources, "static_libs")

    def get_jni_shared_library_select(self):
        shared_resources = []
        for res in self.resources:
            if res.endswith("staticdebug") or res.endswith("static"):
                pass
            else:
                shared_resources.append(res)

        return self.__get_select(shared_resources, "shared_jni_libs")

    def has_incompatible_targets(self):
        if "linuxathena" not in self.resources:
            return True


class CcMetaDependency:
    def __init__(self, repo_name, name, deps, platform_deps, has_static, jni_deps):
        self.repo_name = repo_name
        self.name = name
        self.deps = deps
        self.parent_folder = name
        self.platform_deps = platform_deps
        self.has_static = has_static
        self.jni_deps = jni_deps
