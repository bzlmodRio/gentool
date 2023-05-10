import os
from bazelrio_gentool.utils import (
    render_templates,
    TEMPLATE_BASE_DIR,
)
from bazelrio_gentool.load_cached_versions import load_cached_version_info
from bazelrio_gentool.generate_shared_files import (
    write_shared_root_files,
    write_shared_test_files,
)
from bazelrio_gentool.cli import GenericCliArgs
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies

from bazelrio_gentool.dependency_helpers import BaseLocalDependencyWriterHelper


class MandetoryDependencySetting(BaseLocalDependencyWriterHelper):
    def __init__(self, repo_name, version, use_local_version):

        cached_version = load_cached_version_info(repo_name, version)
        self.commitish = cached_version["commitish"]

        BaseLocalDependencyWriterHelper.__init__(
            self,
            repo_name=repo_name,
            version=version,
            sha=cached_version["sha"],
            url_base="https://github.com/bzlmodRio",
            use_local_version=use_local_version,
        )

    def __repr__(self):
        return f"MandetoryDependencySetting: {self.repo_name}, {self.version}, {self.use_local_version}"


def create_default_mandatory_settings(generic_cli: GenericCliArgs):
    default_rules_bzlmodrio_toolchain = MandetoryDependencySetting(
        "rules_bzlmodrio_toolchains",
        "2023-7",
        generic_cli.use_local_roborio,
    )
    default_rules_bazelrio = MandetoryDependencySetting(
        "rules_bazelrio",
        "0.0.10",
        generic_cli.use_local_bazelrio,
    )
    default_rules_pmd = MandetoryDependencySetting(
        "rules_pmd",
        "6.43.0",
        generic_cli.use_local_rules_pmd,
    )
    default_rules_checkstyle = MandetoryDependencySetting(
        "rules_checkstyle",
        "10.1",
        generic_cli.use_local_rules_checkstyle,
    )
    default_rules_spotless = MandetoryDependencySetting(
        "rules_spotless",
        "2.34.0",
        generic_cli.use_local_rules_spotless,
    )
    default_rules_wpiformat = MandetoryDependencySetting(
        "rules_wpiformat",
        "2022.30",
        generic_cli.use_local_rules_wpiformat,
    )
    default_rules_wpi_styleguide = MandetoryDependencySetting(
        "rules_wpi_styleguide",
        "1.0.0",
        generic_cli.use_local_rules_wpi_styleguide,
    )

    return MandatoryDependencySettings(
        bcr_branch="megadiff",
        rules_bzlmodrio_toolchain=default_rules_bzlmodrio_toolchain,
        rules_bazelrio=default_rules_bazelrio,
        rules_pmd=default_rules_pmd,
        rules_checkstyle=default_rules_checkstyle,
        rules_spotless=default_rules_spotless,
        rules_wpiformat=default_rules_wpiformat,
        rules_wpi_styleguide=default_rules_wpi_styleguide,
    )


class MandatoryDependencySettings:
    def __init__(
        self,
        rules_bzlmodrio_toolchain,
        rules_bazelrio,
        rules_pmd,
        rules_checkstyle,
        rules_spotless,
        rules_wpiformat,
        rules_wpi_styleguide,
        bcr_branch="main",
    ):
        self.bcr_branch = bcr_branch
        self.rules_bzlmodrio_toolchain = rules_bzlmodrio_toolchain
        self.rules_bazelrio = rules_bazelrio
        self.rules_pmd = rules_pmd
        self.rules_checkstyle = rules_checkstyle
        self.rules_spotless = rules_spotless
        self.rules_wpiformat = rules_wpiformat
        self.rules_wpi_styleguide = rules_wpi_styleguide


def generate_module_project_files(
    module_directory, group, mandatory_dependencies, no_roborio=False, test_macos=True
):
    write_shared_root_files(module_directory, group, test_macos=test_macos)
    write_shared_test_files(module_directory, group)

    template_files = [
        "maven_cpp_deps.bzl",
        "MODULE.bazel",
        "WORKSPACE",
        "private/non_bzlmod_dependencies/BUILD.bazel",
        "private/non_bzlmod_dependencies/download_dependencies.bzl",
        "private/non_bzlmod_dependencies/setup_dependencies.bzl",
        "tests/MODULE.bazel",
        "tests/WORKSPACE",
    ]

    if group.executable_tools or group.java_native_tools:
        template_files.extend(
            [
                "libraries/tools/BUILD",
                "libraries/tools/executable_launcher.sh",
                "libraries/tools/tool_launchers.bzl",
            ]
        )

    render_templates(
        template_files,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "library_wrapper"),
        group=group,
        mandatory_dependencies=mandatory_dependencies,
        bazel_dependencies=get_bazel_dependencies(),
        no_roborio=no_roborio,
    )

    if group.java_deps:
        render_templates(
            ["maven_java_deps.bzl"],
            module_directory,
            os.path.join(TEMPLATE_BASE_DIR, "library_wrapper"),
            group=group,
            mandatory_dependencies=mandatory_dependencies,
            no_roborio=no_roborio,
        )
