
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template

def write_shared_root_files(module_directory, group):
    template_files = [
        ".bazelignore",
        ".bazelrc-buildbuddy",
        ".bazelversion",
        # ".bazelrc",
        ".gitignore",
        # # ".bazelversion",
        "BUILD.bazel",
        "README.md",
        "WORKSPACE.bzlmod",
        ".styleguide",
        ".styleguide-license",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "shared", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, group=group)
        # render_template(template_file, output_file, group=config)
        
def write_shared_test_files(module_directory, group):
    template_files = [
        # ".bazelignore",
        ".bazelrc-buildbuddy",
        ".bazelversion",
        "WORKSPACE.bzlmod",
        # # ".bazelrc",
        # ".gitignore",
        # # # ".bazelversion",
        # "BUILD.bazel",
        # "README.md",
        # "WORKSPACE.bzlmod",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "shared", tf + ".jinja2")
        output_file = os.path.join(module_directory, "tests", tf)
        render_template(template_file, output_file, group=group)
        # render_template(template_file, output_file, group=config)