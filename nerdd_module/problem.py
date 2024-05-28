from typing import NamedTuple

__all__ = ["Problem", "InvalidSmiles", "UnknownProblem"]


class Problem(NamedTuple):
    type: str
    message: str


InvalidSmiles = lambda: Problem(type="invalid_smiles", message="Invalid SMILES string")

UnknownProblem = lambda: Problem(type="unknown", message="Unknown error occurred")
