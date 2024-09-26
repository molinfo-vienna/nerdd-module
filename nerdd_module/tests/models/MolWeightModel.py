from rdkit.Chem.Descriptors import MolWt

from nerdd_module import SimpleModel
from nerdd_module.preprocessing import Sanitize

__all__ = ["MolWeightModel"]


class MolWeightModel(SimpleModel):
    def __init__(
        self, preprocessing_steps=[Sanitize()], version="order_based", **kwargs
    ):
        assert version in ["order_based", "mol_ids", "mols", "error"], (
            f"version must be one of 'order_based', 'mol_ids', 'mols', or 'error',"
            f"but got {version}."
        )

        super().__init__(preprocessing_steps, **kwargs)
        self._version = version

    def _predict_mols(self, mols, multiplier):
        if self._version == "order_based":
            return [{"weight": MolWt(m) * multiplier} for m in mols]
        elif self._version == "mol_ids":
            return [
                {"mol_id": i, "weight": MolWt(m) * multiplier}
                for i, m in enumerate(mols)
            ]
        elif self._version == "mols":
            return [{"mol": m, "weight": MolWt(m) * multiplier} for m in mols]
        elif self._version == "error":
            raise ValueError("This is an error")

    def _get_base_config(self):
        return {
            "name": "mol_weight_model",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "weight", "type": "float"},
            ],
        }
