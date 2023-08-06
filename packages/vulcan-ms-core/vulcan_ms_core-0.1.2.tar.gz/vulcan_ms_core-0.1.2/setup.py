from setuptools import find_packages, setup

setup(
    name="vulcan_ms_core",
    packages=[
        "vulcan_ms_core",
        "vulcan_ms_core.vucan",
        "vulcan_ms_core.vucan.core",
        "vulcan_ms_core.vucan.core.db",
        "vulcan_ms_core.vucan.core.db.mixins",
        "vulcan_ms_core.vucan.core.exceptions",
        "vulcan_ms_core.vucan.core.fastapi",
        "vulcan_ms_core.vucan.core.fastapi.dependencies",
        "vulcan_ms_core.vucan.core.fastapi.middlewares",
        "vulcan_ms_core.vucan.core.fastapi.schemas",
        "vulcan_ms_core.vucan.core.helpers",
        "vulcan_ms_core.vucan.core.helpers.cache",
        "vulcan_ms_core.vucan.core.repository",
        "vulcan_ms_core.vucan.core.utils",
    ],
    version="0.1.2",
    description="Library for Vulcan Microservices",
    author="Overnight",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
