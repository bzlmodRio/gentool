import os
from bazelrio_gentool.utils import (
    TEMPLATE_BASE_DIR,
    render_templates,
)
from bazelrio_gentool.dependency_helpers import BaseDependencyWriterHelper


def write_shared_root_files(
    module_directory,
    group,
    include_raspi_compiler=False,
    test_macos=True,
    include_windows_arm_compiler=True,
):
    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".github/workflows/publish.yml",
        # "generate/WORKSPACE",
        ".bazelignore",
        ".bazelrc-buildbuddy",
        ".bazelversion",
        ".bazelrc",
        ".bazelrc-cc",
        ".bazelrc-java",
        ".gitignore",
        "BUILD.bazel",
        "README.md",
        "WORKSPACE.bzlmod",
        ".styleguide",
        ".styleguide-license",
    ]

    if os.path.exists(os.path.join(module_directory, "generate", "auto_update.py")):
        template_files.append(".github/workflows/auto_update.yml")

    render_templates(
        template_files,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "shared"),
        group=group,
        include_raspi_compiler=include_raspi_compiler,
        include_windows_arm_compiler=include_windows_arm_compiler,
        test_macos=test_macos,
    )


def write_shared_test_files(module_directory, group):
    template_files = [
        ".bazelrc-buildbuddy",
        ".bazelversion",
        ".bazelrc",
        ".bazelrc-cc",
        ".bazelrc-java",
        "WORKSPACE.bzlmod",
    ]

    render_templates(
        template_files,
        os.path.join(module_directory, "tests"),
        os.path.join(TEMPLATE_BASE_DIR, "shared"),
        group=group,
    )


def write_shared_generator_files(module_directory, group, dependencies):
    template_files = [
        ".bazelversion",
        "WORKSPACE.bzlmod",
    ]

    render_templates(
        template_files,
        os.path.join(module_directory, "generate"),
        os.path.join(TEMPLATE_BASE_DIR, "shared"),
        group=group,
    )

    template_files = [
        "WORKSPACE",
        "MODULE.bazel",
    ]

    # dependencies = []

    # if group.repo_name in ["bzlmodrio-allwpilib", "bzlmodrio-phoenix", "bzlmodrio-phoenix6", "bzlmodrio-navx", "bzlmodrio-revlib", "bzlmodrio-photonlib", "bzlmodrio-pathplannerlib"]:
    #     dependencies.append("bzlmodrio-opencv")
    #     dependencies.append("bzlmodrio-ni")

    # if group.repo_name in ["bzlmodrio-phoenix"]:
    #     dependencies = ["bzlmodrio-allwpilib", "bzlmodrio-phoenix6"] + dependencies

    # if group.repo_name in ["bzlmodrio-navx", "bzlmodrio-revlib", "bzlmodrio-phoenix6", "bzlmodrio-photonlib", "bzlmodrio-pathplannerlib"]:
    #     dependencies = ["bzlmodrio-allwpilib"] + dependencies

    render_templates(
        template_files,
        os.path.join(module_directory, "generate"),
        os.path.join(TEMPLATE_BASE_DIR, "generator"),
        group=group,
        bazel_dependencies=get_bazel_dependencies(),
        dependencies=dependencies,
    )


class BazelDependencySetting(BaseDependencyWriterHelper):
    def __init__(
        self,
        repo_name,
        version,
        sha,
        needs_stripped_prefix=False,
        old_release_style=False,
    ):
        BaseDependencyWriterHelper.__init__(
            self,
            repo_name,
            version,
            sha,
            "https://github.com/bazelbuild",
            old_release_style=old_release_style,
            needs_stripped_prefix=needs_stripped_prefix,
        )

    def download_repository(self, indent_num, maybe=True):
        if self.repo_name == "googletest":
            return f"""http_archive(
    name = "googletest",
    sha256 = "{self.sha}",
    strip_prefix = "googletest-{self.version}",
    urls = ["https://github.com/google/googletest/archive/refs/tags/v{self.version}.tar.gz"],
)"""
        #         if self.use_long_form:
        #             return self.temp_longform_http_archive(indent_num, maybe)
        return self.http_archive(indent_num=indent_num, maybe=maybe, native=False)


#     def temp_longform_http_archive(self, indent_num, maybe):
#         indent = " " * indent_num
#         file_extension = "zip" if self.use_zip else "tar.gz"
#         output = f"""{indent}{self.repo_name.upper()}_COMMITISH = "{self.version}"
#     {self.repo_name.upper()}_SHA = "{self.sha}"
#     """

#         if maybe:
#             output += f"maybe(\n    http_archive,"
#         else:
#             output += f"http_archive("

#         output += f"""
# {indent}    name = "{self.repo_name}",
# {indent}    sha256 = {self.repo_name.upper()}_SHA,
# {indent}    strip_prefix = "{self.repo_name}-{{}}".format({self.repo_name.upper()}_COMMITISH),
# {indent}    url = "https://github.com/bazelbuild/{self.repo_name}/archive/{{}}.{file_extension}".format({self.repo_name.upper()}_COMMITISH),
# )"""
#         return output


def get_bazel_dependencies():
    def add_dep(repo_name, sha="", **kwargs):
        output[repo_name] = BazelDependencySetting(repo_name, sha=sha, **kwargs)

    output = {}

    add_dep(repo_name="platforms", version="0.0.7", sha="")
    add_dep(
        repo_name="rules_python",
        version="0.24.0",
        sha="0a8003b044294d7840ac7d9d73eef05d6ceb682d7516781a4ec62eeb34702578",
        needs_stripped_prefix=True,
    )
    add_dep(
        repo_name="rules_java",
        version="6.4.0",
        sha="27abf8d2b26f4572ba4112ae8eb4439513615018e03a299f85a8460f6992f6a3",
        # use_long_form=True,
    )
    add_dep(
        repo_name="rules_jvm_external",
        version="5.3",
        sha="d31e369b854322ca5098ea12c69d7175ded971435e55c18dd9dd5f29cc5249ac",
        needs_stripped_prefix=True,
        # use_zip=True,
        # use_long_form=True,
    )
    add_dep(repo_name="rules_cc", version="0.0.9", sha="")
    add_dep(
        repo_name="googletest",
        version="1.14.0",
        sha="8ad598c73ad796e0d8280b082cebd82a630d73e73cd3c70057938a6501bba5d7",
    )
    add_dep(
        repo_name="rules_proto",
        version="5.3.0-21.7",
        sha="dc3fb206a2cb3441b485eb1e423165b231235a1ea9b031b4433cf7bc1fa460dd",
        old_release_style=True,
        needs_stripped_prefix=True,
    )
    add_dep(
        repo_name="bazel_skylib",
        version="1.4.2",
        sha="66ffd9315665bfaafc96b52278f57c7e2dd09f5ede279ea6d39b2be471e7e3aa",
    )

    return output
