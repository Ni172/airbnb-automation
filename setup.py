from setuptools import setup, find_packages

setup(
    name="pytest-suite-timeout",
    version="0.1",
    packages=["pytest_suite_timeout"],  # refers to your plugin package
    entry_points={
        'pytest11': [
            'suite-timeout = pytest_suite_timeout',
        ],
    },
)
