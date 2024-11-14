import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Iterable, Iterator, List, Optional, Tuple

from rdkit.Chem import Mol
from stringcase import snakecase  # type: ignore

from ..config import JobParameter
from ..problem import Problem
from ..steps import OutputStep, Step
from ..util import call_with_mappings

logger = logging.getLogger(__name__)


# an unknown prediction problem indicates that the model raised an exception during
# prediction
def UnknownPredictionProblem() -> Problem:
    return Problem("unknown_prediction_error", "An unknown error occured during prediction.")


# an incomplete prediction problem indicates that the model successfully returns
# predictions, but part of the input molecules are missing in the results
def IncompletePredictionProblem() -> Problem:
    return Problem("incomplete_prediction_error", "The model couldn't process the molecule.")


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
            PredictionStep(self, batch_size=self.batch_size, **kwargs),
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

    batch_size = property(_get_batch_size)

    def _get_name(self) -> str:
        return snakecase(self.__class__.__name__)

    name = property(fget=lambda self: self._get_name())

    def _get_description(self) -> str:
        return ""

    description = property(fget=lambda self: self._get_description())

    def _get_job_parameters(self) -> List[JobParameter]:
        return []

    job_parameters = property(fget=lambda self: self._get_job_parameters())


class PredictionStep(Step):
    def __init__(self, model: Model, batch_size: int, **kwargs: Any) -> None:
        super().__init__()
        self.model = model
        self.batch_size = batch_size
        self.kwargs = kwargs

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        # We need to process the molecules in batches, because most ML models perform
        # better when predicting multiple molecules at once. Additionally, we want to
        # filter out molecules that could not be preprocessed.
        def _batch_and_filter(
            source: Iterator[dict], n: int
        ) -> Iterator[Tuple[List[dict], List[dict]]]:
            batch = []
            none_batch = []
            for record in source:
                if record["preprocessed_mol"] is None:
                    none_batch.append(record)
                else:
                    batch.append(record)
                    if len(batch) == n:
                        yield batch, none_batch
                        batch = []
                        none_batch = []
            if len(batch) > 0 or len(none_batch) > 0:
                yield batch, none_batch

        for batch, none_batch in _batch_and_filter(source, self.batch_size):
            # return the records where mols are None
            yield from none_batch

            # process the batch
            yield from self._process_batch(batch)

    def _process_batch(self, batch: List[dict]) -> Iterator[dict]:
        # each molecule gets a unique id (0, 1, ..., n) as its temporary id
        mol_ids = [record["mol_id"] for record in batch]
        mols = [record["preprocessed_mol"] for record in batch]
        temporary_mol_ids = range(len(batch))
        for id, mol in zip(temporary_mol_ids, mols):
            mol.SetProp("_TempId", str(id))

        # do the actual prediction
        try:
            if len(batch) > 0:
                predictions = list(
                    call_with_mappings(
                        self.model._predict_mols,
                        {**self.kwargs, "mols": mols},
                    )
                )
            else:
                predictions = []

            # check that the predictions are a list
            assert isinstance(predictions, list), "The predictions must be an iterable."
            assert all(
                isinstance(record, dict) for record in predictions
            ), "The predictions must be a list of dictionaries."
        except Exception as e:
            logger.error(e, exc_info=True)

            # if an error occurs, we want to catch it and yield the error message
            predictions = [
                {
                    "mol_id": i,
                    "problems": [UnknownPredictionProblem()],
                }
                for i, _ in enumerate(batch)
            ]

        # During prediction, molecules might have been removed / reordered.
        # There are three ways to connect the predictions to the original molecules:
        # 1. predictions have a key "mol_id" that contains the molecule ids
        # 2. predictions have a key "mol" that contains the molecules that were passed
        #    to the _predict_mols method (they have a secret _TempId property that we
        #    can use for the matching)
        # 3. the list of predictions has as many records as the batch (and we assume
        #    that the order of the molecules stayed the same)
        if all("mol_id" in record for record in predictions):
            pass
        elif all("mol" in record for record in predictions):
            # check that molecule names contain only valid ids
            for record in predictions:
                mol_id_from_mol = int(record["mol"].GetProp("_TempId"))
                record["mol_id"] = mol_id_from_mol

                # we don't need the molecule anymore (we have it in the batch)
                del record["mol"]
        else:
            assert len(predictions) == len(batch), (
                "The number of predicted molecules must be equal to the number of "
                "valid input molecules."
            )
            for i, record in enumerate(predictions):
                record["mol_id"] = i

        # check that mol_id contains only valid ids
        mol_id_set = set(temporary_mol_ids)
        for record in predictions:
            assert (
                record["mol_id"] in mol_id_set
            ), f"The mol_id {record['mol_id']} is not in the batch."

        # create a mapping from mol_id to record (for quick access)
        mol_id_to_record = defaultdict(list)
        for record in predictions:
            mol_id_to_record[record["mol_id"]].append(record)

        # add all records that are missing in the predictions
        for mol_id, record in zip(temporary_mol_ids, batch):
            if mol_id not in mol_id_to_record:
                # notify the user that the molecule could not be predicted
                record["problems"].append(IncompletePredictionProblem())

                # add the record to the mapping
                mol_id_to_record[mol_id].append(record)

        # If the result has multiple entries per mol_id, check that atom_id or
        # derivative_id is present in multi-entry results.
        if len(predictions) > len(batch):
            for _, records in mol_id_to_record.items():
                if len(records) > 1:
                    has_atom_id = all("atom_id" in record for record in records)
                    has_derivative_id = all("derivative_id" in record for record in records)
                    assert has_atom_id or has_derivative_id, (
                        "The result contains multiple entries per molecule, but does "
                        "not contain atom_id or derivative_id."
                    )

        # TODO: check range and completeness of atom ids and derivative ids

        for key, records in mol_id_to_record.items():
            for record in records:
                # merge the prediction with the original record
                result = {
                    **batch[key],
                    **record,
                }

                # remove the temporary id
                result["preprocessed_mol"].ClearProp("_TempId")

                # add the original mol id
                result["mol_id"] = mol_ids[key]

                # merge problems from preprocessing and prediction
                preprocessing_problems = batch[key].get("problems", [])
                prediction_problems = record.get("problems", [])
                result["problems"] = preprocessing_problems + prediction_problems

                yield result
