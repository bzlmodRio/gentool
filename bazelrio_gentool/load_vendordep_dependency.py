import os
import json
from bazelrio_gentool.deps.dependency_container import DependencyContainer


def vendordep_dependency(
    module_name,
    vendor_file,
    fail_on_hash_miss,
    has_static_libraries,
    install_name_lookup=None,
    maven_dependency_ignore_list=None
):
    install_name_lookup = install_name_lookup or {}
    maven_dependency_ignore_list = maven_dependency_ignore_list or []

    PLATFORM_BLACKLIST = set(
        [
            "windowsx86",
            "linuxaarch64bionic",
            "linuxraspbian",
        ]
    )

    with open(vendor_file, "r") as f:
        vendor_dep = json.load(f)

        os.path.basename(os.path.dirname(vendor_file))

        maven_url = vendor_dep["mavenUrls"][0]
        if maven_url.endswith("/"):
            maven_url = maven_url[:-1]
        version = vendor_dep["version"]
        year = vendor_dep["frcYear"]

        maven_dep = DependencyContainer(
            module_name, version=version, year=year, maven_url=maven_url
        )
        maven_dep.extra_maven_repos.append(maven_url)

        # Add all the headers and sources first
        for cpp_dep in sorted(
            vendor_dep["cppDependencies"], key=lambda x: x["artifactId"]
        ):
            if cpp_dep["artifactId"] in maven_dependency_ignore_list:
                continue

            resources = []
            for platform in cpp_dep["binaryPlatforms"]:
                if platform not in PLATFORM_BLACKLIST:
                    resources.append(platform)
                    if has_static_libraries:
                        resources.append(platform + "static")

            if cpp_dep["artifactId"] in install_name_lookup:
                d = install_name_lookup[cpp_dep["artifactId"]]
                has_install_name_patches = True
                artifact_install_name = d["artifact_install_name"]
                extra_install_name_dependencies = d["deps"]
            else:
                has_install_name_patches = False
                artifact_install_name = None
                extra_install_name_dependencies = None

            maven_dep.create_cc_dependency(
                name=cpp_dep["artifactId"],
                parent_folder=cpp_dep["artifactId"],
                headers=cpp_dep["headerClassifier"],
                sources=cpp_dep.get("sourcesClassifier", None),
                resources=resources,
                group_id=cpp_dep["groupId"],
                version=cpp_dep["version"],
                has_jni=False,
                fail_on_hash_miss=fail_on_hash_miss,
                has_install_name_patches=has_install_name_patches,
                artifact_install_name=artifact_install_name,
                extra_install_name_dependencies=extra_install_name_dependencies,
            )

        for java_dep in sorted(
            vendor_dep["javaDependencies"], key=lambda x: x["artifactId"]
        ):
            if java_dep["artifactId"] in maven_dependency_ignore_list:
                continue
            maven_dep.create_java_dependency(
                name=java_dep["artifactId"],
                group_id=java_dep["groupId"],
                parent_folder="parent",
                version=java_dep["version"],
            )

        for cc_dep in maven_dep.cc_deps:
            if cc_dep.extra_install_name_dependencies is None:
                continue

            resolved_extra_deps = []
            for extra_dep in cc_dep.extra_install_name_dependencies:
                if type(extra_dep) == str:
                    resolved_extra_deps.append(maven_dep.get_cc_dependency(extra_dep))
                else:
                    resolved_extra_deps.append(extra_dep)
            cc_dep.extra_install_name_dependencies = resolved_extra_deps

        return maven_dep
