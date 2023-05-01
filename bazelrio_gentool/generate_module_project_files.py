import os
from bazelrio_gentool.utils import render_template, write_file, TEMPLATE_BASE_DIR
from bazelrio_gentool.load_cached_versions import load_cached_version_info
from bazelrio_gentool.cli import GenericCliArgs


class BazelDependencySetting:
    def __init__(self, repo_name, version, sha, url):
        self.repo_name = repo_name
        self.version = version
        self.sha = sha
        self.url = url

        
def get_bazel_dependencies():

    def add_dep(repo_name, *kwargs):
        output[repo_name] = BazelDependencySetting(repo_name, *kwargs)

    output = {}

    add_dep("platforms", "0.0.6", "", "")
    add_dep("rules_java", "5.4.0", "", "")
    add_dep("rules_jvm_external", "4.5", "b17d7388feb9bfa7f2fa09031b32707df529f26c91ab9e5d909eb1676badd9a6", "")
    add_dep("rules_cc", "0.0.4", "", "")
    add_dep("googletest", "1.12.1", "24564e3b712d3eb30ac9a85d92f7d720f60cc0173730ac166f27dda7fed76cb2", "")
    
    return output




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
        "6.39.0",
        generic_cli.use_local_rules_pmd,
    )
    default_rules_checkstyle = MandetoryDependencySetting(
        "rules_checkstyle",
        "10.1",
        generic_cli.use_local_rules_checkstyle,
    )
    default_rules_spotless = MandetoryDependencySetting(
        "rules_spotless",
        "2022.30",
        generic_cli.use_local_rules_spotless,
    )
    default_rules_wpiformat = MandetoryDependencySetting(
        "rules_wpiformat",
        "2022.30",
        generic_cli.use_local_rules_wpiformat,
    )
    default_rules_wpi_styleguide = MandetoryDependencySetting(
        "rules_wpi_styleguide",
        "2022.30",
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
    module_directory, group, mandetory_dependencies, no_roborio=False
):

    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".bazelrc",
        ".bazelrc-buildbuddy",
        ".bazelignore",
        ".gitignore",
        ".styleguide",
        ".styleguide-license",
        "BUILD.bazel",
        "README.md",
        "maven_cpp_deps.bzl",
        "MODULE.bazel",
        "WORKSPACE.bzlmod",
        "WORKSPACE",
        "private/non_bzlmod_dependencies/BUILD.bazel",
        "private/non_bzlmod_dependencies/download_dependencies.bzl",
        "private/non_bzlmod_dependencies/setup_dependencies.bzl",
        "tests/.bazelrc",
        "tests/.bazelrc-buildbuddy",
        "tests/.bazelversion",
        "tests/MODULE.bazel",
        "tests/WORKSPACE.bzlmod",
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

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(
            template_file,
            output_file,
            group=group,
            mandetory_dependencies=mandetory_dependencies,
            bazel_dependencies=get_bazel_dependencies(),
            no_roborio=no_roborio,
        )

        if output_file.endswith(".sh"):
            os.chmod(output_file, 0o755)

    if group.java_deps:
        for tf in [
            "maven_java_deps.bzl",
        ]:
            template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
            output_file = os.path.join(module_directory, tf)
            render_template(
                template_file,
                output_file,
                group=group,
                mandetory_dependencies=mandetory_dependencies,
                no_roborio=no_roborio,
            )

            if output_file.endswith(".sh"):
                os.chmod(output_file, 0o755)
