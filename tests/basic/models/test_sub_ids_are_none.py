from rdkit.Chem import MolFromSmiles

from nerdd_module import Model
from nerdd_module.config import Task

example_molecules = [
    MolFromSmiles("CCO"),
]


class SubIdsNoneModel(Model):
    def __init__(self, task: Task):
        super().__init__()
        assert task in [
            "atom_property_prediction",
            "derivative_property_prediction",
        ], "Invalid task"
        self._task = task

    def _predict_mols(self, mols):
        return [{"mol_id": 0, "p": 1}, {"mol_id": 0, "p": 1}]

    def _get_base_config(self):
        if self._task == "atom_property_prediction":
            level = "atom"
        elif self._task == "derivative_property_prediction":
            level = "derivative"
        else:
            raise ValueError(f"Invalid task: {self._task}")

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


def test_sub_ids_are_none_atom_property_prediction():
    model = SubIdsNoneModel("atom_property_prediction")
    results = model.predict(example_molecules, output_format="record_list")
    assert len(results) == 2, "Expected two results for atom_property_prediction"
    for i, result in enumerate(results):
        assert "atom_id" in result, f"Expected atom_id in result {i}"
        assert result["atom_id"] == i, f"Expected atom_id {i} in result {i}"


def test_sub_ids_are_none_derivative_property_prediction():
    model = SubIdsNoneModel("derivative_property_prediction")
    results = model.predict(example_molecules, output_format="record_list")
    assert len(results) == 2, "Expected two results for derivative_property_prediction"
    for i, result in enumerate(results):
        assert "derivative_id" in result, f"Expected derivative_id in result {i}"
        assert result["derivative_id"] == i, f"Expected derivative_id {i} in result {i}"
