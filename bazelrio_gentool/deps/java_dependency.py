

class JavaDependency:
    def __init__(self, name, group_id, version, parent_folder, dependencies, maven_deps=[]):
        self.name = name
        self.version = version
        self.parent_folder = parent_folder
        self.maven_deps = maven_deps
        self.group_id = group_id
        self.dependencies = dependencies

    def __repr__(self):
        return f"JavaDependency: name={self.name}"

    def sorted_dependencies(self):
        output = []

        for dep in self.dependencies:
            if "opencv" in dep.name:
                if "java" in dep.name:
                    output.append(f"@{dep.name}//:{dep.parent_folder}")
                else:
                    output.append(f"@{dep.name}//:jni")
            elif getattr(dep, "has_jni", False):
                output.append(f"@allwpilib//dependencies/cpp/{dep.parent_folder}:jni")
            elif "java" in dep.name:
                output.append(f"@allwpilib//dependencies/java/{dep.parent_folder}",)
            else:
                raise Exception(dep)

        # print(output)

        return sorted(output)

        
# {%- for dep in target.sorted_dependencies() %}
# {%- if dep.has_jni %}
# {%- if "opencv" in dep.parent_folder %}
#         "@opencv-cpp//:jni",
# {%- else %}
#         "@allwpilib//dependencies/cpp/{{dep.parent_folder}}:jni",
# {%- endif %}
# {%- elif "java" in dep.name %}
# {%- if "opencv" in dep.parent_folder %}
#         "@opencv-java//:opencv",
# {%- else %}
#         
# {%- endif %}
# {%- endif %}
# {%- endfor %}
# {%- for maven_dep in target.maven_deps %}
#         artifact("{{maven_dep[0]}}"),
# {%- endfor %}

        # return sorted(self.dependencies, key=lambda dep: dep.name)