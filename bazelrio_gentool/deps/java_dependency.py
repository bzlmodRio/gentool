
from bazelrio_gentool.deps.sha256_helper import get_hash
from bazelrio_gentool.deps.cc_dependency import CcDependency, CcMetaDependency

class JavaDependency():
    def __init__(self, name, group_id, version, parent_folder, dependencies, repo_name, maven_url=None, maven_deps=[]):
        self.name = name
        self.version = version
        self.parent_folder = parent_folder
        self.maven_deps = maven_deps
        self.group_id = group_id
        self.dependencies = dependencies
        self.repo_name = repo_name

        if maven_url is None:
            raise

        self.maven_url = maven_url
        self.fail_on_hash_miss = True
        self.group_id_underscore = self.group_id.replace(".", "_").lower()
        self.import_repo_name = (self.group_id_underscore + "_" + self.name).replace(".", "_").replace("-", "_").lower()

    def __repr__(self):
        return f"JavaDependency: name={self.name}"
        
    def _get_url(self, file_extension, suffix):
        group_as_folder = self.group_id.replace(".", "/")
        url = f"{self.maven_url}/{group_as_folder}/{self.name}/{self.version}/{self.name}-{self.version}"
        if suffix:
            url += f"-{suffix}"
        url += f"{file_extension}"

        return url
        
    def get_url(self):
        return self._get_url(file_extension=".jar", suffix="")

    def get_sha256(self):
        return get_hash(self.get_url(), self.fail_on_hash_miss)

    def sorted_dependencies(self):
        output = []

        for dep in self.dependencies:
            if getattr(dep, "has_jni", False):
                output.append(f"@{dep.repo_name}//libraries/cpp/{dep.parent_folder}:jni")
            elif "java" in dep.name:
                output.append(f"@{dep.repo_name}//libraries/java/{dep.parent_folder}",)
            else:
                raise Exception(dep)

        return sorted(output)

class JavaMetaDependency:
    def __init__(self, repo_name, name, group_id, deps):
        self.repo_name = repo_name
        self.name = name
        self.deps = deps
        self.parent_folder = name
        self.group_id = group_id
        
        self.group_id_underscore = self.group_id.replace(".", "_").lower()
        self.import_repo_name = (self.group_id_underscore + "_" + self.name).replace(".", "_").replace("-", "_").lower()
        # self.platform_deps = platform_deps
        # self.has_static = has_static
        # self.jni_deps = jni_deps

    def sorted_dependencies(self):
        output = []

        for dep in self.deps:
            if getattr(dep, "has_jni", False) or isinstance(dep, CcMetaDependency):
                output.append(f"@{dep.repo_name}//libraries/cpp/{dep.parent_folder}:jni")
            elif "java" in dep.name:
                output.append(f"@{dep.repo_name}//libraries/java/{dep.parent_folder}",)
            else:
                raise Exception(dep)

        return output
