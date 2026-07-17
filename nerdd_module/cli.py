"""Helpers for exposing a :class:`~nerdd_module.model.Model` as a CLI command."""

import logging
import sys
from pathlib import Path
from typing import Any, Callable, List

import rich_click as click
from decorator import decorator
from stringcase import spinalcase

from .config import JobParameter
from .input import Reader
from .model import Model
from .output import FileWriter, Writer

__all__ = ["auto_cli"]

input_description = """{description}

INPUT molecules are provided as file paths or strings. The following formats are
supported:

{input_format_list}

Note that input formats shouldn't be mixed.
"""


def infer_click_type(param: JobParameter) -> click.ParamType:
    """Map a module job parameter to its Click parameter type.

    Parameters
    ----------
    param : JobParameter
        Declared module parameter.

    Returns
    -------
    click.ParamType
        Click type enforcing the parameter's declared type or choices.

    Raises
    ------
    ValueError
        If the parameter type is not supported by the generated CLI.
    """
    if param.choices is not None:
        choices = [str(c.value) for c in param.choices]
        return click.Choice(choices)

    type_map: dict[str, click.ParamType] = {
        "float": click.FLOAT,
        "integer": click.INT,
        "string": click.STRING,
        "bool": click.BOOL,
    }

    t = param.type
    if t not in type_map:
        raise ValueError(f"Unknown type {t} for parameter {param.name}")

    return type_map[t]


class AutoCLICommand(click.RichCommand):
    """Rich Click command generated from a model configuration."""

    def __init__(self, model: Model) -> None:
        self.model = model

        # collect input formats (and examples) from registered readers
        input_format_lines = []
        for ReaderClass in Reader.get_reader_mapping():
            input_format = ReaderClass.config.get("input_format")
            if input_format is None:
                continue

            examples = ReaderClass.config.get("examples", [])
            example = examples[0] if examples else None

            line = f"* {input_format}"
            if example:
                line += f' (example: "{example}")'
            input_format_lines.append(line)

        # compose CLI description
        help_text = input_description.format(
            description=self.model.config.description or "",
            input_format_list="\n".join(input_format_lines),
        )

        # collect output formats from registered writers
        self.output_format_list = [
            output_format
            for output_format, writer in Writer.get_writers(output_file=None).items()
            if isinstance(writer, FileWriter)
        ]

        params: List[click.Parameter] = [
            click.Option(
                ["--log-level"],
                default="warning",
                type=click.Choice(
                    ["debug", "info", "warning", "error", "critical"],
                    case_sensitive=False,
                ),
                help="The logging level.",
            ),
            click.Option(
                ["--format"],
                default="csv",
                type=click.Choice(self.output_format_list, case_sensitive=False),
                help="The output format.",
            ),
            click.Option(
                ["--output"],
                default="stdout",
                type=click.Path(),
                help=(
                    "The output file. If 'stdout' is specified, the output is written " "to stdout."
                ),
            ),
        ]

        # Add job parameters in the order in which they are defined in the configuration.
        for param in model.config.job_parameters:
            # convert parameter name to spinal case (e.g. "max_confs" -> "max-confs")
            param_name = spinalcase(param.name)
            params.append(
                click.Option(
                    [f"--{param_name}"],
                    default=param.default,
                    type=infer_click_type(param),
                    help=param.help_text,
                )
            )

        # Add required input parameter
        params.append(click.Argument(["input"], type=click.Path(), nargs=-1, required=True))

        # Show metavars below the help text instead of in a separate column.
        help_config = click.RichHelpConfiguration(
            text_markup="markdown",
            options_table_column_types=["required", "opt_short", "opt_long", "help"],
            options_table_help_sections=[
                "help",
                "deprecated",
                "envvar",
                "default",
                "required",
                "metavar",
            ],
        )

        # show_default=True: default values are shown in the help text
        super().__init__(
            name="main",
            callback=self._run,
            params=params,
            help=help_text,
            context_settings={
                "show_default": True,
                "rich_help_config": help_config,
            },
        )

    def format_help(
        self,
        ctx: click.Context,
        formatter: click.HelpFormatter,
    ) -> None:
        """Render model and reader examples using the current command path."""
        assert isinstance(ctx, click.RichContext)
        assert isinstance(formatter, click.RichHelpFormatter)

        #
        # Collect examples to show in footer
        #
        examples = []

        # add example_smiles from model config if available
        example_smiles = self.model.config.example_smiles
        if example_smiles is not None:
            examples.append(example_smiles)

        # add examples from registered readers if available
        for ReaderClass in Reader.get_reader_mapping():
            reader_examples = ReaderClass.config.get("examples", [])
            for example in reader_examples:
                # check if example fits on one line
                if len(example) < 120 and "\n" not in example:
                    examples.append(example)

        if len(examples) > 0:
            lines = ["Examples:"]
            lines.extend(f'* {ctx.command_path} "{example}"' for example in examples)
            formatter.config.footer_text = "\n".join(lines) + "\n"
        else:
            formatter.config.footer_text = ""

        super().format_help(ctx, formatter)

    def _run(
        self,
        input: Any,
        format: str,
        output: click.Path,
        log_level: str,
        **kwargs: Any,
    ) -> None:
        """Run the model prediction for parsed command-line arguments."""
        logging.basicConfig(level=log_level.upper())

        # write results
        assert format in self.output_format_list, f"Unknown output format: {format}"

        if str(output).lower() == "stdout":
            output_handle = sys.stdout
        else:
            output_handle = click.open_file(str(output), "wb")

        self.model.predict(
            input,
            output_format=format,
            output_file=output_handle,
            data_dir=Path("."),
            allow_paths_outside_data_dir=True,
            **kwargs,
        )


@decorator
def auto_cli(f: Callable[..., Model], *args: Any, **kwargs: Any) -> None:
    """Turn a zero-argument model factory into an executable Rich Click command.

    Parameters
    ----------
    f : Callable[..., Model]
        Factory that returns the model to expose. Its configuration determines
        command options, help text, and supported file output formats.
    *args : Any
        Positional arguments supplied by :mod:`decorator`.
    **kwargs : Any
        Keyword arguments supplied by :mod:`decorator`.
    """
    model = f()
    AutoCLICommand(model)()
