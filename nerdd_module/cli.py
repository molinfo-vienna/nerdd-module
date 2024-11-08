import logging
import sys
from typing import Any, Callable

import rich_click as click
from decorator import decorator
from stringcase import spinalcase  # type: ignore

from .model import Model

__all__ = ["auto_cli"]

input_description = """{description}

INPUT molecules are provided as file paths or strings. The following formats are
supported:

{input_format_list}

Note that input formats shouldn't be mixed.
"""


def infer_click_type(param: dict) -> click.ParamType:
    if "choices" in param:
        choices = [c["value"] for c in param["choices"]]
        return click.Choice(choices)

    type_map = {
        "float": click.FLOAT,
        "int": click.INT,
        "str": click.STRING,
        "bool": click.BOOL,
    }

    if "type" not in param:
        raise ValueError(f"Parameter {param['name']} does not have a type")

    t = param["type"]

    if t not in type_map:
        raise ValueError(f"Unknown type {t} for parameter {param['name']}")

    return type_map[t]


@decorator
def auto_cli(f: Callable[..., Model], *args: Any, **kwargs: Any) -> None:
    # infer the command name
    # command_name = os.path.basename(sys.argv[0])

    # get the model
    model = f()

    # compose cli description
    input_format_list = "\n".join([f"* {fmt}" for fmt in ["smiles", "sdf", "inchi"]])

    help_text = input_description.format(
        description=model.description, input_format_list=input_format_list
    )

    output_format_list = ["sdf", "csv"]

    # compose footer with examples
    # TODO: add examples
    # examples = []
    # if "example_smiles" in config:
    #     examples.append(config["example_smiles"])

    # if len(examples) > 0:
    #     footer = "Examples:\n"
    #     for example in examples:
    #         footer += f'* {command_name} "{example}"\n'
    # else:
    #     footer = ""
    footer = ""

    #
    # Define the CLI entry point
    #
    def main(
        input: Any,
        format: str,
        output: click.Path,
        log_level: str,
        **kwargs: Any,
    ) -> None:
        logging.basicConfig(level=log_level.upper())

        # write results
        assert format in output_format_list, f"Unknown output format: {format}"

        if str(output).lower() == "stdout":
            output_handle = sys.stdout
        else:
            output_handle = click.open_file(str(output), "wb")

        model.predict(input, output_format=format, output_file=output_handle, **kwargs)

    #
    # Add required input parameter
    #
    main = click.argument("input", type=click.Path(), nargs=-1, required=True)(main)

    #
    # Add job parameters
    #
    for param in model.job_parameters:
        # convert parameter name to spinal case (e.g. "max_confs" -> "max-confs")
        param_name = spinalcase(param["name"])
        main = click.option(
            f"--{param_name}",
            default=param.get("default", None),
            type=infer_click_type(param),
            help=param.get("help_text", None),
        )(main)

    #
    # Add other options
    #
    main = click.option(
        "--output",
        default="stdout",
        type=click.Path(),
        help="The output file. If 'stdout' is specified, the output is written to stdout.",
    )(main)

    main = click.option(
        "--format",
        default="csv",
        type=click.Choice(output_format_list, case_sensitive=False),
        help="The output format.",
    )(main)

    main = click.option(
        "--log-level",
        default="warning",
        type=click.Choice(["debug", "info", "warning", "error", "critical"], case_sensitive=False),
        help="The logging level.",
    )(main)

    #
    # Create Rich command
    #

    # show_metavars_column=False: the column types are not in a separate column
    # append_metavars_help=True: the column types are shown below the help text
    main = click.rich_config(
        help_config=click.RichHelpConfiguration(
            use_markdown=True,
            show_metavars_column=False,
            append_metavars_help=True,
            footer_text=footer,
        )
    )(main)

    # show_default=True: default values are shown in the help text
    main = click.command(context_settings={"show_default": True}, help=help_text)(main)

    main()
