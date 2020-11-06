import os
import pathlib
from setuptools import setup


REQUIREMENTS = ["numpy", "attrs", "oct2py", "Jinja2"]
PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
VERSION = "0.1"
DESCRIPTION = "Pymetheus descripcion corta"  # TODO completar descripcion corta

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()  # TODO completar README

setup(
    name="pymetheus",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=[
        "Diego Sklar",
        "Franco Matzkin",
        "Constanza Quaglia"],
    author_email="dsklar@gmail.com",
    url="https://gitlab.com/dsklar/pymetheus",
    license="MIT",
    keywords=["pymetheus"],
    packages=["pymetheus", "pymetheus.implementations"],
    install_requires=REQUIREMENTS)