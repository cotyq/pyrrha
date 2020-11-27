import os
import pathlib

from setuptools import find_packages, setup

REQUIREMENTS = ["numpy", "oct2py", "Jinja2", "typer"]

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

DESCRIPTION = (
    "pyrrha is a tool for helping in the developement and testing "
    "of Computational Mechanics methods."
)

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()

with open(PATH / "pyrrha" / "pyrrha.py") as fp:
    VERSION = (
        [line for line in fp.readlines() if line.startswith("__version__")][0]
        .split("=", 1)[-1]
        .strip()
        .replace('"', "")
    )

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
    packages=find_packages(include=["pyrrha", "pyrrha.*"]),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    entry_points={"console_scripts": ["pyrrha=pyrrha.pyrrha:main"]},
)
