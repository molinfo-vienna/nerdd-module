import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_read_smiles_file():
    explorer = DepthFirstExplorer()

    input_file = os.path.join(HERE, "data", "test.smiles")

    results = list(explorer.explore(input_file))

    # there are 13 lines in the test.smiles file
    assert len(results) == 13

    for i, r in enumerate(results):
        assert len(r.source) == 1
        assert r.source[0] == input_file
        # all results except the last one are valid
        assert len(r.errors) == (0 if i != 12 else 1)
