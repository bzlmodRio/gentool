
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template


def __maybe_write_file(output_dir, template_dir, filename, target):
    full_file = os.path.join(output_dir, filename)
    
    if not os.path.exists(full_file):
        print(f"Smart file {full_file} does not exist, creating it")

        template_file = os.path.join(template_dir, f"{filename}.jinja2")
        output_file = os.path.join(output_dir, full_file)
        render_template(template_file, output_file, target=target)


def __write_dependency_file(base_output_directory, group, target, language):
    template_base = os.path.join(TEMPLATE_BASE_DIR, "dependencies", language)
    lib_dir = os.path.join(base_output_directory, language, target.parent_folder)
    test_dir = os.path.join(base_output_directory, "..", "tests", language, target.parent_folder)
    
    # Write BUILD file
    template_file = os.path.join(template_base, "libs", "BUILD.bazel.jinja2")
    output_file = os.path.join(lib_dir, "BUILD.bazel")
    render_template(template_file, output_file, group=group, target=target)

    # Write test files
    template_file = os.path.join(template_base, "test", "BUILD.bazel.jinja2")
    output_file = os.path.join(test_dir, "BUILD.bazel")
    render_template(template_file, output_file, group=group, target=target)

    # Test file
    if language == "java":
        main_file = f"Main.{language}"
        test_file = f"BasicTest.{language}"
    else:
        main_file = f"main.{language}"
        test_file = f"test.{language}"

    __maybe_write_file(test_dir, os.path.join(template_base, "test"), main_file, target)
    __maybe_write_file(test_dir, os.path.join(template_base, "test"), test_file, target)


def generate_group(base_output_directory, group):
    for cc_dep in group.cc_deps:
        __write_dependency_file(base_output_directory, group, cc_dep, language="cpp")
        
    for java_dep in group.java_deps:
        __write_dependency_file(base_output_directory, group, java_dep, language="java")
        
    for exe_tool in group.executable_tools:
        template_base = os.path.join(TEMPLATE_BASE_DIR, "dependencies", "tools")
        lib_dir = os.path.join(base_output_directory, "tools", exe_tool.artifact_name.lower() if exe_tool.lower_target_name else exe_tool.artifact_name)
        # test_dir = os.path.join(base_output_directory, "..", "tests", "tools", exe_tool.artifact_name)
        
        # Write BUILD file
        template_file = os.path.join(template_base, "exe", "BUILD.bazel.jinja2")
        output_file = os.path.join(lib_dir, "BUILD")
        render_template(template_file, output_file, target=exe_tool)
        
    for exe_tool in group.java_native_tools:
        print("GOt exie tool")
        template_base = os.path.join(TEMPLATE_BASE_DIR, "dependencies", "tools")
        lib_dir = os.path.join(base_output_directory, "tools", exe_tool.artifact_name)
        # test_dir = os.path.join(base_output_directory, "..", "tests", "tools", exe_tool.artifact_name)
        
        # Write BUILD file
        template_file = os.path.join(template_base, "java", "BUILD.bazel.jinja2")
        output_file = os.path.join(lib_dir, "BUILD")
        render_template(template_file, output_file, target=exe_tool)

    if group.executable_tools or group.java_native_tools:
        template_base = os.path.join(TEMPLATE_BASE_DIR, "dependencies", "tools")
        lib_dir = os.path.join(base_output_directory, '..', "tests")
        print("GOt java tool")
        # test_dir = os.path.join(base_output_directory, "..", "tests", "tools", exe_tool.artifact_name)
        
        # Write BUILD file
        template_file = os.path.join(template_base, "tests", "BUILD.bazel.jinja2")
        output_file = os.path.join(lib_dir, "BUILD.bazel")
        render_template(template_file, output_file, group=group)
