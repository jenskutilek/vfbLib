from vfbLib.compilers.base import BaseCompiler
from vfbLib.typing import BinaryTableDict


class BinaryTableCompiler(BaseCompiler):
    """
    A compiler that compiles binary table data.
    """

    def _compile(self, data: BinaryTableDict) -> None:
        self.write_str(data["tag"])  # FIXME: Add padding here?
        self.stream.write(data["data"])
