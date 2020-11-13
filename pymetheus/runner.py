import numpy as np

from .impl.finite_element_2d_impl import FiniteElement2DImpl
from .method import FiniteElement2D
from .report import Report

IMPLEMENTATIONS = {FiniteElement2D: FiniteElement2DImpl}


class Runner:
    @staticmethod
    def validate_class(programmed_class, seed=None, implementations=None):
        # Search the parent class own implementation
        base_method, method_impl = Runner.search_implementation(
            programmed_class, implementations
        )

        values = base_method.get_random_values()
        programmed_class_instance = programmed_class()
        method_impl_instance = method_impl()

        pipeline = base_method.get_pipeline()
        report = Report()

        for method, args in pipeline:
            method_name = method.__name__
            params = [values[key] for key in args]
            res_p = getattr(programmed_class_instance, method_name)(*params)
            res_i = getattr(method_impl_instance, method_name)(*params)
            Runner().__compare_results(res_p, res_i, method, report)

        return report

    @staticmethod
    def validate_method(
        programmed_class, target_class, method_name, seed=None
    ):
        pass

    @staticmethod
    def search_implementation(programmed_class, implementations=None):
        implementations = (
            IMPLEMENTATIONS if implementations is None else implementations
        )

        for base, impl in implementations.items():
            if issubclass(programmed_class, base):
                return base, impl
        raise NotImplementedError

    @staticmethod
    def __compare_results(res_p, res_i, method, report):
        method_name = method.__name__
        if type(res_p) is not type(res_i):
            report.add_error_type(method_name)
        elif type(res_p) is tuple:
            if len(res_p) != len(res_i):
                report.add_error_type(method_name)
            else:
                for pos, (e_p, e_i) in enumerate(zip(res_p, res_i)):
                    Runner.__compare_elements(e_p, e_i, method, report, pos)

        else:  # Comparar elementos directamente
            Runner.__compare_elements(res_p, res_i, method, report)

    @staticmethod
    def __compare_elements(e_p, e_i, method, report, pos=0):
        method_name = method.__name__

        # Si ambos tienen shape, se comparan los valores
        if hasattr(e_p, "shape") and hasattr(e_i, "shape"):
            if e_p.shape == e_i.shape:
                if np.all(e_p == e_i):  # Las salidas coinciden
                    report.add_success(method_name, pos)
                else:  # Shapes iguales, pero difieren en valor
                    report.add_value_error(method_name, pos)
            else:  # Distinto shape
                report.add_shape_error(method_name, pos)

        # Si no tienen shape, se comparan los valores
        elif e_p == e_i:
            report.add_success(method_name, pos)
        else:
            report.add_value_error(method_name, pos)
