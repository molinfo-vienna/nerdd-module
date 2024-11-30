from nerdd_module.config import ResultProperty
from nerdd_module.converters import Converter, IdentityConverter, VoidConverter

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
