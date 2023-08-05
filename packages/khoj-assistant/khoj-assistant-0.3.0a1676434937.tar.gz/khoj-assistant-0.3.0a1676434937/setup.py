#!/usr/bin/env python

from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent

setup(
    name='khoj-assistant',
    version='0.3.0a1676434937',
    description="A natural language search engine for your personal notes, transactions and images",
    long_description=(this_directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author='Debanjum Singh Solanky, Saba Imran',
    author_email='debanjum+pypi@gmail.com, narmiabas@gmail.com',
    url='https://github.com/debanjum/khoj',
    license="GPLv3",
    keywords="search semantic-search productivity NLP org-mode markdown beancount images",
    python_requires=">=3.8, <3.11",
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        include=["khoj*"]
    ),
    install_requires=[
        "torch == 1.13.1",
        "sentence-transformers == 2.2.2",
        "openai == 0.20.0",
        "pydantic == 1.9.1",
        "fastapi == 0.77.1",
        "uvicorn == 0.17.6",
        "jinja2 == 3.1.2",
        "pyyaml == 6.0",
        "pytest == 7.1.2",
        "pillow == 9.3.0",
        "dateparser == 1.1.1",
        "pyqt6 == 6.3.1",
        "defusedxml == 0.7.1",
        'schedule == 1.1.0',
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["khoj = khoj.main:run"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
