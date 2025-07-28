import logging
from collections import defaultdict
from typing import Any, Callable, DefaultDict, Iterator, List, Set, Tuple

from ..config import Task
from ..problem import IncompletePredictionProblem, UnknownPredictionProblem
from ..steps import Step
from ..util import call_with_mappings

logger = logging.getLogger(__name__)

__all__ = ["PredictionStep"]


class PredictionStep(Step):
    def __init__(self, predict_fn: Callable, task: Task, batch_size: int, **kwargs: Any) -> None:
        super().__init__()
        self._predict_fn = predict_fn
        self._task = task
        self._batch_size = batch_size
        self._kwargs = kwargs

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

        for batch, none_batch in _batch_and_filter(source, self._batch_size):
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
                        self._predict_fn,
                        {**self._kwargs, "mols": mols},
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
            logger.exception("An error occurred during prediction.", exc_info=e)

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

        # depending on the task, we need to check atom_id or derivative_id
        if self._task == "atom_property_prediction":
            sub_id_property = "atom_id"
        elif self._task == "derivative_property_prediction":
            sub_id_property = "derivative_id"
        else:
            sub_id_property = None

        # create a mapping from mol_id to record (for quick access)
        mol_id_to_record: DefaultDict[int, List[dict]] = defaultdict(list)
        for record in predictions:
            current_record_list = mol_id_to_record[record["mol_id"]]
            current_record_list.append(record)
            if len(current_record_list) > 1 and sub_id_property is None:
                raise ValueError(
                    f"There are duplicate records for mol_id={record['mol_id']}, but the "
                    f"prediction task {self._task} requires unique mol_id values. The duplicates "
                    f"are: {current_record_list}."
                )

        # add all records that are missing in the predictions
        for mol_id in temporary_mol_ids:
            if mol_id not in mol_id_to_record:
                # add a dummy record to the mapping
                mol_id_to_record[mol_id].append(
                    {
                        # notify the user that the molecule could not be predicted
                        "problems": [IncompletePredictionProblem()],
                    }
                )

        if sub_id_property is not None:
            # task must be either atom_property_prediction or derivative_property_prediction
            # -> check consistency of sub_id_property
            for mol_id, records in mol_id_to_record.items():
                sub_ids: Set[int] = set()

                for record in records:
                    sub_id = record.get(sub_id_property)
                    if sub_id is not None:
                        # check that sub_id is an integer
                        if not isinstance(sub_id, int):
                            raise ValueError(
                                f"The {sub_id_property} must be an integer, but got {sub_id}. "
                                f"Record: {record}"
                            )

                        sub_ids.add(sub_id)

                if (
                    len(records) == 1
                    and "problems" in records[0]
                    and len(records[0]["problems"]) > 0
                ):
                    # this record was not predicted, so we skip it
                    continue
                elif len(sub_ids) == 0:
                    # no record has a sub id, we assign them (sequentially)
                    for i, record in enumerate(records):
                        record[sub_id_property] = i
                    continue
                elif len(sub_ids) < len(records):
                    # None is not in sub_ids, but the number of unique sub ids is less than
                    # the number of records.
                    # -> there must be duplicates
                    sub_id_list = [record.get(sub_id_property) for record in records]
                    raise ValueError(
                        f"The result with mol_id={mol_id} contains multiple entries per "
                        f"molecule, but the sequence of {sub_id_property} is not unique. "
                        f"Found: {sub_id_list}."
                    )
                else:
                    min_sub_id = min(sub_ids)
                    max_sub_id = max(sub_ids)

                    if min_sub_id != 0:
                        raise ValueError(
                            f"The sequence of {sub_id_property} does not start at 0 for "
                            f"mol_id={mol_id}. Instead, the minimum {sub_id_property} was "
                            f"{min_sub_id}."
                        )
                    elif max_sub_id - min_sub_id + 1 != len(sub_ids):
                        # there are gaps in the sequence of sub ids
                        raise ValueError(
                            f"The result with mol_id={mol_id} contains multiple entries per "
                            f"molecule, but the sequence of {sub_id_property} has gaps. "
                            f"Found: {sub_ids}."
                        )

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
