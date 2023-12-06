from functools import lru_cache

from .inchi_file_reader import InchiFileReader
from .inchi_reader import InchiReader
from .mol_block_reader import MolBlockReader
from .rdkit_mol_reader import RdkitMolReader
from .reader import Reader
from .sdf_file_reader import SdfFileReader
from .smiles_file_reader import SmilesFileReader
from .smiles_reader import SmilesReader

__all__ = ["ReaderRegistry"]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class ReaderRegistry:
    def __init__(self):
        self._readers = []

    def register(self, reader: Reader):
        self._readers.append(reader)

    @property
    def supported_input_types(self) -> frozenset:
        return frozenset([reader.input_type for reader in self._readers])

    @property
    def readers(self):
        return frozenset(self._readers)

    def __iter__(self):
        return iter(self._readers)


registry = ReaderRegistry()
registry.register(SmilesReader())
registry.register(InchiReader())
registry.register(SdfFileReader(max_num_lines_mol_block=10_000))
registry.register(SmilesFileReader())
registry.register(InchiFileReader())
registry.register(MolBlockReader())
registry.register(RdkitMolReader())
