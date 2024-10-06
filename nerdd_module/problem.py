from typing import NamedTuple

__all__ = ["Problem", "InvalidSmiles", "UnknownProblem"]


class Problem(NamedTuple):
    type: str
    message: str


def InvalidSmiles() -> Problem:
    return Problem(type="invalid_smiles", message="Invalid SMILES string")


def UnknownProblem() -> Problem:
    return Problem(type="unknown", message="Unknown error occurred")
