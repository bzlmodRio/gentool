

from bazelrio_gentool.deps.cc_dependency import CcDependency
from bazelrio_gentool.deps.java_dependency import JavaDependency
from bazelrio_gentool.deps.java_native_tool_dependency import JavaNativeToolDependency
from bazelrio_gentool.deps.executable_tool_dependency import ExecutableToolDependency

class DependencyContainer:

    def __init__(self, repo_name, version, maven_url):
        self.repo_name = repo_name
        self.version = version
        self.maven_url = maven_url
        self.java_deps = []
        self.cc_deps = []
        self.java_native_tools = []
        self.executable_tools = []
        self.module_dependencies = {}
        self.dep_lookup = {}
        self.repository_url = None
        self.strip_prefix = None
        self.fail_on_hash_miss = True

    def add_module_dependency(self, name, group):
        self.module_dependencies[name] = group
        self.dep_lookup.update(group.dep_lookup)

    def create_cc_dependency(self, name, dependencies=[], version=None, **kwargs):
        if version is None:
            version = self.version
        # print("XXX", name, version)
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = CcDependency(artifact_name=name, maven_url=self.maven_url, version=version, dependencies=dependencies, **kwargs)

        self.cc_deps.append(dep)
        self.dep_lookup[name] = dep

    def create_java_dependency(self, name, dependencies=[], **kwargs):
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = JavaDependency(name=name, version=self.version, dependencies=dependencies, **kwargs)

        self.java_deps.append(dep)
        self.dep_lookup[name] = dep
        
    def create_java_native_tool(self, group_id, artifact_name, resources):
        self.java_native_tools.append(
            JavaNativeToolDependency(
                group_id=group_id,
                artifact_name=artifact_name,
                resources=resources,
                maven_url=self.maven_url,
                version=self.version,
                fail_on_hash_miss=self.fail_on_hash_miss,
            )
        )

    def create_executable_tool(self, group_id, artifact_name, resources):
        self.executable_tools.append(
            ExecutableToolDependency(
                group_id=group_id,
                artifact_name=artifact_name,
                resources=resources,
                maven_url=self.maven_url,
                version=self.version,
                fail_on_hash_miss=self.fail_on_hash_miss,
            )
        )

    def get_all_maven_dependencies(self):
        all_maven_deps = set()

        for java_dep in self.java_deps:
            all_maven_deps.add((f"{java_dep.group_id}", f"{java_dep.name}:{java_dep.version}"))
            all_maven_deps.update(java_dep.maven_deps)

        return sorted(list(all_maven_deps))
