import os
from bazelrio_gentool.utils import (
    TEMPLATE_BASE_DIR,
    render_templates,
)


def write_shared_root_files(module_directory, group, include_raspi_compiler=False):
    template_files = [
        ".github/workflows/build.yml",
        ".github/workflows/lint.yml",
        ".github/workflows/publish.yml",
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

    render_templates(
        template_files,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "shared"),
        group=group,
        include_raspi_compiler=include_raspi_compiler,
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


class BazelDependencySetting:
    def __init__(self, repo_name, version, sha, use_zip=False, use_long_form=False):
        self.repo_name = repo_name
        self.version = version
        self.sha = sha
        self.use_zip = use_zip
        self.use_long_form = use_long_form

    def download_repository(self, indent, maybe=True):
        file_extension = "zip" if self.use_zip else "tar.gz"
        output = ""

        if self.use_long_form:
            output += f"""{self.repo_name.upper()}_COMMITISH = "{self.version}"
    {self.repo_name.upper()}_SHA = "{self.sha}"
    """

            if maybe:
                output += "maybe(\n    http_archive,"
            else:
                output += "http_archive("

            output += f"""
    name = "{self.repo_name}",
    sha256 = {self.repo_name.upper()}_SHA,
    strip_prefix = "{self.repo_name}-{{}}".format({self.repo_name.upper()}_COMMITISH),
    url = "https://github.com/bazelbuild/{self.repo_name}/archive/{{}}.{file_extension}".format({self.repo_name.upper()}_COMMITISH),
)"""
            return output

        output = ""
        if maybe:
            output += "maybe(\n    http_archive,"
        else:
            output += "http_archive("

        output += f"""
    name = "{self.repo_name}",
    sha256 = "{self.sha}",
    strip_prefix = "{self.repo_name}-{self.version}",
    url = "https://github.com/bazelbuild/{self.repo_name}/archive/refs/tags/{self.version}.tar.gz",
)"""

        return output


def get_bazel_dependencies():
    def add_dep(repo_name, **kwargs):
        output[repo_name] = BazelDependencySetting(repo_name, **kwargs)

    output = {}

    add_dep(repo_name="platforms", version="0.0.6", sha="")
    add_dep(
        repo_name="rules_python",
        version="0.16.2",
        sha="48a838a6e1983e4884b26812b2c748a35ad284fd339eb8e2a6f3adf95307fbcd",
    )
    add_dep(
        repo_name="rules_java",
        version="5.4.0",
        sha="f90111a597b2aa77b7104dbdc685fd35ea0cca3b7c3f807153765e22319cbd88",
        use_long_form=True,
    )
    # add_dep(repo_name="rules_java", version="5.3.5", sha="7df0811e29830e79be984f9d5bf6839ce151702d694038126d7c23296785bf97", use_long_form=True)
    # add_dep("rules_java", "5.4.0", "", "")
    # add_dep(repo_name="rules_jvm_external", version="4.4.2", sha="735602f50813eb2ea93ca3f5e43b1959bd80b213b836a07a62a29d757670b77b", use_zip=True, use_long_form=True)
    add_dep(
        repo_name="rules_jvm_external",
        version="4.5",
        sha="b17d7388feb9bfa7f2fa09031b32707df529f26c91ab9e5d909eb1676badd9a6",
        use_zip=True,
        use_long_form=True,
    )
    add_dep(repo_name="rules_cc", version="0.0.4", sha="")
    add_dep(
        repo_name="googletest",
        version="1.12.1",
        sha="24564e3b712d3eb30ac9a85d92f7d720f60cc0173730ac166f27dda7fed76cb2",
    )
    add_dep(repo_name="rules_proto", version="5.3.0-21.7", sha="")
    add_dep(
        repo_name="bazel_skylib",
        version="1.4.1",
        sha="060426b186670beede4104095324a72bd7494d8b4e785bf0d84a612978285908",
    )

    return output
