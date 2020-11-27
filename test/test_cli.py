import os

from pyrrha.pyrrha import CLI
from pyrrha.report import Status as S

import pytest


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


def test_generate_fe2d(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate", "FiniteElement2D")
    assert ret.success
    assert ret.stdout.strip() == finite_element_2D_template.strip()
    assert ret.stderr == ""


def test_generate_empty_base(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate")
    error_msg = "Error: Missing argument 'BASE'."
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""


def test_generate_fe2d_cli(finite_element_2D_template, script_runner):
    cli = CLI()
    report = cli.validate(os.path.join("test", "FEM2DTest.py"))
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


# def test_generate_empty_base_cli(finite_element_2D_template, script_runner):
#     ret = script_runner.run("pyrrha", "generate")
#     error_msg = "Error: Missing argument 'BASE'."
#     assert not ret.success
#     assert error_msg in ret.stderr
#     assert ret.stdout == ""
