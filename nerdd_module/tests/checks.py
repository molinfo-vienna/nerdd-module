import json

import numpy as np
import pandas as pd
from pytest_bdd import parsers, then


@then(parsers.parse("The result should contain the columns:\n{column_names}"))
def check_result_columns(predictions, column_names):
    column_names = column_names.strip()
    for c in column_names.split("\n"):
        assert (
            c in predictions.columns
        ), f"Column {c} not in predictions {predictions.columns.tolist()}"


@then(
    parsers.parse(
        "the value in column '{column_name}' should be between {low} and {high}"
    )
)
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

    assert (low <= subset[column_name]).all()
    assert (subset[column_name] <= high).all()


@then(parsers.parse("the value in column '{column_name}' should be '{expected_value}'"))
def check_column_value(predictions, column_name, expected_value):
    value = predictions[column_name].iloc[0]

    # expected value is always provided as string
    # try to convert to float if possible
    try:
        expected_value = float(expected_value)
    except ValueError:
        pass

    if expected_value == "(none)":
        # if expected_value is the magic string "(none)", we expect None
        assert pd.isnull(value), f"Column {column_name} is assigned to {value} != None"
    else:
        # otherwise, we expect the value to be equal to the expected value
        assert (
            value == expected_value
        ), f"Column {column_name} is assigned to {value} != {expected_value}"


@then(
    parsers.parse(
        "the value in column '{column_name}' should be a subset of {superset}"
    )
)
def check_column_subset(subset, column_name, superset):
    superset = set(json.loads(superset))

    assert all(
        set(value).issubset(superset) for value in subset[column_name]
    ), f"Column {column_name} contains value not in {superset}"


@then(parsers.parse("the value in column '{column_name}' should be one of {superset}"))
def check_column_membership(subset, column_name, superset):
    superset = json.loads(superset)

    assert isinstance(
        superset, list
    ), f"Expected a list for superset, got {type(superset)}"

    assert (
        subset[column_name].isin(superset).all()
    ), f"Column {column_name} contains value not in {superset}"


@then(parsers.parse("the value in column '{column_name}' should be a png image"))
def check_png_image(subset, column_name):
    if len(subset) == 0:
        return

    assert (
        subset[column_name].str.startswith('<img src="data:image/png;base64,')
    ).all(), f"Column {column_name} does not contain a PNG image"


@then(
    parsers.parse("the value in column '{column_name}' should contain only '{value}'")
)
def check_column_membership_single(predictions, column_name, value):
    if value == "(none)":
        assert all(
            pd.isnull(predictions[column_name])
        ), f"Column {column_name} must be none"
    else:
        assert all(
            value in values for values in predictions[column_name]
        ), f"Column {column_name} contains value {value}"


@then(
    parsers.parse(
        "the value in column '{column_name}' should have type '{expected_type}'"
    )
)
def check_column_type(subset, column_name, expected_type):
    expected_type = eval(expected_type)

    assert (
        subset[column_name].map(lambda x: isinstance(x, expected_type)).all()
    ), f"Column {column_name} has unexpected type"


@then(
    parsers.parse(
        "the value in column '{column_name}' should have length greater than {length}"
    )
)
def check_column_length(subset, column_name, length):
    length = int(length)
    assert (
        subset[column_name].map(lambda x: len(x) > length)
    ).all(), f"Column {column_name} has unexpected length"
