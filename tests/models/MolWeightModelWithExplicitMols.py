import pandas as pd
from nerdd_module import AbstractModel
from rdkit.Chem.Descriptors import MolWt

__all__ = ["MolWeightModelWithExplicitMols"]


class MolWeightModelWithExplicitMols(AbstractModel):
    def __init__(self, preprocessing_pipeline="no_preprocessing", **kwargs):
        super().__init__(preprocessing_pipeline, **kwargs)

    def _predict_mols(self, mols, multiplier):
        return pd.DataFrame(
            {
                "mol": mols,
                "weight": [MolWt(m) * multiplier for m in mols],
            }
        )

    def _get_config(self):
        return {
            "name": "mol_weight_model_with_explicit_mols",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "weight", "type": "float"},
            ],
        }
