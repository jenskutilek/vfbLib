from __future__ import annotations

import pytest

from fontTools.designspaceLib import DesignSpaceDocument
from pathlib import Path
from unittest import TestCase
from vfbLib.ufo import VfbToUfoBuilder
from vfbLib.vfb.vfb import Vfb


def data_path():
    return Path(__file__).parent / "Data"


def vfb_path(name: str) -> Path:
    return data_path() / name


class GlyphCompilerTest(TestCase):
    def test_vfb_to_ufo_mm(self):
        vfb = Vfb(vfb_path("masters.vfb"))
        vfb.decompile()
        builder = VfbToUfoBuilder(vfb)
        ufos, designspace = builder.get_ufos_designspace(data_path())
        assert len(ufos) == 4
        assert isinstance(designspace, DesignSpaceDocument)

        # Master 0
        ufo = ufos[0]
        assert len(ufo) == 2  # 1 glyph only
        glyph = ufo["a"]
        assert len(glyph) == 1
        assert glyph.width == 353
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (176, 181)

        # Master 1
        ufo = ufos[1]
        glyph = ufo["a"]
        assert glyph.width == 457
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (228, 161)

        # Master 2
        ufo = ufos[2]
        glyph = ufo["a"]
        assert glyph.width == 437
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (218, 181)

        # Master 3
        ufo = ufos[3]
        glyph = ufo["a"]
        assert glyph.width == 565
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (281, 151)

    def test_vfb_to_ufo_mm_reader_deepcopy(self):
        # Check that objects have been copied and are not shared anymore between UFOs
        vfb = Vfb(vfb_path("masters.vfb"))
        vfb.decompile()
        builder = VfbToUfoBuilder(vfb)
        ufos = builder.get_ufo_masters(silent=True)
        assert len(ufos) == 4

        ufo0, ufo1, _, _ = ufos

        # Features

        fea0 = (
            "@letters = [a t];\n\n\nlanguagesystem DFLT dflt;\nfeature kern {\n"
            "  pos a t 100 ;\n} kern;"
        )

        assert ufo0.features.text == fea0
        assert ufo1.features.text == fea0
        ufo0.features.text = ufo0.features.text.replace("@letters", "@lower")
        assert ufo0.features.text.startswith("@lower = [a t];")
        assert ufo1.features.text.startswith("@letters = [a t];")

        # Glyphs

        glyph0 = ufo0["a"]
        assert glyph0.width == 353
        glyph0.width = 354
        point = glyph0.contours[0].points[3]
        assert (point.x, point.y) == (176, 181)
        point.x = 200
        glyph0.lib["foo"] = "bar"
        assert glyph0.unicode == 0x61
        glyph0.unicodes.append(0x41)

        # Master 1
        glyph1 = ufo1["a"]
        assert glyph1.width == 457
        point = glyph1.contours[0].points[3]
        assert (point.x, point.y) == (228, 161)
        assert "foo" not in glyph1.lib
        assert glyph1.unicodes == [0x61]

        # Groups

        assert ufo0.groups == {
            "_empty": [],
            ".mtrx5": ["a"],
            "letters": ["a", "t"],
            "public.kern1.a": ["a"],
            "public.kern1.t": ["t"],
            "public.kern2.a": ["a"],
            "public.kern2.t": ["t"],
        }
        assert ufo0.groups == ufo1.groups
        del ufo1.groups[".mtrx5"]
        assert ".mtrx5" in ufo0.groups
        ufo0.groups["_empty"].append("a")
        assert ufo1.groups["_empty"] == []

        # Kerning

        ufo0.kerning[("public.kern1.a", "public.kern2.a")] = -10
        assert ("public.kern1.a", "public.kern2.a") not in ufo1.kerning
        assert ufo0.kerning[("public.kern1.a", "public.kern2.t")] == -73
        ufo0.kerning[("public.kern1.a", "public.kern2.t")] = -72
        assert ufo0.kerning[("public.kern1.a", "public.kern2.t")] == -72
        assert ufo1.kerning[("public.kern1.a", "public.kern2.t")] == -166

        # Lib

        assert "com.lucasfonts.vfblib" in ufo0.lib["com.fontlab.v5.userData"]
        del ufo0.lib["com.fontlab.v5.userData"]
        assert "com.lucasfonts.vfblib" in ufo1.lib["com.fontlab.v5.userData"]
        ufo0.lib["foo"] = "bar"
        assert "foo" not in ufo1.lib