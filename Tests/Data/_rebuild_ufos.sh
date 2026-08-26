#!/usr/bin/env sh

find . -name "*.vfb" | xargs -n 1 vfb3ufo -fo
find . -name "*.vfb" | xargs -n 1 vfb2json
