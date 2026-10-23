#!/usr/bin/env python3
"""補完ファイル nv_src/fill/NN.txt を元のページ nv_src/orig に当て、補完したページを nv_src/pages に書く。
補完ファイルのないページはそのまま写す。

  python3 nv_src/apply.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / 'nv_src' / 'orig'
OUTD = ROOT / 'nv_src' / 'pages'
FILL = ROOT / 'nv_src' / 'fill'
SRC_RE = re.compile(r'(<div class="src[^"]*"[^>]*>)(.*?)(</div>)', re.S)
TR_RE = re.compile(r'(<div class="tr">)(.*?)(</div>)', re.S)
GAP = re.compile(r'\s*(?:……|…)\s*')
CLEAN = (ROOT / 'nv_src' / 'NV_clean.txt').read_text(encoding='utf-8')


def tidy(t):
    t = re.sub(r'\[p\. \d+\]', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s*([।॥?])\s*', r' \1 ', t)
    t = re.sub(r'॥ ([०-९।]+) ॥', r'॥\1॥', t)
    return re.sub(r'^[।॥?,\s]+', '', t.strip())


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
        elif ln[:2] in ('S ', 'J ', 'A ', 'B ', 'T ') or ln in ('S', 'J'):
            cur[ln[0]] = ln[2:].strip()
        elif ln.startswith('O '):
            # O 始まりの文字列<TAB>終わりの文字列：OCR 本文からその間（始まりを含み終わりを含まない）を S とする
            a, _, b = ln[2:].partition('\t')
            i = CLEAN.find(a)
            j = CLEAN.find(b, i + len(a)) if i >= 0 else -1
            if i < 0 or j < 0:
                print(p.name, '見つからない O:', a[:20], b[:20])
            else:
                cur['S'] = tidy(CLEAN[i:j])
        elif ln == 'Y':
            cur['Y'] = True  # 番号つきの列挙の前で改行する
        elif ln[:2] in ('F ', 'R ', 'X '):
            old, _, new = ln[2:].partition('\t')
            cur['F'].append((old, new, ln[0]))
    for k, it in items.items():
        s = it.get('S', '')
        if s in ('', '=', '?'):
            if it.get('A') and s == '?':
                it['S'] = it['A']
            continue
        for old, new, kind in it['F']:
            if kind == 'X':  # 正規表現で一か所
                s2 = re.sub(old, new, s, count=1)
                if s2 == s:
                    print(p.name, k, '直せない:', old)
                s = s2
                continue
            if old not in s:
                print(p.name, k, '直せない:', old)
            s = s.replace(old, new) if kind == 'R' else s.replace(old, new, 1)
        s = (it.get('B', '') + ' ' + s.strip() + ' ' + it.get('A', '')).strip()
        s = re.sub(r'\s+', ' ', s)
        if it.get('Y'):
            s = re.sub(r' (?=[०-९]{1,2}\. )', '<br>', s)
        it['S'] = s
    return items


def fill_block(body, gaps_in, key):
    """body の k 番目の省略を gaps_in[k][key] で置き換える（無い・= のものは残す）。"""
    parts = GAP.split(body)
    seps = GAP.findall(body)
    out = [parts[0]]
    if key == 'J':
        # 訳の省略の位置が原文と違うとき：T 行で訳の何番目の省略かを指定する
        tmap = {}
        for g, it in gaps_in.items():
            if it.get('T', '').startswith('@'):
                continue  # 訳に省略がない箇所：後で T の文字列の直後に入れる
            tmap[int(it['T']) if 'T' in it else g] = it
    for k in range(len(seps)):
        it = tmap.get(k, {}) if key == 'J' else gaps_in.get(k, {})
        v = it.get(key, '')
        if it.get('S', '') in ('', '=', '?') or not v or not it.get('J'):
            out.append(seps[k])
        else:
            if key == 'S' and v.startswith('+'):
                out.append(v[1:].strip().replace('_', ' '))  # 刊本の略記（語の途中の「……」）は空白なしでつなぐ（_ は空白）
            else:
                out.append(' ' + v + ' ' if key == 'S' else v)
        out.append(parts[k + 1])
    res = ''.join(out)
    if key == 'J':
        for it in gaps_in.values():
            a = it.get('T', '')
            if a.startswith('@') and it.get('J') and it.get('S', '') not in ('', '=', '?'):
                if a[1:] in res:
                    res = res.replace(a[1:], a[1:] + it['J'], 1)
                else:
                    print('T の目印が見つからない:', a[1:30])
    return res


# 補完したので、「抜粋した」「省略箇所」などと書いた解説を直す（原文・和訳の欄は対象外）
NOTE_FIX = [
    (r'Uddyotakara の答えは長く、細部は抜き出しにとどめましたが、要点は、', 'Uddyotakara の答えの要点は、'),
    (r'ヒンディー訳所収の本文によって補うべき箇所ですが、ここでは抜き出しにとどめました。', 'OCR テキストによって全文を補いました。'),
    (r'OCR テキストでは Thakur 版 p\.224 の本文が欠落しています（END_OF_PAGE_238 と 239 が続いている）。', 'もとの OCR テキストでは Thakur 版 p.224 の本文が欠けていましたが、別に行った p.224 の OCR によって補いました。'),
    (r'OCR テキストによって全文を補いました。', ''),
    (r'Thakur 版の抜粋で省いた', ''),
    (r'(は、?)読みが定まらないので(?:訳していません|省略しました)', r'\1読みが定まりませんが、文脈から訳しました'),
    (r'は趣旨が取りにくいので、省きました', 'は趣旨が取りにくいですが、文脈から訳しました'),
    (r'は、読みが確かでないので省きました', 'は、読みが確かではありませんが、文脈から訳しました'),
    (r'写本の異読も多いので、要点を抜き出しました。', '写本の異読も多いですが、全文を載せて訳しました。'),
    (r'も読みが定まらないので省略しました', 'も読みが定まりませんが、文脈から訳しました'),
    (r'省略した(?=[「箇部最冒物斑])', '補った'),
    (r'省略箇所', '補った箇所'),
]
KEEP = re.compile(r'<div class="(?:src[^"]*|tr)"[^>]*>.*?</div>', re.S)


def fix_notes(t):
    out, pos = [], 0
    for m in KEEP.finditer(t):
        out.append(fix_text(t[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fix_text(t[pos:]))
    return ''.join(out)


ABRIDGED = re.compile(r'抜き出|抜粋|ほぼ全文|「……」で省略|全文を載せた（「……」')


def fix_sentence(x):
    if not ABRIDGED.search(x) or re.search('[\u0900-\u097F]', x):
        return x
    head = re.match(r'^\s*', x).group(0)
    if x.rstrip().endswith('。'):
        return head + ('原文は省略せずに全文を載せました。' if 'ました' in x else '原文は省略せずに全文を載せた。')
    return head + '原文は省略せずに全文を載せた'


def fix_text(s):
    for a, b in NOTE_FIX:
        s = re.sub(a, b, s)
    # 文（「。」または タグで区切る）ごとに見る
    parts = re.split(r'(<[^>]+>)', s)
    for i in range(0, len(parts), 2):
        parts[i] = ''.join(fix_sentence(x) for x in re.findall(r'[^。]*。|[^。]+$', parts[i]))
    return ''.join(parts)


def main():
    OUTD.mkdir(exist_ok=True)
    bad = 0
    for f in sorted(ORIG.glob('*.html')):
        n = f.name.split('-')[1]
        fp = FILL / f'{int(n):02d}.txt' if n.isdigit() else None
        if not fp or not fp.exists():
            (OUTD / f.name).write_text(fix_notes(f.read_text(encoding="utf-8")), encoding="utf-8")
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
            if ns != nt and filled and not any('T' in v for v in gi.values()):
                print(f.name, 'block', bi, f'原文の省略 {ns} と訳の省略 {nt} が合わない'); bad += 1
            for k, v in gi.items():
                if v.get('S') not in ('', '=', '?', None) and not v.get('J'):
                    print(f.name, 'block', bi, 'gap', k, '和訳がない')
            reps.append((ms.start(2), ms.end(2), fill_block(ms.group(2), gi, 'S')))
            reps.append((mt.start(2), mt.end(2), fill_block(mt.group(2), gi, 'J')))
        for a, b, v in sorted(reps, reverse=True):
            t = t[:a] + v + t[b:]
        t = fix_notes(t)
        (OUTD / f.name).write_text(t, encoding='utf-8')
    if bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
