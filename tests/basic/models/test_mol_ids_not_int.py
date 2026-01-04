import numpy as np

from nerdd_module import Model


class InvalidMolIdsModel(Model):
    """
    A model that returns predictions with invalid molecule IDs.
    """

    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [{"mol_id": "not_an_int", "problems": []} for _ in mols]


def test_invalid_mol_ids():
    """
    Test that the InvalidMolIdsModel raises errors when returning invalid molecule IDs.
    """
    model = InvalidMolIdsModel()
    try:
        model.predict("CCO", output_format="record_list")
        raise AssertionError("Expected ValueError for invalid mol_id, but none was raised.")
    except ValueError:
        pass


class CastableMolIdsModel(Model):
    """
    A model that returns predictions with invalid molecule IDs.
    """

    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [
            {"mol_id": np.array([i], dtype=np.float32)[0], "problems": []}
            for i, _ in enumerate(mols)
        ]


def test_castable_mol_ids():
    """
    Test that the CastableMolIdsModel returns valid predictions.
    """
    model = CastableMolIdsModel()
    try:
        model.predict("CCO", output_format="record_list")
        return
    except Exception:
        raise AssertionError(
            "Expected no error for castable mol_id, but an error was raised."
        ) from None
