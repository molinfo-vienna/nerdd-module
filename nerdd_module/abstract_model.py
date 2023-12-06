from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import pandas as pd
from rdkit.Chem import Mol, MolToSmiles

from .config import AutoConfiguration, Configuration
from .io import MoleculeEntry, guess_and_read
from .preprocessing import Pipeline, Step, registry

__all__ = ["AbstractModel"]


class CustomPreprocessingStep(Step):
    def __init__(self, fn: Callable[[Mol], Tuple[Mol, List[str]]]):
        super().__init__()
        self.fn = fn

    def _run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        return self.fn(mol)


class AbstractModel(ABC):
    def __init__(
        self,
        preprocessing_pipeline: Union[str, Pipeline, Iterable[Step], None],
        num_processes: int = 1,
    ):
        #
        # preprocessing pipeline
        #
        if preprocessing_pipeline is None or preprocessing_pipeline == "custom":
            self.preprocessing_pipeline = Pipeline(
                steps=[CustomPreprocessingStep(self._preprocess_single_mol)]
            )
        elif isinstance(preprocessing_pipeline, Pipeline):
            self.preprocessing_pipeline = preprocessing_pipeline
        elif isinstance(preprocessing_pipeline, str):
            if preprocessing_pipeline in registry:
                self.preprocessing_pipeline = registry[preprocessing_pipeline]
            else:
                raise ValueError(
                    "Invalid preprocessing pipeline. Choose one of the following: "
                    ", ".join(list(registry.keys()) + ["custom"])
                )
        elif isinstance(preprocessing_pipeline, Iterable) and all(
            isinstance(step, Step) for step in preprocessing_pipeline
        ):
            # mypy assumes that preprocessing_pipeline might be a string (although we
            # checked this case above) and complains about that when constructing the
            # pipeline
            # --> explicitly assert that preprocessing_pipeline is not a string
            assert not isinstance(preprocessing_pipeline, str)
            self.preprocessing_pipeline = Pipeline(steps=preprocessing_pipeline)
        else:
            raise ValueError(
                f"Invalid preprocessing pipeline {preprocessing_pipeline}."
            )

        #
        # reading molecules
        #

        # add methods for all supported formats
        # TODO

        #
        # other parameters
        #
        self.num_processes = num_processes

    def _preprocess_single_mol(self, mol: Mol) -> Tuple[Mol, List[str]]:
        # if this method is called, the preprocessing_pipeline was set to "custom"
        # and this method has to be overwritten
        raise NotImplementedError()

    @abstractmethod
    def _predict_mols(self, mols: List[Mol], **kwargs) -> pd.DataFrame:
        pass

    def _predict_entries(
        self,
        inputs: Iterable[MoleculeEntry],
        **kwargs,
    ) -> pd.DataFrame:
        """
        'preprocessed_mol', 'mol_id', 'input_mol', 'input_type', 'name',
        'input_smiles', 'preprocessed_smiles', 'atom_id', 'mass', 'errors',
        'input'
        """
        #
        # LOAD MOLECULES
        #
        df_load = pd.DataFrame(
            inputs,
            columns=["input", "input_type", "source", "mol", "load_errors"],
        )
        df_load["mol_id"] = range(len(df_load))

        #
        # PREPROCESS ALL MOLECULES
        #
        df_preprocess = pd.DataFrame(
            [self.preprocessing_pipeline.run(mol) for mol in df_load.mol],
            columns=["preprocessed_mol", "preprocessing_errors"],
        )

        # necessary for models that create multiple (or zero) entries per molecule
        df_preprocess["mol_id"] = range(len(df_preprocess))

        # add raw molecules to dataframe
        df_preprocess["input_mol"] = df_load.mol

        # add name to dataframe
        df_preprocess["name"] = [
            (mol.GetProp("_Name") if mol is not None and mol.HasProp("_Name") else "")
            for mol in df_preprocess.input_mol
        ]

        # add smiles columns for web UI
        def _to_smiles(mol):
            try:
                return MolToSmiles(mol)
            except:
                return None

        #
        # PREPARE PREDICTION OF MOLECULES
        #

        # each molecule gets its unique id (0, 1, ..., n) as its name
        for id, mol in zip(df_preprocess.mol_id, df_preprocess.preprocessed_mol):
            if mol is not None:
                mol.SetProp("_Name", str(id))

        # do the prediction on molecules that are not None
        df_valid_subset = df_preprocess[df_preprocess.preprocessed_mol.notnull()]

        #
        # PREDICTION
        #
        df_predictions = self._predict_mols(
            df_valid_subset.preprocessed_mol.tolist(), **kwargs
        )

        #
        # POST PROCESSING AND ERROR HANDLING
        #

        # make sure that reserved column names do not appear in the output dataframe
        reserved_column_names = ["input", "name", "input_mol"]
        assert (
            set(df_predictions.columns).intersection(reserved_column_names) == set()
        ), f"Do not use reserved column names {', '.join(reserved_column_names)}!"

        # during prediction, molecules might have been removed / reordered
        # there are three ways to connect the predictions to the original molecules:
        # 1. df_prediction contains a column "mol_id" that contains the molecule ids
        # 2. df_prediction contains a column "mol" that contains the molecules, which
        #    have the id as their name so that we can match them to the original
        # 3. df_prediction has the same length as the number of valid molecules
        #    (and we assume that the order of the molecules is the same)
        if "mol_id" in df_predictions.columns:
            # check that mol_id contains only valid ids
            assert set(df_predictions.mol_id).issubset(
                set(df_valid_subset.mol_id)
            ), "The mol_id column must only contain valid ids!"
            # use mol_id as index
            df_predictions.set_index("mol_id", drop=True, inplace=True)
        elif "mol" in df_predictions.columns:
            # check that molecule names contain only valid ids
            names = df_predictions.mol.apply(lambda mol: int(mol.GetProp("_Name")))
            assert set(names).issubset(
                set(df_preprocess.mol_id)
            ), "The molecule names must only contain valid ids!"

            # use mol_id as index
            df_predictions.set_index(
                names,
                inplace=True,
            )
            df_predictions.drop(columns="mol", inplace=True)
        else:
            assert len(df_predictions) == len(df_valid_subset), (
                "The number of predicted molecules must be equal to the number of "
                "valid input molecules."
            )
            # use index from input series (type cast if series was empty)
            df_predictions.set_index(
                df_valid_subset.index.astype("int64"), inplace=True
            )

        # add column that indicates whether a molecule was missing
        missing_mol_ids = set(df_preprocess.mol_id).difference(df_predictions.index)
        df_preprocess["missing"] = df_preprocess.mol_id.isin(missing_mol_ids)

        # merge the preprocessed molecules with the predictions
        df_result = df_preprocess.merge(
            df_predictions, left_on="mol_id", right_index=True, how="left"
        )

        # if the result has multiple entries per mol_id, check that atom_id or
        # derivative_id is present
        if len(df_result) > df_result.mol_id.nunique():
            assert (
                "atom_id" in df_result.columns or "derivative_id" in df_result.columns
            ), (
                "The result contains multiple entries per molecule, but does not "
                "contain atom_id or derivative_id."
            )

        # merge errors from preprocessing and prediction
        if "prediction_errors" in df_result.columns:
            df_result["errors"] = (
                df_result.preprocessing_errors + df_result.prediction_errors
            )
            df_result.drop(columns=["prediction_errors"], inplace=True)
        else:
            df_result["errors"] = df_result.preprocessing_errors
        df_result["errors"] = df_result.errors + df_result.missing.map(
            lambda x: ["!1"] if x else []
        )
        df_result.drop(columns=["missing", "preprocessing_errors"], inplace=True)

        # convert errors to string
        if "errors" in df_result.columns:
            df_result["errors"] = df_result.errors.map(lambda x: ", ".join(set(x)))
        else:
            df_result["errors"] = ""

        # delete mol column (not needed anymore)
        df_load.drop(columns=["mol"], inplace=True)

        # merge load and prediction
        df_result = df_result.merge(df_load, on="mol_id", how="left")

        # merge errors from loading and prediction
        df_result["errors"] = [
            ", ".join(set(load_errors + [prediction_errors]))
            for load_errors, prediction_errors in zip(
                df_result.load_errors, df_result.errors
            )
        ]

        df_result.drop(columns=["load_errors"], inplace=True)

        # reorder columns
        mandatory_columns = [
            "mol_id",
            "input",
            "input_type",
            "source",
            "name",
            "input_mol",
            "preprocessed_mol",
            "errors",
        ]
        remaining_columns = [c for c in df_result.columns if c not in mandatory_columns]
        df_result = df_result[mandatory_columns + remaining_columns]

        return df_result

    def predict(
        self,
        inputs: Union[Iterable[str], Iterable[Mol], str, Mol],
        input_type=None,
        **kwargs,
    ):
        entries = guess_and_read(inputs)

        return self._predict_entries(entries, **kwargs)

    def get_config(self) -> Configuration:
        return AutoConfiguration(self)
