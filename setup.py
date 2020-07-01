#!/usr/bin/env python

from setuptools import setup

version = "0.14"

with open("README.rst", encoding="utf-8") as fi:
    readme = fi.read()

requirements = [
 "yaml",
]

setup(
    name="distriploy",
    version=version,
    description=("Release deployment utility"),
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Jérôme Carretero",
    author_email="cJ-py-spam@zougloub.eu",
    url="https://github.com/exmakhina/distriploy",
    packages=["distriploy"],
    package_dir={"distriploy": "distriploy"},
    entry_points={"console_scripts": ["distriploy = distriploy.__main__:main"]},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
     "osf": ["osfclient"],
    },
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        'Operating System :: Unix',
        'Operating System :: MacOS',
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "releng",
        "deployment",
        "distribution",
    ],
)
