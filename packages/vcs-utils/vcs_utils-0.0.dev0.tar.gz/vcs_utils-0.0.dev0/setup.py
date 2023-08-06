from setuptools import setup, find_packages

import json
import os


def read_pipenv_dependencies(fname):
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


if __name__ == '__main__':
    setup(
        name='vcs_utils',
        version=os.getenv('PACKAGE_VERSION', '0.0.dev0'),
        package_dir={'': 'package'},
        packages=find_packages('package'),
        description='A demo package.'
    )
