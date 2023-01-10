

from bazelrio_gentool.deps.cc_dependency import CcDependency
from bazelrio_gentool.deps.java_dependency import JavaDependency
from bazelrio_gentool.deps.java_native_tool_dependency import JavaNativeToolDependency
from bazelrio_gentool.deps.executable_tool_dependency import ExecutableToolDependency


class ModuleDependency:
    def __init__(self, container, use_local_version, local_rel_folder, override_version=None):
        self.container = container
        if override_version:
            container.version = override_version
        self.local_rel_folder = local_rel_folder
        self.use_local_version = use_local_version


class DependencyContainer:

    def __init__(self, repo_name, version, year, maven_url):
        self.repo_name = repo_name
        self.sanitized_repo_name = repo_name.replace("-", "_")
        self.version = version
        self.year = year
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

    def add_module_dependency(self, dependency):
        if not isinstance(dependency, ModuleDependency):
            raise
        self.module_dependencies[dependency.container.repo_name] = dependency
        self.dep_lookup.update(dependency.container.dep_lookup)

    def create_cc_dependency(self, name, dependencies=[], version=None, **kwargs):
        if version is None:
            version = self.version
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = CcDependency(artifact_name=name, maven_url=self.maven_url, version=version, dependencies=dependencies, repo_name=self.repo_name, **kwargs)

        self.cc_deps.append(dep)
        self.dep_lookup[name] = dep

    def create_java_dependency(self, name, dependencies=[], **kwargs):
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = JavaDependency(name=name, version=self.version, dependencies=dependencies, repo_name=self.repo_name, **kwargs)

        self.java_deps.append(dep)
        self.dep_lookup[name] = dep
        
    def create_java_native_tool(self, main_class, group_id, artifact_name, resources):
        self.java_native_tools.append(
            JavaNativeToolDependency(
                main_class=main_class,
                group_id=group_id,
                artifact_name=artifact_name,
                resources=resources,
                maven_url=self.maven_url,
                version=self.version,
                repo_name=self.repo_name,
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
                repo_name=self.repo_name,
                fail_on_hash_miss=self.fail_on_hash_miss,
            )
        )

    def get_all_maven_dependencies(self):
        all_maven_deps = set()

        for java_dep in self.java_deps:
            all_maven_deps.add((f"{java_dep.group_id}", f"{java_dep.name}:{java_dep.version}"))
            all_maven_deps.update(java_dep.maven_deps)

        return sorted(list(all_maven_deps))
