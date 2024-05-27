from itertools import chain, islice, repeat
from typing import Generator, Iterable, Optional

from .explorer import Explorer
from .reader import MoleculeEntry, Problem, Reader
from .reader_registry import ReaderRegistry

__all__ = ["DepthFirstExplorer"]


class InvalidInputReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input, explore) -> Generator[MoleculeEntry, None, None]:
        yield MoleculeEntry(
            raw_input=input,
            input_type="unknown",
            source=tuple(["input"]),
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
    ):
        super().__init__()

        if readers is None:
            self.reader_registry = ReaderRegistry()
        else:
            self.reader_registry = readers

        self.num_test_entries = num_test_entries
        self.threshold = threshold
        self.state_stack = [self.empty_state()]
        self.maximum_depth = maximum_depth

    def empty_state(self):
        return dict(first_guess=[])

    def explore(self, input) -> Generator[MoleculeEntry, None, None]:
        # create a new child node and set it as the current node
        state = self.empty_state()
        parent = self.state_stack[-1]
        self.state_stack.append(state)

        depth = len(self.state_stack)
        if depth > self.maximum_depth:
            raise ValueError(f"Maximum depth of {self.maximum_depth} reached")

        readers_iter = chain(
            zip(parent["first_guess"], repeat("guess")),
            zip(self.reader_registry, repeat("builtin")),
        )

        # try all readers and take a sample of the first num_test_entries
        # the reader with most valid molecule entries will be used
        best_reader: Optional[Reader] = None
        best_mode = None
        best_score = 0
        best_ratio = 0.0
        generator = None
        sample = []
        for reader, mode in readers_iter:
            try:
                # read at most num_test_entries entries
                generator = reader.read(input, self.explore)
                sample = list(islice(generator, self.num_test_entries))
                valid_entries = [entry for entry in sample if entry.mol is not None]

                score = len(valid_entries)
                ratio = len(valid_entries) / len(sample)

                if score > best_score or (score == best_score and ratio > best_ratio):
                    best_reader = reader
                    best_mode = mode
                    best_score = score
                    best_ratio = ratio

                    if score == self.num_test_entries:
                        break
            except Exception:
                pass

            # clean up tree
            while len(self.state_stack) > depth:
                self.state_stack.pop()
            generator = None

        if generator is None:
            if best_reader is None:
                generator = InvalidInputReader().read(input, self.explore)
            else:
                generator = best_reader.read(input, self.explore)
                sample = list(islice(generator, self.num_test_entries))
        else:
            if best_mode is not None and best_mode != "guess":
                parent["first_guess"].append(best_reader)

        yield from sample
        yield from generator
