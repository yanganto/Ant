from setuptools import find_packages, setup

setup(
    name="antbot",
    packages=find_packages(),
    install_requires=['slackclient'],
    version="0.1.1",
    description="A slack chat bot doing scripts on the server",
    author="yanganto",
    author_email="yanganto@gmail.com",
    url="https://github.com/yanganto/Ant",
    keywords=["slack", "bot"],
    download_url="",
    license="MIT",
    include_package_data=True,
    package_data={
        'antbot': ['ant.conf.example'],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat"
    ],
    entry_points={'console_scripts': [
        'antbot = antbot.__main__:cli',
    ]},
    long_description="""\
AntBot - a slack chat bot execute simple script jobs
---
a slack bot can execute commands by slack chat room ( @bot_name: command ),
wherein these commands are specified in a folder.

This version requires Python 3.5+
"""
)
