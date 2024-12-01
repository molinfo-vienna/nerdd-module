from nerdd_module.input import DepthFirstExplorer
from pytest_bdd import parsers, then, when


@when(
    parsers.parse("the reader gets the representations as input"),
    target_fixture="predictions",
)
def entries(representations):
    if len(representations) == 1:
        return list(DepthFirstExplorer().explore(representations[0]))
    else:
        return list(DepthFirstExplorer().explore(representations))


@when("the reader gets the file name(s) as input", target_fixture="predictions")
def entries_from_file(files):
    return list(DepthFirstExplorer().explore(files))


@then("the result should contain the same number of non-null entries as the input")
def check_predictions_nonnull(representations, predictions):
    assert len([e for e in predictions if e.mol is not None]) == len(
        [e for e in representations if e is not None]
    )


@then("the source of each entry should be one of the file names")
def check_source(files, predictions):
    for entry in predictions:
        assert entry.source[0] in files, f"source {entry.source[0]} not in {files}"
