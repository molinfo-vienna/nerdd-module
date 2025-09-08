import re
from functools import reduce

import numpy as np
from hypothesis import given as hgiven
from hypothesis import seed, settings
from hypothesis import strategies as st
from hypothesis_rdkit import mols
from pytest_bdd import given, parsers
from rdkit.Chem import MolToInchi, MolToMolBlock, MolToSmiles
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

from ..polyfills import BlockLogs


@given(parsers.parse("a random seed set to {seed:d}"), target_fixture="random_seed")
def random_seed(seed):
    return seed


@given(
    parsers.parse("an input molecule specified by '{input}'"),
    target_fixture="representations",
)
def representations_from_input(input):
    return [input]


@given(
    parsers.parse("the representations of the molecules in {input_type} format"),
    target_fixture="representations",
)
def representations_from_molecules(molecules, input_type):
    input_type = input_type.lower()

    if input_type == "smiles":
        converter = MolToSmiles
    elif input_type == "mol_block":
        converter = MolToMolBlock
    elif input_type == "inchi":
        converter = MolToInchi
    elif input_type == "rdkit_mol":

        def converter(mol):
            return mol
    else:
        raise ValueError(f"Unknown input_type: {input_type}")

    with BlockLogs():
        result = [converter(mol) if mol is not None else None for mol in molecules]

    return result


@given(
    parsers.re(r"a list of (?P<num>\d+) random molecules(?:, where(?P<conditions>[\s\S]*))?"),
    target_fixture="molecules",
)
def molecules(num, conditions, random_seed=0):
    num = int(num)

    filters = []
    maps = []

    if conditions is not None:

        def filter_weight(min_weight, max_weight):
            min_weight = float(min_weight)
            max_weight = float(max_weight)
            return lambda mol: (min_weight <= CalcExactMolWt(mol) <= max_weight)

        def map_to_none(num_none):
            num_none = int(num_none)

            # draw indices of molecules that should be set to None
            indices = np.random.choice(num, num_none, replace=False)

            return lambda ms: [m if i not in indices else None for i, m in enumerate(ms)]

        expressions = [
            # filters are functions that return True if the molecule should be kept
            (
                "filter",
                r"each mol has a weight between (?P<min_weight>\d+) and (?P<max_weight>\d+)",
                filter_weight,
            ),
            # maps are functions that modify the molecule
            ("map", r"(?P<num_none>\d+) entries are None", map_to_none),
        ]

        conditions_list = [c for c in conditions.split("\n") if c.strip() != ""]

        for condition in conditions_list:
            for kind, expression, f in expressions:  # noqa: B007
                # conditions might be a markdown list (starting with a star character)
                expression = r"\s*(\*\s*)?" + expression + r"\s*"

                match = re.match(expression, condition)
                if match:
                    params = match.groupdict()
                    break

            assert match is not None, f"Could not parse condition: {condition}"

            if kind == "filter":
                filters.append(f(**params))
            elif kind == "map":
                maps.append(f(**params))
            else:
                raise ValueError(f"Unknown kind: {kind}")

    def filter_func(mol):
        return all(f(mol) for f in filters)

    def map_func(ms):
        return reduce(lambda ms, f: f(ms), maps, ms)

    result = None

    # pytest-bdd and hypothesis don't play well together (yet)
    # --> use this workaround to generate random molecules
    @hgiven(st.lists(mols().filter(filter_func), min_size=num, max_size=num, unique_by=MolToSmiles))
    @settings(max_examples=1, deadline=None)
    @seed(random_seed)
    def generate(ms):
        nonlocal result
        result = ms

    generate()

    # apply maps
    result = map_func(result)

    for m in result:
        if m is None:
            continue
        m.SetProp("_Name", "mol")

    return result
