from bazelrio_gentool.deps.base_dependency import BaseDependency
from bazelrio_gentool.deps.sha256_helper import get_hash


class MultiResourceDependency(BaseDependency):
    def __init__(self, file_extension, resources, suffix="", **kwargs):
        BaseDependency.__init__(self, **kwargs)
        self.resources = resources
        self.suffix = suffix
        self.file_extension = file_extension

    def get_url(self, resource):
        return self._get_url(self.file_extension, resource)

    def get_sha256(self, resource):
        return get_hash(self.get_url(resource), self.fail_on_hash_miss)
