
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