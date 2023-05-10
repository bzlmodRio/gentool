import os
from bazelrio_gentool.utils import (
    TEMPLATE_BASE_DIR,
    render_templates,
)
from bazelrio_gentool.dependency_helpers import BaseDependencyWriterHelper


def write_shared_root_files(
    module_directory, group, include_raspi_compiler=False, test_macos=True
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
        test_macos=test_macos,
    )


def write_shared_test_files(module_directory, group):
    template_files = [
        ".bazelrc-buildbuddy",
        ".bazelversion",
        ".bazelrc",
        "WORKSPACE.bzlmod",
    ]

    render_templates(
        template_files,
        os.path.join(module_directory, "tests"),
        os.path.join(TEMPLATE_BASE_DIR, "shared"),
        group=group,
    )


class BazelDependencySetting(BaseDependencyWriterHelper):
    def __init__(self, repo_name, version, sha, needs_stripped_prefix=False):
        BaseDependencyWriterHelper.__init__(
            self, repo_name, version, sha, "https://github.com/bazelbuild", needs_stripped_prefix=needs_stripped_prefix
        )

    def download_repository(self, indent_num, maybe=True):
#         if self.repo_name == "googletest":
#             return """http_archive(
#     name = "googletest",
#     sha256 = "24564e3b712d3eb30ac9a85d92f7d720f60cc0173730ac166f27dda7fed76cb2",
#     strip_prefix = "googletest-release-1.12.1",
#     urls = ["https://github.com/google/googletest/archive/release-1.12.1.zip"],
# )"""
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
    def add_dep(repo_name, **kwargs):
        output[repo_name] = BazelDependencySetting(repo_name, **kwargs)

    output = {}

    add_dep(repo_name="platforms", version="0.0.6", sha="")
    add_dep(
        repo_name="rules_python",
        version="0.21.0",
        sha="94750828b18044533e98a129003b6a68001204038dc4749f40b195b24c38f49f",
        needs_stripped_prefix=True,
    )
    add_dep(
        repo_name="rules_java",
        version="5.5.0",
        sha="",  # "f90111a597b2aa77b7104dbdc685fd35ea0cca3b7c3f807153765e22319cbd88",
        # use_long_form=True,
    )
    add_dep(
        repo_name="rules_jvm_external",
        version="5.2",
        sha="3824ac95d9edf8465c7a42b7fcb88a5c6b85d2bac0e98b941ba13f235216f313",
        # use_zip=True,
        # use_long_form=True,
    )
    add_dep(repo_name="rules_cc", version="0.0.6", sha="")
    add_dep(
        repo_name="googletest",
        version="1.12.1",
        sha="24564e3b712d3eb30ac9a85d92f7d720f60cc0173730ac166f27dda7fed76cb2",
    )
    add_dep(
        repo_name="rules_proto",
        version="5.3.0-21.7",
        sha="dc3fb206a2cb3441b485eb1e423165b231235a1ea9b031b4433cf7bc1fa460dd",
    )
    add_dep(
        repo_name="bazel_skylib",
        version="1.4.1",
        sha="b8a1527901774180afc798aeb28c4634bdccf19c4d98e7bdd1ce79d1fe9aaad7",
    )

    return output
