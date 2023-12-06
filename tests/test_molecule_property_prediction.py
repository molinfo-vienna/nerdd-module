import numpy as np
import pandas as pd
from pytest_bdd import parsers, scenario, then, when
from rdkit.Chem.Descriptors import MolWt


@scenario(
    "features/molecule_property_prediction.feature", "Predicting a molecular property"
)
def test_molecule_property_prediction():
    pass


@when(
    "the subset of the result where the input was not None is considered",
    target_fixture="subset",
)
def subset_without_none(predictions):
    # filter None entries
    return predictions[predictions.input_mol.notnull()]


@then(parsers.parse("the result should contain the columns:\n{column_names}"))
def check_result_columns(predictions, column_names):
    column_names = column_names.strip()
    for c in column_names.split("\n"):
        assert (
            c in predictions.columns
        ), f"Column {c} not in predictions {predictions.columns.tolist()}"


@then(parsers.parse("the input type column should be '{input_type}'"))
def check_input_type_column(predictions, input_type):
    assert (
        predictions.input_type == input_type
    ).all(), f"Not all predictions have the input_type {input_type}"


@then("the name column should contain valid names")
def check_name_column(subset):
    if len(subset) > 0:
        assert subset.name.notnull().all(), "Some molecules have no name"


@then("the input column should contain the input representation")
def check_input_column(representations, subset):
    # if input is not a mol, then smiles / mol_blocks were provided
    # --> there must be a column called "input"
    if not subset.input_type.eq("rdkit_mol").all():
        assert "input" in subset.columns, "Column input not in predictions"

        valid_molecules = [m for m in representations if m is not None]

        # the input column must contain the input representation (e.g. smiles)
        assert (
            subset.input == valid_molecules
        ).all(), "Input column contains wrong data"


@then(
    parsers.parse("the weight column should contain the (multiplied) molecule weights")
)
def check_weight_column(subset, multiplier):
    if len(subset) > 0:
        expected_weights = subset.preprocessed_mol.map(MolWt) * multiplier
        assert np.allclose(
            subset.weight, expected_weights
        ), f"the provided weights do not match the expected weights"
