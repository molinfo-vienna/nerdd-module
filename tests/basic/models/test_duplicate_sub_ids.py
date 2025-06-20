from rdkit.Chem import MolFromSmiles

from nerdd_module import Model
from nerdd_module.config import Task

example_molecules = [
    MolFromSmiles("CCO"),
]

class DuplicateSubIdsModel(Model):

    def __init__(self, task : Task):
        super().__init__()
        assert task in ["atom_property_prediction", "derivative_property_prediction"], "Invalid task"
        self._task = task

    def _predict_mols(self, mols):
        sub_id = "atom_id" if self._task == "atom_property_prediction" else "derivative_id"
        return [{ "mol_id": 0, sub_id: 0, "p": 1 }, { "mol_id": 0, sub_id: 0, "p": 2 }]
    
    def _get_base_config(self):
        if self._task == "atom_property_prediction":
            level = "atom"
        elif self._task == "derivative_property_prediction":
            level = "derivative"
        else:
            raise ValueError(f"Invalid task: {self._task}")

        return {
            "task": self._task,
            "result_properties": [{
                "name": "p", 
                "type": "int",
                "level": level,
            }]
        }
    

def test_model_returns_duplicate_sub_ids_atom_property_prediction():
    model = DuplicateSubIdsModel("atom_property_prediction")
    try:
        model.predict(example_molecules, output_format="record_list")
    except ValueError:
        assert True, "Expected ValueError due to duplicate sub_ids"
        return
    assert False, "Expected ValueError due to duplicate sub_ids not raised"

def test_model_returns_duplicate_sub_ids_derivative_property_prediction():
    model = DuplicateSubIdsModel("derivative_property_prediction")
    try:
        model.predict(example_molecules, output_format="record_list")
    except ValueError:
        assert True, "Expected ValueError due to duplicate sub_ids"
        return
    assert False, "Expected ValueError due to duplicate sub_ids not raised"