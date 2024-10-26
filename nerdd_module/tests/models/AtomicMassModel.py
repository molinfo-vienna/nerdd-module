from nerdd_module import SimpleModel
from nerdd_module.preprocessing import Sanitize

__all__ = ["AtomicMassModel"]


allowed_versions = ["mol_ids", "mols", "iterator", "error"]


class AtomicMassModel(SimpleModel):
    def __init__(self, preprocessing_steps=[Sanitize()], version="mol_ids", **kwargs):
        assert (
            version in allowed_versions
        ), f"version must be one of {allowed_versions}, got {version}"

        super().__init__(preprocessing_steps, **kwargs)
        self._version = version

        if self._version == "iterator":
            self._predict_mols = self._predict_mols_iter

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

    def _predict_mols_iter(self, mols, multiplier):
        if self._version == "iterator":
            for mol in mols:
                for atom in mol.GetAtoms():
                    yield {
                        "mol": mol,
                        "atom_id": atom.GetIdx(),
                        "mass": atom.GetMass() * multiplier,
                    }

    def _get_base_config(self):
        return {
            "name": "atomic_mass_model",
            "version": "0.1",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "mass", "type": "float", "level": "atom"},
            ],
        }
