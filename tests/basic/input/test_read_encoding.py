import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_read_special_encoding():
    explorer = DepthFirstExplorer()

    input_file_path = os.path.join(HERE, "data", "test_special_encoding.sdf")

    results = list(explorer.explore(input_file_path))

    # if the file was not read correctly, we would get 1 entry with a lot of garbage
    assert len(results) == 2

    for r in results:
        assert len(r.source) == 1
        assert r.source[0] == input_file_path
        assert r.input_type == "mol_block"
