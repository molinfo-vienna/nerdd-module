from pathlib import Path

import pytest

from nerdd_module.input import DepthFirstExplorer, FileReader


def test_none_data_dir_disables_file_system_access():
    reader = FileReader(data_dir=None)

    with pytest.raises(PermissionError, match="file system access is disabled"):
        list(reader.read("molecules.smi", lambda _: iter(())))


def test_disabled_file_reader_is_not_considered(monkeypatch):
    # we need to make sure that CWD is the directory containing this test
    monkeypatch.chdir(Path(__file__).parent)

    entries = list(DepthFirstExplorer(data_dir=None).explore("./data/test.smiles"))

    assert len(entries) == 1
    assert entries[0].mol is None

    # this test would succeed for the wrong reasons if the input file was not found
    # -> we check if the path is resolved correctly by setting data_dir="."
    entries = list(DepthFirstExplorer(data_dir=".").explore("./data/test.smiles"))
    assert len(entries) == 13


def test_default_reader_allows_absolute_paths_outside_current_directory(tmp_path):
    input_file = tmp_path / "molecules.smi"
    input_file.write_text("CCO ethanol\n")

    entries = list(DepthFirstExplorer().explore(str(input_file)))

    assert len(entries) == 1
    assert entries[0].mol is not None


def test_relative_paths_are_resolved_against_data_dir(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    input_file = data_dir / "molecules.smi"
    input_file.write_text("CCO ethanol\n")

    entries = list(DepthFirstExplorer(data_dir=data_dir).explore("molecules.smi"))

    assert len(entries) == 1
    assert entries[0].mol is not None


@pytest.mark.parametrize("use_absolute_path", [False, True])
def test_containment_accepts_paths_inside_data_dir(tmp_path, use_absolute_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    input_file = data_dir / "molecules.smi"
    input_file.write_text("CCO ethanol\n")
    filename = input_file if use_absolute_path else Path(input_file.name)

    entries = list(
        DepthFirstExplorer(
            data_dir=data_dir,
            allow_paths_outside_data_dir=False,
        ).explore(str(filename))
    )

    assert len(entries) == 1
    assert entries[0].mol is not None


@pytest.mark.parametrize("use_absolute_path", [False, True])
def test_containment_rejects_paths_outside_data_dir(tmp_path, use_absolute_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    input_file = tmp_path / "outside.smi"
    input_file.write_text("CCO ethanol\n")
    filename = input_file if use_absolute_path else Path("..") / input_file.name
    reader = FileReader(data_dir=data_dir, allow_paths_outside_data_dir=False)

    with pytest.raises(PermissionError, match="input path must be within data_dir"):
        list(reader.read(str(filename), lambda _: iter(())))


@pytest.mark.parametrize("use_absolute_path", [False, True])
def test_unrestricted_reader_allows_paths_outside_data_dir(tmp_path, use_absolute_path):
    # data_dir is set to tmp_path / data
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # but data lives next to data_dir
    input_file = tmp_path / "outside.smi"
    input_file.write_text("CCO ethanol\n")
    filename = input_file if use_absolute_path else Path("..") / input_file.name

    entries = list(
        DepthFirstExplorer(
            data_dir=data_dir,
            allow_paths_outside_data_dir=True,
        ).explore(str(filename))
    )

    assert len(entries) == 1
    assert entries[0].mol is not None


def test_containment_rejects_symlink_escape(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    input_file = tmp_path / "outside.smi"
    input_file.write_text("CCO ethanol\n")
    link = data_dir / "link.smi"

    # skip this test if file system (e.g. Windows) does not support symbolic links
    try:
        link.symlink_to(input_file)
    except OSError:
        pytest.skip("symbolic links are not supported")

    reader = FileReader(data_dir=data_dir, allow_paths_outside_data_dir=False)

    with pytest.raises(PermissionError, match="input path must be within data_dir"):
        list(reader.read(link.name, lambda _: iter(())))
