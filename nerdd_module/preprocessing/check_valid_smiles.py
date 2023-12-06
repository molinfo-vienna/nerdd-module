from typing import List, Tuple

from rdkit.Chem import Mol, MolFromSmiles, MolToSmiles

from .step import Step

__all__ = ["CheckValidSmiles"]


class CheckValidSmiles(Step):
    def __init__(self):
        super().__init__()

    def _run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        """
        Function that checks if each rdkit mol is convertable into a smiles and back
        into a molecule
        """
        errors = []

        smi = MolToSmiles(mol, True)
        check_mol = MolFromSmiles(smi)
        if check_mol is None:
            errors.append("V1")
            mol = None

        return mol, errors
