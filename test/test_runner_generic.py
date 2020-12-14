# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

from abc import abstractmethod

import numpy as np

from pyrrha.method import Method
from pyrrha.report import Status
from pyrrha.runner import Runner

import pytest


@pytest.fixture
def test_base_method():
    class BaseMethod(Method):
        @classmethod
        def get_initial_values(cls, seed=None):
            a = np.eye(3)
            b = 2 * np.ones((3, 3))
            return {"a": a, "b": b}

        def run(self):
            ...

        @classmethod
        def get_pipeline(cls):
            return [
                (cls.sum, ["a", "b"]),
                (cls.sort, ["a", "b"]),
                (cls.get_first_elem, ["a"]),
            ]

        @abstractmethod
        def sum(self, a, b):
            raise NotImplementedError()

        @abstractmethod
        def sort(self, a, b):
            raise NotImplementedError()

        @abstractmethod
        def get_first_elem(self, a):
            raise NotImplementedError()

    return BaseMethod


@pytest.fixture
def test_impl_method(test_base_method):
    class ImplMethod(test_base_method):
        def sum(self, a, b):
            return a + b

        def sort(self, a, b):
            return (a, b) if a[0, 0] < b[0, 0] else (b, a)

        def get_first_elem(self, a):
            return float(a[0, 0])

    return ImplMethod


@pytest.fixture
def test_programmed_method_accepted(test_base_method):
    class ProgrammedMethodAccepted(test_base_method):
        def sum(self, a, b):
            return a + b

        def sort(self, a, b):
            return (a, b) if a[0, 0] < b[0, 0] else (b, a)

        def get_first_elem(self, a):
            return float(a[0, 0])

    return ProgrammedMethodAccepted


@pytest.fixture
def test_programmed_method_value_error(test_base_method):
    class ProgrammedMethodValueError(test_base_method):
        def sum(self, a, b):
            return a

        def sort(self, a, b):
            return (a, b) if a[0, 0] > b[0, 0] else (b, a)

        def get_first_elem(self, a):
            return 42

    return ProgrammedMethodValueError


@pytest.fixture
def test_programmed_method_tuple_error(test_base_method):
    class ProgrammedMethodTypeError(test_base_method):
        def sum(self, a, b):
            return a, b

        def sort(self, a, b):
            return a, a, b

        def get_first_elem(self, a):
            return float(a[0, 0])

    return ProgrammedMethodTypeError


@pytest.fixture
def test_programmed_method_shape_error(test_base_method):
    class ProgrammedMethodShapeError(test_base_method):
        def sum(self, a, b):
            return np.eye(4)

        def sort(self, a, b):
            return (a, b) if a[0, 0] < b[0, 0] else (b, a)

        def get_first_elem(self, a):
            return float(a[0, 0])

    return ProgrammedMethodShapeError


@pytest.fixture
def test_programmed_method_shape_no_shape(test_base_method):
    class ProgrammedMethodShapeNoShapeError(test_base_method):
        def sum(self, a, b):
            return 5

        def sort(self, a, b):
            return (a, b) if a[0, 0] < b[0, 0] else (b, a)

        def get_first_elem(self, a):
            return a

    return ProgrammedMethodShapeNoShapeError


@pytest.fixture
def implementations(test_base_method, test_impl_method):
    return {test_base_method: test_impl_method}


def test_validate_class_accepted(
    test_programmed_method_accepted, implementations
):
    runner = Runner(test_programmed_method_accepted, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.SUCCESS},
        {"name": "sort", "position": 0, "status": Status.SUCCESS},
        {"name": "sort", "position": 1, "status": Status.SUCCESS},
        {"name": "get_first_elem", "position": 0, "status": Status.SUCCESS},
    ]

    runner.validate_class()

    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_class_value_error(
    test_programmed_method_value_error, implementations
):
    runner = Runner(test_programmed_method_value_error, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.VALUE_ERROR},
        {"name": "sort", "position": 0, "status": Status.VALUE_ERROR},
        {"name": "sort", "position": 1, "status": Status.VALUE_ERROR},
        {
            "name": "get_first_elem",
            "position": 0,
            "status": Status.VALUE_ERROR,
        },
    ]

    runner.validate_class()

    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_class_tuple_error(
    test_programmed_method_tuple_error, implementations
):
    runner = Runner(test_programmed_method_tuple_error, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.TYPE_ERROR},
        {"name": "sort", "position": 0, "status": Status.TYPE_ERROR},
        {"name": "get_first_elem", "position": 0, "status": Status.SUCCESS},
    ]

    runner.validate_class()

    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_class_shape_error(
    test_programmed_method_shape_error, implementations
):
    runner = Runner(test_programmed_method_shape_error, implementations)

    result = {"name": "sum", "position": 0, "status": Status.SHAPE_ERROR}

    runner.validate_class()

    assert result in runner.report.results


def test_validate_method_shape_no_shape_error(
    test_programmed_method_shape_no_shape, implementations
):
    runner = Runner(test_programmed_method_shape_no_shape, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.TYPE_ERROR},
        {"name": "sort", "position": 0, "status": Status.SUCCESS},
        {"name": "sort", "position": 1, "status": Status.SUCCESS},
        {"name": "get_first_elem", "position": 0, "status": Status.TYPE_ERROR},
    ]

    runner.validate_class()
    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_method_accepted(
    test_programmed_method_accepted, implementations
):
    runner = Runner(test_programmed_method_accepted, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.SUCCESS},
    ]

    runner.validate_method("sum")

    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_method_value_error(
    test_programmed_method_value_error, implementations
):
    runner = Runner(test_programmed_method_value_error, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.VALUE_ERROR},
    ]

    runner.validate_method("sum")

    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_method_tuple_error(
    test_programmed_method_tuple_error, implementations
):
    runner = Runner(test_programmed_method_tuple_error, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.TYPE_ERROR},
    ]

    runner.validate_method("sum")

    assert len(runner.report.results) == len(target_result)
    assert all([a == b for a, b in zip(runner.report.results, target_result)])
