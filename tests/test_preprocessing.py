from pytest_bdd import scenario, then


@scenario("features/preprocessing.feature", "Preprocessing molecules")
def test_preprocessing():
    pass


@then("the preprocessed molecules are valid")
def preprocessed_molecules_are_valid(preprocessed_molecules):
    for mol, errors in preprocessed_molecules:
        assert mol is not None and mol.GetNumAtoms() > 0
