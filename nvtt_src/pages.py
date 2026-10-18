#!/usr/bin/env python3
"""Thakur 刊本（1996）の OCR から各頁の書き出しを取り出し、NVTT_text.txt に [p. N] を入れる。

使い方: python3 nvtt_src/pages.py 全体OCR.txt 補遺OCR(pp.100-147).txt
- 全体 OCR は PDF の 1 頁＝刊本 1 頁。刊本頁 = PDF 頁 - 13（p.251 まで）、- 15（p.252 以降）。
  PDF 114–129 は pp.149–164 の重複、PDF 265–266 は pp.250–251 の重複なので使わない。
- 補遺 OCR は pp.100–147（前半は見開き）。
各頁の本文冒頭を IAST に直して正規化し、GRETIL 本文（同じく正規化）の中を前から順に探す。
"""
import re
import sys
from pathlib import Path

from indic_transliteration import sanscript

ROOT = Path(__file__).resolve().parent.parent
D = str.maketrans('०१२३४५६७८९', '0123456789')


def split_pages(path):
    return re.split(r'END_OF_PAGE_\d+\n?', Path(path).read_text(encoding='utf-8'))[:-1]


HEAD = re.compile(r'^(\[.*\]\s*$|\s*[०-९]{1,3}\s*$|.*टीका\s*(\[सूत्र)?\s*$|\[?सूत्र\s*$|[०-९.]+\]\s*$|.*प्रकरणम्\s*[०-९]*\s*$|[०-९.]+\]\s.*$|[०-९]{1,3}\s+न्याय.*$)')


def body_start(txt):
    """頁冒頭の柱（頁番号・書名・論題名）を除いた本文の始まり。"""
    ls = [l for l in txt.split('\n') if l.strip()]
    k = 0
    while k < len(ls) and k < 5 and HEAD.match(ls[k].strip()):
        k += 1
    return ' '.join(ls[k:k + 3])


def norm(s):
    s = s.lower()
    s = re.sub(r'[ṃṅñṇnm]', 'n', s)
    s = s.replace('ś', 's').replace('ṣ', 's')
    return re.sub(r'[^a-zāīūṛṝḷēōḥṭḍ]', '', s)


def main(full, extra):
    pages = {}
    fp = split_pages(full)
    for i, tx in enumerate(fp, start=1):
        if i < 14 or 114 <= i <= 129 or i in (265, 266):
            continue
        n = i - 13 if i < 265 else i - 15
        if 100 <= n <= 147:
            continue
        pages[n] = tx
    for tx in split_pages(extra):
        # 頁番号だけの行（3 桁）を頁の区切りとする（前半は見開き 2 頁）
        idx = [(m.start(), int(m.group(1).translate(D)))
               for m in re.finditer(r'(?m)^\s*([०-९]{3})\s*$', tx)]
        for k, (st, n) in enumerate(idx):
            en = idx[k + 1][0] if k + 1 < len(idx) else len(tx)
            pages[n] = tx[st:en]

    lines = (ROOT / 'NVTT_text.txt').read_text(encoding='utf-8').split('\n')
    lines = [re.sub(r'\[p\. \d+\]', '', l) for l in lines]
    # 正規化した本文と、その各文字の (行, 桁)
    stream, where = [], []
    for li, l in enumerate(lines):
        for ci, ch in enumerate(l):
            c = norm(ch)
            if c:
                stream.append(c)
                where.append((li, ci))
    S = ''.join(stream)
    pos = 0
    found, miss = {}, []
    for n in sorted(pages):
        if n == 1:
            continue
        b = body_start(pages[n])
        b = re.sub(r'^[०-९]+\s*', '', b)
        key = norm(sanscript.transliterate(b, sanscript.DEVANAGARI, sanscript.IAST))
        hit = None
        for win in (6000, 20000, 60000):
            cands = []
            for off in range(0, min(len(key) - 14, 120), 5):
                k = key[off:off + 14]
                j = S.find(k, pos, pos + win)
                while j >= 0:
                    cands.append((j - off, off))
                    j = S.find(k, j + 1, pos + win)
            cands.sort()
            # 二つ以上の鍵が近い位置で一致したものを採る
            # 一致した鍵の数がいちばん多いまとまりを採る（同数なら前のもの）
            best = None
            for c, _ in cands:
                grp = [(d, o) for d, o in cands if abs(d - c) <= 40]
                k = len({o for d, o in grp})
                if k >= 2 and (best is None or k > best[0]):
                    # 位置は最も前の鍵（頁の書き出しに近い鍵）から求める
                    best = (k, min(grp, key=lambda t: t[1])[0])
            if best:
                hit = max(pos, best[1])
            if hit is not None:
                break
        if hit is None:
            miss.append(n)
            continue
        found[n] = hit
        if hit - pos < 8000:          # 遠すぎる一致は基準にしない（後で順序を検査）
            pos = hit + 1
    # 頁の順と位置の順が食い違うものを除く
    ns = sorted(found)
    for k, n in enumerate(ns):
        later = [found[m] for m in ns[k + 1:k + 6]]
        if later and found[n] >= min(later):
            del found[n]
            miss.append(n)
    miss.sort()
    found[1] = S.find(norm('viśvavyāpī'))   # p.1 は帰敬偈から
    # 挿入
    ins = {}
    for n, h in found.items():
        li, ci = where[h]
        ins.setdefault(li, []).append((ci, n))
    # 行の中に [p. N] を差し込む（行番号は変えない）
    out = []
    for li, l in enumerate(lines):
        for ci, n in sorted(ins.get(li, []), reverse=True):
            l = l[:ci] + f'[p. {n}]' + l[ci:]
        out.append(l)
    (ROOT / 'NVTT_text.txt').write_text('\n'.join(out), encoding='utf-8')
    print('pages', len(pages), 'found', len(found), 'missing', len(miss))
    print('missing:', miss)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
