from nerdd_module import Problem
from nerdd_module.config import ResultProperty
from nerdd_module.converters import (
    Converter,
    IdentityConverter,
    ProblemListConverter,
    VoidConverter,
)

primitive_data_types = [
    "int",
    "float",
    "string",
    "bool",
]

output_formats = ["sdf", "csv", "pandas", "record_list", "iterator"]


def test_basic_data_types():
    for primitive_data_type in primitive_data_types:
        for output_format in output_formats:
            result_property = ResultProperty(name="test", type=primitive_data_type)
            converter = Converter.get_converter(result_property, output_format)
            assert converter is not None
            assert isinstance(converter, IdentityConverter)


def test_non_existing_data_type():
    result_property = ResultProperty(name="test", type="non_existing_data_type")
    for output_format in output_formats:
        converter = Converter.get_converter(result_property, output_format)
        assert isinstance(converter, VoidConverter)


def test_problem_list_converter():
    result_property = ResultProperty(name="test", type="problem_list")
    problem_list = [Problem("problem_type", "problem_description")]
    for output_format in output_formats:
        converter = Converter.get_converter(result_property, output_format)
        converted_value = converter.convert(problem_list, {})
        assert isinstance(converter, ProblemListConverter)
        if output_format in ["pandas", "record_list", "iterator"]:
            assert isinstance(converted_value, list)
            assert len(converted_value) == len(problem_list)
            assert isinstance(converted_value[0], Problem)
        else:
            assert isinstance(converted_value, str)
            assert converted_value.startswith("problem_type")
