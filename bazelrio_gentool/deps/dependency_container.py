

from bazelrio_gentool.deps.cc_dependency import CcDependency, CcMetaDependency
from bazelrio_gentool.deps.java_dependency import JavaDependency, JavaMetaDependency
from bazelrio_gentool.deps.java_native_tool_dependency import JavaNativeToolDependency
from bazelrio_gentool.deps.executable_tool_dependency import ExecutableToolDependency
from bazelrio_gentool.load_cached_versions import load_cached_version_info


class ModuleDependency:
    def __init__(self, container, use_local_version, local_rel_folder, override_version=None,
                 remote_repo="TODO"):
        self.container = container
        if override_version:
            container.version = override_version
        self.local_rel_folder = local_rel_folder
        self.use_local_version = use_local_version
        
        cached_version = load_cached_version_info(container.repo_name, container.version)
        self.remote_sha = cached_version['sha']
        self.remote_commitish = cached_version['commitish']
        self.remote_repo = remote_repo


class DependencyContainer:

    def __init__(self, repo_name, version, year, maven_url):
        self.repo_name = repo_name
        self.sanitized_repo_name = repo_name.replace("-", "_")
        self.version = version
        self.year = year
        self.maven_url = maven_url
        self.java_deps = []
        self.java_meta_deps = []
        self.cc_deps = []
        self.cc_meta_deps = []
        self.java_native_tools = []
        self.executable_tools = []
        self.module_dependencies = {}
        self.dep_lookup = {}
        self.repository_url = None
        self.strip_prefix = None
        self.fail_on_hash_miss = True
        self.extra_maven_repos = []

    def __repr__(self):
        output = f"DepContainer: {self.repo_name}, {self.version}"
        return output

    def add_module_dependency(self, dependency, meta_deps=None):
        if not isinstance(dependency, ModuleDependency):
            raise
        self.module_dependencies[dependency.container.repo_name] = dependency
        self.dep_lookup.update(dependency.container.dep_lookup)

        for repo_name, subdep in dependency.container.module_dependencies.items():
            self.add_module_dependency(subdep)

        if meta_deps:
            for meta_dep in meta_deps:
                self.dep_lookup[meta_dep] = dict(repo_name=dependency.container.repo_name, parent_folder=meta_dep)

    def create_cc_dependency(self, name, dependencies=[], version=None, **kwargs):
        if version is None:
            version = self.version
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = CcDependency(artifact_name=name, maven_url=self.maven_url, version=version, dependencies=dependencies, repo_name=self.repo_name, **kwargs)

        self.cc_deps.append(dep)
        self.dep_lookup[name] = dep

    def create_java_dependency(self, name, dependencies=[], **kwargs):
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = JavaDependency(name=name, version=self.version, dependencies=dependencies, repo_name=self.repo_name, maven_url=self.maven_url, **kwargs)

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

    def create_executable_tool(self, group_id, artifact_name, resources, lower_target_name=False):
        self.executable_tools.append(
            ExecutableToolDependency(
                group_id=group_id,
                artifact_name=artifact_name,
                resources=resources,
                maven_url=self.maven_url,
                version=self.version,
                repo_name=self.repo_name,
                fail_on_hash_miss=self.fail_on_hash_miss,
                lower_target_name = lower_target_name,
            )
        )

    def has_direct_maven_deps(self):
        for java_dep in self.java_deps:
            if java_dep.maven_deps:
                print("Has maven deps....", java_dep)
                return True
                
        return False

    def has_any_maven_deps(self):
        if self.has_direct_maven_deps():
            return True
                
        for module_dep in self.module_dependencies.values():
            if module_dep.container.has_any_maven_deps():
                return True            

        print("NO MAVEN DEPS", self)
        return False


    def get_all_maven_dependencies2(self):
        all_maven_deps = set()

        for java_dep in self.java_deps:
            #all_maven_deps.add((f"{java_dep.group_id}", f"{java_dep.name}:{java_dep.version}"))
            all_maven_deps.update(java_dep.maven_deps)

        return sorted(list(all_maven_deps))


    def sorted_cc_deps(self):
        output = []
        
        for cpp_dep in self.cc_deps:
            if cpp_dep.headers:
                output.append(f"{cpp_dep.get_archive_name('headers')}")
            if cpp_dep.sources:
                output.append(f"{cpp_dep.get_archive_name('sources')}")

            for resource in cpp_dep.resources:
                if cpp_dep.get_sha256(resource):
                    output.append(f"{cpp_dep.get_archive_name(resource)}")
        
        output = sorted(output)

        return '"' + "\",\n    \"".join(output) + "\","
                

    def add_cc_meta_dependency(self, name, deps, platform_deps, has_static=False, jni_deps=None):

        dependencies = [self.dep_lookup[d] for d in deps]
        pd = {}
        for k, v in platform_deps.items():
            pd[k] = [self.dep_lookup[d] for d in v]
        jnid = {}
        if jni_deps:
            for k, v in jni_deps.items():
                jnid[k] = [self.dep_lookup[d] for d in v]
            # platform_deps = {k, v for self.dep_lookup[d] for d in platform_deps]

        dep = CcMetaDependency(self.repo_name, name, dependencies, pd, has_static, jnid)
        self.cc_meta_deps.append(dep)
        self.dep_lookup[name] = dep

    def add_java_meta_dependency(self, name, deps, group_id):
        dependencies = [self.dep_lookup[d] for d in deps]

        dep = JavaMetaDependency(self.repo_name, name, deps=dependencies, group_id=group_id)
        self.java_meta_deps.append(dep)
        self.dep_lookup[name] = dep
