import os
from jinja2 import Template

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_BASE_DIR = os.path.join(SCRIPT_DIR, "templates")


def __make_if_not_exist(f):
    dir = os.path.dirname(f)

    if not os.path.exists(dir):
        os.makedirs(dir)


def write_file(filename, contents):
    __make_if_not_exist(filename)
    # print(f"Writing to {filename}")
    with open(filename, 'wb') as f:
        f.write(bytes(contents, "utf-8"))

        
def render_template(template_file, output_file, **kwargs):
    template_file = os.path.join(TEMPLATE_BASE_DIR, template_file)
    
    template_contents = open(template_file, "r").read()
    output = Template(template_contents).render(**kwargs)
    write_file(output_file, output)