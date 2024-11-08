import warnings
from typing import List, Optional, Tuple

from rdkit.Chem import Mol
from rdkit.rdBase import BlockLogs

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

# before importing chembl_structure_pipeline, we need to suppress RDKit warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="rdkit.Chem.MolStandardize",
)

try:
    # importing chembl_structure_pipeline already logs messages
    # --> suppress them temporarily
    with BlockLogs():
        from chembl_structure_pipeline import get_parent_mol, standardize_mol

    import_error = None
except ImportError as e:
    # raise ImportError later when using this class
    # --> this allows to use the rest of the package without chembl_structure_pipeline
    import_error = e

__all__ = ["GetParentMolWithCsp", "StandardizeWithCsp"]


class StandardizeWithCsp(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__()

        if import_error is not None:
            raise import_error

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems: List[Problem] = []

        # chembl structure pipeline cannot handle molecules with 3D coordinates
        # --> delete conformers
        mol.RemoveAllConformers()

        # standardization via chembl structure pipeline
        preprocessed_mol = standardize_mol(mol)

        if preprocessed_mol is None:
            problems.append(Problem("csp_error", "Could not standardize the molecule."))
            preprocessed_mol = mol

        return preprocessed_mol, problems


class GetParentMolWithCsp(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__()

        if import_error is not None:
            raise import_error

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems = []

        # chembl structure pipeline cannot handle molecules with 3D coordinates
        # --> delete conformers
        mol.RemoveAllConformers()

        # get parent molecule via chembl structure pipeline
        preprocessed_mol, exclude_flag = get_parent_mol(mol)
        if exclude_flag or preprocessed_mol is None:
            problems.append(Problem("csp_error", "Could not remove small fragments."))
        if preprocessed_mol is None:
            preprocessed_mol = mol

        return preprocessed_mol, problems
