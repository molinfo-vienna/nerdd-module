import numpy as np
from hypothesis import given as hgiven
from hypothesis import settings
from hypothesis import strategies as st
from hypothesis_rdkit import smiles
from pytest_bdd import given, parsers
from rdkit.Chem import MolFromSmiles, MolToInchi, MolToMolBlock, MolToSmiles


@given(
    parsers.parse(
        "a list of {num:d} random molecules, where {num_none:d} entries are None"
    ),
    target_fixture="molecules",
)
def molecules(num, num_none):
    result = None

    @hgiven(st.lists(smiles(), min_size=num, max_size=num, unique=True))
    @settings(max_examples=1, deadline=None)
    def generate(smiles):
        nonlocal result
        result = [MolFromSmiles(s) for s in smiles]

    generate()

    # replace random entries with None
    indices = np.random.choice(num, num_none, replace=False)
    for i in indices:
        result[i] = None

    return result


@given(
    parsers.parse("the representations of the molecules as {input_type}"),
    target_fixture="representations",
)
def representations(molecules, input_type):
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

    result = [converter(mol) if mol is not None else None for mol in molecules]

    return result
