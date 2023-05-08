import os
from bazelrio_gentool.utils import (
    TEMPLATE_BASE_DIR,
    render_template,
    render_templates,
)
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies
from bazelrio_gentool.generate_shared_files import (
    write_shared_root_files,
    write_shared_test_files,
)


def generate_toolchain(module_directory, container, mandatory_dependencies):
    write_shared_root_files(module_directory, container, include_raspi_compiler=True)
    write_shared_test_files(module_directory, container)

    template_files = [
        "extensions.bzl",
        "maven_deps.bzl",
        ".styleguide",
        "WORKSPACE",
        "toolchains/BUILD.bazel",
        "toolchains/configure_cross_compiler.bzl",
        "toolchains/load_toolchains.bzl",
        "toolchains/cross_compiler/BUILD.bazel",
        "toolchains/cross_compiler/BUILD.tpl",
        "toolchains/cross_compiler/BUILD.bazel",
        "toolchains/cross_compiler/cc-toolchain-config.bzl",
        "toolchains/cross_compiler/command_wrapper.tpl",
        "MODULE.bazel",
        "tests/BUILD.bazel",
        "tests/MODULE.bazel",
        "tests/WORKSPACE",
    ]

    bazel_deps = get_bazel_dependencies()

    render_templates(
        template_files,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "toolchains"),
        group=container,
        bazel_dependencies=bazel_deps,
        mandatory_dependencies=mandatory_dependencies,
    )

    for config in container.configs:
        template_file = os.path.join(
            TEMPLATE_BASE_DIR, "toolchains", "per_toolchain", "constraint_build.jinja2"
        )
        output_file = os.path.join(
            module_directory,
            f"constraints/is_{config.short_name.replace('-', '')}/BUILD.bazel",
        )
        render_template(template_file, output_file, config=config)

        template_file = os.path.join(
            TEMPLATE_BASE_DIR, "toolchains", "per_toolchain", "platforms_build.jinja2"
        )
        output_file = os.path.join(
            module_directory,
            f"platforms/{config.short_name.replace('-', '')}/BUILD.bazel",
        )
        render_template(template_file, output_file, config=config)
