from nerdd_module import SimpleModel
from nerdd_module.preprocessing import Sanitize

__all__ = ["AtomicMassModel"]


class AtomicMassModel(SimpleModel):
    def __init__(self, preprocessing_steps=[Sanitize()], version="mol_ids", **kwargs):
        assert version in [
            "mol_ids",
            "mols",
            "error",
        ], f"version must be one of 'mol_ids', 'mols', or 'error', but got {version}."

        super().__init__(preprocessing_steps, **kwargs)
        self._version = version

    def _predict_mols(self, mols, multiplier):
        if self._version == "mol_ids":
            return [
                {
                    "mol_id": i,
                    "atom_id": a.GetIdx(),
                    "mass": a.GetMass() * multiplier,
                }
                for i, m in enumerate(mols)
                for a in m.GetAtoms()
            ]
        elif self._version == "mols":
            return [
                {
                    "mol": m,
                    "atom_id": a.GetIdx(),
                    "mass": a.GetMass() * multiplier,
                }
                for m in mols
                for a in m.GetAtoms()
            ]
        elif self._version == "error":
            raise ValueError("This is an error.")

    def _get_base_config(self):
        return {
            "name": "atomic_mass_model",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "mass", "type": "float", "level": "atom"},
            ],
        }
