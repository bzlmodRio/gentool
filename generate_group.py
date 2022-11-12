
import os
from utils import TEMPLATE_BASE_DIR, write_file, render_template



def __write_project_files(template_base, output_directory, target):

    tests_dir = os.path.join(output_directory, "tests")

    write_file(os.path.join(output_directory, "WORKSPACE"), "")
    write_file(os.path.join(output_directory, "WORKSPACE.bzlmod"), "")
    write_file(os.path.join(output_directory, "tests", "WORKSPACE"), "")

    template_files = [
        "MODULE.bazel",
        "BUILD.bazel",
        "tests/.bazelrc",
        "tests/MODULE.bazel",
        "tests/BUILD.bazel",
        "tests/WORKSPACE.bzlmod",
        "tests/.bazelversion",
    ]

    for tf in template_files:
        template_file = os.path.join(template_base, tf + ".jinja2")
        output_file = os.path.join(output_directory, tf)

        render_template(template_file, output_file, target=target)


def __write_cc_dep(base_output_directory, cc_dep):
    output_dir = os.path.join(base_output_directory, cc_dep.parent_folder, cc_dep.name)

    template_base = os.path.join(TEMPLATE_BASE_DIR, "cpp")
    __write_project_files(template_base, output_dir, cc_dep)
    
    main_file = os.path.join(output_dir, "tests", "main.cpp")
    if not os.path.exists(main_file):
        print("Test file doesn't exit")
        render_template(os.path.join(template_base, "tests/main.cpp.jinja2"), main_file)
    
def __write_java_dep(base_output_directory, cc_dep):
    output_dir = os.path.join(base_output_directory, cc_dep.parent_folder, cc_dep.name)

    template_base = os.path.join(TEMPLATE_BASE_DIR, "java")
    __write_project_files(template_base, output_dir, cc_dep)
    
    main_file = os.path.join(output_dir, "tests", "Main.java")
    if not os.path.exists(main_file):
        print("Test file doesn't exit")
        render_template(os.path.join(template_base, "tests/main.java.jinja2"), main_file)


def generate_group(base_output_directory, group):
    for cc_dep in group.cc_deps:
        __write_cc_dep(base_output_directory, cc_dep)
        
    for java_dep in group.java_deps:
        __write_java_dep(base_output_directory, java_dep)