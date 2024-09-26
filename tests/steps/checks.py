from collections import defaultdict
from typing import Iterable

from pytest_bdd import parsers, then

from nerdd_module import Problem


@then("the result should contain the same number of rows as the input")
def check_result_length(representations, predictions):
    if len(representations) == 0:
        # expect one entry saying that nothing could be read from this source
        assert len(predictions) == 1
    else:
        assert len(predictions) == len(representations)


@then(
    "the number of unique atom ids should be the same as the number of atoms in the "
    "input"
)
def check_atom_ids(subset):
    records_per_mol_id = defaultdict(list)

    for record in subset:
        records_per_mol_id[record["mol_id"]].append(record)

    for mol_id, records in records_per_mol_id.items():
        mol = records[0]["preprocessed_mol"]
        num_atom_ids = len(set([r["atom_id"] for r in records]))
        num_atoms = mol.GetNumAtoms()
        assert num_atom_ids == num_atoms, (
            f"Number of atom ids ({num_atom_ids}) does not match number of atoms "
            f"({num_atoms})"
        )


@then("the result should contain as many rows as atoms in the input molecules")
def check_result_length_atom(molecules, predictions):
    num_expected_predictions = sum(
        m.GetNumAtoms() if m is not None else 1 for m in molecules
    )

    if num_expected_predictions == 0:
        # expect one entry saying that nothing could be read from this source
        num_expected_predictions += 1

    assert len(predictions) == num_expected_predictions


@then("the problems column should be a list of problem instances")
def check_problem_column(predictions):
    for record in predictions:
        problems_list = record["problems"]
        assert isinstance(problems_list, Iterable)
        for e in problems_list:
            assert isinstance(
                e, Problem
            ), f"Expected Problem, got {e} of type {type(e)}"


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
