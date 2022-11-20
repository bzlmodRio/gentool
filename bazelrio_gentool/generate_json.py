
import os
import json
import subprocess
from bazelrio_gentool.utils import render_template, write_file, SCRIPT_DIR, TEMPLATE_BASE_DIR
from bazelrio_gentool.deps.cc_dependency import CcDependency


# def __write_json(json_file, cc_dep, resource, patches):
#     json_def = {
#         "build_file": None,
#         "build_targets": ['X'],
#         "compatibility_level": "1",
#         "deps": [],
#         "module_dot_bazel": None,
#         "name": f"{cc_dep.name}-{resource}".lower(),
#         "patch_strip": 0,
#         "patches": patches,
#         "presubmit_yml": None,
#         "strip_prefix": None,
#         "test_module_build_targets": [],
#         "test_module_path": None,
#         "test_module_test_targets": [],
#         "url": cc_dep.get_url(resource),
#         "version": cc_dep.version
#     }

#     write_file(json_file, json.dumps(json_def, indent=4))
    
# def __write_top_level_json(json_file, group, target, lang, deps):

#     template_file = os.path.join(TEMPLATE_BASE_DIR, "repo_json", lang, "top_level.json.jinja2")
#     render_template(template_file, json_file, group=group, target=target, deps=deps)


def generate_json(central_registery_location, group, module_json_template):
    
    template_file = os.path.join(module_json_template)
    json_file = os.path.join(central_registery_location, "json", group.repo_name, group.version, "config.json")
    
    module_bazel_file=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(module_json_template)), "..", "MODULE.bazel")).replace("\\", "\\\\")
    render_template(template_file, json_file, group=group, module_bazel_file=module_bazel_file )

    # module_directory = os.path.join(central_registery_location, "json", group.repo_name)
    # if True: #not os.path.exists(module_directory):
    #     create_module(central_registery_location, group)



    # create_module(central_registery_location, json_file)


    
def create_module(central_registery_location, json_file):


    os.chdir(central_registery_location)
    if not os.path.exists(json_file):
        raise

    args = ["python", './tools/add_module.py', '--input', json_file]
    # args = ["python", './tools/add_module.py']
    print("  ".join(args))
    subprocess.check_call(args)
            
