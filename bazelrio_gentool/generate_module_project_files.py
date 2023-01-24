import os
from bazelrio_gentool.utils import render_template, write_file, TEMPLATE_BASE_DIR


class MandetoryDependencySetting:
    def __init__(self, version, use_local_version, sha, commitish):
        self.version = version
        self.use_local_version = use_local_version
        self.sha = sha
        self.commitish = commitish


def create_default_mandatory_settings(
    use_local_roborio,
    use_local_bazelrio,
    use_local_bzlmodrio_gentool,
):
    default_rules_roborio_toolchain = MandetoryDependencySetting(
        "2023-7.6",
        use_local_roborio,
        sha="c8a6fc0acac4a08aa884b59d13af9c3da010a4eed416ee10ccc05c73b9753deb",
        commitish="8668e36043c7489a9669a9281f7024272b36d583",
    )
    default_rules_bazelrio = MandetoryDependencySetting(
        "0.0.7",
        use_local_bazelrio,
        sha="a8e997def42472dd2f31cd90b855c0aeab93aabe1b436cd48f4e1efdd760f01c",
        commitish="bd9c8375bf4f5a91d08cbf64e359c0b30aaf7433",
    )
    default_rules_bzlmodrio_gentool = MandetoryDependencySetting(
        "0.0.3",
        use_local_bzlmodrio_gentool,
        sha="91dbeb541a6151eab3f4dfa37318b81e3f4fa964e45ebea48665cb2b3e471353",
        commitish="dummy_version",
    )

    return MandatoryDependencySettings(
        bcr_branch="megadiff",
        rules_roborio_toolchain=default_rules_roborio_toolchain,
        rules_bazelrio=default_rules_bazelrio,
        bzlmodrio_gentool=default_rules_bzlmodrio_gentool,
    )


class MandatoryDependencySettings:
    def __init__(
        self,
        rules_roborio_toolchain,
        rules_bazelrio,
        bzlmodrio_gentool,
        bcr_branch="main",
    ):
        self.bcr_branch = bcr_branch
        self.rules_roborio_toolchain = rules_roborio_toolchain
        self.rules_bazelrio = rules_bazelrio
        self.bzlmodrio_gentool = bzlmodrio_gentool


def generate_module_project_files(module_directory, group, mandetory_dependencies):

    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".bazelrc",
        ".bazelignore",
        ".gitignore",
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
        )

        if output_file.endswith(".sh"):
            os.chmod(output_file, 0o755)

    if group.java_deps:
        for tf in ["maven_java_deps.bzl"]:
            template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
            output_file = os.path.join(module_directory, tf)
            render_template(
                template_file,
                output_file,
                group=group,
                mandetory_dependencies=mandetory_dependencies,
            )

            if output_file.endswith(".sh"):
                os.chmod(output_file, 0o755)
