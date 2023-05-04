
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template

def write_shared_root_files(module_directory, group):
    template_files = [
        ".bazelignore",
        ".bazelrc-buildbuddy",
        ".bazelversion",
        # ".bazelrc",
        ".gitignore",
        # # ".bazelversion",
        "BUILD.bazel",
        "README.md",
        "WORKSPACE.bzlmod",
        ".styleguide",
        ".styleguide-license",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "shared", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, group=group)
        # render_template(template_file, output_file, group=config)
        
def write_shared_test_files(module_directory, group):
    template_files = [
        # ".bazelignore",
        ".bazelrc-buildbuddy",
        ".bazelversion",
        "WORKSPACE.bzlmod",
        # # ".bazelrc",
        # ".gitignore",
        # # # ".bazelversion",
        # "BUILD.bazel",
        # "README.md",
        # "WORKSPACE.bzlmod",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "shared", tf + ".jinja2")
        output_file = os.path.join(module_directory, "tests", tf)
        render_template(template_file, output_file, group=group)
        # render_template(template_file, output_file, group=config)


        

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
