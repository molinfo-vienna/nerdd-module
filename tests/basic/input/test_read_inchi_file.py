import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_read_inchi_file():
    explorer = DepthFirstExplorer()

    results = list(explorer.explore(os.path.join(HERE, "data", "test.inchi")))

    # there are 5 lines in the test.inchi file
    assert len(results) == 5

    for i, r in enumerate(results):
        # only the first 3 rows are valid
        assert len(r.errors) == (0 if i not in [3, 4] else 1)
