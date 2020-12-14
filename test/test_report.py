# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

from pyrrha.report import Report, Status

import pytest


@pytest.fixture
def test_report():
    return Report()


def test_add_error_type(test_report):
    test_report.add_error_type("method_error", pos=1)
    target_result = {
        "name": "method_error",
        "position": 1,
        "status": Status.TYPE_ERROR,
    }
    assert target_result in test_report.results


def test_add_value_error(test_report):
    test_report.add_value_error("method_error")
    target_result = {
        "name": "method_error",
        "position": 0,
        "status": Status.VALUE_ERROR,
    }
    assert target_result in test_report.results


def test_add_shape_error(test_report):
    test_report.add_shape_error("method_error", pos=2)
    target_result = {
        "name": "method_error",
        "position": 2,
        "status": Status.SHAPE_ERROR,
    }
    assert target_result in test_report.results


def test_add_success(test_report):
    test_report.add_success("success_method")
    target_result = {
        "name": "success_method",
        "position": 0,
        "status": Status.SUCCESS,
    }
    assert target_result in test_report.results


def test_report_str(test_report):
    test_report.add_success("success_method")
    target_str = """RETURN
METHOD              POSITION  STATUS
---------------------------------------------
success_method      0         SUCCESS """
    lines_target = target_str.split("\n")
    text_target = "\n".join([line.strip() for line in lines_target])
    lines_report = str(test_report).split("\n")
    text_report = "\n".join([line.strip() for line in lines_report])
    assert text_report == text_target


def test_report_str_empty(test_report):
    assert str(test_report) == ""
