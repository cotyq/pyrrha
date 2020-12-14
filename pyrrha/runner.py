# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

"""Runner class for method/class comparison.

The Runner class allows to compare two different implementations of a
certain abstract class, by comparing a particular method only, or the whole
set of abstract methods that need to be implemented.
"""

import numpy as np

from .report import Report


class Runner:
    """Load the implementation of a certain class looking its inheritance.

    Parameters
    ----------
    programmed_class : Method
        Implementation of a base class.
    implementations : dict
        Dictionary containing the base classes as keys and the correct
        implementations as values.
    seed : int
        Seed for the random generation.

    Attributes
    ----------
    implementations : dict
        Implementations of the base class for comparing with the programmed
        classes.
    base_method : class
        Parent of programmed_class
    method_impl : class
        Sibling of programmed_class, which will be used for comparing.
    values : dict
        Dictionary of initial arrays used for testing the classes methods.
    programmed : Method
        Instance of programmed_class.
    implementation : Method
        Instance of programmed_class.
    """

    def __init__(self, programmed_class, implementations, seed=None):
        self.report = Report()

        self.implementations = implementations

        self.base_method, self.method_impl = self.search_implementation(
            programmed_class
        )

        self.values = self.base_method.get_initial_values(seed)
        try:
            self.programmed = programmed_class()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize programmed class ({e}).")
        self.implementation = self.method_impl()

    def validate_class(self):
        """Obtain the method pipeline and compare both implementations.

        Validate the class comparing all the methods outputs according
        to the pipeline established in the abstract parent class. The
        pipeline is a list of tuples composed of the abstract methods, that
        need to be implemented with their corresponding arguments as a list of
        strings. The compare_method_with_impl method will be called,
        which will compare the results of the previously set classes.

        Returns
        -------
        Report
              Report of the comparisons performed
        """
        # Get list of abstract methods that need to be implemented.
        pipeline = self.base_method.get_pipeline()

        for method, args in pipeline:  # For each method
            self.compare_method_with_impl(method.__name__, args)

        return self.report

    def validate_method(self, method_name):
        """Validate a single method against the implementation.

        Compare the output of a given implemented method with the output of
        a previous set implementation. The result will be stored in
        self.report.

        Parameters
        ----------
        method_name : Method to compare
        """
        # Get list of abstract methods that need to be implemented.
        pipeline = self.base_method.get_pipeline()

        # Get the corresponding arguments for that method
        try:
            args = next(
                arg for met, arg in pipeline if met.__name__ == method_name
            )
            self.compare_method_with_impl(method_name, args)
        except StopIteration:
            raise ValueError(
                "The method '{}' is not defined in the "
                "class.".format(method_name)
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute method {method_name} ({e})."
            )
        return self.report

    def compare_method_with_impl(self, method_name, args):
        """Run the same method in both implementations and compare results.

        Given a particular method and its args, check both
        implementations results. The result will be stored in self.report.

        Parameters
        ----------
        method_name : Implemented method.
        args : List of strings containing the method arguments.

        """
        # Get the necessary params from the values dictionary into a list
        params = [self.values[key] for key in args]

        # Call both implemented methods and compare their results
        try:
            res_p = getattr(self.programmed, method_name)(*params)
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute method {method_name} ({e})."
            )
        res_i = getattr(self.implementation, method_name)(*params)
        self.compare_results(res_p, res_i, method_name)

    def search_implementation(self, programmed_class):
        """Locate the parent class implementation of a particular class.

        Search the parent class implementation in the implementations
        dictionary.

        Parameters
        ----------
        programmed_class : Programmed class to validate. This Class inherits
        from a base class, that should be present in the implementations
        dictionary.

        Returns
        -------
        tuple
            Tuple containing base class and implementation.
        """
        for base, impl in self.implementations.items():
            if issubclass(programmed_class, base):
                return base, impl
        raise NotImplementedError

    def compare_results(self, res_p, res_i, method_name):
        """Compare two outputs depending of its type.

        From both implementations outputs, compare types, shapes and
        values and save the comparison statuses in the report.

        Parameters
        ----------
        res_p : Output of the programmed class.
        res_i : Output of the implementation.
        method_name : Compared method.

        """
        res_p = float(res_p) if type(res_p) == int else res_p
        res_i = float(res_i) if type(res_i) == int else res_i

        if Runner.error_type(res_p, res_i):
            self.report.add_error_type(method_name)
        else:
            # Create list of tuples with programmed/implemented results
            res_t = (
                zip(res_p, res_i) if type(res_p) is tuple else [(res_p, res_i)]
            )
            for pos, (e_p, e_i) in enumerate(res_t):
                self.compare_elements(
                    e_p, e_i, method_name, pos
                )  # Compare values

    @staticmethod
    def error_type(res_p, res_i):
        """Type error output checking.

        Compare types and tuple lenghts of the outputs and return True if they
        are not the same.

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

    def compare_elements(self, e_p, e_i, method_name, pos=0):
        """Compare outputs elements and save to report.

        Compare elements from two methods outputs directly. They can be arrays
        or numbers. This function is meant to be called from compare_results,
        in where tuple checks are also performed. The results will be stored in
        self.report.


        Parameters
        ----------
        e_p : Output of the programmed class.
        e_i : Output of the implementation.
        method_name : Method to test.
        pos : Position in the output tuple (zero if it doesn't come from a
        tuple).
        """
        # If both contains the 'shape' attribute (arrays)
        if hasattr(e_p, "shape") and hasattr(e_i, "shape"):
            if e_p.shape == e_i.shape:  # Same shape
                if np.all(e_p == e_i):  # Same values
                    self.report.add_success(method_name, pos)
                else:  # Same shape but different values
                    self.report.add_value_error(method_name, pos)
            else:  # Different shape
                self.report.add_shape_error(method_name, pos)

        # For example: tuple and matrix
        elif (
            hasattr(e_p, "shape")
            and not hasattr(e_i, "shape")
            or not hasattr(e_p, "shape")
            and hasattr(e_i, "shape")
        ):
            self.report.add_error_type(method_name, pos)

        # No shape attribute
        elif e_p == e_i:
            self.report.add_success(method_name, pos)
        else:
            self.report.add_value_error(method_name, pos)
