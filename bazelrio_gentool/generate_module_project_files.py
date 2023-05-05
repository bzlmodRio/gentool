import os
from bazelrio_gentool.utils import render_template, render_templates, write_file, TEMPLATE_BASE_DIR
from bazelrio_gentool.load_cached_versions import load_cached_version_info
from bazelrio_gentool.generate_shared_files import write_shared_root_files, write_shared_test_files
from bazelrio_gentool.cli import GenericCliArgs
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies




class MandetoryDependencySetting:
    def __init__(self, repo_name, version, use_local_version):
        self.repo_name = repo_name
        self.version = version
        self.use_local_version = use_local_version

        cached_version = load_cached_version_info(repo_name, version)
        self.sha = cached_version["sha"]
        self.commitish = cached_version["commitish"]

    def __repr__(self):
        return f"MandetoryDependencySetting: {self.repo_name}, {self.version}, {self.use_local_version}"

    def maybe_local_repository(self):
        local_path = f"../../../rules/{self.repo_name}"
        if self.use_local_version:
            return f"""
local_repository(
    name = "{self.repo_name}",
    path = "{local_path}",
)"""
        return ""
        
    def local_module_override(self):
        if self.use_local_version:
            return f"""
local_path_override(
    module_name = "{self.repo_name}",
    path = "../../{self.repo_name}",
)"""

        return ""
        
    def download_repository(self, num_indent, native=True, maybe=False):
        indent = " " * num_indent
        native_text = "native." if native else ""
        local_path = f"../../../rules/{self.repo_name}"
        if self.use_local_version:
            output = f"{indent}"
            if maybe:
                output += f"maybe(\n    {indent}{native_text}local_repository,"
            else:
                output += "http_archive("

            output += f"""
{indent}    name = "{self.repo_name}",
{indent}    path = "{local_path}",
{indent})"""
            return output

        output = f"{indent}"
        if maybe:
            output += "maybe(\n    http_archive,"
        else:
            output += "http_archive("
     
        output += f"""
{indent}name = "{self.repo_name}",
{indent}sha256 = "{ self.sha }",
{indent}strip_prefix = "{self.repo_name}-{self.version}",
{indent}url = "https://github.com/bzlmodRio/{self.repo_name}/archive/refs/tags/{self.version}.tar.gz",
    )"""

        return output


def create_default_mandatory_settings(generic_cli: GenericCliArgs):
    default_rules_roborio_toolchain = MandetoryDependencySetting(
        "rules_bzlmodrio_toolchains",
        "2023-7",
        generic_cli.use_local_roborio,
    )
    default_rules_bazelrio = MandetoryDependencySetting(
        "rules_bazelrio",
        "0.0.9",
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
        rules_roborio_toolchain=default_rules_roborio_toolchain,
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
        rules_roborio_toolchain,
        rules_bazelrio,
        rules_pmd,
        rules_checkstyle,
        rules_spotless,
        rules_wpiformat,
        rules_wpi_styleguide,
        bcr_branch="main",
    ):
        self.bcr_branch = bcr_branch
        self.rules_roborio_toolchain = rules_roborio_toolchain
        self.rules_bazelrio = rules_bazelrio
        self.rules_pmd = rules_pmd
        self.rules_checkstyle = rules_checkstyle
        self.rules_spotless = rules_spotless
        self.rules_wpiformat = rules_wpiformat
        self.rules_wpi_styleguide = rules_wpi_styleguide


def generate_module_project_files(
    module_directory, group, mandatory_dependencies, no_roborio=False
):
    write_shared_root_files(module_directory, group)
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

    render_templates(template_files, module_directory, os.path.join(TEMPLATE_BASE_DIR, "library_wrapper"), 
            group=group,
            mandatory_dependencies=mandatory_dependencies,
            bazel_dependencies=get_bazel_dependencies(),
            no_roborio=no_roborio,)

    if group.java_deps:
        render_templates(["maven_java_deps.bzl"], module_directory, os.path.join(TEMPLATE_BASE_DIR, "library_wrapper"), 
                group=group,
                mandatory_dependencies=mandatory_dependencies,
                no_roborio=no_roborio,)
