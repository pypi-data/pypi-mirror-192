from setuptools import find_packages, setup

setup(
    name="vulcan_ms_core",
    packages=find_packages(include=["vulcan_ms_core"]),
    version="0.1.0",
    description="Library for Vulcan Microservices",
    author="Overnight",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
