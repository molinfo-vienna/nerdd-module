from ast import literal_eval

import numpy as np
from pytest_bdd import parsers, then


@then(parsers.parse("The result should contain the columns:\n{expected_column_names}"))
def check_result_columns(predictions, expected_column_names):
    expected_column_names = expected_column_names.strip().split("\n")
    for c in expected_column_names:
        for record in predictions:
            assert c in record, f"Column {c} not in record {list(record.keys())}"


@then(parsers.parse("the value in column '{column_name}' should be between {low} and {high}"))
def check_column_range(subset, column_name, low, high):
    if low == "infinity":
        low = np.inf
    elif low == "-infinity":
        low = -np.inf
    else:
        low = float(low)

    if high == "infinity":
        high = np.inf
    elif high == "-infinity":
        high = -np.inf
    else:
        high = float(high)

    values = [record[column_name] for record in subset]

    assert all(
        low <= v <= high for v in values
    ), f"Column {column_name} is assigned to {values} not in [{low}, {high}]"


@then(parsers.parse("the value in column '{column_name}' should be equal to {expected_value}"))
def check_column_value_equality(subset, column_name, expected_value):
    if len(subset) == 0:
        return

    values = [record[column_name] for record in subset]

    # expected value is always provided as string
    # try to convert to float if possible
    try:
        expected_value = literal_eval(expected_value)
    except:
        pass

    if expected_value is None:
        # if expected_value is the magic string "(none)", we expect None
        assert all(
            v is None for v in values
        ), f"Column {column_name} is assigned to {values} != None"
    else:
        # otherwise, we expect the value to be equal to the expected value
        assert all(
            v == expected_value for v in values
        ), f"Column {column_name} is assigned to {values} != {expected_value}"


@then(parsers.parse("the value in column '{column_name}' should not be equal to {forbidden_value}"))
def check_column_value_inequality(subset, column_name, forbidden_value):
    if len(subset) == 0:
        return

    values = [record[column_name] for record in subset]

    # expected value is always provided as string
    # try to convert to float if possible
    try:
        forbidden_value = literal_eval(forbidden_value)
    except:
        pass

    if forbidden_value is None:
        # if expected_value is the magic string "(none)", we expect None
        assert all(
            v is not None for v in values
        ), f"Column {column_name} is assigned to {values} == None"
    else:
        # otherwise, we expect the value to be equal to the expected value
        assert all(
            v != forbidden_value for v in values
        ), f"Column {column_name} is assigned to {values} == {forbidden_value}"


@then(parsers.parse("the value in column '{column_name}' should be a subset of {superset}"))
def check_column_subset(subset, column_name, superset):
    superset = set(literal_eval(superset))

    values = [record[column_name] for record in subset]

    assert all(
        set(value).issubset(superset) for value in values
    ), f"Column {column_name} contains value not in {superset}"


@then(parsers.parse("the value in column '{column_name}' should be one of {superset}"))
def check_column_membership(subset, column_name, superset):
    superset = literal_eval(superset)

    assert isinstance(superset, list), f"Expected a list for superset, got {type(superset)}"

    values = [record[column_name] for record in subset]

    assert all(
        value in superset for value in values
    ), f"Column {column_name} contains value not in {superset}"


@then(parsers.parse("the value in column '{column_name}' should be a png image"))
def check_png_image(subset, column_name):
    if len(subset) == 0:
        return

    assert (
        subset[column_name].str.startswith('<img src="data:image/png;base64,')
    ).all(), f"Column {column_name} does not contain a PNG image"


@then(parsers.parse("the value in column '{column_name}' should have type '{expected_type}'"))
def check_column_type(subset, column_name, expected_type):
    expected_type = eval(expected_type)

    values = [record[column_name] for record in subset]

    assert all(
        isinstance(value, expected_type) for value in values
    ), f"Column {column_name} has unexpected type"


@then(
    parsers.parse("the value in column '{column_name}' should have length greater than {length:d}")
)
def check_column_length(subset, column_name, length):
    values = [record[column_name] for record in subset]

    assert all(
        len(value) > length for value in values
    ), f"Column {column_name} has unexpected length"


@then(
    parsers.parse(
        "when '{condition_column_name}' is {condition_value} "
        "the value in column '{column_name}' should be {expected_value}"
    )
)
def check_conditional_column_value(
    subset, condition_column_name, condition_value, column_name, expected_value
):
    # expected value is always provided as string
    # try to convert to float if possible
    try:
        expected_value = literal_eval(expected_value)
    except:
        pass

    # same for condition value
    try:
        condition_value = literal_eval(condition_value)
    except:
        pass

    # condition value can be (none) to indicate None
    if condition_value is None:
        subset = [record for record in subset if record[condition_column_name] is None]
    else:
        subset = [record for record in subset if record[condition_column_name] == condition_value]

    values = [record[column_name] for record in subset]
    assert (
        len(values) > 0
    ), f"No rows found for condition {condition_column_name} == {condition_value}"

    # expected value can be None
    if expected_value is None:
        assert all(
            value is None for value in values
        ), f"Column {column_name} is assigned to {values} != None"
    else:
        # otherwise, we expect the value to be equal to the expected value
        assert all(
            value == expected_value for value in values
        ), f"Column {column_name} is assigned to {values} != {expected_value}"
