from itertools import chain, islice, repeat
from typing import Any, Iterable, Iterator, Optional

from .explorer import Explorer
from .reader import ExploreCallable, MoleculeEntry, Problem, Reader

__all__ = ["DepthFirstExplorer"]


class InvalidInputReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        yield MoleculeEntry(
            raw_input=input,
            input_type="unknown",
            source=("input",),
            mol=None,
            errors=[Problem("invalid_input", "Invalid input")],
        )

    def __repr__(self) -> str:
        return "InvalidInputReader()"


class DepthFirstExplorer(Explorer):
    def __init__(
        self,
        readers: Optional[Iterable[Reader]] = None,
        num_test_entries: int = 10,
        threshold: float = 0.5,
        maximum_depth: int = 50,
        **kwargs: Any,
    ):
        super().__init__()

        if readers is None:
            self._readers = list(Reader.get_readers(**kwargs))
        else:
            self._readers = list(readers)

        self._num_test_entries = num_test_entries
        self._threshold = threshold
        self._state_stack = [self._empty_state()]
        self._maximum_depth = maximum_depth

    def _empty_state(self) -> dict:
        return dict(first_guess=[])

    def explore(self, input: Any) -> Iterator[MoleculeEntry]:
        # create a new child node and set it as the current node
        state = self._empty_state()
        parent = self._state_stack[-1]
        self._state_stack.append(state)

        depth = len(self._state_stack)
        if depth > self._maximum_depth:
            raise ValueError(f"Maximum depth of {self._maximum_depth} reached")

        readers_iter = chain(
            zip(parent["first_guess"], repeat("guess")),
            zip(self._readers, repeat("builtin")),
        )

        # try all readers and take a sample of the first num_test_entries
        # the reader with most valid molecule entries will be used
        best_reader: Optional[Reader] = None
        best_mode = None
        best_score = 0
        best_ratio = 0.0
        best_num_invalid_results = 0
        generator = None
        sample = []
        for reader, mode in readers_iter:
            try:
                # read at most num_test_entries entries
                generator = self._read(reader, input)
                sample = list(islice(generator, self._num_test_entries))
                valid_entries = [entry for entry in sample if entry.mol is not None]

                score = len(valid_entries)
                ratio = len(valid_entries) / len(sample)
                num_invalid_results = len(sample) - len(valid_entries)

                if (
                    score > best_score
                    # if the score is the same, prefer the reader with higher ratio
                    # of valid entries
                    or (score == best_score and ratio > best_ratio)
                    # if the ratio is the same, prefer the reader with less invalid
                    # results
                    or (
                        score == best_score
                        and ratio == best_ratio
                        and num_invalid_results < best_num_invalid_results
                    )
                ):
                    best_reader = reader
                    best_mode = mode
                    best_score = score
                    best_ratio = ratio
                    best_num_invalid_results = num_invalid_results

                    if score == self._num_test_entries:
                        break
            except Exception:
                pass

            # clean up tree
            while len(self._state_stack) > depth:
                self._state_stack.pop()
            generator = None

        if generator is None:
            if best_reader is None:
                generator = self._read(InvalidInputReader(), input)
                sample = []
            else:
                generator = self._read(best_reader, input)
                sample = list(islice(generator, self._num_test_entries))
        else:
            if best_mode is not None and best_mode != "guess":
                parent["first_guess"].append(best_reader)

        yield from sample
        yield from generator

        self._state_stack.pop()
