#!/usr/bin/env python3
"""OCRテキスト（jainelibrary No. 002777 の docx から抽出した km.txt）を
ウパーディエー版の節（§）ごとに切り出す作業用スクリプト。

使い方: sections.py km.txt 2 5          → §2〜§5 の本文
        sections.py km.txt 2 5 --foot   → その範囲の頁の脚注（異読）も表示
OCRでは § が「६」と読まれているので、「६N)」または行頭の「N)」を節の始まりとみなす。
"""
import re, sys

MARK = re.compile(r'(jainelibrary|jalnelibrary|ainelibrary|Education Int|Personal [Uu]se)', re.I)
FOOT = re.compile(r'^\s*[0-9]{1,2}\)\s')
HEAD = re.compile(r'^\s*(उ[ज्]*जोयणस[ूु]?रिविर[इड][य्]*या|उजोयणसूरिविरइया|कुवलय ?माला)\s*')
DIG = '०१२३४५६७८९'


def dev(n):
    return ''.join(DIG[int(c)] for c in str(n))


def load(path):
    L = open(path, encoding='utf-8').read().split('\n')
    text, foot, page = [], {}, 1
    prev = False
    for l in L[358:5540]:
        m = bool(MARK.search(l))
        if m and not prev:
            page += 1
        prev = m or (prev and len(l.strip()) < 30)
        if m or len(l.strip()) < 12:
            continue
        if (FOOT.match(l) and re.search(r'\b(P|J|JP|I)\b', l)) or len(re.findall(r'(?<![०-९\d])[0-9]{1,2}\)\s', l)) >= 2 or 'references 1)' in l:
            foot.setdefault(page, []).append(l)
            continue
        l = HEAD.sub('', l)
        l = re.sub(r'(?<![०-९\d])\s(3|6|9|12|15|18|21|24|27|30|33)\s(?![०-९\d)])', ' ', l)  # 余白の行番号
        text.append((page, l))
    return text, foot


def split(text):
    """節番号を順に探す。見つからない番号は飛ばして次を探す（最大3つ先まで）。"""
    joined, owner = '', []
    for page, l in text:
        owner.append((len(joined), page))
        joined += l + ' '

    def page_at(pos):
        p = 1
        for off, pg in owner:
            if off > pos:
                break
            p = pg
        return p

    def find(n, pos):
        d = r'\s?'.join(dev(n))
        pats = [r'(?<![०-५७८])%s\s?\)' % d, r'(?<![०-९0-9])%d\)' % n]
        best = None
        for p in pats:
            m = re.compile(p).search(joined, pos, pos + 20000)
            if m and (best is None or m.start() < best.start()):
                best = m
        return best

    marks, pos, n = [(1, 0, 0)], 0, 1
    while True:
        for k in (1, 2, 3):
            m = find(n + k, pos + 1)
            if m:
                n, pos = n + k, m.start()
                marks.append((n, m.start(), m.end()))
                break
        else:
            break
    secs = {}
    for i, (n, st, en) in enumerate(marks):
        stop = marks[i + 1][1] if i + 1 < len(marks) else len(joined)
        secs[n] = (sorted({page_at(st), page_at(stop - 1)}), [joined[en:stop]])
    return secs


if __name__ == '__main__':
    text, foot = load(sys.argv[1])
    secs = split(text)
    a, b = int(sys.argv[2]), int(sys.argv[3])
    pages = []
    for n in range(a, b + 1):
        if n not in secs:
            print('=== §%d : 見つからず ===' % n)
            continue
        pg, body = secs[n]
        pages += [p for p in pg if p not in pages]
        print('=== §%d (pdf頁 %s) ===' % (n, pg))
        print(re.sub(r'\s+', ' ', ' '.join(body)).strip())
    if '--foot' in sys.argv:
        for p in pages:
            print('--- 脚注 pdf頁 %d ---' % p)
            print('\n'.join(foot.get(p, [])))
