from setuptools import setup, find_packages

setup(
    name="pytest-suite-timeout",
    version="0.1",
    description="A simple Pytest plugin to enforce per-suite timeout",
    packages=["pytest_suite_timeout"],
    entry_points={
        "pytest11": ["suite_timeout = pytest_suite_timeout"]
    },
    install_requires=[],  # No external packages
)
