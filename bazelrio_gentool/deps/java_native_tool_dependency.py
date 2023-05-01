from bazelrio_gentool.deps.multi_resource_dependency import MultiResourceDependency


class JavaNativeToolDependency(MultiResourceDependency):
    def __init__(self, main_class, **kwargs):
        MultiResourceDependency.__init__(self, file_extension=".jar", **kwargs)
        self.fail_on_hash_miss = True
        self.main_class = main_class
