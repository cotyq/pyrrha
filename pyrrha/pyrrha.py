__version__ = "0.1"

from inspect import getmro, isclass, ismethod

import typer

from .constants import IMPLEMENTATIONS
from .method import Method
from .runner import Runner
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
        app = typer.Typer()
        for k in dir(self):
            if k.startswith("_"):
                continue
            v = getattr(self, k)
            if ismethod(v) and k != "get_commands":
                decorator = app.command()
                decorator(v)
        return app

    def version(self):
        """Print pyrrha version."""
        print(VERSION)

    def generate(self, base, output=""):
        """Generate template from given base class

        Parameters
        ----------
        output: str
            The name of the generated class
        base: str
            The name of the base file
        """
        base_class = self._get_base_class(base)

        template = TemplateGenerator.gen_template(base_class)
        if output == "":
            print(template)
        else:
            try:
                with open(output, "w") as file:
                    file.write(template)
            except FileNotFoundError:
                raise typer.BadParameter(
                    "wrong output file name ({})".format(output)
                )

    def validate(self, file, method=""):
        try:
            a = {}
            exec(open(file).read(), globals(), a)
            globals().update(a)
            chk = None
            for k, v in a.items():
                if (
                    isclass(v)
                    and getmro(v)[1] != Method
                    and issubclass(v, Method)
                ):
                    chk = v
                    break
            if chk is None:
                raise typer.BadParameter(
                    "no appropiate class found in {}".format(file)
                )

            runner = Runner(chk, IMPLEMENTATIONS)
            report = runner.validate_class()
            print(report.results)
            return report

        except FileNotFoundError:
            raise typer.BadParameter("file not found ({})".format(file))

    def _get_base_class(self, base):
        base_class = [b for b in IMPLEMENTATIONS.keys() if b.__name__ == base]
        if not base_class:
            raise typer.BadParameter("wrong class name ({}).".format(base))
        return base_class[0]


def main():
    """Run the pyrrha CLI interface."""
    cli = CLI()
    app = cli.get_commands()
    app()


if __name__ == "__main__":
    main()
