from pytest_bdd import given, parsers, when

from ..models import (
    AtomicMassModel,
    MolWeightModel,
    MolWeightModelWithExplicitMolIds,
    MolWeightModelWithExplicitMols,
)


@given(
    parsers.parse("a prediction parameter 'multiplier' set to {multiplier:d}"),
    target_fixture="multiplier",
)
def multiplier(multiplier):
    return multiplier


@given(
    parsers.parse("an example model predicting molecular weight, version {version}"),
    target_fixture="predictor",
)
def molecule_property_predictor(version):
    if version == "no_ids":
        return MolWeightModel()
    elif version == "with_ids":
        return MolWeightModelWithExplicitMolIds()
    elif version == "with_mols":
        return MolWeightModelWithExplicitMols()


@given(
    parsers.parse("an example model predicting atomic masses, version {version}"),
    target_fixture="predictor",
)
def atom_property_predictor(version):
    # if version == "no_ids":
    return AtomicMassModel()
    # elif version == "with_ids":
    #     return MolWeightModelWithExplicitMolIds()
    # elif version == "with_mols":
    #     return MolWeightModelWithExplicitMols()


@when(
    parsers.parse("the model is used on the molecules given as {input_type}"),
    target_fixture="predictions",
)
def predictions(representations, predictor, input_type, multiplier):
    return predictor.predict(
        representations, input_type=input_type, multiplier=multiplier
    )
