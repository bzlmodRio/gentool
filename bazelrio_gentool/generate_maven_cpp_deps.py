
import os
from utils import TEMPLATE_BASE_DIR, write_file, render_template


def generate_maven_cpp_deps(base_output_directory, group):
    output_file = os.path.join(base_output_directory, "maven_cpp_deps.bzl")
    template_file = os.path.join(TEMPLATE_BASE_DIR, "maven_cpp_deps.jinja2")

    render_template(template_file, output_file, group=group)