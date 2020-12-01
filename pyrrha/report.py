from enum import Enum


class Status(Enum):
    SUCCESS = 0
    TYPE_ERROR = 1
    VALUE_ERROR = 2
    SHAPE_ERROR = 3


class Report:
    def __init__(self):
        self.results = []

    def __str__(self):
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
        self.results.append(
            {"name": method_name, "position": pos, "status": Status.TYPE_ERROR}
        )

    def add_value_error(self, method_name, pos=0):
        self.results.append(
            {
                "name": method_name,
                "position": pos,
                "status": Status.VALUE_ERROR,
            }
        )

    def add_shape_error(self, method_name, pos=0):
        self.results.append(
            {
                "name": method_name,
                "position": pos,
                "status": Status.SHAPE_ERROR,
            }
        )

    def add_success(self, method_name, pos=0):
        self.results.append(
            {"name": method_name, "position": pos, "status": Status.SUCCESS}
        )
