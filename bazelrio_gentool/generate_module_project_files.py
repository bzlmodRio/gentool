
import os
from bazelrio_gentool.utils import render_template, write_file, TEMPLATE_BASE_DIR

class MandetoryDependencySetting:
    def __init__(self, version, use_local_version):
        self.version = version
        self.use_local_version = use_local_version
        
DEFAULT_RULES_ROBORIO_TOOLCHAIN = MandetoryDependencySetting("2023-7.3", False)
DEFAULT_RULES_BAZELRIO = MandetoryDependencySetting("", True)


class MandetoryDependencySettings:

    def __init__(self, bcr_branch, rules_roborio_toolchain=DEFAULT_RULES_ROBORIO_TOOLCHAIN, rules_bazelrio=DEFAULT_RULES_BAZELRIO):
        self.bcr_branch = bcr_branch
        self.rules_roborio_toolchain = rules_roborio_toolchain
        self.rules_bazelrio = rules_bazelrio


def generate_module_project_files(module_directory, group, mandetory_dependencies):

    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".bazelrc",
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

    if group.executable_tools or group.java_native_tools:
        template_files.extend([
            "dependencies/tools/BUILD",
            "dependencies/tools/executable_launcher.sh",
            "dependencies/tools/tool_launchers.bzl"
        ])

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, group=group, mandetory_dependencies=mandetory_dependencies)

        if output_file.endswith(".sh"):
            os.chmod(output_file, 0o755)


    if group.get_all_maven_dependencies():
        for tf in ["maven_java_deps.bzl"]:
            template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
            output_file = os.path.join(module_directory, tf)
            render_template(template_file, output_file, group=group, mandetory_dependencies=mandetory_dependencies)

            if output_file.endswith(".sh"):
                os.chmod(output_file, 0o755)
