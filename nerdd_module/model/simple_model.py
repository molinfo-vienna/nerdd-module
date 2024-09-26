import sys
from abc import abstractmethod
from typing import Any, Iterable, List, Optional, Tuple, Union

from rdkit.Chem import Mol

from ..config import (
    Configuration,
    DefaultConfiguration,
    DictConfiguration,
    MergedConfiguration,
    PackageConfiguration,
    SearchYamlConfiguration,
)
from ..input import DepthFirstExplorer
from ..preprocessing import PreprocessingStep
from ..problem import Problem
from ..steps import Step
from ..util import get_file_path_to_instance
from .add_smiles import AddSmiles
from .assign_mol_id import AssignMolId
from .assign_name import AssignName
from .enforce_schema import EnforceSchema
from .model import Model
from .read_input import ReadInput
from .write_output import WriteOutput

__all__ = ["SimpleModel"]


class SimpleModel(Model):
    def __init__(self, preprocessing_steps: Iterable[Step] = []):
        super().__init__()
        self._preprocessing_steps = preprocessing_steps

    def _get_input_steps(
        self, input: Any, input_format: Optional[str], **kwargs
    ) -> List[Step]:
        return [
            ReadInput(DepthFirstExplorer(), input),
            AssignMolId(),
            AssignName(),
            *self._preprocessing_steps,
            # the following step ensures that the column preprocessed_mol is created
            # (even is self._preprocessing_steps is empty)
            CustomPreprocessingStep(self),
        ]

    def _get_output_steps(self, output_format: Optional[str], **kwargs) -> List[Step]:
        output_format = output_format or "pandas"

        return [
            AddSmiles("input_mol", "input_smiles"),
            AddSmiles("preprocessed_mol", "preprocessed_smiles"),
            EnforceSchema(self._get_config()),
            WriteOutput(output_format, **kwargs),
        ]

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        return mol, []

    @abstractmethod
    def _predict_mols(self, mols: List[Mol], **kwargs) -> List[dict]:
        pass

    def _get_base_config(self) -> Union[Configuration, dict]:
        return {}

    def _get_config(self) -> Configuration:
        # get base configuration specified in this class
        base_config = self._get_base_config()
        if isinstance(base_config, dict):
            base_config = DictConfiguration(base_config)

        # get the class of the nerdd module, e.g. <CypstrateModel>
        nerdd_module_class = self.__class__

        # get the module name of the nerdd module class
        # e.g. "cypstrate.cypstrate_model"
        python_module = nerdd_module_class.__module__

        # get the root module name, e.g. "cypstrate"
        root_module = python_module.split(".")[0]

        configs = [
            DefaultConfiguration(self),
            SearchYamlConfiguration(get_file_path_to_instance(self)),
            PackageConfiguration(f"{root_module}.data"),
            # base config comes last -> highest priority
            base_config,
        ]

        # add default properties mol_id, raw_input, etc.
        task = MergedConfiguration(*configs).get_task()

        # check whether we need to add to add a property "atom_id" or "derivative_id"
        task_based_property = []
        if task == "atom_property_prediction":
            task_based_property = [
                {"name": "atom_id", "type": "integer"},
            ]
        elif task == "derivative_property_prediction":
            task_based_property = [
                {"name": "derivative_id", "type": "integer"},
            ]

        default_properties_start = [
            {"name": "mol_id", "type": "integer"},
            *task_based_property,
            {"name": "raw_input", "type": "string"},
            {"name": "input_type", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "input_mol", "type": "mol"},
            {"name": "input_smiles", "type": "string"},
            {"name": "preprocessed_mol", "type": "mol"},
            {"name": "preprocessed_smiles", "type": "string"},
        ]

        default_properties_end = [
            {"name": "problems", "type": "problem_list"},
        ]

        configs = [
            DictConfiguration({"result_properties": default_properties_start}),
            *configs,
            DictConfiguration({"result_properties": default_properties_end}),
        ]

        return MergedConfiguration(*configs)

    def get_config(self) -> dict:
        return self._get_config().get_dict()


class CustomPreprocessingStep(PreprocessingStep):
    def __init__(self, model: SimpleModel):
        super().__init__()
        self.model = model

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        return self.model._preprocess(mol)
