import os
from bazelrio_gentool.utils import (
    TEMPLATE_BASE_DIR,
    render_templates,
)
from bazelrio_gentool.generate_shared_files import write_shared_root_files
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies
from bazelrio_gentool.deps.dependency_container import DependencyContainer


class StyleguideGroup(DependencyContainer):
    def __init__(
        self,
        short_name,
        is_java=False,
        is_python=False,
        has_protobuf=False,
        include_wpiformat=True,
        **kwargs
    ):
        DependencyContainer.__init__(self, **kwargs)
        self.short_name = short_name
        self.is_java = is_java
        self.is_python = is_python
        self.has_protobuf = has_protobuf
        self.include_wpiformat = include_wpiformat


def generate_styleguide_rule(
    module_directory, group: StyleguideGroup, mandatory_dependencies
):
    write_shared_root_files(module_directory, group)

    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".bazelversion",
        "MODULE.bazel",
        "WORKSPACE",
        "dependencies/BUILD.bazel",
        "dependencies/load_dependencies.bzl",
        "dependencies/load_rule_dependencies.bzl",
    ]

    if group.is_python:
        template_files.append("BUILD.bazel")

    bazel_dependencies = get_bazel_dependencies()

    render_templates(
        template_files,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "styleguide"),
        group=group,
        bazel_dependencies=bazel_dependencies,
        mandatory_dependencies=mandatory_dependencies,
    )
