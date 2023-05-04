import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template
from bazelrio_gentool.generate_shared_files import write_shared_root_files
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies





def generate_styleguide_rule(module_directory, group, short_name, mandetory_dependencies):
    write_shared_root_files(module_directory, group)
    
    template_files = [
        ".github/workflows/build.yml",
        ".bazelversion",
        "MODULE.bazel",
        "WORKSPACE",
        "dependencies/BUILD.bazel",
        "dependencies/load_dependencies.bzl",
        "dependencies/load_rule_dependencies.bzl",

    ]
    
    bazel_dependencies=get_bazel_dependencies()
    
    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "styleguide", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, group=group, bazel_dependencies=bazel_dependencies, short_name=short_name, mandetory_dependencies=mandetory_dependencies)
        # render_template(template_file, output_file, group=config)


    # template_files = [
    #     # ".github/workflows/build.yml",
    #     # ".github/workflows/lint.yml",
    #     # ".bazelrc-buildbuddy",
    #     # ".bazelignore",
    #     # ".bazelrc",
    #     # ".gitignore",
    #     # # ".bazelversion",
    #     # "BUILD.bazel",
    #     # "README.md",
    #     # "WORKSPACE.bzlmod",
    # ]

    # for tf in template_files:
    #     template_file = os.path.join(TEMPLATE_BASE_DIR, "module", tf + ".jinja2")
    #     output_file = os.path.join(module_directory, tf)
    #     render_template(template_file, output_file, group=group)
    #     # render_template(template_file, output_file, group=config)


    print("FJKLSDFJ")
