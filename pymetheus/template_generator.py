import abc
import inspect
import attr

from jinja2 import Template

TEMPLATE = Template("""
class {{cls_name}}({{cls_base_name}}):
{% for method in methods %}
{{method}}
{% endfor %}
""")

class TemplateGenerator(abc.ABC):
    
    @classmethod
    def gen_template(cls):

        cls_base_name = cls.__name__
        cls_name = cls_base_name.replace("Template", "")


        methods = []

        abstracts = vars(cls)["__abstractmethods__"]
        for abst_name in sorted(abstracts):
            abst = getattr(cls, abst_name)
            source = inspect.getsource(abst)
            source = "\n".join(source.splitlines()[1:])
            methods.append(source)

        tpl = TEMPLATE.render(
            cls_name=cls_name,
            cls_base_name=cls_base_name,
            methods=methods).strip()

        return tpl

@attr.s()      
class FiniteElement2DTemplate(TemplateGenerator):

    @abc.abstractmethod
    def heat_initialize(self):
        pass

    @abc.abstractmethod
    def heat_dirichlet(self):
        pass

    @abc.abstractmethod
    def heat_neumann(self):
        pass

    @abc.abstractmethod
    def heat_robin(self):
        pass

    @abc.abstractmethod
    def gen_system(self):
        pass

    @abc.abstractmethod
    def heat_pcond(self):
        pass
    
    @abc.abstractmethod
    def heat_solve(self):
        pass

@attr.s()      
class FiniteVolumne2DTemplate(TemplateGenerator):
  
    @abc.abstractmethod
    def heat_dirichlet(self):
        pass

    @abc.abstractmethod
    def heat_neumann(self):
        pass

    @abc.abstractmethod
    def heat_robin(self):
        pass
  
@attr.s()      
class FiniteDifference2DTemplate(TemplateGenerator):
  
    @abc.abstractmethod
    def heat_dirichlet(self):
        pass

    @abc.abstractmethod
    def heat_neumann(self):
        pass

    @abc.abstractmethod
    def heat_robin(self):
        pass