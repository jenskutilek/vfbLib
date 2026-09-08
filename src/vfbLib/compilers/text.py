from typing import TYPE_CHECKING, Any

from vfbLib.compilers.base import BaseCompiler

if TYPE_CHECKING:
    from vfbLib.typing import NameRecordDict


class NameRecordsCompiler(BaseCompiler):
    def _compile(self, data: "list[NameRecordDict] | Any") -> None:
        self.write_value(len(data))  # number of records
        for nr in data:
            self.write_value(nr["name_id"])
            self.write_value(nr["platform_id"])
            self.write_value(nr["encoding_id"])
            self.write_value(nr["language_id"])
            name = nr["string"]
            self.write_value(len(name))
            for char in name:
                if nr["platform_id"] == 1 and nr["encoding_id"] == 0:
                    try:
                        char = char.encode("macroman")
                    except ValueError:
                        char = "?"
                o = ord(char)
                self.write_value(o)


class OpenTypeStringCompiler(BaseCompiler):
    """
    A compiler that compiles string data that represents OpenType feature code.
    """

    def _compile(self, data: list[str] | Any) -> None:
        self.write_str("\n".join(data))


class StringCompiler(BaseCompiler):
    """
    A compiler that compiles string data.
    """

    def _compile(self, data: str | Any) -> None:
        self.write_str(data)


class VendorIdCompiler(BaseCompiler):
    """
    A compiler that compiles string data, padded to 4 bytes.
    """

    def _compile(self, data: str | Any) -> None:
        self.write_str(data, pad=4)
