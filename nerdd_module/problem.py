from typing import Iterable, NamedTuple

__all__ = [
    "Problem",
    "UnknownPredictionProblem",
    "IncompletePredictionProblem",
    "InvalidSmiles",
    "UnknownProblem",
    "InvalidWeightProblem",
    "InvalidElementsProblem",
]


class Problem(NamedTuple):
    type: str
    message: str


# an unknown prediction problem indicates that the model raised an exception during
# prediction
def UnknownPredictionProblem() -> Problem:
    return Problem("unknown_prediction_error", "An unknown error occured during prediction.")


# an incomplete prediction problem indicates that the model successfully returns
# predictions, but part of the input molecules are missing in the results
def IncompletePredictionProblem() -> Problem:
    return Problem("incomplete_prediction_error", "The model couldn't process the molecule.")


def InvalidSmiles() -> Problem:
    return Problem(type="invalid_smiles", message="Invalid SMILES string")


def UnknownProblem() -> Problem:
    return Problem(type="unknown", message="Unknown error occurred")


def InvalidWeightProblem(weight: float, min_weight: float, max_weight: float) -> Problem:
    return Problem(
        type="invalid_weight",
        message=(f"Molecular weight {weight:.2f} out of range [{min_weight}, {max_weight}]"),
    )


def InvalidElementsProblem(invalid_elements: Iterable[str]) -> Problem:
    invalid_element_list = list(invalid_elements)
    if len(invalid_element_list) > 3:
        invalid_elements_str = ", ".join(invalid_element_list[:3]) + "..."
    else:
        invalid_elements_str = ", ".join(invalid_element_list)

    return Problem(
        "invalid_elements",
        f"Molecule contains invalid elements {invalid_elements_str}",
    )
