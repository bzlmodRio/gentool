
import os
import sys
import json
import subprocess
from bazelrio_gentool.utils import render_template, write_file, SCRIPT_DIR, TEMPLATE_BASE_DIR
from bazelrio_gentool.deps.cc_dependency import CcDependency
from bazelrio_gentool.generate_module_project_files import generate_module_project_files, create_default_mandatory_settings
from bazelrio_gentool.load_cached_versions import update_cached_version
import hashlib
from urllib.request import urlopen

def generate_json(central_registery_location, group, module_json_template, module_template, **kwargs):
    if module_json_template is None:
        module_json_template = os.path.join(TEMPLATE_BASE_DIR, "publish", "module_config.json.jinja2")
        
    if module_template is None:
        module_template = os.path.join(TEMPLATE_BASE_DIR, "publish", "module_config.jinja2")

    hash = subprocess.check_output(args=["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    mandatory_dependencies = create_default_mandatory_settings(
        use_local_roborio=False,
        use_local_bazelrio=False,
        use_local_rules_pmd=False,
        use_local_rules_checkstyle=False,
        use_local_rules_wpiformat=False)
    
    module_bazel_file = os.path.join(central_registery_location, "json", group.repo_name, group.version + group.patch, "MODULE.bazel")

    render_template(module_template, module_bazel_file, group=group, module_bazel_file=module_bazel_file, hash=hash, mandetory_dependencies=mandatory_dependencies, **kwargs)
    
    json_file = os.path.join(central_registery_location, "json", group.repo_name, group.version + group.patch, "config.json")
    render_template(module_json_template, json_file, group=group, module_bazel_file=module_bazel_file, hash=hash, **kwargs)

    module_directory = os.path.join(central_registery_location, "json", group.repo_name)

    create_module(central_registery_location, json_file)
    update_cached_versions(group, json_file, hash)

    return json_file


def update_cached_versions(group, json_file, hash):
    json_info = json.load(open(json_file, 'r'))    
    url_result = urlopen(json_info['url'])
    data = url_result.read()
    sha256 = hashlib.sha256(data).hexdigest()
    
    update_cached_version(group.repo_name, group.version, sha256, hash)

    
def create_module(central_registery_location, json_file):
    os.chdir(central_registery_location)
    if not os.path.exists(json_file):
        raise

    args = ["python3", './tools/add_module.py', '--input', json_file]
    # args = ["python", './tools/add_module.py']
    print("  ".join(args))
    subprocess.check_call(args)
            
