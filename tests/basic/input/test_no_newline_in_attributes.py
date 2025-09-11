import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_no_newline_in_attributes():
    input_path = os.path.join(HERE, "data", "test.smiles")

    explorer = DepthFirstExplorer()

    results = list(explorer.explore(input_path))

    assert len(results) == 13

    mols_with_name = 0
    for r in results:
        assert "\n" not in r.raw_input
        if r.mol is not None and r.mol.HasProp("_Name"):
            mols_with_name += 1
            assert "\n" not in r.mol.GetProp("_Name")

    assert mols_with_name == 12
