import logging
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, Iterable, List, Optional, Tuple, Union

from rdkit.Chem import Mol

from ..config import (
    Configuration,
    DefaultConfiguration,
    DictConfiguration,
    MergedConfiguration,
    Module,
    PackageConfiguration,
    SearchYamlConfiguration,
)
from ..input import DepthFirstExplorer
from ..preprocessing import PreprocessingStep
from ..problem import Problem
from ..steps import OutputStep, Step
from ..util import get_file_path_to_instance
from .assign_name_step import AssignNameStep
from .convert_representations_step import ConvertRepresentationsStep
from .enforce_schema_step import EnforceSchemaStep
from .prediction_step import PredictionStep
from .read_input_step import ReadInputStep
from .write_output_step import WriteOutputStep

logger = logging.getLogger(__name__)


class Model(ABC):
    def __init__(self, preprocessing_steps: Iterable[Step] = []) -> None:
        super().__init__()

        assert isinstance(
            preprocessing_steps, Iterable
        ), f"Expected Iterable for argument preprocessing_steps, got {type(preprocessing_steps)}"
        assert all(isinstance(step, Step) for step in preprocessing_steps), (
            f"Expected all elements of preprocessing_steps to be of type Step, "
            f"got {[type(step) for step in preprocessing_steps if not isinstance(step, Step)]}"
        )

        self._preprocessing_steps = preprocessing_steps

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        return mol, []

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
            AssignNameStep(),
            *self._preprocessing_steps,
            # the following step ensures that the column preprocessed_mol is created
            # (even if self._preprocessing_steps is empty)
            CustomPreprocessingStep(self),
        ]

    @abstractmethod
    def _predict_mols(self, mols: List[Mol], **kwargs: Any) -> Iterable[dict]:
        pass

    def _get_postprocessing_steps(self, output_format: Optional[str], **kwargs: Any) -> List[Step]:
        output_format = output_format or "pandas"
        return [
            EnforceSchemaStep(self.config, output_format),
            ConvertRepresentationsStep(self.config, output_format, **kwargs),
            WriteOutputStep(output_format, config=self.config, **kwargs),
        ]

    def predict(
        self,
        input: Any,
        input_format: Optional[str] = None,
        output_format: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        input_steps = self._get_input_steps(input, input_format, **kwargs)
        preprocessing_steps = self._get_preprocessing_steps(input, input_format, **kwargs)
        postprocessing_steps = self._get_postprocessing_steps(output_format, **kwargs)
        output_step = postprocessing_steps[-1]

        assert isinstance(output_step, OutputStep), "The last step must be an OutputStep."

        # make mypy happy by restricting the type of self.config.task
        assert self.config.task is not None

        steps = [
            *input_steps,
            *preprocessing_steps,
            PredictionStep(
                self._predict_mols,
                task=self.config.task,
                batch_size=self.config.batch_size,
                **kwargs,
            ),
            *postprocessing_steps,
        ]

        # build the pipeline from the list of steps
        pipeline = None
        for t in steps:
            pipeline = t(pipeline)

        # the last pipeline step holds the result
        return output_step.get_result()

    #
    # Configuration
    #
    def _get_base_config(self) -> Union[Configuration, dict]:
        # get the class of the nerdd module, e.g. <CypstrateModel>
        nerdd_module_class = self.__class__

        # get the module name of the nerdd module class
        # e.g. "cypstrate.cypstrate_model"
        python_module = nerdd_module_class.__module__

        # get the root module name, e.g. "cypstrate"
        root_module = python_module.split(".")[0]

        configs: List[Configuration] = []

        try:
            configs.append(  # TODO: remove "."
                SearchYamlConfiguration(get_file_path_to_instance(self) or ".")
            )
        except Exception:
            pass

        try:
            configs.append(PackageConfiguration(f"{root_module}.data", filename="nerdd.yml"))
        except Exception:
            pass

        return MergedConfiguration(*configs)

    def _get_config(self) -> Configuration:
        # get base configuration specified in this class
        base_config = self._get_base_config()
        if isinstance(base_config, dict):
            base_config = DictConfiguration(base_config)

        # ensure that mandatory properties are present
        base_config = MergedConfiguration(DefaultConfiguration(self), base_config)

        # add default properties mol_id, raw_input, etc.
        task = base_config.get_dict().task

        # check whether we need to add to add a property "atom_id" or "derivative_id"
        task_based_property = []
        if task == "atom_property_prediction":
            task_based_property = [
                {"name": "atom_id", "type": "int", "visible": False},
            ]
        elif task == "derivative_property_prediction":
            task_based_property = [
                {"name": "derivative_id", "type": "int", "visible": False},
            ]

        default_properties_start = [
            {"name": "mol_id", "type": "int", "visible": False},
            *task_based_property,
            {
                "name": "input_text",
                "visible_name": "Input text",
                "type": "string",
                "visible": False,
            },
            {
                "name": "input_type",
                "visible_name": "Input type",
                "type": "string",
                "visible": False,
            },
            {
                "name": "source",
                "visible_name": "Source",
                "type": "source_list",
                "visible": False,
            },
            {"name": "name", "visible_name": "Name", "type": "string"},
            {
                "name": "input_mol",
                "visible_name": "Input Structure",
                "type": "mol",
                "visible": False,
            },
            {
                "name": "input_smiles",
                "visible_name": "Input SMILES",
                "type": "representation",
                "from_property": "input_mol",
                "visible": False,
            },
            {
                "name": "preprocessed_mol",
                "visible_name": "Preprocessed Structure",
                "type": "mol",
            },
            {
                "name": "preprocessed_smiles",
                "visible_name": "Preprocessed SMILES",
                "type": "representation",
                "from_property": "preprocessed_mol",
                "visible": False,
            },
        ]

        default_properties_end = [
            {
                "name": "problems",
                "visible_name": "Problems",
                "type": "problem_list",
                "visible": False,
            },
        ]

        configs = [
            DictConfiguration({"result_properties": default_properties_start}),
            base_config,
            DictConfiguration({"result_properties": default_properties_end}),
        ]

        return MergedConfiguration(*configs)

    @cached_property
    def config(self) -> Module:
        return self._get_config().get_dict()


class CustomPreprocessingStep(PreprocessingStep):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        try:
            return self.model._preprocess(mol)
        except Exception as e:
            return None, [Problem(type="preprocessing_error", message=str(e))]
