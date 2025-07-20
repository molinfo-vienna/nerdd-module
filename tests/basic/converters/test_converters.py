from nerdd_module import Problem
from nerdd_module.config import Module, ResultProperty
from nerdd_module.converters import (
    BasicTypeConverter,
    Converter,
    ProblemListConverter,
    ProblemListIdentityConverter,
    SourceListConverter,
    SourceListIdentityConverter,
    VoidConverter,
)

config = Module(name="test")

primitive_data_types = [
    "int",
    "float",
    "string",
    "bool",
]

output_formats = ["sdf", "csv", "pandas", "record_list", "iterator", "non-existing"]


def test_basic_data_types():
    for primitive_data_type in primitive_data_types:
        for output_format in output_formats:
            result_property = ResultProperty(name="test", type=primitive_data_type)
            converter = Converter.get_converter(config, result_property, output_format)
            assert converter is not None
            assert isinstance(converter, BasicTypeConverter)


def test_non_existing_data_type():
    result_property = ResultProperty(name="test", type="non_existing_data_type")
    for output_format in output_formats:
        converter = Converter.get_converter(config, result_property, output_format)
        assert isinstance(converter, VoidConverter)


def test_problem_list_converter():
    result_property = ResultProperty(name="test", type="problem_list")
    problem_list = [Problem("problem_type", "problem_description")]
    for output_format in output_formats:
        converter = Converter.get_converter(config, result_property, output_format)
        converted_value = converter.convert(problem_list, {})
        if output_format in ["pandas", "record_list", "iterator"]:
            assert isinstance(converter, ProblemListIdentityConverter)
            assert isinstance(converted_value, list)
            assert len(converted_value) == len(problem_list)
            assert isinstance(converted_value[0], Problem)
        elif output_format in ["sdf", "csv"]:
            assert isinstance(converter, ProblemListConverter)
            assert isinstance(converted_value, str)
            assert converted_value.startswith("problem_type")
        else:
            assert isinstance(converter, VoidConverter)
            assert converted_value is Converter.HIDE


def test_source_list_converter():
    result_property = ResultProperty(name="test", type="source_list")
    source_list = ("source1", "source2")
    for output_format in output_formats:
        converter = Converter.get_converter(config, result_property, output_format)
        converted_value = converter.convert(source_list, {})
        if output_format in ["pandas", "record_list", "iterator"]:
            assert isinstance(converter, SourceListIdentityConverter)
            assert isinstance(converted_value, tuple)
            assert len(converted_value) == len(source_list)
            assert isinstance(converted_value[0], str)
            assert isinstance(converted_value[1], str)
        elif output_format in ["sdf", "csv"]:
            assert isinstance(converter, SourceListConverter)
            assert isinstance(converted_value, str)
        else:
            assert isinstance(converter, VoidConverter)
            assert converted_value is Converter.HIDE
