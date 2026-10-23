#!/usr/bin/env python3
"""補完ファイルの各省略について、OCR 本文の前後の文脈を表示する（境目の確認用）。

  python3 nv_src/show.py NN [番号 ...]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gaps  # noqa: E402

n = int(sys.argv[1])
want = set(sys.argv[2:])
for i, g in enumerate(gaps.gaps_of(gaps.PAGES / f'nyayavarttika-{n}-taiyaku.html')):
    if want and str(i) not in want:
        continue
    print(f'=== {i}: @ {g["block"]} {g["gap"]}  pp.{g["pp"]}')
    print('  左:', g['left'][-50:])
    print('  右:', g['right'][:50])
    t = g.get('text')
    if t is None:
        print('  （見つからない）')
        continue
    k = gaps.CLEAN.find(t)
    print('  OCR:', '【' + gaps.CLEAN[max(0, k - 70):k] + '】' + re.sub(r'\s+', ' ', t) + '【' + gaps.CLEAN[k + len(t):k + len(t) + 70] + '】')
