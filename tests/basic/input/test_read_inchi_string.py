from rdkit.Chem import Mol, MolFromSmiles, MolToInchi

from nerdd_module.input import DepthFirstExplorer


def test_read_inchi_string():
    explorer = DepthFirstExplorer()

    inp = (
        "InChI=1S/C14H20N2O4S/c1-2-20-14(17)15-8-10-16(11-9-15)21(18,19)12-13-6-4-3-5-7-13"
        "/h3-7H,2,8-12H2,1H3"
    )

    results = list(explorer.explore(inp))

    assert len(results) == 1

    result = results[0]

    assert result.raw_input == inp
    assert result.input_type == "inchi"
    assert isinstance(result.mol, Mol)


def test_read_inchi_bytes():
    explorer = DepthFirstExplorer()

    inp = (
        b"InChI=1S/C14H20N2O4S/c1-2-20-14(17)15-8-10-16(11-9-15)21(18,19)12-13-6-4-3-5-7-13"
        b"/h3-7H,2,8-12H2,1H3"
    )

    results = list(explorer.explore(inp))

    assert len(results) == 1

    result = results[0]

    assert result.raw_input == inp.decode("utf-8")
    assert result.input_type == "inchi"
    assert isinstance(result.mol, Mol)


def test_read_long_inchi_string():
    explorer = DepthFirstExplorer()

    # generate a long InChI string
    long_smiles = "C" * 5000
    long_inchi = MolToInchi(MolFromSmiles(long_smiles), options="-LargeMolecules")
    assert len(long_inchi) > 20000

    results = list(explorer.explore(long_inchi))

    assert len(results) == 1

    result = results[0]

    # InchiReader will return an invalid molecule
    # -> DepthFirstExplorer will use InvalidInputReader as fallback
    # -> we will get a record with input_type "unknown"
    assert result.input_type == "unknown"
    assert result.mol is None
