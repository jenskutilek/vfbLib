from unittest import TestCase

from vfbLib.parsers.text import NameRecordsParser, StringParser


class StringParserTest(TestCase):
    def test_links_1(self):
        data = "57 74 30 20 57 64 31 20"
        expected = "Wt0 Wd1 "  # Trailing space does not get stripped
        result = StringParser().parse_hex(data)
        assert result == expected


class NameRecordsParserTest(TestCase):
    def test_windows_cyrillic(self) -> None:
        data = (
            "8c"  # one record follows
            "8c 8e 8c faad"  # 1 3 1 1049
            "99"  # 14
            " faae fad2 fad0 facc face ab faad fac9 fad1 fad5 ab fab3 fad4 fad2"
            # 1050 1086 1084 1080 1082 32 1049 1077 1085 1089 32 1055 1088 1086
        )
        result = NameRecordsParser().parse_hex(data)
        assert result == [
            {
                "name_id": 1,
                "platform_id": 3,
                "encoding_id": 1,
                "language_id": 1049,
                "string": "Комик Йенс Про",
            }
        ]

    def test_mac_cyrillic(self) -> None:
        data = (
            "8c"  # one record follows
            "8c 8c 92 ab"  # 1 1 7 32
            "99"  # 14
            "f71e f782 f780 f77c f77e ab f71d f779 f781 f785 ab f723 f784 f782"
            # 138  238  236  232  234 32  137  229  237  142 32  143  240  238
        )
        result = NameRecordsParser().parse_hex(data)
        assert result == [
            {
                "name_id": 1,
                "platform_id": 1,
                "encoding_id": 7,
                "language_id": 32,
                "string": "Комик Йенс Про",
            }
        ]
