# make the python rules available
load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

# make the dependencies from requirements.txt available
load("@knora_py_deps//:requirements.bzl", "requirement")

py_test(
    name = "test_create_ontology",
    srcs = ["test_create_ontology.py"],
    deps = [
        "//knora:knora"
    ],
    data = [
        "test-onto.json"
    ],
)

py_test(
    name = "test_create_resource",
    srcs = ["test_create_resource.py"],
    deps = [
        "//knora:knora",
    ],
    data = [
        "test-onto.json",
        "test.tif"
    ],
)

py_test(
    name = "test_knora",
    srcs = ["test_knora.py"],
    deps = [
        "//knora:knora",
    ],
)