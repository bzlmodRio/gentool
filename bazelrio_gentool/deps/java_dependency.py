

class JavaDependency:
    def __init__(self, name, group_id, version, parent_folder, dependencies, repo_name, maven_deps=[]):
        self.name = name
        self.version = version
        self.parent_folder = parent_folder
        self.maven_deps = maven_deps
        self.group_id = group_id
        self.dependencies = dependencies
        self.repo_name = repo_name

    def __repr__(self):
        return f"JavaDependency: name={self.name}"

    def sorted_dependencies(self):
        output = []

        for dep in self.dependencies:
            if getattr(dep, "has_jni", False):
                output.append(f"@{dep.repo_name}//dependencies/cpp/{dep.parent_folder}:jni")
            elif "java" in dep.name:
                output.append(f"@{dep.repo_name}//dependencies/java/{dep.parent_folder}",)
            else:
                raise Exception(dep)

        # print(output)

        return sorted(output)
