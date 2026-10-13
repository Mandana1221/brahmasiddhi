#!/usr/bin/env python3
"""L/V 範囲に、刊本の脚注領域（脚注行の後〜次の頁標識まで）の行が混じっていないか調べる。"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
T = (ROOT / 'NVTP_text.txt').read_text(encoding='utf-8').split('\n')
FOOT = re.compile(r'^[०-९]{1,2}\s*\.|[A-Za-z]')
zone = [False] * (len(T) + 1)
inz = False
for i, l in enumerate(T, 1):
    s = l.strip()
    if s.startswith('[p. '):
        inz = False
    elif re.match(r'^[०-९]{1,2}\s*\.', s):
        inz = True
    zone[i] = inz
for p in sys.argv[1:]:
    for ln in Path(p).read_text(encoding='utf-8').split('\n'):
        m = re.match(r'^[LV]\s+(\d+)-(\d+)', ln)
        if not m: continue
        a, b = int(m.group(1)), int(m.group(2))
        for i in range(a, b + 1):
            s = T[i-1].strip()
            if zone[i] and s and not FOOT.search(s) and not s.startswith('[p.'):
                print(p, ln.strip(), i, s[:60])
