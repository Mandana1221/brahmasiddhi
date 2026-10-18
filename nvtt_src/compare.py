#!/usr/bin/env python3
"""GRETIL 本文と刊本 OCR を頁ごとに比べ、語の違いを一覧にする（校正の下調べ用）。

使い方: python3 nvtt_src/compare.py 全体OCR.txt 補遺OCR.txt 開始頁 終了頁
"""
import difflib
import re
import sys
from pathlib import Path

from indic_transliteration import sanscript

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages as P  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def ocr_pages(full, extra):
    out = {}
    for i, tx in enumerate(P.split_pages(full), start=1):
        if i < 14 or 114 <= i <= 129 or i in (265, 266):
            continue
        n = i - 13 if i < 265 else i - 15
        if not 100 <= n <= 147:
            out[n] = tx
    for tx in P.split_pages(extra):
        idx = [(m.start(), int(m.group(1).translate(P.D)))
               for m in re.finditer(r'(?m)^\s*([०-९]{3})\s*$', tx)]
        for k, (st, n) in enumerate(idx):
            out[n] = tx[st:idx[k + 1][0] if k + 1 < len(idx) else len(tx)]
    return out


def ocr_body(tx):
    """柱と脚注を除いた本文（IAST）。行末のハイフンはつなぐ。"""
    ls = [l for l in tx.split('\n') if l.strip()]
    k = 0
    while k < len(ls) and k < 5 and P.HEAD.match(ls[k].strip()):
        k += 1
    body = []
    for l in ls[k:]:
        if re.match(r'^\s*[०-९]+\s*\.', l):        # 脚注
            break
        l = re.sub(r'^\s*[०-९]{1,2}\s+', '', l)    # 行番号
        l = re.sub(r'(?<=[ऀ-ॿ])[०-९]{1,2}(?=\S)|[०-९]{1,2}(?=[ऀ-ॿ])', '', l)
        body.append(l.strip())
    t = ' '.join(body)
    t = re.sub(r'-\s+', '', t)
    return sanscript.transliterate(t, sanscript.DEVANAGARI, sanscript.IAST)


def words(s):
    s = re.sub(r'[|/।॥—\-–?,;:()\[\]\'‘’"“”0-9]', ' ', s)
    return s.split()


if __name__ == '__main__' and sys.argv[1] == 'propose':
    pass
elif __name__ == '__main__':
    full, extra, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    ocr = ocr_pages(full, extra)
    text = (ROOT / 'NVTT_text.txt').read_text(encoding='utf-8')
    for n in range(a, b + 1):
        m1 = text.find(f'[p. {n}]')
        m2 = text.find(f'[p. {n + 1}]')
        g = re.sub(r'nys_\S+:', '', text[m1:m2]).replace(f'[p. {n}]', '')
        gw, ow = words(g), words(ocr_body(ocr[n]))
        sm = difflib.SequenceMatcher(None, gw, ow, autojunk=False)
        print(f'===== p.{n}')
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != 'equal':
                print(f'  {op:7} G: {" ".join(gw[i1:i2])[:90]}\n          O: {" ".join(ow[j1:j2])[:90]}')


def propose(full, extra, a, b):
    """1 語対 1 語の違いを、訂正表の候補（行番号<TAB>誤<TAB>正）として出す。採否は人が決める。"""
    ocr = ocr_pages(full, extra)
    lines = (ROOT / 'NVTT_text.txt').read_text(encoding='utf-8').split('\n')
    plain = [re.sub(r'\[p\. \d+\]', '', l) for l in lines]
    text = '\n'.join(lines)
    for n in range(a, b + 1):
        m1, m2 = text.find(f'[p. {n}]'), text.find(f'[p. {n + 1}]')
        l1 = text.count('\n', 0, m1)
        g = re.sub(r'nys_\S+:', '', text[m1:m2]).replace(f'[p. {n}]', '')
        gw, ow = words(g), words(ocr_body(ocr[n]))
        sm = difflib.SequenceMatcher(None, gw, ow, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != 'replace' or i2 - i1 != j2 - j1:
                continue
            for gw1, ow1 in zip(gw[i1:i2], ow[j1:j2]):
                if difflib.SequenceMatcher(None, gw1, ow1).ratio() < 0.75:
                    continue
                for k in range(l1, min(l1 + 80, len(plain))):
                    if gw1 in plain[k]:
                        print(f'{k + 1}\t{gw1}\t{ow1}')
                        break


if __name__ == '__main__' and sys.argv[1] == 'propose':
    propose(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
