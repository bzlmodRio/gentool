
from bazelrio_gentool.deps.multi_resource_dependency import MultiResourceDependency

class JavaNativeToolDependency(MultiResourceDependency):
    def __init__(self, **kwargs):
        MultiResourceDependency.__init__(self, file_extension = ".jar", **kwargs)
        self.fail_on_hash_miss = True
