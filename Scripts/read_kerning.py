#!/usr/bin/env python3

from sys import argv

from vfbLib.enum import F
from vfbLib.vfb.vfb import Vfb


def print_kerning_classes(vfb_path):
    vfb = Vfb(vfb_path)
    vfb.decompile()
    for entry in vfb.entries:
        if entry.id == F.KerningClassFlags:
            print("Kerning Class Flags:")
            print(entry.data)
            print()
            kerning_class_flags = entry.data
        elif entry.id == F.GlyphClass:
            if not entry.data.startswith("_"):
                continue

            print(entry.data)
            class_name, contents = entry.data.split(":")
            sides = kerning_class_flags[class_name][0]
            if sides & 1024:
                print("  Is 1st in pair")
            if sides & 2048:
                print("  Is 2nd in pair")
            print()


if __name__ == "__main__":
    print_kerning_classes(argv[1])
