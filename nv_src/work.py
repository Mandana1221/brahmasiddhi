#!/usr/bin/env python3
"""ページ NN の各省略について、補う原文（S）と、和訳の前後の文脈を表示する（訳を書くため）。

  python3 nv_src/work.py NN [文脈の字数]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
w = int(sys.argv[2]) if len(sys.argv) > 2 else 120
t = (ROOT / 'nv_src' / 'orig' / f'nyayavarttika-{n}-taiyaku.html').read_text(encoding='utf-8')
tr = [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<div class="tr">(.*?)</div>', t, re.S)]
fill = (ROOT / 'nv_src' / 'fill' / f'{n:02d}.txt').read_text(encoding='utf-8')
cur = None
for ln in fill.split('\n'):
    if ln.startswith('@ '):
        b, g = map(int, ln[2:].split()[:2])
        cur = (b, g)
        print('\n' + ln)
    elif ln.startswith('S ') and cur:
        b, g = cur
        parts = re.split(r'……|…', tr[b])
        if g + 1 < len(parts):
            print('  訳前:', parts[g][-w:])
            print('  訳後:', parts[g + 1][:w])
        else:
            print('  （訳の省略の数が合わない）')
        print(ln)
