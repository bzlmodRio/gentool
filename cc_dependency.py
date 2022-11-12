

class CcDependency:
    def __init__(self, name, maven_url, group_id, version, parent_folder, dependencies, resources, headers, has_jni):
        self.name = name
        self.version = version
        self.parent_folder = parent_folder
        self.has_jni = has_jni
        self.resources = resources
        self.headers = headers
        self.dependencies = dependencies
        self.maven_url = maven_url
        self.group_id = group_id

    def get_url(self, resource):
        group_as_folder = self.group_id.replace(".", "/")
        return f"{self.maven_url}/{group_as_folder}/{self.name}/{self.version}/{self.name}-{self.version}-{resource}.zip"

    def __repr__(self):
        return f"CcDependency: name={self.name}"