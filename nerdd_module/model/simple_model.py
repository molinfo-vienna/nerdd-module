from abc import abstractmethod
from typing import Any, Iterable, List, Optional, Tuple, Union

from rdkit.Chem import Mol

from ..config import (
    Configuration,
    DefaultConfiguration,
    DictConfiguration,
    JobParameter,
    MergedConfiguration,
    Module,
    PackageConfiguration,
    SearchYamlConfiguration,
)
from ..input import DepthFirstExplorer
from ..preprocessing import PreprocessingStep
from ..problem import Problem
from ..steps import Step
from ..util import get_file_path_to_instance
from .assign_mol_id_step import AssignMolIdStep
from .assign_name_step import AssignNameStep
from .convert_representations_step import ConvertRepresentationsStep
from .enforce_schema_step import EnforceSchemaStep
from .model import Model
from .read_input_step import ReadInputStep
from .write_output_step import WriteOutputStep

__all__ = ["SimpleModel"]


class SimpleModel(Model):
    def __init__(self, preprocessing_steps: Iterable[Step] = []) -> None:
        super().__init__()
        assert isinstance(preprocessing_steps, Iterable), (
            f"Expected Iterable for argument preprocessing_steps, "
            f"got {type(preprocessing_steps)}"
        )
        assert all(isinstance(step, Step) for step in preprocessing_steps), (
            f"Expected all elements of preprocessing_steps to be of type Step, "
            f"got {[type(step) for step in preprocessing_steps if not isinstance(step, Step)]}"
        )
        self._preprocessing_steps = preprocessing_steps

    def _get_input_steps(
        self, input: Any, input_format: Optional[str], **kwargs: Any
    ) -> List[Step]:
        return [
            ReadInputStep(DepthFirstExplorer(**kwargs), input),
        ]

    def _get_preprocessing_steps(
        self, input: Any, input_format: Optional[str], **kwargs: Any
    ) -> List[Step]:
        return [
            AssignMolIdStep(),
            AssignNameStep(),
            *self._preprocessing_steps,
            # the following step ensures that the column preprocessed_mol is created
            # (even is self._preprocessing_steps is empty)
            CustomPreprocessingStep(self),
        ]

    def _get_postprocessing_steps(self, output_format: Optional[str], **kwargs: Any) -> List[Step]:
        output_format = output_format or "pandas"
        return [
            EnforceSchemaStep(self._get_config(), output_format),
            ConvertRepresentationsStep(
                self.get_config().result_properties, output_format, **kwargs
            ),
            WriteOutputStep(output_format, **kwargs),
        ]

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        return mol, []

    @abstractmethod
    def _predict_mols(self, mols: List[Mol], **kwargs: Any) -> List[dict]:
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
            # TODO: remove "."
            SearchYamlConfiguration(get_file_path_to_instance(self) or "."),
            PackageConfiguration(f"{root_module}.data"),
            # base config comes last -> highest priority
            base_config,
        ]

        # add default properties mol_id, raw_input, etc.
        task = MergedConfiguration(*configs).get_dict().task

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
            {"name": "input_text", "type": "string"},
            {"name": "input_type", "type": "string"},
            {"name": "source", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "input_mol", "type": "mol"},
            {"name": "preprocessed_mol", "type": "mol"},
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

    def get_config(self) -> Module:
        return self._get_config().get_dict()

    def _get_batch_size(self) -> int:
        default = super()._get_batch_size()
        return self.get_config().batch_size or default

    def _get_name(self) -> str:
        default = super()._get_name()
        return self.get_config().name or default

    def _get_description(self) -> str:
        default = super()._get_description()
        return self.get_config().description or default

    def _get_job_parameters(self) -> List[JobParameter]:
        return super()._get_job_parameters() + self.get_config().job_parameters


class CustomPreprocessingStep(PreprocessingStep):
    def __init__(self, model: SimpleModel):
        super().__init__()
        self.model = model

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        return self.model._preprocess(mol)
