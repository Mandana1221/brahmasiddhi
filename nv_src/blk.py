#!/usr/bin/env python3
"""ページ NN の欄 b の原文と和訳を表示する。  python3 nv_src/blk.py NN b [b ...]"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
t = (ROOT / 'nv_src' / 'orig' / f'nyayavarttika-{n}-taiyaku.html').read_text(encoding='utf-8')
src = re.findall(r'<div class="src[^"]*"[^>]*>(.*?)</div>', t, re.S)
tr = re.findall(r'<div class="tr">(.*?)</div>', t, re.S)
for b in sys.argv[2:]:
    b = int(b)
    print(f'--- {b} 原文:', src[b])
    print(f'--- {b} 和訳:', tr[b])
