from rdkit.Chem import MolFromSmiles

from nerdd_module import Model
from nerdd_module.config import Task

example_molecules = [
    MolFromSmiles("CCO"),
]


class ReturnNothingModel(Model):
    """
    A model that does not return any predictions.
    """

    def __init__(self, task: Task):
        super().__init__()
        self._task = task

    def _predict_mols(self, mols):
        return []

    def _get_base_config(self):
        if self._task == "molecular_property_prediction":
            level = "molecule"
        elif self._task == "atom_property_prediction":
            level = "atom"
        elif self._task == "derivative_property_prediction":
            level = "derivative"
        else:
            raise ValueError(f"Unknown task: {self._task}")

        return {
            "task": self._task,
            "result_properties": [
                {
                    "name": "p",
                    "type": "int",
                    "level": level,
                }
            ],
        }


def test_model_returns_nothing_molecular_property_prediction():
    """
    Test that the ReturnNothingModel does not return any predictions.
    """
    model = ReturnNothingModel("molecular_property_prediction")
    results = model.predict(example_molecules, output_format="record_list")
    assert len(results) == 1, "Expected one result"
    assert len(results[0]["problems"]) == 1, "Expected one problem in the result"


def test_model_returns_nothing_atom_property_prediction():
    """
    Test that the ReturnNothingModel does not return any predictions.
    """
    model = ReturnNothingModel("atom_property_prediction")
    results = model.predict(example_molecules, output_format="record_list")
    assert len(results) == 1, "Expected one result"
    assert len(results[0]["problems"]) == 1, "Expected one problem in the result"


def test_model_returns_nothing_derivative_property_prediction():
    """
    Test that the ReturnNothingModel does not return any predictions.
    """
    model = ReturnNothingModel("derivative_property_prediction")
    results = model.predict(example_molecules, output_format="record_list")
    assert len(results) == 1, "Expected one result"
    assert len(results[0]["problems"]) == 1, "Expected one problem in the result"
