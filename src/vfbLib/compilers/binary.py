from vfbLib.compilers.base import BaseCompiler
from vfbLib.typing import BinaryTableDict, BinaryTrueTypeTableDict


class BinaryTableCompiler(BaseCompiler):
    """
    A compiler that compiles binary table data.
    """

    def _compile(self, data: BinaryTableDict) -> None:
        self.write_str(data["tag"])  # FIXME: Add padding here?
        self.stream.write(data["data"])


class BinaryTrueTypeTableCompiler(BaseCompiler):
    """
    A compiler that compiles binary TrueType table data (cvt, prep, fpgm).
    """

    def _compile(self, data: BinaryTrueTypeTableDict) -> None:
        self.stream.write(data["data"])
