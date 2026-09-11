import logging
from typing import TYPE_CHECKING, Any

from vfbLib.compilers.base import BaseCompiler
from vfbLib.parsers.text import platform_encoding_to_python

if TYPE_CHECKING:
    from vfbLib.typing import NameRecordDict


logger = logging.getLogger(__name__)


class NameRecordsCompiler(BaseCompiler):
    def _compile(self, data: "list[NameRecordDict] | Any") -> None:
        self.write_value(len(data))  # number of records
        for nr in data:
            self.write_value(nr["name_id"])
            platform_id = nr["platform_id"]
            self.write_value(platform_id)
            encoding_id = nr["encoding_id"]
            self.write_value(encoding_id)
            self.write_value(nr["language_id"])
            python_encoding = platform_encoding_to_python.get(platform_id, {}).get(
                encoding_id, ""
            )
            if python_encoding == "":
                # We have not encountered those
                logger.warning(
                    "Could not determine string encoding for name record for platform "
                    f"{platform_id} and encoding {encoding_id}. Please file an issue on"
                    " the vfbLib GitHub."
                )
                python_encoding = "utf_16_be"  # FIXME: What happens?
            name = nr["string"]
            self.write_value(len(name))
            for char in name:
                b = char.encode(python_encoding)
                self.write_value(int.from_bytes(b))


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
