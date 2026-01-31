from typing import Any, Iterator

import pytest
from click.testing import CliRunner

from nerdd_module.cli import AutoCLICommand
from nerdd_module.config import JobParameter
from nerdd_module.input import ExploreCallable, MoleculeEntry, Reader
from nerdd_module.input.reader_config import ReaderConfig
from nerdd_module.tests.models import MolWeightModel


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
    result = CliRunner().invoke(
        AutoCLICommand(MolWeightModel()),
        ["--help"],
        prog_name="python -m example.model",
        color=False,
    )

    assert result.exit_code == 0
    assert "Usage: python -m example.model [OPTIONS] INPUT..." in result.output
    assert 'python -m example.model "compounds.smiles"' in result.output


def test_examples_are_collected_when_help_is_rendered(reset_reader_registry):
    command = AutoCLICommand(MolWeightModel())

    # we check if our example reader is not present yet
    result = CliRunner().invoke(command, ["--help"], prog_name="model", color=False)
    assert result.exit_code == 0
    assert 'model "late-example"' not in result.output

    class LateReader(Reader):
        config = ReaderConfig(examples=["late-example"])

        def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
            return iter(())

    # now, it should be present
    result = CliRunner().invoke(command, ["--help"], prog_name="model", color=False)
    assert result.exit_code == 0
    assert 'model "late-example"' in result.output


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

    command = AutoCLICommand(MolWeightModel())
    result = CliRunner().invoke(command, ["--help"], prog_name="model", color=False)
    assert result.exit_code == 0
    assert '• model "short-example"' in result.output
    assert '• model "first line\nsecond line"' not in result.output
    assert f'• model "{"x" * 120}"' not in result.output


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
