
from bazelrio_gentool.deps.sha256_helper import get_hash

class BundledExecutableToolsDependency:
    def __init__(self, url_base, tool_name, children_tools, fail_on_hash_miss, version, resources):
        self.url_base = url_base
        self.resources = resources
        self.tool_name = tool_name
        self.version = version
        self.children_tools = children_tools
        self.fail_on_hash_miss = fail_on_hash_miss

    def get_archive_name(self, suffix=""):
        group_underscore = self.tool_name.replace(".", "_").lower()
        archive_name = f"bazelrio_{group_underscore}"
        if suffix:
            archive_name += f"_{suffix.lower()}"

        return archive_name

    def get_url(self, resource):
        return f"{self.url_base}/v{self.version}/{self.tool_name}-v{self.version}-{resource}.zip"

    def get_sha256(self, resource):
        return get_hash(self.get_url(resource), self.fail_on_hash_miss)
