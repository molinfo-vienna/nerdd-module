from typing import NamedTuple, Callable

__all__ = ["Problem", "InvalidSmiles", "UnknownProblem"]


class Problem(NamedTuple):
    type: str
    message: str


InvalidSmiles: Callable[..., Problem] = lambda: Problem(
    type="invalid_smiles", message="Invalid SMILES string"
)

UnknownProblem: Callable[..., Problem] = lambda: Problem(
    type="unknown", message="Unknown error occurred"
)
