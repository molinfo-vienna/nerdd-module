import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_read_gzip():
    explorer = DepthFirstExplorer()

    gzip_file_path = os.path.join(HERE, "data", "test.smiles.gz")

    results = list(explorer.explore(gzip_file_path))

    assert len(results) == 12

    for r in results:
        assert len(r.source) == 1
        assert r.source[0] == gzip_file_path
        assert r.input_type == "smiles"


def test_read_tar_gzip():
    explorer = DepthFirstExplorer()

    input_file_path = os.path.join(HERE, "data", "test.tar.gz")

    results = list(explorer.explore(input_file_path))

    assert len(results) == 12

    for r in results:
        assert len(r.source) == 2
        assert r.source[0] == input_file_path
        assert r.source[1] == "10_compounds.smiles"
        assert r.input_type == "smiles"


def test_read_tar_gzip_with_folder():
    explorer = DepthFirstExplorer()

    tar_file_path = os.path.join(HERE, "data", "test_with_folder.tar.gz")

    results = list(explorer.explore(tar_file_path))

    assert len(results) == 12

    for r in results:
        assert len(r.source) == 2
        assert r.source[0] == tar_file_path
        assert r.source[1] == "./folder/10_compounds.smiles"
        assert r.input_type == "smiles"
