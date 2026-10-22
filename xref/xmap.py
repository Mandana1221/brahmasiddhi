#!/usr/bin/env python3
"""NBh（バーシュヤ全訳）・NV（ヴァールッティカ対訳）・NVTT（タートパリヤ・ティーカー全訳）・NVTP（パリシュッディ全訳）の
対応表をスートラ番号で作る。

  python3 xref/xmap.py NV対訳のディレクトリ   →  xref/xmap.json

NV は nyayavarttika-N-taiyaku.html の各ブロック（id="uN"）の「NS a.b.c(–d)」（ヒンディー訳の番号の
ページは xref/thakur.py で Thakur 版の番号に直す）、
NBh・NVTT は nbh_src・nvtt_src の partXX.txt の「NS …」、NVTP は nvtp_src/partXX.txt の「sūtra …」から読む。
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thakur  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HEAD = re.compile(r'^(#+)\s+(\S+)\s*\|\s*([^|]*?)\s*(?:\|\s*(.*))?$')
RANGE = re.compile(r'([1-5])\.([12])\.(\d+)(付)?(?:\s*[–-]\s*(?:[1-5]\.[12]\.)?(\d+))?')


def sutras(tag):
    """'NS 4.2.21–25' / 'sūtra 5.1.5–6' / 'NS 2.2.14–2.2.16' → ['4.2.21', …]。"""
    out = []
    for m in RANGE.finditer(tag):
        a, b, c = m.group(1), m.group(2), int(m.group(3))
        if m.group(4):                 # 付スートラ（Thakur 版でスートラに数えない文。例：2.1.32付）
            out.append(f'{a}.{b}.{c}付')
            continue
        d = int(m.group(5)) if m.group(5) else c
        out += [f'{a}.{b}.{n}' for n in range(c, max(c, d) + 1)]
    return out


def parts(src, prefix, key):
    """partXX.txt の見出しのうち、タグが key で始まるもの。同じスートラは最も深い見出しを採る。"""
    res = {}
    for p in sorted((ROOT / src).glob('part*.txt')):
        meta = {}
        for line in p.read_text(encoding='utf-8').split('\n'):
            if line.startswith('=id '):
                meta['id'] = line[4:].strip()
            m = HEAD.match(line)
            if not m:
                continue
            lv, num, ttl, tag = len(m.group(1)), m.group(2), m.group(3), (m.group(4) or '')
            if re.fullmatch(r'(第[\d–]+)?スートラ', ttl) or num.endswith('.0'):
                continue        # スートラ本文だけの節（「N.0 第Nスートラ」など）は採らず、親の節を採る
            got = tag.split(None, 1)[1] if tag.startswith(key) and ' ' in tag else ''
            got += ' ' + ' '.join(re.findall(r'[1-5]\.[12]\.\d+(?:[–-]\d+)?', ttl))
            if not got.strip():
                continue
            tag = got
            ent = {'file': f'{prefix}_zenyaku_{meta["id"]}.html', 'id': 'n' + num.replace('.', '-'),
                   'num': num, 'title': ttl, 'lv': lv}
            for s in sutras(tag):
                old = res.get(s)
                if old is None or (old['file'] == ent['file'] and lv > old['lv']):
                    res[s] = ent
    return res


def nv(nvdir):
    """NV 対訳の各ブロックのスートラ（Thakur 版の番号に直して）。"""
    res = {}
    for f in sorted(Path(nvdir).glob('nyayavarttika-*-taiyaku.html'), key=lambda x: int(x.name.split('-')[1])):
        t = f.read_text(encoding='utf-8')
        sec, sno = '', ''
        hindi = thakur.page_no(f.name) in thakur.HINDI_PAGES
        pat = (r'<span class="sec-no">([^<]*)</span><h2>(.*?)</h2>|<div class="mula[^"]*" id="(u\d+)">\s*'
               r'<span class="ref">([^<]*)</span>\s*<div class="src[^"]*"[^>]*>(.*?)</div>')
        for m in re.finditer(pat, t, re.S):
            if m.group(2) is not None:
                sno, sec = m.group(1), html.unescape(re.sub(r'<[^>]*>', '', m.group(2)))
                continue
            uid, ref = m.group(3), html.unescape(m.group(4))
            if 'NS' not in ref:
                continue
            if hindi:
                ref, sec = thakur.conv_lat(ref), thakur.conv_lat(sec)
            ss = sutras(ref.split('NS', 1)[1])
            ent = {'file': f.name, 'id': uid, 'sec': sno, 'title': sec, 'ref': ref.strip()}
            for s in ss:
                res.setdefault(s, []).append(ent)
    return res


def main():
    nvmap = nv(sys.argv[1])
    tt = parts('nvtt_src', 'nvtt', ('NS',))
    tp = parts('nvtp_src', 'nvtp', ('NS', 'sūtra'))
    nb = parts('nbh_src', 'nbh', ('NS',))
    keys = sorted(set(nvmap) | set(tt) | set(tp) | set(nb), key=lambda s: tuple(int(x.rstrip('付')) for x in s.split('.')) + (s.endswith('付'),))
    out = {k: {'nbh': nb.get(k), 'nv': nvmap.get(k, []), 'nvtt': tt.get(k), 'nvtp': tp.get(k)} for k in keys}
    for k, v in out.items():           # 付スートラは、対応がなければ本スートラの節に
        if k.endswith('付'):
            for t in ('nbh', 'nvtt', 'nvtp'):
                v[t] = v[t] or out.get(k[:-1], {}).get(t)
    (ROOT / 'xref' / 'xmap.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(keys), 'sūtras;',
          'nbh', sum(1 for v in out.values() if v['nbh']),
          'nv', sum(1 for v in out.values() if v['nv']),
          'nvtt', sum(1 for v in out.values() if v['nvtt']),
          'nvtp', sum(1 for v in out.values() if v['nvtp']))


if __name__ == '__main__':
    main()
