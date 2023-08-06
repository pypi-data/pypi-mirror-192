from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'im testing a basic sayhello thingy'

# Setting up
setup(
    name="lollosayhello",
    version=VERSION,
    author="Lollino (Lorenzo Mogicato)",
    author_email="<lorenzo.mogicato@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[], # TODO per ora niente poi è da riempire
    keywords=['lollino'],
    classifiers=[
        "Development Status :: 1 - Planning",
        # "Intended Audience :: ILVOTeam",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)