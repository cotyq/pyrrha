__version__ = "0.1"

import inspect

import clize

from .constants import IMPLEMENTATIONS
from .template_generator import TemplateGenerator

VERSION = __version__


class CLI:
    """Pyrrha console client."""

    footnotes = "\n".join(
        [
            "MIT License.",
            "Copyright (c) 2020.",
            "Diego Sklar, Constanza Quaglia, Franco Matzkin.",
        ]
    )

    def get_commands(self):
        methods = {}
        for k in dir(self):
            if k.startswith("_"):
                continue
            v = getattr(self, k)
            if inspect.ismethod(v) and k != "get_commands":
                methods[k] = v
        return methods

    def version(self):
        """Print pyrrha version."""
        print(VERSION)

    def generate(self, base, *, output=""):
        """Generate template from given base class

        Parameters
        ----------
        output: str
            The name of the generated class
        base: str
            The name of the base file
        """
        base_class = self._get_base_class(base)
        print(TemplateGenerator.gen_template(base_class))

    def _get_base_class(self, base):
        base_class = [b for b in IMPLEMENTATIONS.keys() if b.__name__ == base]
        if not base_class:
            raise clize.ArgumentError
        return base_class[0]


def main():
    """Run the pyrrha CLI interface."""
    cli = CLI()
    commands = tuple(cli.get_commands().values())
    clize.run(*commands, description=cli.__doc__, footnotes=cli.footnotes)


if __name__ == "__main__":
    main()
