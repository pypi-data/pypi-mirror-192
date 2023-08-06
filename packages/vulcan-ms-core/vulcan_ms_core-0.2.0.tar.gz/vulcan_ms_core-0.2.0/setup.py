from setuptools import find_packages, setup

setup(
    name="vulcan_ms_core",
    packages=[
        "vucan",
        "vucan.core",
        "vucan.core.db",
        "vucan.core.db.mixins",
        "vucan.core.exceptions",
        "vucan.core.fastapi",
        "vucan.core.fastapi.dependencies",
        "vucan.core.fastapi.middlewares",
        "vucan.core.fastapi.schemas",
        "vucan.core.helpers",
        "vucan.core.helpers.cache",
        "vucan.core.repository",
        "vucan.core.utils",
    ],
    version="0.2.0",
    description="Library for Vulcan Microservices",
    author="Overnight",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
