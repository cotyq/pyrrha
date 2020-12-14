# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

"""Public module."""
import abc
import inspect

from jinja2 import Template

# template format to generate each method
TEMPLATE = Template(
    """from pyrrha.method import {{cls_base_name}}


class {{cls_name}}({{cls_base_name}}):
{% for method in methods %}
    def {{method}}:
        pass
{% endfor %}
"""
)


class TemplateGenerator(abc.ABC):
    """Class to generate Template Class of Numerical Method.

    class inherited from ABC
    """

    @staticmethod
    def gen_template(cls):
        """Generate the template according to the class received.

        Parameters
        ----------
        cls : class
               class received.

        Returns
        -------
        string with template generated.
        """
        cls_base_name = cls.__name__
        cls_name = cls_base_name + "Template"

        methods = []

        abstracts = vars(cls)["__abstractmethods__"]
        for abst_name in sorted(abstracts):
            abst = getattr(cls, abst_name)
            signature = inspect.signature(abst)
            source = "{}{}".format(abst_name, signature)
            methods.append(source)

        tpl = TEMPLATE.render(
            cls_name=cls_name, cls_base_name=cls_base_name, methods=methods
        )

        return tpl
