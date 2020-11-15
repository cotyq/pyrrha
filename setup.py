import os
import pathlib

from setuptools import setup


REQUIREMENTS = ["numpy", "attrs", "oct2py", "Jinja2"]
PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
VERSION = "0.1"
DESCRIPTION = (
    "pyrrha is a tool for helping in the developement and testing "
    "of Computational Mechanics methods."
)

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()  # TODO completar README

setup(
    name="pyrrha",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=["Diego Sklar", "Franco Matzkin", "Constanza Quaglia"],
    author_email="dsklar@gmail.com",
    url="https://gitlab.com/dsklar/pyrrha",
    license="MIT",
    keywords=["pyrrha"],
    packages=["pyrrha", "pyrrha.impl"],
    install_requires=REQUIREMENTS,
)
