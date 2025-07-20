from rdkit.Chem import Mol

from nerdd_module.input import DepthFirstExplorer


def test_read_smiles_string():
    explorer = DepthFirstExplorer()

    results = list(explorer.explore("CCCCCCCCCCCCO"))

    assert len(results) == 1

    result = results[0]

    assert result.raw_input == "CCCCCCCCCCCCO"
    assert result.input_type == "smiles"
    assert isinstance(result.mol, Mol)


def test_read_smiles_bytes():
    explorer = DepthFirstExplorer()

    results = list(explorer.explore(b"CCCCCCCCCCCCO"))

    assert len(results) == 1

    result = results[0]

    assert result.raw_input == "CCCCCCCCCCCCO"
    assert result.input_type == "smiles"
    assert isinstance(result.mol, Mol)
