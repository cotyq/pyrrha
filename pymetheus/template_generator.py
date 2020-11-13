import abc
import inspect

from jinja2 import Template


TEMPLATE = Template(
    """
class {{cls_name}}({{cls_base_name}}):
{% for method in methods %}
    {{method}}:
        pass
{% endfor %}
"""
)


class TemplateGenerator(abc.ABC):
    @staticmethod
    def gen_template(cls):

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
        ).strip()

        return tpl


# import method
# clase = TemplateGenerator.gen_template(method.FiniteElement2D)
