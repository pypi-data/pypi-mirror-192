from setuptools import find_packages, setup

setup(
    name="vulcan_ms_core",
    packages=[
        "vucan",
        "vucan.core",
        "vucan.core.db",
        "vucan.core.enum",
        "vucan.core.exceptions",
        "vucan.core.fastapi",
        "vucan.core.fastapi.dependencies",
        "vucan.core.fastapi.middlewares",
        "vucan.core.fastapi.schemas",
        "vucan.core.helpers",
        "vucan.core.helpers.cache",
        "vucan.core.mixins",
        "vucan.core.repository",
        "vucan.core.utils",
    ],
    version="0.2.1",
    description="Library for Vulcan Microservices",
    author="Overnight",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
