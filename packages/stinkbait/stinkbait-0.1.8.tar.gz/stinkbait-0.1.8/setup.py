# Copyright (c) 2020, Train GRC, inc.
# All rights reserved.
# Licensed under the MIT License.
# For full license text, see the LICENSE file in the repo root

import setuptools
import os
import configparser
import uuid

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.1.8'

REQUIRED_PACKAGES = [
    'bs4',
    'boto3',
    'botocore',
    'argparse',
    'jinja2',
    'markdown',
    'pyyaml',
    'schema',
    'stinkbait',
]
PROJECT_URLS = {
    "Code": "https://github.com/traingrc/stinkbait",
    "Documentation": "https://traingrc.com",
    "Example Report": "https://traingrc.com",
}

def get_version():
    print(type(VERSION))
    config = configparser.ConfigParser()
    config.read('config.ini')
    #If config.ini doesn't have a stinkbait section, add it
    if not config.has_section('STINKBAIT'):
        config.add_section('STINKBAIT')
    #If config.ini doesn't have a stinkbait_version, add it
    if not config.has_option('STINKBAIT', 'stinkbait_version'):
        config.set('STINKBAIT', 'stinkbait_version', str(VERSION))
    stinkbait_instance_id = uuid.uuid4().hex
    if not config.has_option('STINKBAIT', 'stinkbait_instance_id'):
        config.set('STINKBAIT', 'stinkbait_instance_id', stinkbait_instance_id)
    return config.get('STINKBAIT', 'stinkbait_version')

def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()

setuptools.setup(
    name="stinkbait",
    version=get_version(),
    include_package_data=True,
    author="Wes Ladd",
    author_email="wesladd@traingrc.com",
    description="Security Awareness Testing and Training Tool",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/traingrc/stinkbait",
    package_data={'src.ext_resources.quietriot': ["results/*.txt","wordlists/*.txt","*.txt","enumeration/*"]},
    packages=setuptools.find_packages(),
    install_requires=REQUIRED_PACKAGES,
    project_urls=PROJECT_URLS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": 'stinkbait=stinkbait.main:main'},
    zip_safe=True,
    keywords='aws cloud infrastructure for security awareness testing and training',
    python_requires='>=3.6',
)