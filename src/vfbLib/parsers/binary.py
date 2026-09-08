from vfbLib.parsers.base import BaseParser
from vfbLib.typing import BinaryTableDict, BinaryTrueTypeTableDict


class BinaryTableParser(BaseParser):
    def _parse(self) -> BinaryTableDict:
        tag = self.read_str(4)
        data = self.stream.read()
        return {"tag": tag, "data": data}


class BinaryTrueTypeTableParser(BaseParser):
    def _parse(self) -> BinaryTrueTypeTableDict:
        data = self.stream.read()
        return {"data": data}
