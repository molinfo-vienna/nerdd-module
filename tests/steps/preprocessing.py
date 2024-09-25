from pytest_bdd import given, parsers, then, when

from nerdd_module.input import DepthFirstExplorer
from nerdd_module.model import ReadInput
from nerdd_module.preprocessing import FilterByElement, Sanitize


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


@then(parsers.parse("the subset should contain the problem '{problem}'"))
def check_problem_in_list(subset, problem):
    for record in subset:
        problems = record.get("problems", [])
        assert problem in [
            p.type for p in problems
        ], f"Problem list lacks problem {problem} in record {record}"


@then(parsers.parse("the subset should not contain the problem '{problem}'"))
def check_problem_not_in_list(subset, problem):
    for record in subset:
        problems = record.get("problems", [])
        assert problem not in [
            p.type for p in problems
        ], f"Problem list contains problem {problem} in record {record}"
