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
        has_install_name_patches=True,
        artifact_install_name=None,
        extra_install_name_dependencies=None,
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

        self.has_install_name_patches = has_install_name_patches
        if has_install_name_patches and artifact_install_name is None:
            self.artifact_install_name = self.parent_folder
        else:
            self.artifact_install_name = artifact_install_name
        self.extra_install_name_dependencies = extra_install_name_dependencies or []

    def get_header_archive_name(self):
        return self.get_archive_name("headers")

    def __repr__(self):
        return f"CcDependency: name={self.name}, parent_folder={self.parent_folder}"

    def get_build_file_content(self, resource):
        if resource == "headers":
            return "cc_library_headers"
        elif resource == "sources":
            return "cc_library_sources"
        elif "static" not in resource:
            return "cc_library_shared"
        else:
            return "cc_library_static"

    def set_install_name_patches(patches):
        self.install_name_patches = patches

    def maybe_patch_args(self, resource):
        if "shared" not in self.get_build_file_content(resource):
            return ""
        if "osx" not in resource:
            return ""

        if not self.has_install_name_patches:
            return ""

        def get_dependent_patches(dep):
            if type(dep) == dict:
                artifact_install_name = dep["parent_folder"]
                has_install_name_patches = False
                return []
            else:
                artifact_install_name = dep.artifact_install_name
                has_install_name_patches = dep.has_install_name_patches
            output = []

            if not has_install_name_patches:
                return output

            if self != dep:
                output.append(
                    f'            "install_name_tool -change lib{artifact_install_name}.dylib @rpath/lib{artifact_install_name}.dylib osx/universal/shared/lib{self.artifact_install_name}.dylib",'
                )

            for dep in dep.get_sorted_dependencies():
                output.extend(get_dependent_patches(dep))
            return output

        def get_extra_dependent_patches(extra_dep):
            patches = []
            for dep in extra_dep.extra_install_name_dependencies:
                patches.extend(get_extra_dependent_patches(dep))

            for dep in extra_dep.extra_install_name_dependencies:
                patches.extend(get_dependent_patches(dep))

            return patches

        output = "\n        patch_cmds = [\n"
        output += f'            "install_name_tool -id @rpath/lib{self.artifact_install_name}.dylib osx/universal/shared/lib{self.artifact_install_name}.dylib",'
        # output += patches

        patches = set()

        patches.update(get_dependent_patches(self))
        patches.update(get_extra_dependent_patches(self))

        patches = sorted(patches)
        if patches:
            output += "\n" + "\n".join(patches)

        output += "\n        ],"
        return output

    def get_sorted_dependencies(self):
        def sort_helper(dep):
            if type(dep) == dict:
                print(dep)
                repo_name = dep["repo_name"]
                parent_folder = dep["parent_folder"]
            else:
                repo_name = dep.repo_name
                parent_folder = dep.parent_folder
            return (repo_name, parent_folder)

        output = sorted(self.dependencies, key=sort_helper)
        return output

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
        "windowsarm64": "@rules_bazelrio//conditions:windows_arm",
        "windowsarm64debug": "@rules_bazelrio//conditions:windows_arm_debug",
        "windowsarm64static": "@rules_bazelrio//conditions:windows_arm",
        "windowsarm64staticdebug": "@rules_bazelrio//conditions:windows_arm_debug",
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
        "linuxathena": "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio",
        "linuxathenadebug": "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio_debug",
        "linuxathenastatic": "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio",
        "linuxathenastaticdebug": "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio_debug",
        "linuxarm32": "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32",
        "linuxarm32debug": "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32_debug",
        "linuxarm32static": "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32",
        "linuxarm32staticdebug": "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32_debug",
        "linuxarm64": "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64",
        "linuxarm64debug": "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64_debug",
        "linuxarm64static": "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64",
        "linuxarm64staticdebug": "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64_debug",
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
                print("Unknown resource for select: ", full_res)
            # condition = self.__resource_type_to_condition(res)
            # if condition:
            #     lines.append(f'        "{condition}": ["@{self.get_archive_name(res)}//:shared_libs"]')

        return ",\n".join(sorted(lines)) + ","

    def get_shared_library_interface_select(self):
        shared_resources = []
        for res in self.resources:
            if res.endswith("staticdebug") or res.endswith("static"):
                pass
            elif "windows" in res:
                shared_resources.append(res)

        return self.__get_select(shared_resources, "static_libs")

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
        return len(self.get_incompatible_targets()) != 0

    def __is_invalid_resource(self, resource_base):
        return resource_base not in self.resources

    def __get_invalid_toolchain(
        self, resource_base, toolchain_name, is_custom_toolchain
    ):
        if self.__is_invalid_resource(resource_base):
            if is_custom_toolchain:
                return f"@rules_bzlmodrio_toolchains//constraints/is_{toolchain_name}:{toolchain_name}"
            else:
                return f"@bazel_tools//src/conditions:{toolchain_name}"

    def get_shared_incompatible_targets(self):
        output = []

        output.append(self.__get_invalid_toolchain("linuxathena", "roborio", True))
        output.append(self.__get_invalid_toolchain("linuxarm32", "bullseye32", True))
        output.append(self.__get_invalid_toolchain("linuxarm64", "bullseye64", True))
        output.append(self.__get_invalid_toolchain("raspi32", "raspi32", True))

        output.append(self.__get_invalid_toolchain("windowsx86-64", "windows", False))
        output.append(
            self.__get_invalid_toolchain("linuxx86-64", "linux_x86_64", False)
        )

        if self.__is_invalid_resource("osxx86-64") and self.__is_invalid_resource(
            "osxuniversal"
        ):
            output.append(f"@bazel_tools//src/conditions:darwin")

        return sorted([x for x in output if x is not None])

    def get_static_incompatible_targets(self):
        output = []

        output.append(self.__get_invalid_toolchain("linuxathenastatic", "roborio", True))
        output.append(self.__get_invalid_toolchain("linuxarm32static", "bullseye32", True))
        output.append(self.__get_invalid_toolchain("linuxarm64static", "bullseye64", True))
        output.append(self.__get_invalid_toolchain("raspi32static", "raspi32", True))

        output.append(self.__get_invalid_toolchain("windowsx86-64static", "raspi32", False))
        output.append(self.__get_invalid_toolchain("linuxx86-64static", "linux_x86_64", False))

        if self.__is_invalid_resource("osxx86-64static") and self.__is_invalid_resource("osxuniversalstatic"):
            output.append(f"@bazel_tools//src/conditions:darwin")

        return sorted([x for x in output if x is not None])

    def get_jni_incompatible_targets(self):
        return self.get_shared_incompatible_targets()


class CcMetaDependency:
    def __init__(
        self,
        repo_name,
        name,
        deps,
        platform_deps,
        has_static,
        jni_deps,
        shared_library_name=None,
    ):
        self.repo_name = repo_name
        self.name = name
        self.deps = deps
        self.parent_folder = name
        self.platform_deps = platform_deps
        self.has_static = has_static
        self.jni_deps = jni_deps
        self.shared_library_name = shared_library_name
