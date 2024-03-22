import pandas as pd
from pytest_bdd import parsers, scenario, then, when


@then("the result should be a pandas DataFrame")
def check_result_type(predictions):
    assert isinstance(predictions, pd.DataFrame)


@then("the result should contain the same number of rows as the input")
def check_result_length(representations, predictions):
    if len(representations) == 0:
        # expect one entry saying that nothing could be read from this source
        assert len(predictions) == 1
    else:
        assert len(predictions) == len(representations)


@then(parsers.parse("the result should contain the columns:\n{column_names}"))
def check_result_columns(predictions, column_names):
    column_names = column_names.strip()
    for c in column_names.split("\n"):
        assert (
            c in predictions.columns
        ), f"Column {c} not in predictions {predictions.columns.tolist()}"


@then(parsers.parse("the input type column should be '{input_type}'"))
def check_input_type_column(subset, input_type):
    assert (
        subset.input_type == input_type
    ).all(), f"Not all predictions have the input_type {input_type}"


@then("the result should contain as many rows as atoms in the input molecules")
def check_result_length_atom(molecules, predictions):
    num_expected_predictions = sum(
        m.GetNumAtoms() if m is not None else 1 for m in molecules
    )

    if num_expected_predictions == 0:
        # expect one entry saying that nothing could be read from this source
        num_expected_predictions += 1

    assert len(predictions) == num_expected_predictions
