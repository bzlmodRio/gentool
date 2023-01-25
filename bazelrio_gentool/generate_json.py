
import os
import sys
import json
import subprocess
from bazelrio_gentool.utils import render_template, write_file, SCRIPT_DIR, TEMPLATE_BASE_DIR
from bazelrio_gentool.deps.cc_dependency import CcDependency
from bazelrio_gentool.generate_module_project_files import generate_module_project_files, create_default_mandatory_settings


def generate_json(central_registery_location, group, module_json_template, module_template):

    if module_json_template is None:
        module_json_template = os.path.join(TEMPLATE_BASE_DIR, "publish", "module_config.json.jinja2")
        
    if module_template is None:
        module_template = os.path.join(TEMPLATE_BASE_DIR, "publish", "module_config.jinja2")

    hash = subprocess.check_output(args=["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    mandatory_dependencies = create_default_mandatory_settings(
        use_local_roborio=False,
        use_local_bazelrio=False,
        use_local_bzlmodrio_gentool=False)
    
    module_bazel_file = os.path.join(central_registery_location, "json", group.repo_name, group.version, "MODULE.bazel")

    render_template(module_template, module_bazel_file, group=group, module_bazel_file=module_bazel_file, hash=hash, mandetory_dependencies=mandatory_dependencies)
    
    json_file = os.path.join(central_registery_location, "json", group.repo_name, group.version, "config.json")
    render_template(module_json_template, json_file, group=group, module_bazel_file=module_bazel_file, hash=hash)

    module_directory = os.path.join(central_registery_location, "json", group.repo_name)

    create_module(central_registery_location, json_file)

    return json_file

    
def create_module(central_registery_location, json_file):


    os.chdir(central_registery_location)
    if not os.path.exists(json_file):
        raise

    args = ["python3", './tools/add_module.py', '--input', json_file]
    # args = ["python", './tools/add_module.py']
    print("  ".join(args))
    subprocess.check_call(args)
            
