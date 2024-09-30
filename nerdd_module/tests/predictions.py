from pytest_bdd import when


@when(
    "the subset of the result where the input was not None is considered",
    target_fixture="subset",
)
def subset_without_none(predictions):
    # remove None entries
    return [p for p in predictions if p["input_mol"] is not None]
