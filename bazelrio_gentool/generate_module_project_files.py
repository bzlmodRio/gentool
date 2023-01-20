
import os
from bazelrio_gentool.utils import render_template, write_file, TEMPLATE_BASE_DIR

class MandetoryDependencySetting:
    def __init__(self, version, use_local_version):
        self.version = version
        self.use_local_version = use_local_version

def create_default_mandatory_settings(
    use_local_roborio,
    use_local_bazelrio,
    use_local_bzlmodrio_gentool,
):
    default_rules_roborio_toolchain = MandetoryDependencySetting("2023-7.5", use_local_roborio)
    default_rules_bazelrio = MandetoryDependencySetting("0.0.5", use_local_bazelrio)
    default_rules_bzlmodrio_gentool = MandetoryDependencySetting("0.0.3", use_local_bzlmodrio_gentool)
    
    return MandatoryDependencySettings(bcr_branch="megadiff", 
                 rules_roborio_toolchain=default_rules_roborio_toolchain, 
                 rules_bazelrio=default_rules_bazelrio, 
                 bzlmodrio_gentool=default_rules_bzlmodrio_gentool,
    )



class MandatoryDependencySettings:

    def __init__(self, 
                 rules_roborio_toolchain, 
                 rules_bazelrio, 
                 bzlmodrio_gentool,
                 bcr_branch = "main"):
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
