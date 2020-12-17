#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pathlib import Path

version_path = Path(__file__).parent / "karton/autoit_ripper/__version__.py"
version_info = {}
exec(version_path.read_text(), version_info)

setup(
    name="karton-autoit-ripper",
    version=version_info["__version__"],
    description="AutoIt script ripper for Karton framework",
    namespace_packages=["karton"],
    packages=["karton.autoit_ripper"],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "karton-autoit-ripper=karton.autoit_ripper:AutoItRipperKarton.main"
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    package_data={"karton.autoit_ripper": ["autoit.yar"]},
)

