from rdkit.Chem import SanitizeMol

from .preprocessing_step import PreprocessingStep

__all__ = ["Sanitize"]


class Sanitize(PreprocessingStep):
    def __init__(self):
        super().__init__()

    def _preprocess(self, mol):
        errors = []

        # sanitize molecule
        SanitizeMol(mol)

        return mol, errors
