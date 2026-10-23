#!/usr/bin/env python3
"""Thakur 版『ニヤーヤ・バーシュヤ・ヴァールッティカ』の OCR（nv_src/NVdevAll.txt）から、
柱・脚注・行番号を除いた本文の流れを作る。頁の始まりに [p. N]（刊本の頁）を置く。

  python3 nv_src/clean.py  → nv_src/NV_clean.txt
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'nv_src' / 'NVdevAll.txt'
OUT = ROOT / 'nv_src' / 'NV_clean.txt'

DIG = '०१२३४५६७८९'
OFFSET = 14  # PDF の頁番号 − 刊本の頁番号 − 1（END_OF_PAGE_n は n 番目の PDF 頁の終わり）
D2A = str.maketrans(DIG, '0123456789')
LINENO = re.compile(r'^([०-९]{1,2})\s+(?=\S)')
FOOT = re.compile(r'^[०-९]+\.\s')
SIGLA = re.compile(r'(?:\s|^)(?:C|J|om|var|added)(?:\s|\.|$)|॰|०[ऀ-ॿ]')
HEAD_EVEN = re.compile(r'^([०-९]+)\s+न्यायभाष्यवार्त्?तिकम्')
HEAD_ODD = re.compile(r'^[०-९.]+\]?.*\s([०-९]+)\s*$')


def page_of(line):
    s = line.strip()
    if re.fullmatch(r'[०-९]+', s):
        return int(s.translate(D2A))
    m = re.match(r'^([०-९]+)\s+न्याय', s)
    if m:
        return int(m.group(1).translate(D2A))
    m = re.search(r'\s([०-९]+)$', s)
    if m and (']' in s[:14] or 'प्रकरण' in s):
        return int(m.group(1).translate(D2A))
    return None


def main():
    pages = SRC.read_text(encoding='utf-8').split('\n')
    chunks, cur = [], []
    for ln in pages:
        if ln.startswith('END_OF_PAGE_'):
            chunks.append(cur)
            cur = []
        else:
            cur.append(ln)
    out = []
    started = False
    last = 0
    for idx, ch in enumerate(chunks):
        lines = [x.rstrip() for x in ch]
        nonempty = [i for i, x in enumerate(lines) if x.strip()]
        if not nonempty:
            continue
        h = lines[nonempty[0]].strip()
        pg = page_of(h)
        if pg is None:
            if not started:
                continue
            body = lines
        else:
            started = True
            body = lines[nonempty[0] + 1:]
        pg = idx - OFFSET  # 柱の数字は OCR の誤りが多いので、PDF の頁から刊本の頁を出す
        if not started:
            continue
        # 脚注（頁の下）を切る
        cut = len(body)
        for i, x in enumerate(body):
            s = x.strip()
            if FOOT.match(s) and SIGLA.search(s):
                cut = i
                break
        body = body[:cut]
        if pg is not None:
            out.append(f'[p. {pg}]')
        for x in body:
            s = x.strip()
            if not s:
                out.append('')
                continue
            if re.fullmatch(r'[०-९]{1,3}', s):
                continue
            m = LINENO.match(s)
            if m and int(m.group(1).translate(D2A)) % 5 == 0:
                s = s[m.end():]
            out.append(s)
    text = '\n'.join(out)
    # 行末のハイフンで切れた語をつなぐ
    text = re.sub(r'-\n+(\[p\. \d+\])\n+', r'\1', text)
    text = re.sub(r'-\n(?=\S)', '', text)
    # 脚注の番号（語に付いた数字）を除く。॥…॥ の中の番号は残す
    text = re.sub(r'(?<=[ऀ-ॣॱ-ॿ])[०-९]+(?![०-९]*[।॥])', '', text)
    text = re.sub(r'(?<![॥।०-९])[०-९]+(?=[ऀ-ॣॱ-ॿ])', '', text)
    OUT.write_text(text, encoding='utf-8')
    print('wrote', OUT, len(text))


if __name__ == '__main__':
    main()
