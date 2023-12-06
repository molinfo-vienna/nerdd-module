import pandas as pd
from nerdd_module import AbstractModel

__all__ = ["AtomicMassModel"]


class AtomicMassModel(AbstractModel):
    def __init__(self, preprocessing_pipeline="no_preprocessing", **kwargs):
        super().__init__(preprocessing_pipeline, **kwargs)

    def _predict_mols(self, mols, multiplier):
        return pd.DataFrame(
            {
                "mol": [m for m in mols for _ in m.GetAtoms()],
                "atom_id": [a.GetIdx() for m in mols for a in m.GetAtoms()],
                "mass": [a.GetMass() * multiplier for m in mols for a in m.GetAtoms()],
            }
        )

    def _get_config(self):
        return {
            "name": "atomic_mass_model",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "mass", "type": "float", "level": "atom"},
            ],
        }
