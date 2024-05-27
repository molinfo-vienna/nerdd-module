from typing import NamedTuple

__all__ = ["Problem", "InvalidSmiles", "UnknownProblem", "InvalidWeightProblem"]


class Problem(NamedTuple):
    type: str
    message: str


InvalidSmiles = lambda: Problem(type="invalid_smiles", message="Invalid SMILES string")

UnknownProblem = lambda: Problem(type="unknown", message="Unknown error occurred")

InvalidWeightProblem = lambda weight, min_weight, max_weight: Problem(
    type="invalid_weight",
    message=f"Molecular weight {weight:.2f} out of range [{min_weight}, {max_weight}]",
)
