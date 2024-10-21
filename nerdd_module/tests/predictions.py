from pytest_bdd import given, parsers, when

from .models import AtomicMassModel, MolWeightModel


@given(
    parsers.parse("a prediction parameter 'multiplier' set to {multiplier:d}"),
    target_fixture="multiplier",
)
def multiplier(multiplier):
    return multiplier


@given(
    parsers.parse("the mol weight model (version '{version}')"),
    target_fixture="model",
)
def mol_weight_model(version):
    return MolWeightModel(version=version)


@when(
    parsers.parse("the mol weight model (version '{version}') generates predictions for the molecule representations"),
    target_fixture="predictions",
)
def predictions_mol_weight_model(representations, version, input_type, multiplier):
    model = MolWeightModel(version=version)
    return model.predict(
        representations,
        input_type=input_type,
        multiplier=multiplier,
        output_format="record_list",
    )


@when(
    parsers.parse("the atomic mass model (version '{version}') generates predictions for the molecule representations"),
    target_fixture="predictions",
)
def predictions_atomic_mass_model(representations, version, input_type, multiplier):
    model = AtomicMassModel(version=version)
    return model.predict(
        representations,
        input_type=input_type,
        multiplier=multiplier,
        output_format="record_list",
    )


@when(
    "the subset of the result where the input was not None is considered",
    target_fixture="subset",
)
def subset_without_none(predictions):
    # remove None entries
    return [p for p in predictions if p["input_mol"] is not None]
