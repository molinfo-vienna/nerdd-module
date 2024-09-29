import logging
import os
import sys

import rich_click as click
from decorator import decorator
from stringcase import spinalcase  # type: ignore

__all__ = ["auto_cli"]

input_description = """{description}

INPUT molecules are provided as file paths or strings. The following formats are 
supported:

{input_format_list}

Note that input formats shouldn't be mixed.
"""


def infer_click_type(param):
    if "choices" in param:
        choices = [c["value"] for c in param["choices"]]
        return click.Choice(choices)

    type_map = {
        "float": float,
        "int": int,
        "str": str,
        "bool": bool,
    }

    return type_map[param.get("type")]


@decorator
def auto_cli(f, *args, **kwargs):
    # infer the command name
    command_name = os.path.basename(sys.argv[0])

    # get the model
    model = f()

    config = model.get_config()

    # compose cli description
    description = config.get("description", "")

    input_format_list = "\n".join([f"* {fmt}" for fmt in ["smiles", "sdf", "inchi"]])

    help_text = input_description.format(
        description=description, input_format_list=input_format_list
    )

    output_format_list = ["sdf", "csv"]

    # compose footer with examples
    examples = []
    if "example_smiles" in config:
        examples.append(config["example_smiles"])

    if len(examples) > 0:
        footer = "Examples:\n"
        for example in examples:
            footer += f'* {command_name} "{example}"\n'
    else:
        footer = ""

    # show_default=True: default values are shown in the help text
    # show_metavars_column=False: the column types are not in a separate column
    # append_metavars_help=True: the column types are shown below the help text
    @click.command(context_settings={"show_default": True}, help=help_text)
    @click.rich_config(
        help_config=click.RichHelpConfiguration(
            use_markdown=True,
            show_metavars_column=False,
            append_metavars_help=True,
            footer_text=footer,
        )
    )
    @click.argument("input", type=click.Path(), nargs=-1, required=True)
    def main(
        input,
        format: str,
        output: click.Path,
        log_level: str,
        **kwargs,
    ):
        logging.basicConfig(level=log_level.upper())

        # write results
        assert format in output_format_list, f"Unknown output format: {format}"

        if str(output).lower() == "stdout":
            output_handle = sys.stdout
        else:
            output_handle = click.open_file(str(output), "wb")

        model.predict(input, output_format=format, output_file=output_handle, **kwargs)

    #
    # Add job parameters
    #
    for param in config.get("job_parameters", []):
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
        type=click.Choice(
            ["debug", "info", "warning", "error", "critical"], case_sensitive=False
        ),
        help="The logging level.",
    )(main)

    return main()
