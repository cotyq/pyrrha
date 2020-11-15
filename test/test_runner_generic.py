from abc import abstractmethod

from pyrrha.method import Method
from pyrrha.report import Status
from pyrrha.runner import Runner

import pytest


@pytest.fixture
def test_base_method():
    class BaseMethod(Method):
        @classmethod
        def get_initial_values(cls, seed=None):
            return {"a": 5, "b": 7}

        def run(self):
            ...

        @classmethod
        def get_pipeline(cls):
            return [(cls.sum, ["a", "b"]), (cls.sort, ["a", "b"])]

        @abstractmethod
        def sum(self, a, b):
            raise NotImplementedError()

        @abstractmethod
        def sort(self, a, b):
            raise NotImplementedError()

    return BaseMethod


@pytest.fixture
def test_impl_method(test_base_method):
    class ImplMethod(test_base_method):
        def sum(self, a, b):
            return a + b

        def sort(self, a, b):
            return (a, b) if a < b else (b, a)

    return ImplMethod


@pytest.fixture
def test_programmed_method_accepted(test_base_method):
    class ProgrammedMethodAccepted(test_base_method):
        def sum(self, a, b):
            return a + b

        def sort(self, a, b):
            return (a, b) if a < b else (b, a)

    return ProgrammedMethodAccepted


@pytest.fixture
def test_programmed_method_value_error(test_base_method):
    class ProgrammedMethodValueError(test_base_method):
        def sum(self, a, b):
            return a

        def sort(self, a, b):
            return (a, b) if a > b else (b, a)

    return ProgrammedMethodValueError


@pytest.fixture
def test_programmed_method_tuple_error(test_base_method):
    class ProgrammedMethodTypeError(test_base_method):
        def sum(self, a, b):
            return a, b

        def sort(self, a, b):
            return a, a, b

    return ProgrammedMethodTypeError


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
    ]

    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_class_value_error(
    test_programmed_method_value_error, implementations
):
    runner = Runner(test_programmed_method_value_error, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.VALUE_ERROR},
        {"name": "sort", "position": 0, "status": Status.VALUE_ERROR},
        {"name": "sort", "position": 1, "status": Status.VALUE_ERROR},
    ]

    assert all([a == b for a, b in zip(runner.report.results, target_result)])


def test_validate_class_tuple_error(
    test_programmed_method_tuple_error, implementations
):
    runner = Runner(test_programmed_method_tuple_error, implementations)

    target_result = [
        {"name": "sum", "position": 0, "status": Status.TYPE_ERROR},
        {"name": "sort", "position": 0, "status": Status.TYPE_ERROR},
    ]

    assert all([a == b for a, b in zip(runner.report.results, target_result)])
