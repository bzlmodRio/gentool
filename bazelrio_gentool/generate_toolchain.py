
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template

def generate_toolchain(module_directory, config):

    
    template_files = [
        "extensions.bzl",
        "maven_deps.bzl",
        "constraints/is_roborio/BUILD",
        "platforms/roborio/BUILD",
        "toolchains/BUILD",
        "toolchains/configure_cross_compiler.bzl",
        "toolchains/load_toolchains.bzl",
        "toolchains/cross_compiler/BUILD",
        "toolchains/cross_compiler/BUILD.tpl",
        "toolchains/cross_compiler/BUILD",
        "toolchains/cross_compiler/cc-toolchain-config.bzl",
        "toolchains/cross_compiler/command_wrapper.tpl",
        "toolchains/cross_compiler/toolchain.tpl",
        
        "MODULE.bazel",
        "tests/BUILD.bazel",
        "tests/MODULE.bazel",
        "tests/WORKSPACE",
        "tests/WORKSPACE.bzlmod",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "toolchains", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, config=config)
        
    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".bazelrc",
        ".gitignore",
        "BUILD.bazel",
        "README.md",
        "WORKSPACE.bzlmod",
        # "WORKSPACE",
        "tests/.bazelrc",
        "tests/.bazelversion",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, config=config)
