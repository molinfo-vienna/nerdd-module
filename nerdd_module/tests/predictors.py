from ast import literal_eval

from pytest_bdd import given, parsers, when

from .models import AtomicMassModel, MolWeightModel


@given(
    parsers.parse("a prediction parameter 'multiplier' set to {multiplier:d}"),
    target_fixture="multiplier",
)
def multiplier(multiplier):
    return multiplier


@given(
    parsers.parse("an example model predicting molecular weight, version '{version}'"),
    target_fixture="predictor",
)
def molecule_property_predictor(version):
    return MolWeightModel(version=version)


@given(
    parsers.parse("an example model predicting atomic masses, version '{version}'"),
    target_fixture="predictor",
)
def atom_property_predictor(version):
    return AtomicMassModel(version=version)


@when(
    parsers.parse("the model generates predictions for the molecule representations"),
    target_fixture="predictions",
)
def predictions(representations, predictor, input_type, multiplier):
    return predictor.predict(
        representations,
        input_type=input_type,
        multiplier=multiplier,
        output_format="record_list",
    )
