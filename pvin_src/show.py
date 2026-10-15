#!/usr/bin/env python3
"""作業用：本文の行を文番号つきで表示する。 python3 pvin_src/show.py 120 125"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

a = int(sys.argv[1])
b = int(sys.argv[2]) if len(sys.argv) > 2 else a
for n in range(a, b + 1):
    ss = build.sentences(n)
    if len(ss) <= 1:
        print(f'{n}: {build.TEXT[n - 1].strip()}')
    else:
        for i, s in enumerate(ss, 1):
            print(f'{n}:{i}  {s}')
