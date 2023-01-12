
import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR, write_file, render_template

def generate_toolchain(module_directory, config):

    
    template_files = [
        "maven_deps.bzl",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "toolchains", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(template_file, output_file, config=config)
