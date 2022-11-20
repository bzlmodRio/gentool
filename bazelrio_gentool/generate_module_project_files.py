
import os
from bazelrio_gentool.utils import render_template, write_file, TEMPLATE_BASE_DIR

def generate_module_project_files(module_directory, group):

    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".gitignore",
        "BUILD.bazel",
        "README.md",
        "maven_cpp_deps.bzl",
        "MODULE.bazel",
        "WORKSPACE.bzlmod",
        "WORKSPACE",
        "tests/.bazelrc",
        "tests/.bazelversion",
        "tests/MODULE.bazel",
        "tests/WORKSPACE.bzlmod",
        "tests/WORKSPACE",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, group=group)
