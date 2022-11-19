

class JavaDependency:
    def __init__(self, name, group_id, version, parent_folder, dependencies, maven_deps=[]):
        self.name = name
        self.version = version
        self.parent_folder = parent_folder
        self.maven_deps = maven_deps
        self.group_id = group_id
        self.dependencies = dependencies

    def __repr__(self):
        return f"JavaDependency: name={self.name}"