from nerdd_module import SimpleModel
from nerdd_module.preprocessing import Sanitize
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

__all__ = ["MolWeightModel"]

allowed_versions = ["order_based", "mol_ids", "mols", "iterator", "error"]


class MolWeightModel(SimpleModel):
    def __init__(self, preprocessing_steps=[Sanitize()], version="order_based", **kwargs):
        assert (
            version in allowed_versions
        ), f"version must be one of {allowed_versions}, got {version}"

        super().__init__(preprocessing_steps, **kwargs)
        self._version = version

        if self._version == "iterator":
            self._predict_mols = self._predict_mols_iterator

    def _predict_mols(self, mols, multiplier):
        if self._version == "order_based":
            return [{"weight": CalcExactMolWt(m) * multiplier} for m in mols]
        elif self._version == "mol_ids":
            return [
                {"mol_id": i, "weight": CalcExactMolWt(m) * multiplier} for i, m in enumerate(mols)
            ]
        elif self._version == "mols":
            return [{"mol": m, "weight": CalcExactMolWt(m) * multiplier} for m in mols]
        elif self._version == "error":
            raise ValueError("This is an error")

    def _predict_mols_iterator(self, mols, multiplier):
        if self._version == "iterator":
            for mol in mols:
                yield {"weight": CalcExactMolWt(mol) * multiplier}

    def _get_base_config(self):
        return {
            "name": "mol_scale",
            "version": "0.1",
            "description": "Computes the molecular weight of a molecule",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "weight", "type": "float"},
            ],
        }
