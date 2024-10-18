import numpy as np
from hypothesis import given as hgiven
from hypothesis import seed, settings
from hypothesis import strategies as st

# TODO: remove "type: ignore" later
from hypothesis_rdkit import mols  # type: ignore
from pytest_bdd import given, parsers
from rdkit.Chem import MolToInchi, MolToMolBlock, MolToSmiles
from rdkit.rdBase import BlockLogs


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
    parsers.parse("the representations of the molecules"),
    target_fixture="representations",
)
def representations_from_molecules(molecules, input_type):
    if input_type == "smiles":
        converter = MolToSmiles
    elif input_type == "mol_block":
        converter = MolToMolBlock
    elif input_type == "inchi":
        converter = MolToInchi
    elif input_type == "rdkit_mol":
        converter = lambda mol: mol
    else:
        raise ValueError(f"Unknown input_type: {input_type}")

    with BlockLogs():
        result = [converter(mol) if mol is not None else None for mol in molecules]

    return result


@given(
    parsers.parse("a list of {num:d} random molecules, where {num_none:d} entries are None"),
    target_fixture="molecules",
)
def molecules(num, num_none, random_seed=0):
    result = None

    # pytest-bdd and hypothesis don't play well together (yet)
    # --> use this workaround to generate random molecules
    @hgiven(st.lists(mols(), min_size=num, max_size=num, unique_by=MolToSmiles))
    @settings(max_examples=1, deadline=None)
    @seed(random_seed)
    def generate(ms):
        nonlocal result
        result = ms

    generate()

    # replace random entries with None
    indices = np.random.choice(num, num_none, replace=False)
    for i in indices:
        result[i] = None

    return result


@given(parsers.parse("the input type is '{input_type}'"), target_fixture="input_type")
def input_type(input_type):
    return input_type
