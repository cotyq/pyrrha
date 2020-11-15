import numpy as np

from .report import Report


class Runner:
    def __init__(self, programmed_class, implementations, seed=None):
        """Look up the implementation of the programmed class according to
        its inheritance.

        Parameters
        ----------
        programmed_class : Implementation of a base class
        implementations : Dictionary containing the base classes as keys and
        the correct implementations as values.
        seed : Random seed.
        """

        self.report = Report()

        # Implementations of the base class for comparing with the programmed
        # classes.
        self.implementations = implementations

        # Search the parent class implementation
        self.base_method, self.method_impl = self.search_implementation(
            programmed_class
        )

        self.values = self.base_method.get_initial_values(seed)
        self.programmed = programmed_class()
        self.implementation = self.method_impl()

    def validate_class(self):
        """Validate the class comparing all the methods outputs according
        to the pipeline established in the abstract parent class. The
        pipeline is a list of tuples composed of the abstract methods that
        need to be implemented with their corresponding arguments as a list of
        strings.

        Returns
        -------
        Report
              Report of the comparisons performed
        """
        # Get list of abstract methods that need to be implemented.
        pipeline = self.base_method.get_pipeline()

        for method, args in pipeline:  # For each method
            self.compare_method_with_impl(method, args)

        return self.report

    def validate_method(self, method):
        """Compare the output of a given implemented method with the output of
        a previous set implementation.

        Parameters
        ----------
        method : Method to compare

        Returns
        -------
        Report
              Report of the comparisons performed
        """
        # Get list of abstract methods that need to be implemented.
        pipeline = self.base_method.get_pipeline()

        # Get the corresponding arguments for that method
        args = next(arg for met, arg in pipeline if met == method)
        self.compare_method_with_impl(method, args)

        return self.report

    def compare_method_with_impl(self, method, args):
        """Given a particular method and its args, check both
        implementations results.

        Parameters
        ----------
        method : Implemented method.
        args : List of strings containing the method arguments.

        Returns
        -------

        """
        method_name = method.__name__

        # Get the necessary params from the values dictionary into a list
        params = [self.values[key] for key in args]

        # Call both implemented methods and compare their results
        res_p = getattr(self.programmed, method_name)(*params)
        res_i = getattr(self.implementation, method_name)(*params)
        self.compare_results(res_p, res_i, method)

    def search_implementation(self, programmed_class):
        """Search the parent class implementation in the implementations
        dictionary.

        Parameters
        ----------
        programmed_class : Programmed class to validate. This Class inherits
        from a base class, that should be present in the implementations
        dictionary.
        implementations : Dictionary that contains the base class and
        correct implementations for comparing with programmed_class.

        Returns
        -------
        tuple
            Tuple containing base class and implementation.
        """
        for base, impl in self.implementations.items():
            if issubclass(programmed_class, base):
                return base, impl
        raise NotImplementedError

    def compare_results(self, res_p, res_i, method):
        """From both implementations outputs, compare types, shapes and
        values and save the comparison statuses in the report.

        Parameters
        ----------
        res_p : Output of the programmed class.
        res_i : Output of the implementation.
        method : Method compared

        """
        method_name = method.__name__
        if Runner.error_type(res_p, res_i):
            self.report.add_error_type(method_name)

        # Create list of tuples with programmed/implemented results
        res_t = zip(res_p, res_i) if type(res_p) is tuple else [(res_p, res_i)]
        for pos, (e_p, e_i) in enumerate(res_t):
            self.compare_elements(e_p, e_i, method, pos)  # Compare values

    @staticmethod
    def error_type(res_p, res_i):
        """Compare types and tuple lenghts of the outputs and return True
        if they are not the same.

        Parameters
        ----------
        res_p : Programmed class output.
        res_i : Implemented class output.

        Returns
        -------
        bool
            True if the dims/shapes aren't equal.

        """
        if type(res_p) is not type(res_i):  # Compare types
            return True
        if type(res_p) is tuple:  # If tuple
            if len(res_p) != len(res_i):  # Compare tuple length
                return True
        return False

    def compare_elements(self, e_p, e_i, method, pos=0):
        """Compare elements from two methods outputs directly. They can be
        arrays or numbers. This function is meant to be called from
        compare_results, in where tuple checks are also performed.

        Parameters
        ----------
        e_p : Output of the programmed class.
        e_i : Output of the implementation.
        method : Method to test.
        pos : Position in the output tuple (zero if it doesn't come from a
        tuple).
        """
        method_name = method.__name__

        # If both contains the 'shape' attribute (arrays)
        if hasattr(e_p, "shape") and hasattr(e_i, "shape"):
            if e_p.shape == e_i.shape:  # Same shape
                if np.all(e_p == e_i):  # Same values
                    self.report.add_success(method_name, pos)
                else:  # Same shape but different values
                    self.report.add_value_error(method_name, pos)
            else:  # Different shape
                self.report.add_shape_error(method_name, pos)

        # No shape attribute
        elif e_p == e_i:
            self.report.add_success(method_name, pos)
        else:
            self.report.add_value_error(method_name, pos)
