
import re
from bazelrio_gentool.deps.multi_resource_dependency import MultiResourceDependency

class CcDependency(MultiResourceDependency):
    def __init__(self, artifact_name, maven_url, group_id, version, parent_folder, dependencies, resources, headers, has_jni, repo_name, fail_on_hash_miss=True):
        MultiResourceDependency.__init__(self, 
                                         artifact_name=artifact_name, 
                                         group_id=group_id,
                                         maven_url=maven_url,
                                         version=version,
                                         file_extension=".zip",
                                         resources=resources,
                                         repo_name=repo_name,
                                         fail_on_hash_miss=fail_on_hash_miss)
        self.name = artifact_name
        self.parent_folder = parent_folder
        self.has_jni = has_jni
        self.headers = headers
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

    def get_shared_library_select(self):
        lines = []
        for res in self.resources:
            if res == "windowsx86-64":
                lines.append(f'        "@bazel_tools//src/conditions:windows": ["@{self.get_archive_name(res)}//:shared_libs"]')
            elif res == "linuxx86-64":
                lines.append(f'        "@bazel_tools//src/conditions:linux_x86_64": ["@{self.get_archive_name(res)}//:shared_libs"]')
            elif res == "osxx86-64":
                lines.append(f'        "@bazel_tools//src/conditions:darwin": ["@{self.get_archive_name(res)}//:shared_libs"]')
            elif res == "linuxathena":
                lines.append(f'        "@rules_roborio_toolchain//constraints/is_roborio:roborio": ["@{self.get_archive_name(res)}//:shared_libs"]')
            # else:
            #     print(res)

        return ",\n".join(lines)

    def has_incompatible_targets(self):
        if "linuxathena" not in self.resources:
            return True