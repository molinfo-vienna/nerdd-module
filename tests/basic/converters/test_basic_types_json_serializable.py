import json

import numpy as np
from rdkit.Chem import MolFromSmiles

from nerdd_module import Model

example_molecules = [
    MolFromSmiles("CCO"),
    MolFromSmiles("CCN"),
]

class ModelReturningNumpyTypes(Model):

    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [
            { "mol_id": 0, "p": np.int32(3), "q": np.float32(3.1), "r": np.bool_(False), "s": np.str_("test") }, 
            { "mol_id": 1, "p": np.int32(4), "q": np.float32(4.2), "r": np.bool_(True), "s": np.str_("example") }
        ]
    
    def _get_base_config(self):

        return {
            "result_properties": [{
                "name": "p", 
                "type": "int",
            }, {
                "name": "q", 
                "type": "float",
            }, {
                "name": "r", 
                "type": "bool",
            }, {
                "name": "s", 
                "type": "string",
            }]
        }
    
def test_basic_types_json_serializable():
    model = ModelReturningNumpyTypes()
    
    results = model.predict(example_molecules, output_format="record_list")

    # check types
    for r in results:
        assert isinstance(r["p"], int)
        assert isinstance(r["q"], float)
        assert isinstance(r["r"], bool)
        assert isinstance(r["s"], str)

    # this should not raise an error
    json.dumps([dict(p=r["p"], q=r["q"], r=r["r"], s=r["s"]) for r in results])