from rdkit.Chem import Mol

from nerdd_module.input import DepthFirstExplorer


def test_read_smiles_string():
    explorer = DepthFirstExplorer()

    results = list(explorer.explore("CCCCCCCCCCCCO"))

    # there are 13 lines in the test.smiles file
    assert len(results) == 1

    result = results[0]
    
    assert result.raw_input == "CCCCCCCCCCCCO"
    assert result.input_type == "smiles"
    assert isinstance(result.mol, Mol)