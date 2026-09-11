import logging
from re import search

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import FeaturesDict, NameRecordDict

logger = logging.getLogger(__name__)


platform_encoding_to_python: dict[int, dict[int, str]] = {
    0: {  # Unicode
        0: "",  # Unicode 1.0 semantics—deprecated
        1: "",  # Unicode 1.1 semantics—deprecated
        2: "",  # ISO/IEC 10646 semantics—deprecated
        3: "utf_16_be",  # Unicode 2.0 and onwards semantics, Unicode BMP only
        4: "utf_16_be",  # Unicode 2.0 and onwards semantics, Unicode full repertoire
    },
    1: {  # Macintosh
        0: "macroman",  # Roman
        1: "",  # Japanese
        2: "",  # Chinese (Traditional)
        3: "",  # Korean
        4: "",  # Arabic
        5: "",  # Hebrew
        6: "mac_greek",  # Greek
        7: "mac_cyrillic",  # Russian
        8: "",  # RSymbol
        9: "",  # Devanagari
        10: "",  # Gurmukhi
        11: "",  # Gujarati
        12: "",  # Odia
        13: "",  # Bangla
        14: "",  # Tamil
        15: "",  # Telugu
        16: "",  # Kannada
        17: "",  # Malayalam
        18: "",  # Sinhalese
        19: "",  # Burmese
        20: "",  # Khmer
        21: "",  # Thai
        22: "",  # Laotian
        23: "",  # Georgian
        24: "",  # Armenian
        25: "",  # Chinese (Simplified)
        26: "",  # Tibetan
        27: "",  # Mongolian
        28: "",  # Geez
        29: "",  # Slavic
        30: "",  # Vietnamese
        31: "",  # Sindhi
        32: "",  # Uninterpreted
    },
    # https://learn.microsoft.com/en-us/typography/opentype/spec/name#windows-encoding-ids
    3: {  # Windows,
        0: "utf_16_be",  # Symbol
        1: "utf_16_be",  # Unicode BMP
        2: "utf_16_be",  # ShiftJIS
        3: "cp936",  # PRC, CP 936
        4: "cp950",  # Big5, CP 950
        5: "cp949",  # Wansung, CP 949
        6: "utf_16_be",  # Johab
        7: "utf_16_be",  # Reserved
        8: "utf_16_be",  # Reserved
        9: "utf_16_be",  # Reserved
        10: "utf_16_be",  # Unicode full repertoire
    },
}


class NameRecordsParser(BaseParser):
    def _parse(self) -> list[NameRecordDict]:
        num = self.read_value()
        result = []
        for _ in range(num):
            nameID = self.read_value()
            platID = self.read_value()
            encID = self.read_value()
            langID = self.read_value()
            name_length = self.read_value()
            name_codes = [self.read_value() for _ in range(name_length)]
            name = ""
            python_encoding = platform_encoding_to_python.get(platID, {}).get(encID, "")
            if python_encoding == "":
                # We have not encountered those
                logger.warning(
                    "Could not determine string encoding for name record for platform "
                    f"{platID} and encoding {encID}. Please file an issue on the vfbLib"
                    " GitHub."
                )
                python_encoding = "utf_16_be"  # FIXME: What happens?
            for c in name_codes:
                num_bytes = 2 if python_encoding == "utf_16_be" or platID == 3 else 1
                s = c.to_bytes(num_bytes)
                char = s.decode(python_encoding, errors="replace")
                name += char

            result.append(
                NameRecordDict(
                    name_id=nameID,
                    platform_id=platID,
                    encoding_id=encID,
                    language_id=langID,
                    string=name,
                )
            )

        return result


class OpenTypeStringParser(BaseParser):
    """
    A parser that reads data as a strings and returns it as a list.
    """

    @staticmethod
    def build_fea_dict(data: list[str]) -> FeaturesDict:
        """
        Parse the OpenType feature code into a structure that is more manageable. This
        is not used in vfbLib, but may be used in code that wants to read OpenType
        features from a VFB.

        Args:
            data (list[str]): The OpenType feature code (AFDKO syntax) as a list of
                lines.

        Returns:
            dict[str, list[dict]]: The feature code split into prefix and actual
                features.
        """
        fea = FeaturesDict(prefix=[], features=[])
        prefix: list[str] = []
        feature: list[str] = []
        tag = ""
        in_prefix = True
        for line in data:
            if "#" in line:
                code, _ = line.split("#", 1)
            else:
                code = line

            if s := search(r"\s*feature\s*([a-z0-9]{4})\s*\{", code):
                # New feature

                if in_prefix:
                    # Flush the prefix code
                    fea["prefix"] = prefix
                    in_prefix = False
                else:
                    # Flush the previous feature
                    fea["features"].append({"tag": tag, "code": feature})

                tag = s.groups()[0]
                feature = [line]
            elif in_prefix:
                prefix.append(line)
            else:
                feature.append(line)

        # Flush the last feature
        fea["features"].append({"tag": tag, "code": feature})

        return fea

    def _parse(self) -> list[str]:
        s = self.read_str_all()
        # Filter more than 2 consecutive empty lines
        lines = []
        c = 0
        for line in s.splitlines():
            if line.strip():
                c = 0
                lines.append(line)
            else:
                if c < 2:
                    lines.append(line)
                c += 1

        if len(lines) > 1:
            # Remove empty lines at the end, except one
            while not lines[-1]:
                lines.pop()
        lines.append("")
        return lines


class StringParser(BaseParser):
    """
    A parser that reads data as strings.
    """

    def _parse(self):
        return self.read_str_all().strip("\00")
