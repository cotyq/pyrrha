"""Report handling."""

from enum import Enum


class Status(Enum):
    """Status class.

    Possible statuses of a method run.
    """

    SUCCESS = 0
    TYPE_ERROR = 1
    VALUE_ERROR = 2
    SHAPE_ERROR = 3


class Report:
    """Report class.

    Store and show the status of pyrrha validations.
    """

    def __init__(self):
        self.results = []

    def __str__(self):
        """Return the string representation of the object."""
        if not self.results:
            return ""

        out = "{:20}{:10}{:15}".format("", "RETURN", "")
        out += "\n{:20}{:10}{:15}".format("METHOD", "POSITION", "STATUS")
        out += "\n" + "-" * 45
        for r in self.results:
            out += "\n{:20}{:10}{:15}".format(
                r["name"], str(r["position"]), r["status"].name
            )
        return out

    def add_error_type(self, method_name, pos=0):
        """Add error type result to the report.

        Parameters
        ----------
        method_name : str
            Name of the executed method.
        pos: int
            Position in the output tuple.
        """
        self.results.append(
            {"name": method_name, "position": pos, "status": Status.TYPE_ERROR}
        )

    def add_value_error(self, method_name, pos=0):
        """Add value error result to the report.

        Parameters
        ----------
        method_name : str
            Name of the executed method.
        pos: int
            Position in the output tuple.
        """
        self.results.append(
            {
                "name": method_name,
                "position": pos,
                "status": Status.VALUE_ERROR,
            }
        )

    def add_shape_error(self, method_name, pos=0):
        """Add shape error result to the report.

        Parameters
        ----------
        method_name : str
            Name of the executed method.
        pos: int
            Position in the output tuple.
        """
        self.results.append(
            {
                "name": method_name,
                "position": pos,
                "status": Status.SHAPE_ERROR,
            }
        )

    def add_success(self, method_name, pos=0):
        """Add successful result to the report.

        Parameters
        ----------
        method_name : str
            Name of the executed method.
        pos: int
            Position in the output tuple.
        """
        self.results.append(
            {"name": method_name, "position": pos, "status": Status.SUCCESS}
        )
