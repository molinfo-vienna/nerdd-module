import os

from nerdd_module.input import DepthFirstExplorer

HERE = os.path.dirname(__file__)


def test_read_zip():
    explorer = DepthFirstExplorer()

    zip_file_path = os.path.join(HERE, "data", "test.zip")

    results = list(explorer.explore(zip_file_path))

    assert len(results) == 12

    for r in results:
        assert len(r.source) == 2
        assert r.source[0] == zip_file_path
        assert r.source[1] == "10_compounds.smiles"
        assert r.input_type == "smiles"


def test_read_zip_with_folder():
    explorer = DepthFirstExplorer()

    zip_file_path = os.path.join(HERE, "data", "test_with_folder.zip")

    results = list(explorer.explore(zip_file_path))

    assert len(results) == 12

    for r in results:
        assert len(r.source) == 2
        assert r.source[0] == zip_file_path
        assert r.source[1] == "folder/10_compounds.smiles"
        assert r.input_type == "smiles"
