
import os
from utils import render_template, write_file, SCRIPT_DIR, TEMPLATE_BASE_DIR
import json
import subprocess
from cc_dependency import CcDependency


def __write_json(json_file, cc_dep, resource, patches):
    json_def = {
        "build_file": None,
        "build_targets": ['X'],
        "compatibility_level": "1",
        "deps": [],
        "module_dot_bazel": None,
        "name": f"{cc_dep.name}-{resource}".lower(),
        "patch_strip": 0,
        "patches": patches,
        "presubmit_yml": None,
        "strip_prefix": None,
        "test_module_build_targets": [],
        "test_module_path": None,
        "test_module_test_targets": [],
        "url": cc_dep.get_url(resource),
        "version": cc_dep.version
    }

    write_file(json_file, json.dumps(json_def, indent=4))
    
def __write_top_level_json(json_file, group, target, lang, deps):

    template_file = os.path.join(TEMPLATE_BASE_DIR, "repo_json", lang, "top_level.json.jinja2")
    render_template(template_file, json_file, group=group, target=target, deps=deps)


def generate_json(central_registery_location, group):
    output_directory = os.path.join(central_registery_location, "json")

    json_files = []

    # for cc_dep in group.cc_deps:
    #     if cc_dep.headers:
    #         json_file = os.path.join(output_directory, cc_dep.version, cc_dep.name, cc_dep.headers + ".json")
    #         json_files.append(json_file)
    #         __write_json(json_file, cc_dep, cc_dep.headers, [os.path.join(SCRIPT_DIR, "patches", "headers", "add_build_file.patch")])

    #     for resource in cc_dep.resources:
    #         json_file = os.path.join(output_directory, cc_dep.version, cc_dep.name, resource + ".json")
    #         json_files.append(json_file)
    #         __write_json(json_file, cc_dep, resource, [os.path.join(SCRIPT_DIR, "patches", "libraries", "add_build_file.patch")])
    

    if group.repository_url:
        for java_dep in group.java_deps:
            json_file = os.path.join(output_directory, java_dep.version, java_dep.name + ".json")
            json_files.append(json_file)
            __write_top_level_json(json_file, group, java_dep, "java", deps=[])

        for cc_dep in group.cc_deps:
            json_file = os.path.join(output_directory, cc_dep.version, cc_dep.name + ".json")

            deps = []

            if cc_dep.headers:
                deps.append([f"{cc_dep.name}-{cc_dep.headers}", f"{cc_dep.version}"])

            for resource in cc_dep.resources:
                deps.append([f"{cc_dep.name}-{resource}", f"{cc_dep.version}"])

            for dep in cc_dep.dependencies:
                deps.append([dep.name, dep.version])

            json_files.append(json_file)
            __write_top_level_json(json_file, group, cc_dep, "cpp", deps)

    run_json_stuff(central_registery_location, json_files)
    
    if group.repository_url:
        for java_dep in group.java_deps:
            module_file = os.path.join(central_registery_location, "modules", java_dep.name, java_dep.version, "MODULE.bazel")
            
            template_file = os.path.join(TEMPLATE_BASE_DIR, "repo_json", "java", "MODULE.bazel.jinja2")
            render_template(template_file, module_file, group=group, target=java_dep)


    
def run_json_stuff(central_registery_location, json_gen_files):
    os.chdir(central_registery_location)
    for def_file in json_gen_files:
        args = ["python", './tools/add_module.py', '--input', def_file]
        # args = ["python", './tools/add_module.py']
        print("  ".join(args))
        subprocess.check_call(args)
            
