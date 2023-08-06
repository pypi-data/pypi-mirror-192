from setuptools import find_packages, setup

setup(
    name="vulcan_ms_core",
    packages=find_packages(include=["vulcan_ms_core"]),
    include_package_data=True,
    version="0.1.1",
    description="Library for Vulcan Microservices",
    author="Overnight",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
