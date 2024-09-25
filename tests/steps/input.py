from tempfile import NamedTemporaryFile

import numpy as np
from pytest_bdd import given, parsers, then, when

from nerdd_module.input import DepthFirstExplorer


@given(
    parsers.parse("a file containing the representations"),
    target_fixture="representation_files",
)
def representation_file(representations, input_type):
    with NamedTemporaryFile("w", delete=False) as f:
        for representation in representations:
            if representation is None:
                f.write("None")
            else:
                f.write(representation)
            if input_type in ["smiles", "inchi"]:
                f.write("\n")
            elif input_type == "mol_block":
                f.write("\n$$$$\n")
        f.flush()
        return f.name


@given(
    parsers.parse(
        "a list of {num_files:d} files containing the representations",
    ),
    target_fixture="representation_files",
)
def representation_files(representations, input_type, num_files):
    # choose num_files-1 numbers to split the representations into num_files parts
    # the while loop makes sure that each part contains at least one valid molecule
    while True:
        split_indices = np.random.choice(
            len(representations), size=num_files - 1, replace=False
        )
        split_indices = np.sort(split_indices)

        # split the representations
        split_representations = np.split(representations, split_indices)

        # check if each part contains at least one valid molecule
        if all(
            any(representation is not None for representation in split_representation)
            for split_representation in split_representations
        ):
            break

    # write the representations to files
    representations_files = []

    for _, split_representation in enumerate(split_representations):
        with NamedTemporaryFile("w", delete=False) as f:
            for representation in split_representation:
                if representation is None:
                    f.write("None")
                else:
                    f.write(representation)
                if input_type in ["smiles", "inchi"]:
                    f.write("\n")
                elif input_type == "mol_block":
                    f.write("\n$$$$\n")
            f.flush()
            representations_files.append(f.name)

    return representations_files


@when(
    parsers.parse(
        "the reader gets the representations as input with input type {input_type}"
    ),
    target_fixture="entries",
)
def entries(representations, input_type):
    if input_type == "unknown":
        input_type = None
    if len(representations) == 1:
        return list(DepthFirstExplorer().explore(representations[0]))
    else:
        return list(DepthFirstExplorer().explore(representations))


@when("the reader gets the file name(s) as input", target_fixture="entries")
def entries_from_file(representation_files):
    return list(DepthFirstExplorer().explore(representation_files))


@then("the result should contain the same number of entries as the input")
def check_predictions(representations, entries):
    if len(representations) == 0:
        # expect one entry saying that nothing could be read from this source
        assert len(entries) == 1
    else:
        assert len(entries) == len(representations)


@then("the result should contain the same number of non-null entries as the input")
def check_predictions_nonnull(representations, entries):
    assert len([e for e in entries if e.mol is not None]) == len(
        [e for e in representations if e is not None]
    )


@then("the source of each entry should be one of the file names")
def check_source(representation_files, entries):
    for entry in entries:
        assert (
            entry.source[0] in representation_files
        ), f"source {entry.source[0]} not in {representation_files}"
