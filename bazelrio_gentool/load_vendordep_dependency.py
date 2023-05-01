import os
import json
from bazelrio_gentool.deps.dependency_container import DependencyContainer


def vendordep_dependency(
    module_name, vendor_file, year, fail_on_hash_miss, has_static_libraries
):
    PLATFORM_BLACKLIST = set(
        [
            "windowsx86",
            "linuxaarch64bionic",
            "linuxraspbian",
        ]
    )

    with open(vendor_file, "r") as f:
        vendor_dep = json.load(f)

        vendor_name = os.path.basename(os.path.dirname(vendor_file))

        maven_url = vendor_dep["mavenUrls"][0]
        if maven_url.endswith("/"):
            maven_url = maven_url[:-1]
        version = vendor_dep["version"]

        maven_dep = DependencyContainer(
            module_name, version=version, year=year, maven_url=maven_url
        )
        maven_dep.extra_maven_repos.append(maven_url)

        # Add all the headers and sources first
        for cpp_dep in sorted(
            vendor_dep["cppDependencies"], key=lambda x: x["artifactId"]
        ):
            resources = []
            for platform in cpp_dep["binaryPlatforms"]:
                if platform not in PLATFORM_BLACKLIST:
                    resources.append(platform)
                    if has_static_libraries:
                        resources.append(platform + "static")

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
            )

        for java_dep in sorted(
            vendor_dep["javaDependencies"], key=lambda x: x["artifactId"]
        ):
            maven_dep.create_java_dependency(
                name=java_dep["artifactId"],
                group_id=java_dep["groupId"],
                parent_folder="parent",
                version=java_dep["version"],
            )

        return maven_dep
