import logging
import os
import sys

import rich_click as click
from decorator import decorator
from nerdd_module.io import WriterRegistry
from stringcase import spinalcase

__all__ = ["auto_cli"]

input_description = """{description}

INPUT molecules are provided as file paths or strings. The following formats are 
supported:

{format_list}

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

    config = model.get_config().get_dict()

    # compose cli description
    description = config.get("description", "")

    format_list = "\n".join([f"* {fmt}" for fmt in ["smiles", "sdf", "inchi"]])

    help_text = input_description.format(
        description=description, format_list=format_list
    )

    # compose footer with examples
    examples = []
    if "example_smiles" in config:
        examples.append(config["example_smiles"])

    if len(examples) > 0:
        footer = "Examples:\n"
        for example in examples:
            footer += f"* {command_name} {example}\n"
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

        df_result = model.predict(input, **kwargs)

        # write results
        assert format in WriterRegistry().supported_formats
        writer = WriterRegistry().get_writer(format)

        if output.lower() == "stdout":
            assert not writer.writes_bytes, "stdout does not support binary output"
            output_handle = sys.stdout
        else:
            mode = "wb" if writer.writes_bytes else "w"
            output_handle = click.open_file(output, mode)

        entries = (tup._asdict() for tup in df_result.itertuples(index=False))
        writer.write(output_handle, entries)

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
        type=click.Choice(WriterRegistry().supported_formats, case_sensitive=False),
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
