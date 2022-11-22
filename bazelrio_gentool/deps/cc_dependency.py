
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
        # self.name = name
        # self.version = version
        self.name = artifact_name
        self.parent_folder = parent_folder
        self.has_jni = has_jni
        # self.resources = resources
        self.headers = headers
        self.dependencies = dependencies
        # self.maven_url = maven_url
        # self.group_id = group_id

    def get_header_archive_name(self):
        return self.get_archive_name("headers")

    # def get_url(self, resource):
    #     group_as_folder = self.group_id.replace(".", "/")
    #     return f"{self.maven_url}/{group_as_folder}/{self.name}/{self.version}/{self.name}-{self.version}-{resource}.zip"

    def __repr__(self):
        return f"CcDependency: name={self.name}"

    # def get_sha256(self, resource):
    #     return None
    #     return _get_hash(self.get_url(resource), self.fail_on_hash_miss)

    # def get_archive_name(self, suffix=""):
    #     group_underscore = self.group_id.replace(".", "_").lower()

    #     # Having a year in the bazel name makes things tricky downstream. Remove it.
    #     year_search = re.findall("20[0-9]{2}", group_underscore)
    #     if year_search:
    #         group_underscore = group_underscore.replace(year_search[0], "")

    #     archive_name = f"__bazelrio_{group_underscore}_{self.name.lower()}"
    #     if suffix:
    #         archive_name += f"_{suffix}"

    #     return archive_name

    def get_build_file_content(self, resource):
        if resource == "headers":
            return "cc_library_headers"
        elif resource == "sources":
            return "cc_library_sources"
        elif "static" not in resource:
            return "cc_library_shared"
        else:
            return "cc_library_static"