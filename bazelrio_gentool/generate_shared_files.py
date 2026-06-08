import os
from bazelrio_gentool.utils import (
    TEMPLATE_BASE_DIR,
    render_templates,
)
from bazelrio_gentool.dependency_helpers import BaseDependencyWriterHelper


def write_shared_root_files(
    module_directory,
    group,
    include_linuxarm32_compiler=True,
    include_linuxarm64_compiler=True,
    include_systemcore_compiler=False,
    test_macos=True,
    include_windows_arm_compiler=True,
    include_styleguide=True,
):
    if not include_linuxarm32_compiler:
        raise
    if not include_linuxarm64_compiler:
        raise
    template_files = [
        ".github/actions/setup-build-buddy/action.yml",
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".github/workflows/publish.yml",
        ".gitattributes",
        # "generate/WORKSPACE",
        ".bazelignore",
        ".bazelrc-buildbuddy",
        ".bazelversion",
        ".bazelrc",
        ".bazelrc-cc",
        ".gitignore",
        "BUILD.bazel",
        "README.md",
        ".clang-format",
        ".wpiformat",
        ".wpiformat-license",
    ]

    if os.path.exists(os.path.join(module_directory, "generate", "auto_update.py")):
        template_files.append(".github/workflows/auto_update.yml")

    render_templates(
        template_files,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "shared"),
        group=group,
        include_linuxarm32_compiler=include_linuxarm32_compiler,
        include_linuxarm64_compiler=include_linuxarm64_compiler,
        include_systemcore_compiler=include_systemcore_compiler,
        include_windows_arm_compiler=include_windows_arm_compiler,
        test_macos=test_macos,
        include_styleguide=include_styleguide,
    )


def write_shared_test_files(module_directory, group):
    template_files = [
        ".bazelrc-buildbuddy",
        ".bazelversion",
        ".bazelrc",
        ".bazelrc-cc",
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
        url_base="https://github.com/bazelbuild",
    ):
        BaseDependencyWriterHelper.__init__(
            self,
            repo_name,
            version,
            sha,
            url_base,
            old_release_style=old_release_style,
            needs_stripped_prefix=needs_stripped_prefix,
        )

    def download_repository(self, indent_num, maybe=True):
        if self.repo_name == "googletest":
            version = self.version.replace(".bcr.1", "")
            return f"""http_archive(
    name = "googletest",
    sha256 = "{self.sha}",
    strip_prefix = "googletest-{version}",
    urls = ["https://github.com/google/googletest/archive/refs/tags/v{version}.tar.gz"],
)"""
        if self.repo_name == "protobuf":
            version = self.version.replace(".bcr.1", "")
            return f"""{" " * indent_num}http_archive(
    name = "com_google_protobuf",
    sha256 = "{self.sha}",
    strip_prefix = "protobuf-{version}",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v{version}.tar.gz"],
)"""
        if self.repo_name == "rules_shell":
            return f"""{" " * indent_num}http_archive(
    name = "{self.repo_name}",
    sha256 = "{self.sha}",
    strip_prefix = "rules_shell-{self.version}",
    url = "https://github.com/bazelbuild/{self.repo_name}/releases/download/v{self.version}/rules_shell-v{self.version}.tar.gz",
)"""
        if self.repo_name == "bazel_features":
            return f"""{" " * indent_num}http_archive(
    name = "{self.repo_name}",
    sha256 = "{self.sha}",
    strip_prefix = "bazel_features-{self.version}",
    url = "https://github.com/bazel-contrib/{self.repo_name}/releases/download/v{self.version}/bazel_features-v{self.version}.tar.gz",
)"""
        return self.http_archive(indent_num=indent_num, maybe=maybe, native=False)


def get_bazel_dependencies():
    def add_dep(repo_name, sha="", **kwargs):
        output[repo_name] = BazelDependencySetting(repo_name, sha=sha, **kwargs)

    output = {}

    add_dep(
        repo_name="bazel_features",
        version="1.31.0",
        sha="a015f3f2ebf4f1ac3f4ca8ea371610acb63e1903514fa8725272d381948d2747",
        needs_stripped_prefix=True,
        url_base="https://github.com/bazel-contrib",
    )
    add_dep(
        repo_name="bazel_skylib",
        version="1.8.1",
        sha="51b5105a760b353773f904d2bbc5e664d0987fbaf22265164de65d43e910d8ac",
    )
    add_dep(
        repo_name="googletest",
        version="1.17.0",
        sha="8ad598c73ad796e0d8280b082cebd82a630d73e73cd3c70057938a6501bba5d7",
    )
    add_dep(
        repo_name="platforms",
        version="0.0.11",
        sha="",
    )
    add_dep(
        repo_name="rules_cc",
        version="0.2.13",
        needs_stripped_prefix=True,
        sha="0d3b4f984c4c2e1acfd1378e0148d35caf2ef1d9eb95b688f8e19ce0c41bdf5b",
    )
    add_dep(
        repo_name="rules_java",
        version="8.16.1",
        sha="1558508fc6c348d7f99477bd21681e5746936f15f0436b5f4233e30832a590f9",
        # use_long_form=True,
    )
    add_dep(
        repo_name="rules_jvm_external",
        version="6.8",
        sha="c18a69d784bcd851be95897ca0eca0b57dc86bb02e62402f15736df44160eb02",
        needs_stripped_prefix=True,
        # use_zip=True,
        # use_long_form=True,
    )
    add_dep(
        repo_name="rules_shell",
        version="0.4.0",
        sha="3e114424a5c7e4fd43e0133cc6ecdfe54e45ae8affa14fadd839f29901424043",
        needs_stripped_prefix=True,
    )
    add_dep(
        repo_name="rules_proto",
        version="7.0.2",
        sha="0e5c64a2599a6e26c6a03d6162242d231ecc0de219534c38cb4402171def21e8",
        old_release_style=True,
        needs_stripped_prefix=True,
    )
    add_dep(
        repo_name="rules_python",
        version="1.7.0",
        sha="f609f341d6e9090b981b3f45324d05a819fd7a5a56434f849c761971ce2c47da",
        needs_stripped_prefix=True,
    )
    add_dep(
        repo_name="protobuf",
        version="29.0",
        sha="10a0d58f39a1a909e95e00e8ba0b5b1dc64d02997f741151953a2b3659f6e78c",
        needs_stripped_prefix=True,
    )

    return output
