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
    if s.startswith('#'):          # GRETIL の出典注記（# yogabhāṣye # など）は空行に
        out.append('')
        continue
    if s.startswith('nys_'):
        out.append(s)
        continue
    s = re.sub(r'#[^#\n]*#\s*', '', s)      # 行中の出典注記（# muṇḍaka 2/2/8 # など）を外す
    s = re.sub(r'\(\s*\d+\s*/\s*\d+\s*\)\s*', '', s)   # 『評釈』刊本の頁・行の参照（(181/4) など）を外す
    s = re.sub(r'\s*\(sū\.\s*\d+\)', '', s)   # (sū. 6) などの注記を外す
    s = re.sub(r'(?<=[^\s/])/(?=[^\s/])', 'ñ', s)   # GRETIL では ñ が / になっている箇所がある
    for piece in re.findall(r'.*?(?://|/|$)', s):
        piece = piece.strip()
        if piece:
            out.append(piece)
# 訂正表（corrections.txt）を当てる
bad = []
for cl in (ROOT / 'nvtt_src' / 'corrections.txt').read_text(encoding='utf-8').split('\n'):
    if not cl.strip() or cl.startswith('#'):
        continue
    no, old, new = cl.split('\t')
    i = int(no) - 1
    if old == '*':                 # 行ごと削除（GRETIL の重複行など）
        out[i] = ''
        continue
    if old == '+':                 # 空行に本文を補う（GRETIL の欠落を刊本 OCR から補う）
        if out[i].strip():
            bad.append(f'{no} + (空行ではない)')
            continue
        out[i] = new
        continue
    if old not in out[i]:
        # 連声で語頭・語末の a が前後の音と融合している場合は、その a を外して当てる
        o2, n2 = old, new
        if o2.startswith('a') and n2.startswith('a'):
            o2, n2 = o2[1:], n2[1:]
        if o2 not in out[i] and o2.endswith('a') and n2.endswith('a'):
            o2, n2 = o2[:-1], n2[:-1]
        if o2 not in out[i] and old.endswith('a') and new.endswith('a'):
            o2, n2 = old[:-1], new[:-1]
        if o2 not in out[i]:
            bad.append(f'{no} {old}')
            continue
        old, new = o2, n2
    out[i] = out[i].replace(old, new, 1)
if bad:
    sys.exit('訂正できない:\n' + '\n'.join(bad))
(ROOT / 'NVTT_text.txt').write_text('\n'.join(out).strip() + '\n', encoding='utf-8')
print(len(out), 'lines')
