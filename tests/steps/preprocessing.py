from pytest_bdd import given, parsers, when

from nerdd_module.input import DepthFirstExplorer
from nerdd_module.model import ReadInput
from nerdd_module.preprocessing import (
    FilterByElement,
    FilterByWeight,
    GetParentMolWithCsp,
    Sanitize,
    StandardizeWithCsp,
)
from nerdd_module.tests.preprocessing import DummyPreprocessingStep


#
# DUMMY PREPROCESSING STEP
#
@when(
    parsers.parse(
        "the molecules are preprocessed by a dummy preprocessing step in mode '{mode}'"
    ),
    target_fixture="predictions",
)
def preprocessed_molecules_dummy_preprocessing_step(representations, mode):
    input_step = ReadInput(DepthFirstExplorer(), representations)
    sanitize = Sanitize()
    dummy_preprocessing_step = DummyPreprocessingStep(mode)
    return list(dummy_preprocessing_step(sanitize(input_step())))


#
# FILTER BY ELEMENT
#
@given(
    parsers.parse("the list of allowed elements is {l}"),
    target_fixture="allowed_elements",
)
def allowed_elements(l):
    return eval(l)


@given(
    parsers.parse("the parameter remove_invalid_molecules is set to {value}"),
    target_fixture="remove_invalid_molecules",
)
def remove_invalid_molecules(value):
    return eval(value)


@when(
    parsers.parse("the molecules are filtered by element"),
    target_fixture="predictions",
)
def preprocessed_molecules_filter_by_element(
    representations, allowed_elements, remove_invalid_molecules
):
    input_step = ReadInput(DepthFirstExplorer(), representations)
    sanitize = Sanitize()
    filter_by_element = FilterByElement(
        allowed_elements, remove_invalid_molecules=remove_invalid_molecules
    )
    return list(filter_by_element(sanitize(input_step())))


@when(
    parsers.parse(
        "the molecules are filtered by weight (range=[{min_weight:d}, {max_weight:d}], remove_invalid_molecules={remove_invalid_molecules})"
    ),
    target_fixture="predictions",
)
def preprocessed_molecules_filter_by_weight(
    representations, min_weight, max_weight, remove_invalid_molecules
):
    remove_invalid_molecules = eval(remove_invalid_molecules)

    input_step = ReadInput(DepthFirstExplorer(), representations)
    sanitize = Sanitize()
    filter_by_weight = FilterByWeight(
        min_weight=min_weight,
        max_weight=max_weight,
        remove_invalid_molecules=remove_invalid_molecules,
    )
    return list(filter_by_weight(sanitize(input_step())))


#
# STANDARDIZE_WITH_CSP
#
@when(
    parsers.parse("the molecules are standardized with CSP"),
    target_fixture="predictions",
)
def preprocessed_molecules_standardize_with_csp(representations):
    input_step = ReadInput(DepthFirstExplorer(), representations)
    sanitize = Sanitize()
    standardize = StandardizeWithCsp()
    return list(standardize(sanitize(input_step())))


#
# GET_PARENT_MOL_WITH_CSP
#
@when(
    parsers.parse("small fragments are removed from the molecules with CSP"),
    target_fixture="predictions",
)
def preprocessed_molecules_get_parent_mol_with_csp(representations):
    input_step = ReadInput(DepthFirstExplorer(), representations)
    sanitize = Sanitize()
    get_parent_mol = GetParentMolWithCsp()
    return list(get_parent_mol(sanitize(input_step())))
