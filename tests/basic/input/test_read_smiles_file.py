import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_read_smiles_file():
    explorer = DepthFirstExplorer()

    results = list(explorer.explore(os.path.join(HERE, "data", "test.smiles")))

    # there are 13 lines in the test.smiles file
    assert len(results) == 13

    for i, r in enumerate(results):
        # all results except the last one are valid
        assert len(r.errors) == (0 if i != 12 else 1)
