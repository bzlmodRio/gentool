import os
import json
import subprocess
from bazelrio_gentool.utils import (
    render_template,
    TEMPLATE_BASE_DIR,
)
from bazelrio_gentool.generate_module_project_files import (
    create_default_mandatory_settings,
)
from bazelrio_gentool.load_cached_versions import update_cached_version
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies
import hashlib
from urllib.request import urlopen
from bazelrio_gentool.cli import GenericCliArgs
from typing import NamedTuple


def publish_module(
    central_registery_location, group, module_json_template, module_template, **kwargs
):
    if module_json_template is None:
        module_json_template = os.path.join(
            TEMPLATE_BASE_DIR, "publish", "module_config.json.jinja2"
        )

    if module_template is None:
        raise Exception("Dont do this anymore")

    if not module_template.startswith(TEMPLATE_BASE_DIR):
        raise Exception("Dont do this anymore")

    commitish = (
        subprocess.check_output(args=["git", "rev-parse", "HEAD"])
        .decode("utf-8")
        .strip()
    )

    class DummyArgs(NamedTuple):
        use_local_roborio: bool = False
        use_local_bazelrio: bool = False
        use_local_rules_pmd: bool = False
        use_local_rules_checkstyle: bool = False
        use_local_rules_wpiformat: bool = False
        use_local_rules_spotless: bool = False
        use_local_rules_wpi_styleguide: bool = False

    mandatory_dependencies = create_default_mandatory_settings(
        GenericCliArgs(DummyArgs())
    )

    # use_local_roborio=False,
    # use_local_bazelrio=False,
    # use_local_rules_pmd=False,
    # use_local_rules_checkstyle=False,
    # use_local_rules_wpiformat=False,

    module_bazel_file = os.path.join(
        central_registery_location,
        "json",
        group.repo_name,
        group.version + group.patch,
        "MODULE.bazel",
    )

    render_template(
        module_template,
        module_bazel_file,
        group=group,
        module_bazel_file=module_bazel_file,
        hash=commitish,
        mandatory_dependencies=mandatory_dependencies,
        bazel_dependencies=get_bazel_dependencies(),
        **kwargs
    )

    json_file = os.path.join(
        central_registery_location,
        "json",
        group.repo_name,
        group.version + group.patch,
        "config.json",
    )
    render_template(
        module_json_template,
        json_file,
        group=group,
        module_bazel_file=module_bazel_file,
        hash=commitish,
        **kwargs
    )

    os.path.join(central_registery_location, "json", group.repo_name)

    create_module(central_registery_location, json_file)
    update_cached_versions(group, json_file, commitish)

    return json_file


def update_cached_versions(group, json_file, commitish):
    json_info = json.load(open(json_file, "r"))
    url_result = urlopen(json_info["url"])
    data = url_result.read()
    sha256 = hashlib.sha256(data).hexdigest()

    update_cached_version(group.repo_name, group.version, sha256, commitish)


def create_module(central_registery_location, json_file):
    os.chdir(central_registery_location)
    print("Changed to ", central_registery_location)
    if not os.path.exists(json_file):
        raise

    args = [
        "python3",
        "./tools/add_module.py",
        "--input",
        json_file,
        "--registry",
        central_registery_location,
    ]
    # args = ["python", './tools/add_module.py']
    print("  ".join(args))
    subprocess.check_call(args)
    print("_--------------------------------")
