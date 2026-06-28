import numpy as np

from nerdd_module import Model


class InvalidAtomIdsModel(Model):
    """
    A model that returns predictions with invalid atom IDs.
    """

    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [
            {"mol_id": i, "atom_id": "not_an_int", "some_property": 42, "problems": []}
            for i, _ in enumerate(mols)
        ]

    def _get_base_config(self):
        return {
            "task": "atom_property_prediction",
            # for atom property prediction, we need at least one atom-level property
            "result_properties": [
                {
                    "name": "some_property",
                    "level": "atom",
                    "type": "int",
                }
            ],
        }


def test_invalid_atom_ids():
    """
    Test that the InvalidAtomIdsModel raises errors when returning invalid atom IDs.
    """
    model = InvalidAtomIdsModel()
    try:
        model.predict("CCO", output_format="record_list")
        raise AssertionError("Expected ValueError for invalid atom_id, but none was raised.")
    except ValueError:
        pass


class CastableAtomIdsModel(Model):
    """
    A model that returns predictions with castable atom IDs.
    """

    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [
            {
                "mol_id": i,
                "atom_id": np.array([j], dtype=np.float32)[0],
                "some_property": 42,
                "problems": [],
            }
            for i, _ in enumerate(mols)
            for j in range(3)
        ]

    def _get_base_config(self):
        return {
            "task": "atom_property_prediction",
            # for atom property prediction, we need at least one atom-level property
            "result_properties": [
                {
                    "name": "some_property",
                    "level": "atom",
                    "type": "int",
                }
            ],
        }


def test_castable_atom_ids():
    """
    Test that the CastableAtomIdsModel returns valid predictions.
    """
    model = CastableAtomIdsModel()
    try:
        model.predict("CCO", output_format="record_list")
        return
    except Exception:
        raise AssertionError(
            "Expected no error for castable atom_id, but an error was raised."
        ) from None
