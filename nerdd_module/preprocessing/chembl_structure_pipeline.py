import warnings
from typing import List, Tuple

from rdkit.Chem import Mol
from rdkit.rdBase import BlockLogs

from ..problem import Problem
from .check_valid_smiles import CheckValidSmiles
from .filter_by_element import FilterByElement
from .filter_by_weight import FilterByWeight
from .pipeline import Pipeline
from .remove_stereochemistry import RemoveStereochemistry
from .step import Step

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

__all__ = ["ChemblStructurePipeline", "GetParentMol", "StandardizeWithCsp"]


class StandardizeWithCsp(Step):
    def __init__(self):
        super().__init__()

        if import_error is not None:
            raise import_error

    def _run(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        errors = []

        # chembl structure pipeline cannot handle molecules with 3D coordinates
        # --> delete conformers
        mol.RemoveAllConformers()

        # standardization via chembl structure pipeline
        preprocessed_mol = standardize_mol(mol)

        if preprocessed_mol is None:
            errors.append(Problem("csp_error", "Cannot standardize molecule"))
            preprocessed_mol = mol

        return preprocessed_mol, errors


class GetParentMol(Step):
    def __init__(self):
        super().__init__()

        if import_error is not None:
            raise import_error

    def _run(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        errors = []

        # chembl structure pipeline cannot handle molecules with 3D coordinates
        # --> delete conformers
        mol.RemoveAllConformers()

        # get parent molecule via chembl structure pipeline
        preprocessed_mol, exclude_flag = get_parent_mol(mol)
        if exclude_flag or preprocessed_mol is None:
            errors.append(Problem("csp_error", "Cannot remove small fragments"))
        if preprocessed_mol is None:
            preprocessed_mol = mol

        return preprocessed_mol, errors


class ChemblStructurePipeline(Pipeline):
    def __init__(
        self,
        min_weight=150,
        max_weight=1500,
        allowed_elements=[
            "H",
            "B",
            "C",
            "N",
            "O",
            "F",
            "Si",
            "P",
            "S",
            "Cl",
            "Se",
            "Br",
            "I",
        ],
        remove_stereochemistry=False,
        remove_invalid_molecules=False,
    ):
        super().__init__(
            steps=[
                StandardizeWithCsp(),
                FilterByWeight(
                    min_weight=min_weight,
                    max_weight=max_weight,
                    remove_invalid_molecules=remove_invalid_molecules,
                ),
                FilterByElement(
                    allowed_elements, remove_invalid_molecules=remove_invalid_molecules
                ),
                GetParentMol(),
            ]
            + ([RemoveStereochemistry()] if remove_stereochemistry else [])
            + [CheckValidSmiles()],
            name="chembl_structure_pipeline",
        )
