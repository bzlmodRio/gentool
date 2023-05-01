#     versions = [
#         "2021-3.4.7-4",
#         "2021-3.4.7-5",
#         "2022-4.5.2-1",
#         # "2023-4.5.5-1",
#         # "2023-4.5.5-2",
#         "2023-4.5.5-3",
#         "2023-4.6.0-1",
#         "2023-4.6.0-2",
#         "2023-4.6.0-3",
#     ]

#     template = """
# {{
#     "build_file": null,
#     "build_targets": [],
#     "compatibility_level": "1",
#     "deps": [],
#     "module_dot_bazel": null,
#     "name": "wpi-opencv",
#     "patch_strip": 0,
#     "patches": [],
#     "presubmit_yml": null,
#     "strip_prefix": "bzlmodRio-opencv-{hash}",
#     "test_module_build_targets": [],
#     "test_module_path": null,
#     "test_module_test_targets": [],
#     "url": "https://github.com/pjreiniger/bzlmodRio-opencv/archive/{hash}.tar.gz",
#     "version": "{version}"
# }}
# """

#     for v in versions:
#         import subprocess
#         xxx = subprocess.check_output(args=["git", "rev-parse", v + '-dev'])
#         hash = xxx.decode("utf-8").strip()

#         outdir = r"C:\Users\PJ\Documents\GitHub\bazelrio_bzlmod\bazel-central-registry\json\wpi-opencv/" + v
#         if not os.path.exists(outdir):
#             os.makedirs(outdir)
#         outfile = outdir + r"/config.json"

#         with open(outfile, 'w') as of:
#             of.write(template.format(version=v, hash=hash))

#     import subprocess
#     for v in versions:
#             json_file = r"C:\Users\PJ\Documents\GitHub\bazelrio_bzlmod\bazel-central-registry\json\wpi-opencv/" + v + r"/config.json"
#             os.chdir(r'C:\Users\PJ\Documents\GitHub\bazelrio_bzlmod\bazel-central-registry')
#             if not os.path.exists(json_file):
#                 raise

#             args = ["python", './tools/add_module.py', '--input', json_file]
#             # args = ["python", './tools/add_module.py']
#             print("  ".join(args))
#             subprocess.check_call(args)


#         # print(v, xxx)

#     raise
