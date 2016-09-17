from setuptools import find_packages, setup

setup(
    name="antbot",
    packages=find_packages(),
    version="0.0.3",
    description="A slack chat bot doing scripts on the server",
    author="yanganto",
    author_email="yanganto@gmail.com",
    url="https://github.com/yanganto/Ant",
    keywords=["slack", "bot"],
    download_url="",
    include_package_data=True,
    package_data={
        'antbot': ['ant.conf.example'],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat"
    ],
    entry_points={'console_scripts': [
        'antbot = antbot.__main__:cli',
    ]},
    long_description="""\
AntBot
---
a slack chat bot doing simple script jobs
This version requires Python 3.5

"""
)
