import numpy as np
import pandas as pd
from pytest_bdd import parsers, scenario, then, when


@scenario(
    "features/atom_property_prediction.feature", "Predicting a property for each atom"
)
def test_atom_property_prediction():
    pass


@when(
    "the subset of the result where the input was not None is considered",
    target_fixture="subset",
)
def subset_without_none(predictions):
    # remove None entries
    return predictions[predictions.input_mol.notnull()]


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
            subset.drop_duplicates("mol_id").input == valid_molecules
        ).all(), "Input column contains wrong data"


@then(parsers.parse("the mass column should contain the (multiplied) atomic masses"))
def check_weight_column(subset, multiplier):
    if len(subset) > 0:
        expected_masses = [
            m.GetAtomWithIdx(int(atom_id)).GetMass() * multiplier
            for (m, atom_id) in zip(subset.preprocessed_mol, subset.atom_id)
        ]
        assert np.allclose(
            subset.mass, expected_masses
        ), f"the provided weights do not match the expected weights"


@then(
    "the number of unique atom ids should be the same as the number of atoms in the "
    "input"
)
def check_atom_ids(subset):
    for _, group in subset.groupby("mol_id"):
        num_atom_ids = group.atom_id.nunique()
        num_atoms = group.preprocessed_mol.iloc[0].GetNumAtoms()
        assert num_atom_ids == num_atoms, (
            f"Number of atom ids ({num_atom_ids}) does not match number of atoms "
            f"({num_atoms})"
        )
