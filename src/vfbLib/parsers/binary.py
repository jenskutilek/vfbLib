from vfbLib.parsers.base import BaseParser
from vfbLib.typing import BinaryTableDict


class BinaryTableParser(BaseParser):
    def _parse(self) -> BinaryTableDict:
        tag = self.read_str(4)
        data = self.stream.read()
        return {"tag": tag, "data": data}
