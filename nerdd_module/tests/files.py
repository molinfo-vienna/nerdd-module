from tempfile import NamedTemporaryFile

import numpy as np
from pytest_bdd import given, parsers

from .representations import representations_from_molecules


@given(
    parsers.parse("a file containing the molecules in {input_type} format"),
    target_fixture="files",
)
def representation_file(molecules, input_type):
    representations = representations_from_molecules(molecules, input_type)

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
        return [f.name]


@given(
    parsers.parse(
        "a list of {num_files:d} files containing the representations in {input_type} format",
    ),
    target_fixture="files",
)
def representation_files(molecules, input_type, num_files):
    representations = representations_from_molecules(molecules, input_type)

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
