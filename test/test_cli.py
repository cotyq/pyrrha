# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

import os
import pathlib
import tempfile

from pyrrha.pyrrha import CLI
from pyrrha.report import Status as S

import pytest


@pytest.fixture
def version():
    path = pathlib.Path(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    )

    with open(path / "pyrrha" / "pyrrha.py") as fp:
        version = (
            [
                line
                for line in fp.readlines()
                if line.startswith("__version__")
            ][0]
            .split("=", 1)[-1]
            .strip()
            .replace('"', "")
        )
    return version


@pytest.fixture
def finite_element_2D_template():
    return """from pyrrha.method import FiniteElement2D


class FiniteElement2DTemplate(FiniteElement2D):

    def heat_dirichlet(self, K, F, dirichlet):
        pass

    def heat_initialize(self, n_nodes):
        pass

    def heat_neumann(self, F, neumann, x_node):
        pass

    def heat_robin(self, K, F, robin, x_node):
        pass
"""


def test_version(version, script_runner):
    ret = script_runner.run("pyrrha", "version")

    assert ret.success
    assert ret.stdout.strip() == version
    assert ret.stderr == ""


def test_generate_fe2d(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate", "FiniteElement2D")
    assert ret.success
    assert ret.stdout.strip() == finite_element_2D_template.strip()
    assert ret.stderr == ""


def test_generate_fe2d_to_file(finite_element_2D_template, script_runner):
    with tempfile.NamedTemporaryFile(mode="r+") as fp:
        ret = script_runner.run(
            "pyrrha", "generate", "FiniteElement2D", "--output", fp.name
        )
        fp.seek(0)
        assert ret.success
        assert fp.read().strip() == finite_element_2D_template.strip()
        assert ret.stderr == ""


def test_generate_empty_base(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate")
    error_msg = "Error: Missing argument 'BASE'."
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_generate_wrong_filename(finite_element_2D_template, script_runner):
    fake_folder = "carpeta"
    file = "FEM2d.py"
    ret = script_runner.run(
        "pyrrha",
        "generate",
        "FiniteElement2D",
        "--output",
        os.path.join(fake_folder, file),
    )
    error_msg = "Error: Invalid value: wrong output file name"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_method_wrong_name(finite_element_2D_template, script_runner):
    path = os.path.join("test", "impl", "FEM2DTest.py")

    ret = script_runner.run(
        "pyrrha", "validate", path, "--method", "heat_init44534ialize"
    )
    error_msg = "Error: Invalid value: The method"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_generate_class_wrong_name(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate", "NonexistentClass")
    error_msg = "wrong class name"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_class_wrong_inher(finite_element_2D_template, script_runner):
    path = os.path.join("test", "impl", "FEM2DTestWrongInheritance.py")
    ret = script_runner.run("pyrrha", "validate", path)
    error_msg = "no appropiate class found in"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_class_empty(finite_element_2D_template, script_runner):
    path = os.path.join("test", "impl", "EmptyFile.py")

    ret = script_runner.run("pyrrha", "validate", path)
    error_msg = "no appropiate class found in"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_class_zero_div(finite_element_2D_template, script_runner):
    path = os.path.join("test", "impl", "FEM2DTestZeroDiv.py")

    ret = script_runner.run("pyrrha", "validate", path)
    error_msg = "Failed to execute method heat_initialize (division by zero)."
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_method_zero_div(finite_element_2D_template, script_runner):
    path = os.path.join("test", "impl", "FEM2DTestZeroDiv.py")

    ret = script_runner.run(
        "pyrrha", "validate", path, "--method", "heat_initialize"
    )
    error_msg = "Failed to execute method heat_initialize"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_class_file_not_found(
    finite_element_2D_template, script_runner
):
    path = os.path.join("test", "impl", "FileNotExists.py")
    ret = script_runner.run("pyrrha", "validate", path)
    error_msg = "file not found"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_class_wrong_init(finite_element_2D_template, script_runner):
    path = os.path.join("test", "impl", "FEM2DTestWrongInit.py")
    ret = script_runner.run("pyrrha", "validate", path)
    error_msg = "Failed to initialize programmed class"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_validate_class_fe2d_cli(finite_element_2D_template):
    cli = CLI()
    report = cli.validate(os.path.join("test", "impl/FEM2DTest.py"))
    repo = [
        {"name": "heat_initialize", "position": 0, "status": S.SUCCESS},
        {"name": "heat_initialize", "position": 1, "status": S.SUCCESS},
        {"name": "heat_initialize", "position": 2, "status": S.SUCCESS},
        {"name": "heat_neumann", "position": 0, "status": S.TYPE_ERROR},
        {"name": "heat_robin", "position": 0, "status": S.TYPE_ERROR},
        {"name": "heat_robin", "position": 1, "status": S.TYPE_ERROR},
        {"name": "heat_dirichlet", "position": 0, "status": S.TYPE_ERROR},
    ]

    assert report.results == repo


def test_validate_method_fe2d_cli(finite_element_2D_template):
    cli = CLI()
    report = cli.validate(
        os.path.join("test", "impl/FEM2DTest.py"), "heat_initialize"
    )
    repo = [
        {"name": "heat_initialize", "position": 0, "status": S.SUCCESS},
        {"name": "heat_initialize", "position": 1, "status": S.SUCCESS},
        {"name": "heat_initialize", "position": 2, "status": S.SUCCESS},
    ]

    assert report.results == repo
