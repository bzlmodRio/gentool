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


def generate_toolchain(
    module_directory,
    container,
    mandatory_dependencies,
    include_linuxarm32_compiler=True,
    include_linuxarm64_compiler=True,
    include_systemcore_compiler=True,
):
    if not include_linuxarm32_compiler:
        raise
    if not include_linuxarm64_compiler:
        raise
    if not include_systemcore_compiler:
        raise

    write_shared_root_files(
        module_directory,
        container,
        include_linuxarm32_compiler=include_linuxarm32_compiler,
        include_linuxarm64_compiler=include_linuxarm64_compiler,
        include_systemcore_compiler=include_systemcore_compiler,
    )
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
        print(config)
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

    for extra_platform, cpu in [
        ("linux_x86_64", "x86_64"),
        ("osx", "x86-64"),
        ("windows_arm64", "x86_64"),
        ("windows_x86_64", "x86_64"),
    ]:
        template_file = os.path.join(
            TEMPLATE_BASE_DIR, "toolchains", "per_toolchain", "platforms_build.jinja2"
        )
        output_file = os.path.join(
            module_directory,
            f"platforms/{extra_platform}/BUILD.bazel",
        )
        print(output_file)
        render_template(
            template_file,
            output_file,
            config=dict(
                short_name_no_dash=extra_platform,
                constraint_cpu=cpu,
            ),
            no_constraint=True,
        )
