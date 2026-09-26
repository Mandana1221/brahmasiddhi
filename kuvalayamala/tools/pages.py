#!/usr/bin/env python3
"""OCRテキスト（km.txt）を刊本の頁ごとに分け、本文と脚注を取り出す作業用スクリプト。
使い方: pages.py km.txt 12 15   → 12〜15頁の本文と脚注を表示
        pages.py km.txt --sec 20 → §20 を含む頁を表示
"""
import re, sys

HEAD = re.compile(r'^(उ[ज्]*जोयणस[ूु]?रि|उजोयण|कुवलय ?माला\s*$)')
JUNK = re.compile(r'(jainelibrary|jalnelibrary|ainelibrary|Education Int|Personal [Uu]se|^\s*[-\[\]०-९६.\s]*\]?\s*$|^\s*\d{1,3}\s*$|^[A-Za-z .~\-]*$)')
FOOT = re.compile(r'^\s*\d{1,2}\)\s')


def load(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    pages, cur = [], None
    for i, l in enumerate(lines[357:5540], 358):
        if HEAD.match(l.strip()):
            cur = {'line': i, 'text': [], 'foot': []}
            pages.append(cur)
            rest = HEAD.sub('', l.strip()).strip()
            rest = re.sub(r'^(विरइया|विरड्या|सरिविरइया|सूरिविरइया)\s*', '', rest)
            if rest.startswith('कुवलय'):
                rest = ''
            if rest:
                cur['text'].append(rest)
            continue
        if cur is None or JUNK.search(l):
            continue
        (cur['foot'] if FOOT.match(l) else cur['text']).append(l)
    return pages


if __name__ == '__main__':
    pages = load(sys.argv[1])
    if sys.argv[2] == '--sec':
        pat = re.compile(r'[६§]\s?%s\)' % ''.join('०१२३४५६७८९'[int(c)] for c in sys.argv[3]))
        hits = [n for n, p in enumerate(pages, 1) if any(pat.search(t) for t in p['text'])]
        print('§%s → 頁 %s' % (sys.argv[3], hits))
        sys.exit()
    a, b = int(sys.argv[2]), int(sys.argv[3])
    for n in range(a, b + 1):
        p = pages[n - 1]
        print('=== p. %d (ocr line %d) ===' % (n, p['line']))
        print('\n'.join(p['text']))
        print('--- 脚注 ---')
        print('\n'.join(p['foot']))
