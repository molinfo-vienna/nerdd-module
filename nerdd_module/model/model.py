import logging
from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Optional

from rdkit.Chem import Mol
from stringcase import snakecase  # type: ignore

from ..config import JobParameter
from ..steps import OutputStep, Step
from .prediction_step import PredictionStep

logger = logging.getLogger(__name__)


class Model(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def _predict_mols(self, mols: List[Mol], **kwargs: Any) -> Iterable[dict]:
        pass

    @abstractmethod
    def _get_input_steps(
        self, input: Any, input_format: Optional[str], **kwargs: Any
    ) -> List[Step]:
        pass

    @abstractmethod
    def _get_preprocessing_steps(
        self, input: Any, input_format: Optional[str], **kwargs: Any
    ) -> List[Step]:
        pass

    @abstractmethod
    def _get_postprocessing_steps(self, output_format: Optional[str], **kwargs: Any) -> List[Step]:
        pass

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

        steps = [
            *input_steps,
            *preprocessing_steps,
            PredictionStep(self._predict_mols, batch_size=self.batch_size, **kwargs),
            *postprocessing_steps,
        ]

        # build the pipeline from the list of steps
        pipeline = None
        for t in steps:
            pipeline = t(pipeline)

        # the last pipeline step holds the result
        return output_step.get_result()

    #
    # Properties
    #
    def _get_batch_size(self) -> int:
        return 1

    batch_size = property(fget=lambda self: self._get_batch_size())

    def _get_name(self) -> str:
        return snakecase(self.__class__.__name__)

    name = property(fget=lambda self: self._get_name())

    def _get_description(self) -> str:
        return ""

    description = property(fget=lambda self: self._get_description())

    def _get_job_parameters(self) -> List[JobParameter]:
        return []

    job_parameters = property(fget=lambda self: self._get_job_parameters())
