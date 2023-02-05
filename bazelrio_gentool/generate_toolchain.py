
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template

def generate_toolchain(module_directory, container):

    
    template_files = [
        "extensions.bzl",
        "maven_deps.bzl",
        "WORKSPACE",
        "toolchains/BUILD",
        "toolchains/configure_cross_compiler.bzl",
        "toolchains/load_toolchains.bzl",
        "toolchains/cross_compiler/BUILD",
        "toolchains/cross_compiler/BUILD.tpl",
        "toolchains/cross_compiler/BUILD",
        "toolchains/cross_compiler/cc-toolchain-config.bzl",
        "toolchains/cross_compiler/command_wrapper.tpl",
        
        "MODULE.bazel",
        "tests/BUILD.bazel",
        "tests/MODULE.bazel",
        "tests/WORKSPACE",
        "tests/WORKSPACE.bzlmod",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "toolchains", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, container=container)

    # template_files = [
    #     "constraints/is_roborio/BUILD",
    #     "platforms/roborio/BUILD",
    # ]

    for config in container.configs:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "toolchains", "per_toolchain", "constraint_build.jinja2")
        output_file = os.path.join(module_directory, f"constraints/is_{config.short_name.replace('-', '')}/BUILD.bazel")
        render_template(template_file, output_file, config=config)
        
        template_file = os.path.join(TEMPLATE_BASE_DIR, "toolchains", "per_toolchain", "platforms_build.jinja2")
        output_file = os.path.join(module_directory, f"platforms/{config.short_name.replace('-', '')}/BUILD.bazel")
        render_template(template_file, output_file, config=config)

    # for tf in template_files:
    #     template_file = os.path.join(TEMPLATE_BASE_DIR, "toolchains", tf + ".jinja2")
    #     output_file = os.path.join(module_directory, tf)
    #     # render_template(template_file, output_file, configs=configs)
        
    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".bazelrc-buildbuddy",
        ".bazelignore",
        ".bazelrc",
        ".gitignore",
        "BUILD.bazel",
        "README.md",
        "WORKSPACE.bzlmod",
        "tests/.bazelrc",
        "tests/.bazelrc-buildbuddy",
        "tests/.bazelversion",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, group=container)
        # render_template(template_file, output_file, group=config)
