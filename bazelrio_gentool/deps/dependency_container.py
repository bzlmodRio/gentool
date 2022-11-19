

from bazelrio_gentool.deps.cc_dependency import CcDependency
from bazelrio_gentool.deps.java_dependency import JavaDependency

class DependencyContainer:

    def __init__(self, repo_name, version, maven_url):
        self.repo_name = repo_name
        self.version = version
        self.maven_url = maven_url
        self.java_deps = []
        self.cc_deps = []
        self.dep_lookup = {}
        self.repository_url = None
        self.strip_prefix = None

    def create_cc_dependency(self, name, dependencies=[], version=None, **kwargs):
        if version is None:
            version = self.version
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = CcDependency(artifact_name=name, maven_url=self.maven_url, version=self.version, dependencies=dependencies, **kwargs)

        self.cc_deps.append(dep)
        self.dep_lookup[name] = dep

    def create_java_dependency(self, name, dependencies=[], **kwargs):
        dependencies = [self.dep_lookup[d] for d in dependencies]
        dep = JavaDependency(name=name, version=self.version, dependencies=dependencies, **kwargs)

        self.java_deps.append(dep)
        self.dep_lookup[name] = dep
