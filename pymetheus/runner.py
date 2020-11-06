import inspect

from .impl.finite_element_2d_impl import *
from .method import *

IMPLEMENTATIONS = {
    FiniteElement2D: FiniteElement2DImpl
}


class Runner:
    @staticmethod
    def validate_class(programmed_class, seed=None, implementations=None):
        implementations = IMPLEMENTATIONS if implementations is None \
            else implementations

        # Search the parent class own implementation
        base_method, method_implementation = Runner.__search_implementation(
            programmed_class, implementations)

        # Methods to evaluate are those with validation_classes attribute
        to_evaluate = [(name, getattr(method, 'validation_classes', None)) for
                       name, method
                       in inspect.getmembers(base_method,
                                             predicate=inspect.isfunction)
                       if getattr(method, 'validation_classes', None)]

        values = base_method.get_random_values()
        programmed_class_instance = programmed_class()
        method_implementation_instance = method_implementation()

        programmed_class_instance.set_attributes(values)
        method_implementation_instance.set_attributes(values)

        for method, validator in to_evaluate:
            print(method)
            print(validator)

            # TODO en la siguiente linea va a dar error xq depende el metodo se
            #  le pasan distintos tipos de parametros
            # Una opcion para hacerlo mas 'generico' podria ser pasar los param
            # etros a atributos de la clase, que se seteen de entrada y no
            # se pasen como parametro pero no estoy segura

            # Fixme
            # getattr(method_implementation, method)()

            # Con el resultado de esta evaluacion se iria llenando un
            # reporte de la clase Report

        return method_implementation

    @staticmethod
    def validate_method(programmed_class, target_class, method_name,
                        seed=None):
        pass

    @staticmethod
    def __search_implementation(programmed_class, implementations):
        for base, impl in implementations.items():
            if issubclass(programmed_class, base):
                return base, impl
        raise NotImplementedError
