#!/usr/bin/env python3
"""NV 対訳ページの元（nv_src/orig）の原文欄にある省略「……」を、OCR 本文（nv_src/NV_clean.txt）の中で特定する。

  python3 nv_src/gaps.py [ページ番号 ...]  → 各省略の前後の文脈と、OCR から取り出した欠けた本文を表示
  python3 nv_src/gaps.py --stat           → ページごとの省略数・特定できた数・欠けた本文の字数
"""
import bisect
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'nv_src' / 'orig'
CLEAN = (ROOT / 'nv_src' / 'NV_clean.txt').read_text(encoding='utf-8')
SRC_RE = re.compile(r'(<div class="src[^"]*"[^>]*>)(.*?)(</div>)', re.S)
TR_RE = re.compile(r'(<div class="tr">)(.*?)(</div>)', re.S)
GAP = re.compile(r'\s*(?:……|…)\s*')
KEEP = re.compile(r'[अ-हा-ौॠ-ॣ]')


def norm(s, strip=True):
    """比べるための形：子音字と母音（記号）だけを残す（virama・anusvara・visarga・空白・記号は捨てる）。"""
    if strip:
        s = re.sub(r'<[^>]+>', '', s)
    out, idx = [], []
    for i, ch in enumerate(s):
        if KEEP.match(ch):
            out.append(ch)
            idx.append(i)
    return ''.join(out), idx


NC, NCI = norm(CLEAN, strip=False)
# 刊本の頁 → NC 上の位置
PPOS = {}
for _m in re.finditer(r'\[p\. (\d+)\]', CLEAN):
    PPOS[int(_m.group(1))] = bisect.bisect_left(NCI, _m.start())
REF_RE = re.compile(r'<span class="ref">pp?\.(\d+)(?:[–-](\d+))?')


def region(p0, p1):
    a = PPOS.get(p0 - 1) or PPOS.get(p0 - 2) or PPOS.get(p0) or 0
    b = PPOS.get(p1 + 2) or PPOS.get(p1 + 3) or len(NC)
    return a, b


def _find(segs, lo, hi):
    for L, off, seg in segs:
        k = NC.find(seg, lo, hi)
        if k >= 0:
            return k, L, off
    return None, 0, 0


def find_left(ctx, lo, hi):
    """ctx（省略の直前の本文）の末尾を NC[lo:hi] で探す。編者が文末を縮めていることがあるので、
    末尾から少しずつずらした断片でも探す。見つかれば（NC 上の終わりの位置, 断片の長さ）。"""
    n, _ = norm(ctx)
    segs = [(L, off, n[len(n) - off - L:len(n) - off]) for L in (24, 16, 12, 9)
            for off in range(0, min(len(n) - L, 40) + 1) if len(n) >= L + off]
    k, L, off = _find(segs, lo, hi)
    return (k + L + off, L) if k is not None else (None, 0)


def find_right(ctx, lo, hi):
    n, _ = norm(ctx)
    segs = [(L, off, n[off:off + L]) for L in (24, 16, 12, 9)
            for off in range(0, min(len(n) - L, 40) + 1) if len(n) >= L + off]
    k, L, off = _find(segs, lo, hi)
    return (max(lo, k - off), L) if k is not None else (None, 0)


BOUND = set(' \n।॥?,;—-')
COMB = re.compile(r'[\u0900-\u0903\u093a-\u094f\u0962\u0963]')


def snap(ca, cb):
    """切れ目が語の途中に来たときに語の境目へ寄せる。"""
    # 始め：脚注の数字を飛ばす。母音記号などで始まれば前の語の続きなので次の境目まで進め、
    # 子音字で始まり前も文字なら、その語の頭まで戻す。
    while ca < cb and CLEAN[ca] in '०१२३४५६७८९':
        ca += 1
    if ca < cb and CLEAN[ca - 1] not in BOUND and CLEAN[ca] not in BOUND:
        if COMB.match(CLEAN[ca]):
            while ca < cb and CLEAN[ca] not in BOUND:
                ca += 1
            while ca < cb and CLEAN[ca] in '।॥?, ':
                ca += 1
        else:
            while ca > 0 and CLEAN[ca - 1] not in BOUND:
                ca -= 1
    # 終わり：語の途中なら、その語の終わり（と続く句読点）まで延ばす
    if cb < len(CLEAN) and CLEAN[cb - 1] not in BOUND and CLEAN[cb] not in BOUND:
        while cb < len(CLEAN) and CLEAN[cb] not in BOUND:
            cb += 1
        while cb < len(CLEAN) and CLEAN[cb] in '।॥?':
            cb += 1
    return ca, cb


def page_files():
    return sorted(PAGES.glob('nyayavarttika-*-taiyaku.html'), key=lambda f: int(f.name.split('-')[1]))


def gaps_of(f):
    """ページ f の省略ごとに dict を返す。"""
    t = f.read_text(encoding='utf-8')
    res = []
    for bi, m in enumerate(SRC_RE.finditer(t)):
        body = m.group(2)
        parts = GAP.split(body)
        if len(parts) < 2:
            continue
        r = REF_RE.search(t, max(0, m.start() - 400), m.start())
        if not r:
            r = list(REF_RE.finditer(t, 0, m.start()))[-1]
        p0 = int(r.group(1)); p1 = int(r.group(2) or p0)
        lo, hi = region(p0, p1)
        pos = lo
        for gi in range(len(parts) - 1):
            left, right = parts[gi], parts[gi + 1]
            a, la = find_left(left, pos, hi)
            b, lb = (None, 0)
            if a is not None:
                b, lb = find_right(right, a, hi)
            g = {'block': bi, 'gap': gi, 'pp': f'{p0}-{p1}', 'left': left[-60:], 'right': right[:60], 'la': la, 'lb': lb}
            if a is not None and b is not None and b >= a:
                ca = NCI[a - 1] + 1
                cb = NCI[b] if b < len(NCI) else len(CLEAN)
                ca, cb = snap(ca, cb)
                g['text'] = CLEAN[ca:cb].strip()
                pos = b
            elif a is not None:
                pos = a
            res.append(g)
    return res


def main():
    args = sys.argv[1:]
    if args and args[0] == '--stat':
        tot = ok = chars = 0
        for f in page_files():
            gs = gaps_of(f)
            n_ok = sum(1 for g in gs if 'text' in g)
            c = sum(len(norm(g.get('text', ''))[0]) for g in gs)
            tot += len(gs); ok += n_ok; chars += c
            if gs:
                print(f.name.split('-')[1], len(gs), n_ok, c)
        print('total', tot, 'found', ok, 'chars', chars)
        return
    for a in args:
        f = PAGES / f'nyayavarttika-{a}-taiyaku.html'
        for g in gaps_of(f):
            print(json.dumps(g, ensure_ascii=False))


if __name__ == '__main__':
    main()
