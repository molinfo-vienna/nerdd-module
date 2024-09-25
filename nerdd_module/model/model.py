from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Iterator, List, Optional

from rdkit.Chem import Mol

from ..problem import UnknownProblem
from ..steps import Step
from ..util import call_with_mappings
from .write_output import WriteOutput


class Model(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _predict_mols(self, mols: List[Mol], **kwargs) -> List[dict]:
        pass

    @abstractmethod
    def _get_input_steps(
        self, input: Any, input_format: Optional[str], **kwargs
    ) -> List[Step]:
        pass

    @abstractmethod
    def _get_output_steps(self, output_format: Optional[str], **kwargs) -> List[Step]:
        pass

    def predict(
        self,
        input,
        input_format=None,
        output_format=None,
        **kwargs,
    ) -> Any:
        input_steps = self._get_input_steps(input, input_format, **kwargs)
        output_steps = self._get_output_steps(output_format, **kwargs)

        steps = [
            *input_steps,
            PredictionStep(self, batch_size=1, **kwargs),
            *output_steps,
        ]

        # build the pipeline from the list of transforms
        pipeline = None
        for t in steps:
            pipeline = t(pipeline)

        # the last pipeline step holds the result
        last_step = steps[-1]
        assert isinstance(last_step, WriteOutput)
        return last_step.get_result()


class PredictionStep(Step):
    def __init__(self, model: Model, batch_size: int, **kwargs):
        super().__init__()
        self.model = model
        self.batch_size = batch_size
        self.kwargs = kwargs

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        # We need to process the molecules in batches, because most ML models perform
        # better when predicting multiple molecules at once. Additionally, we want to
        # filter out molecules that could not be preprocessed.
        def _batch_and_filter(source, n):
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
        predictions = call_with_mappings(
            self.model._predict_mols,
            {**self.kwargs, "mols": mols},
        )

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
                record["problems"].append(UnknownProblem())

                # add the record to the mapping
                mol_id_to_record[mol_id].append(record)

        # If the result has multiple entries per mol_id, check that atom_id or
        # derivative_id is present in multi-entry results.
        if len(predictions) > len(batch):
            for _, records in mol_id_to_record.items():
                if len(records) > 1:
                    has_atom_id = all("atom_id" in record for record in records)
                    has_derivative_id = all(
                        "derivative_id" in record for record in records
                    )
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