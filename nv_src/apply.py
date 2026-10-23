#!/usr/bin/env python3
"""補完ファイル nv_src/fill/NN.txt を元のページ nv_src/orig に当て、補完したページを nv_src/pages に書く。
補完ファイルのないページはそのまま写す。

  python3 nv_src/apply.py
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / 'nv_src' / 'orig'
OUTD = ROOT / 'nv_src' / 'pages'
FILL = ROOT / 'nv_src' / 'fill'
SRC_RE = re.compile(r'(<div class="src[^"]*"[^>]*>)(.*?)(</div>)', re.S)
TR_RE = re.compile(r'(<div class="tr">)(.*?)(</div>)', re.S)
GAP = re.compile(r'\s*(?:……|…)\s*')


def read_fill(p):
    """補完ファイルを読む。S は OCR の原文。F 行（「誤り<TAB>正」）で S を直し、
    B 行・A 行で S の前・後に補う。J は和訳。R 行は F と同じだが、すべての箇所を直す。"""
    items = {}
    cur = None
    text = p.read_text(encoding='utf-8')
    pj = p.with_name(p.stem + '.j.txt')  # 訳者が書く分（J・F・A・B、S の差し替え）
    if pj.exists():
        text += '\n' + pj.read_text(encoding='utf-8')
    for ln in text.split('\n'):
        if ln.startswith('@ '):
            b, g = ln[2:].split()[:2]
            cur = items.setdefault((int(b), int(g)), {'F': []})
        elif ln.startswith('#'):
            continue
        elif cur is None:
            continue
        elif ln[:2] in ('S ', 'J ', 'A ', 'B ') or ln in ('S', 'J'):
            cur[ln[0]] = ln[2:].strip()
        elif ln.startswith('F ') or ln.startswith('R '):
            old, _, new = ln[2:].partition('\t')
            cur['F'].append((old, new, ln[0] == 'R'))
    for k, it in items.items():
        s = it.get('S', '')
        if s in ('', '=', '?'):
            if it.get('A') and s == '?':
                it['S'] = it['A']
            continue
        for old, new, every in it['F']:
            if old not in s:
                print(p.name, k, '直せない:', old)
            s = s.replace(old, new) if every else s.replace(old, new, 1)
        s = (it.get('B', '') + ' ' + s.strip() + ' ' + it.get('A', '')).strip()
        it['S'] = re.sub(r'\s+', ' ', s)
    return items


def fill_block(body, gaps_in, key):
    """body の k 番目の省略を gaps_in[k][key] で置き換える（無い・= のものは残す）。"""
    parts = GAP.split(body)
    seps = GAP.findall(body)
    out = [parts[0]]
    for k in range(len(seps)):
        it = gaps_in.get(k, {})
        v = it.get(key, '')
        if it.get('S', '') in ('', '=', '?') or not v:
            out.append(seps[k])
        else:
            out.append(' ' + v + ' ' if key == 'S' else v)
        out.append(parts[k + 1])
    return ''.join(out)


def main():
    OUTD.mkdir(exist_ok=True)
    bad = 0
    for f in sorted(ORIG.glob('*.html')):
        n = f.name.split('-')[1]
        fp = FILL / f'{int(n):02d}.txt' if n.isdigit() else None
        if not fp or not fp.exists():
            shutil.copy(f, OUTD / f.name)
            continue
        items = read_fill(fp)
        t = f.read_text(encoding='utf-8')
        srcs = list(SRC_RE.finditer(t))
        trs = list(TR_RE.finditer(t))
        if len(srcs) != len(trs):
            print(f.name, 'src と tr の数が合わない'); bad += 1
            continue
        reps = []
        for bi, (ms, mt) in enumerate(zip(srcs, trs)):
            gi = {g: v for (b, g), v in items.items() if b == bi}
            if not gi:
                continue
            ns, nt = len(GAP.findall(ms.group(2))), len(GAP.findall(mt.group(2)))
            filled = [k for k, v in gi.items() if v.get('S') not in ('', '=', '?', None) and v.get('J')]
            if ns != nt and filled:
                print(f.name, 'block', bi, f'原文の省略 {ns} と訳の省略 {nt} が合わない'); bad += 1
            for k, v in gi.items():
                if v.get('S') not in ('', '=', '?', None) and not v.get('J'):
                    print(f.name, 'block', bi, 'gap', k, '和訳がない')
            reps.append((ms.start(2), ms.end(2), fill_block(ms.group(2), gi, 'S')))
            reps.append((mt.start(2), mt.end(2), fill_block(mt.group(2), gi, 'J')))
        for a, b, v in sorted(reps, reverse=True):
            t = t[:a] + v + t[b:]
        (OUTD / f.name).write_text(t, encoding='utf-8')
    if bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
