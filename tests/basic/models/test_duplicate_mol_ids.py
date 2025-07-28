from rdkit.Chem import MolFromSmiles

from nerdd_module import Model
from nerdd_module.config import Task

example_molecules = [
    MolFromSmiles("CCO"),
]

class DuplicateMolIdsModel(Model):

    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [{ "mol_id": 0, "p": 1 }, { "mol_id": 0, "p": 2 }]
    
    def _get_base_config(self):

        return {
            "result_properties": [{
                "name": "p", 
                "type": "int",
            }]
        }
    
def test_model_returns_duplicate_mol_ids_molecular_property_prediction():
    model = DuplicateMolIdsModel()
    try:
        model.predict(example_molecules, output_format="record_list")
    except ValueError:
        assert True, "Expected ValueError due to duplicate mol_ids"
        return
    
    assert False, "Expected ValueError due to duplicate mol_ids not raised"