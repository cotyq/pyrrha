import inspect
import impl


class Runner:
    @staticmethod
    def validate_class(programmed_class, seed=None):
        method_implementation = Runner.search_implementation(programmed_class)
        if not method_implementation:
            raise NotImplementedError()

        base_method = programmed_class.__bases__[0]

        # Methods to evaluate are those with validation_classes attribute
        to_evaluate = [(name, getattr(method, 'validation_classes', None))
                       for name, method
                       in inspect.getmembers(base_method, predicate=inspect.isfunction)
                       if getattr(method, 'validation_classes', None)]

        values = base_method.get_random_values()
        programmed_class_instance = programmed_class()
        method_implementation_instance = method_implementation()

        programmed_class_instance.set_values(values)
        method_implementation_instance.set_values(values)

        for method, validator in to_evaluate:
            print(method)
            print(validator)

            # TODO en la siguiente linea va a dar error xq depende el metodo se le pasan distintos tipos de parametros
            # Una opcion para hacerlo mas 'generico' podria ser pasar los parametros a atributos de la clase, que se
            # seteen de entrada y no se pasen como parametro pero no estoy segura

            # Fixme
            # getattr(method_implementation, method)()

            # Con el resultado de esta evaluacion se iria llenando un reporte de la clase Report

        return method_implementation

    @staticmethod
    def validate_method(programmed_class, target_class, method_name, seed=None):
        pass

    @staticmethod
    def search_implementation(programmed_class):
        implementations = [obj for name, obj in inspect.getmembers(impl) if inspect.isclass(obj)]
        for impl_method in implementations:
            base = impl_method.__bases__
            if base == programmed_class.__bases__:
                return impl_method
        return None
