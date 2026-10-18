#!/usr/bin/env python3
"""GRETIL の Nyāyavārttikatātparyaṭīkā（IAST）から NVTT_text.txt を作る。

ヘッダーを落とし、本文を daṇḍa（/ と //）ごとに 1 行に分ける。
空行（段落の区切り）とスートラ行（nys_x,y.z:）はそのまま残す。
使い方: python3 nvtt_src/prep.py GRETIL.txt
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]).read_text(encoding='utf-8').split('\n')
body = src[src.index('# Text') + 1:]
out = []
for ln in body:
    s = ln.strip()
    if not s:
        if out and out[-1] != '':
            out.append('')
        continue
    if s.startswith('nys_') or s.startswith('#'):
        out.append(s)
        continue
    s = re.sub(r'(?<=[^\s/])/(?=[^\s/])', 'ñ', s)   # GRETIL では ñ が / になっている箇所がある
    for piece in re.findall(r'.*?(?://|/|$)', s):
        piece = piece.strip()
        if piece:
            out.append(piece)
(ROOT / 'NVTT_text.txt').write_text('\n'.join(out).strip() + '\n', encoding='utf-8')
print(len(out), 'lines')
