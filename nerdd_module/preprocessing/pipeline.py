from typing import Iterable, List, Optional, Tuple

from rdkit.Chem import Mol
from stringcase import snakecase

from .step import Step

__all__ = ["Pipeline", "make_pipeline"]


class Pipeline:
    def __init__(self, steps: Iterable[Step], name: Optional[str] = None):
        assert all(isinstance(step, Step) for step in steps)
        self._steps = steps
        self._name = name

    def run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        errors = []

        if mol is None:
            errors.append("!1")

        for step in self._steps:
            if mol is None:
                break

            mol, additional_errors = step.run(mol)

            errors.extend(additional_errors)

        return mol, errors

    def __call__(self, mol: Mol) -> Tuple[Mol, List[str]]:
        return self.run(mol)

    @property
    def name(self) -> str:
        if self._name is None:
            if type(self) is Pipeline:
                # class is an instantiation of this class (no subclass)
                # --> getting the name of this class raises an error
                #     (usually no problem except if the pipeline should be registered)
                raise ValueError("Pipeline has no name")
            else:
                # class is deriving from Pipeline
                # return type of subclass deriving from this class
                return snakecase(type(self).__name__)
        return self._name


def make_pipeline(*steps: Step):
    return Pipeline(steps=steps)
