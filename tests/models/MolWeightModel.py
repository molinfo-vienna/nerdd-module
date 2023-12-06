import pandas as pd
from nerdd_module import AbstractModel
from rdkit.Chem.Descriptors import MolWt

__all__ = ["MolWeightModel"]


class MolWeightModel(AbstractModel):
    def __init__(self, preprocessing_pipeline="no_preprocessing", **kwargs):
        super().__init__(preprocessing_pipeline, **kwargs)

    def _predict_mols(self, mols, multiplier):
        return pd.DataFrame(
            {
                "weight": [MolWt(m) * multiplier for m in mols],
            }
        )

    def _get_config(self):
        return {
            "name": "mol_weight_model",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "weight", "type": "float"},
            ],
        }
