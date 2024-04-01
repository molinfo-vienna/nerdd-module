import pandas as pd
from pytest_bdd import parsers, then, when


@when(
    parsers.parse("the model generates predictions for the molecule representations"),
    target_fixture="predictions",
)
def predictions(
    representations,
    model,
    input_type,
):
    return model.predict(
        representations,
    )


@when(
    "The subset of the result where the input was not None is considered",
    target_fixture="subset",
)
def subset_without_none(predictions):
    # remove None entries
    return predictions[predictions.preprocessed_mol.notnull()]


@then("the result should be a pandas DataFrame")
def check_result(predictions):
    assert isinstance(predictions, pd.DataFrame)
