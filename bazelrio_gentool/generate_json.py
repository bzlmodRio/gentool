
import os
import json
import subprocess
from bazelrio_gentool.utils import render_template, write_file, SCRIPT_DIR, TEMPLATE_BASE_DIR
from bazelrio_gentool.deps.cc_dependency import CcDependency


def generate_json(central_registery_location, group, module_json_template):

    
    hash = subprocess.check_output(args=["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    print(hash)
    
    template_file = os.path.join(module_json_template)
    json_file = os.path.join(central_registery_location, "json", group.repo_name, group.version, "config.json")
    
    module_bazel_file=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(module_json_template)), "..", "MODULE.bazel")).replace("\\", "\\\\")
    render_template(template_file, json_file, group=group, module_bazel_file=module_bazel_file, hash=hash)

    module_directory = os.path.join(central_registery_location, "json", group.repo_name)
    if True: #not os.path.exists(module_directory):
        create_module(central_registery_location, json_file)



    # create_module(central_registery_location, json_file)


    
def create_module(central_registery_location, json_file):


    os.chdir(central_registery_location)
    if not os.path.exists(json_file):
        raise

    args = ["python", './tools/add_module.py', '--input', json_file]
    # args = ["python", './tools/add_module.py']
    print("  ".join(args))
    subprocess.check_call(args)
            
