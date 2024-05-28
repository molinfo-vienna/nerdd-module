from rdkit.Chem import SanitizeMol

from .step import Step

__all__ = ["Sanitize"]


class Sanitize(Step):
    def __init__(self):
        super().__init__()

    def _run(self, mol):
        errors = []

        # sanitize molecule
        SanitizeMol(mol)

        return mol, errors
