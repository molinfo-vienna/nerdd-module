from typing import Any, Iterator

import click
import pytest
from click.testing import CliRunner

from nerdd_module.cli import AutoCLICommand
from nerdd_module.config import JobParameter
from nerdd_module.input import ExploreCallable, MoleculeEntry, Reader
from nerdd_module.input.reader_config import ReaderConfig
from nerdd_module.model import Model
from nerdd_module.tests.models import MolWeightModel


def invoke_help(model=None, prog_name: str = "model") -> tuple[int, str]:
    if model is None:
        model = MolWeightModel()

    result = CliRunner().invoke(AutoCLICommand(model), ["--help"], prog_name=prog_name, color=False)
    # Rich Click forces ANSI styling in some CI environments, so compare plain text.
    output = click.unstyle(result.output)
    return result.exit_code, output


@pytest.fixture
def reset_reader_registry():
    # in the following tests we manipulate the reader registry
    # -> we use this fixture to reset it after each test
    registry = Reader.get_reader_mapping()
    original_registry = registry.copy()
    try:
        yield
    finally:
        registry[:] = original_registry


def test_help_uses_click_command_path_for_examples():
    exit_code, output = invoke_help(prog_name="python -m example.model")

    assert exit_code == 0
    assert "Usage: python -m example.model [OPTIONS] INPUT..." in output
    assert "• smiles" in output
    assert "• sdf" in output
    assert "• inchi" in output
    assert 'python -m example.model "compounds.smiles"' in output


def test_help_omits_missing_description():
    class ModelWithoutDescription(Model):
        def _predict_mols(self, mols):
            return [{} for _ in mols]

    exit_code, output = invoke_help(ModelWithoutDescription())

    assert exit_code == 0
    assert "None" not in output


def test_reader_without_config_gets_empty_config(reset_reader_registry):
    class UnconfiguredReader(Reader):
        def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
            return iter(())

    assert UnconfiguredReader.config == ReaderConfig()

    exit_code, _ = invoke_help()
    assert exit_code == 0


def test_examples_from_registered_readers_are_shown(reset_reader_registry):
    # we check if our example reader is not registered yet
    exit_code, output = invoke_help()
    assert exit_code == 0
    assert 'model "custom-example"' not in output

    class ExampleReader(Reader):
        config = ReaderConfig(examples=["custom-example"])

        def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
            return iter(())

    # now, the registered reader's example should be present
    exit_code, output = invoke_help()
    assert exit_code == 0
    assert 'model "custom-example"' in output


def test_footer_filters_long_and_multiline_reader_examples(reset_reader_registry):
    class ExampleReader(Reader):
        config = ReaderConfig(
            examples=[
                "short-example",
                "first line\nsecond line",
                "x" * 120,
            ]
        )

        def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
            return iter(())

    exit_code, output = invoke_help()
    assert exit_code == 0
    assert '• model "short-example"' in output
    assert '• model "first line\nsecond line"' not in output
    assert f'• model "{"x" * 120}"' not in output


def test_input_format_shows_first_configured_example(reset_reader_registry):
    class ExampleReader(Reader):
        config = ReaderConfig(
            input_format="custom-format",
            examples=["example-value", "another-value"],
        )

        def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
            return iter(())

    exit_code, output = invoke_help()

    assert exit_code == 0
    assert 'custom-format (example: "example-value")' in output
    assert 'custom-format (example: "another-value")' not in output


def test_generated_command_preserves_parameter_order():
    model = MolWeightModel()
    model.config.job_parameters.append(JobParameter(name="second_parameter", type="string"))

    command = AutoCLICommand(model)

    assert [param.name for param in command.params] == [
        "log_level",
        "format",
        "output",
        "multiplier",
        "second_parameter",
        "input",
    ]


def test_generated_command_runs_model_prediction():
    result = CliRunner().invoke(
        AutoCLICommand(MolWeightModel()),
        ["--multiplier", "2", "CCO"],
        prog_name="model",
    )

    assert result.exit_code == 0
    assert "92.083729624" in result.output
