
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template



def __write_dependency_file(base_output_directory, target, language):
    template_base = os.path.join(TEMPLATE_BASE_DIR, "dependencies", language)
    lib_dir = os.path.join(base_output_directory, language, target.parent_folder)
    test_dir = os.path.join(base_output_directory, "..", "tests", language, target.parent_folder)
    
    # Write BUILD file
    template_file = os.path.join(template_base, "libs", "BUILD.bazel.jinja2")
    output_file = os.path.join(lib_dir, "BUILD.bazel")
    render_template(template_file, output_file, target=target)

    # Write test files
    template_file = os.path.join(template_base, "test", "BUILD.bazel.jinja2")
    output_file = os.path.join(test_dir, "BUILD.bazel")
    render_template(template_file, output_file, target=target)

    # Test file
    test_file = os.path.join(test_dir, f"main.{language}")
    if not os.path.exists(test_file):
        print("no test file")

        template_file = os.path.join(template_base, "test", f"main.{language}.jinja2")
        output_file = os.path.join(test_dir, test_file)
        render_template(template_file, output_file, target=target)

def generate_group(base_output_directory, group):
    for cc_dep in group.cc_deps:
        __write_dependency_file(base_output_directory, cc_dep, language="cpp")
        
    for java_dep in group.java_deps:
        __write_dependency_file(base_output_directory, java_dep, language="java")