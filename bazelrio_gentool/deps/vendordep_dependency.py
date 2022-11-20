
import os
import json
from bazelrio_gentool.deps.dependency_container import DependencyContainer

def vendordep_dependency(vendor_file):
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

        maven_dep = DependencyContainer("ctre", version, maven_url)

        # Add all the headers and sources first
        for cpp_dep in sorted(
            vendor_dep["cppDependencies"], key=lambda x: x["artifactId"]
        ):
            resources = []
            for platform in cpp_dep["binaryPlatforms"]:
                if platform not in PLATFORM_BLACKLIST:
                    resources.append(platform)
                    # resources.append(platform + "static")

            maven_dep.create_cc_dependency(
                name=cpp_dep["artifactId"],
                parent_folder="parent",
                headers=cpp_dep['headerClassifier'],
                resources=resources,
                group_id=cpp_dep["groupId"],
                version=cpp_dep["version"],
                has_jni=False,
                fail_on_hash_miss=True,
            )

        # # Then grab the native libraries
        # for cpp_dep in sorted(
        #     vendor_dep["cppDependencies"], key=lambda x: x["artifactId"]
        # ):
        #     resources = []
        #     for platform in cpp_dep["binaryPlatforms"]:
        #         if platform not in PLATFORM_BLACKLIST:
        #             resources.append(platform)
        #             resources.append(platform + "static")

        #     maven_dep.create_cc_dependency(
        #         name=cpp_dep["artifactId"],
        #         parent_folder="parent",
        #         resources=resources,
        #         group_id=cpp_dep["groupId"],
        #         version=cpp_dep["version"],
        #         has_jni=False,
        #         fail_on_hash_miss=True,
        #     )

        for java_dep in sorted(
            vendor_dep["javaDependencies"], key=lambda x: x["artifactId"]
        ):
            maven_dep.create_java_dependency(
                name=java_dep["artifactId"], group_id=java_dep["groupId"], parent_folder="parent",
            )

        return maven_dep