from pytest_bdd import parsers, when


@when(
    parsers.parse("the model preprocesses the molecules"),
    target_fixture="preprocessed_molecules",
)
def preprocessed_molecules(molecules, predictor):
    return [predictor.preprocessing_pipeline.run(mol) for mol in molecules]
