from typing import Optional, Type

from rdkit.rdBase import BlockLogs as OriginalBlockLogs
from typing_extensions import Protocol

__all__ = ["BlockLogs"]


class BlockLogsProtocol(Protocol):
    def __init__(self) -> None: ...
    def __enter__(self) -> "BlockLogsProtocol": ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Type[BaseException]],
    ) -> None: ...


BlockLogs: Type[BlockLogsProtocol]

if hasattr(OriginalBlockLogs, "__enter__"):
    BlockLogs = OriginalBlockLogs
else:
    # We would like to use
    #   with BlockLogs(): ...
    # but this does not work with old versions of RDKit. Therefore, we create an instance of
    # BlockLogs that will suppress log messages as long as it exists. When it is deleted (in the
    # "__exit__" block), logs are enabled again.
    class CustomBlockLogs:
        block_logs: Optional[OriginalBlockLogs] = None

        def __enter__(self) -> BlockLogsProtocol:
            self.block_logs = OriginalBlockLogs()
            return self

        def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[Type[BaseException]],
        ) -> None:
            del self.block_logs

    BlockLogs = CustomBlockLogs
