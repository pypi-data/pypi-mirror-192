from setuptools import find_packages, setup

setup(
    name="vulcan_ms_core",
    packages=find_packages(include=["vulcan", "vulcan.*"]),
    version="0.2.4",
    description="Library for Vulcan Microservices",
    author="Overnight",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
