from setuptools import find_packages, setup

setup(
    name="antbot",
    packages=find_packages(),
    version="0.0.1",
    description="",
    author="yanganto",
    author_email="",
    url="https://github.com/yanganto/Ant",
    download_url="",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat"
    ],
    entry_points={'console_scripts': [
        'antbot = antbot.__main__:main',
    ]},
    long_description="""\
AntBot
---
a slack chat bot doing simple script jobs
This version requires Python 3.5

"""
)
