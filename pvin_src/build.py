#!/usr/bin/env python3
"""PVin（プラマーナ・ヴィニシュチャヤ）全訳 HTML のビルド。NVTP 全訳と同じ形式。

pvin_src/partXX.txt（科段・訳文・本文の行番号）と PVin_text.txt（本文、京都・ハーバード方式）から
pvin_zenyaku_XX.html を作る。

partXX.txt の書式（1 行 1 指示）:
  =id 01a
  =title 第1章（1）
  =sub 説明文
  =nav <a ...>前へ</a>...
  # 1 | 見出し | skt            第1階層（# の数＝階層）
  L 12-18                      本文の行番号（PVin_text.txt）。散文として左右対訳に
  L 123:1-4                    行 123 の第 1〜4 文（「. 」で区切った文番号）。123:5- は第 5 文から行末まで
  V 20-23                      偈のカード（ローマ字付き）。行番号の指定は L と同じ
  J 和訳                        直前の L / V の訳（複数行可、空行で段落）
  N ノート                      ノート
  G 要旨                        節の要旨
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kh  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEXT = (ROOT / 'PVin_text.txt').read_text(encoding='utf-8').split('\n')
CSS = (ROOT / 'pvin_src' / 'style.css.part').read_text(encoding='utf-8')

SENT = re.compile(r'(?<=[.?])\s+')
REF = re.compile(r'^(\d+)(?::(\d+)(-(\d*))?)?(?:-(\d+)(?::(\d+))?)?$')


def sentences(n):
    return [s for s in SENT.split(TEXT[n - 1].strip()) if s]


def src(ref):
    """'12-18' / '123:1-4' / '123:5-' / '123:2' / '12-14:3' を本文の文字列のリストに。"""
    m = REF.match(ref)
    if not m:
        raise ValueError(ref)
    a = int(m.group(1))
    if m.group(2):                                   # 行内の文番号
        ss = sentences(a)
        s0 = int(m.group(2))
        if m.group(3) is None:
            s1 = s0
        elif m.group(4) == '':
            s1 = len(ss)
        else:
            s1 = int(m.group(4))
        if not (1 <= s0 <= s1 <= len(ss)):
            raise ValueError(f'{ref}: line {a} has {len(ss)} sentences')
        return [' '.join(ss[s0 - 1:s1])]
    b = int(m.group(5) or a)
    out = [TEXT[i - 1].strip() for i in range(a, b + 1)]
    if m.group(6):                                   # 最終行の途中の文まで
        out[-1] = ' '.join(sentences(b)[:int(m.group(6))])
    return [s for s in out if s]


def render_sa(lines):
    t = ' '.join(lines)
    return html.escape(kh.dev(t, '<k>{}</k>')).replace('&lt;k&gt;', '<span class="kno">').replace('&lt;/k&gt;', '</span>')


def render_verse(lines, fn):
    out = []
    for ln in lines:
        t = html.escape(fn(ln, '\x01{}\x02'))
        out.append(t.replace('\x01', '<span class="kno">').replace('\x02', '</span>'))
    return '<br>'.join(out)


def ja(lines):
    paras = '\n'.join(lines).strip().split('\n\n')
    return ''.join(f'<p>{p.strip()}</p>' for p in paras if p.strip())


def build(part):
    meta = {}
    out = []
    stack = []
    cur = None
    toc = []

    def flush():
        nonlocal cur
        if not cur:
            return
        k = cur['kind']
        if k == 'L':
            out.append(f'<div class="seg"><div class="seg-sa dev">{render_sa(src(cur["ref"]))}</div>'
                       f'<div class="seg-ja">{ja(cur["ja"])}</div></div>')
        elif k == 'V':
            lines = src(cur['ref'])
            out.append(f'<div class="sutra"><div class="sutra-text">{render_verse(lines, kh.dev)}</div>'
                       f'<div class="sutra-iast">{render_verse(lines, kh.iast)}</div>'
                       f'<div class="sutra-jp">{ja(cur["ja"])}</div></div>')
        elif k == 'N':
            out.append(f'<div class="tnote"><span class="tnote-h">ノート</span>{ja(cur["ja"])}</div>')
        elif k == 'G':
            out.append(f'<p class="gist">{" ".join(x.strip() for x in cur["ja"])}</p>')
        cur = None

    def close_to(level):
        while stack and stack[-1] >= level:
            stack.pop()
            out.append('</div></details>')

    for raw in part.read_text(encoding='utf-8').split('\n'):
        line = raw.rstrip()
        if line.startswith('='):
            k, _, v = line[1:].partition(' ')
            meta[k] = v.strip()
            continue
        m = re.match(r'^(#+)\s+(\S+)\s*\|\s*([^|]*?)\s*(?:\|\s*(.*))?$', line)
        if m:
            flush()
            lv = len(m.group(1))
            close_to(lv)
            num, ttl, sk = m.group(2), m.group(3), (m.group(4) or '').strip()
            nid = 'n' + num.replace('.', '-')
            cls = 'node' + (f' lv{lv}' if lv <= 2 else '')
            sk_html = f' <span class="sk">{html.escape(sk)}</span>' if sk else ''
            out.append(f'<details class="{cls}" id="{nid}"><summary><span class="num">{num}</span>'
                       f'<span class="ttl">{html.escape(ttl)}{sk_html}</span></summary><div class="body">')
            stack.append(lv)
            if lv == 1:
                toc.append((nid, num, ttl))
            continue
        m = re.match(r'^([LV])\s+(\S+)\s*$', line)
        if m:
            flush()
            cur = {'kind': m.group(1), 'ref': m.group(2), 'ja': []}
            continue
        m = re.match(r'^([JNG])\s?(.*)$', line)
        if m and (cur is None or m.group(1) != 'J' or cur['kind'] in 'LV'):
            if m.group(1) in 'NG':
                flush()
                cur = {'kind': m.group(1), 'ja': [m.group(2)]}
            else:
                cur['ja'].append(m.group(2))
            continue
        if cur is not None:
            cur['ja'].append(line)
    flush()
    close_to(1)

    toc_html = ''.join(f'<li><a href="#{i}"><span class="n">{html.escape(n)}</span>{html.escape(t)}</a></li>'
                       for i, n, t in toc)
    nav = meta.get('nav', '')
    page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(meta.get("htitle", "プラマーナ・ヴィニシュチャヤ全訳"))}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
{CSS}
<style>
.kno {{ font-family: 'Cormorant Garamond', serif; font-size: 0.78rem; font-style: normal; font-weight: 600; color: var(--accent); border: 1px solid var(--accent-soft); border-radius: 3px; padding: 0 0.3rem; margin: 0 0.2rem; white-space: nowrap; }}
.seg-ja p, .sutra-jp p, .tnote p {{ margin-bottom: 0.5rem; }}
.pnav {{ display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; font-size: 0.9rem; margin: 1rem 0; }}
</style>
</head>
<body>
<div class="header">
  <div class="header-devanagari">प्रमाणविनिश्चयः</div>
  <h1>プラマーナ・ヴィニシュチャヤ　全訳</h1>
  <div class="header-sub">Dharmakīrti, Pramāṇaviniścaya · Japanese Translation</div>
  <div class="header-jp">{html.escape(meta.get("title", ""))}<br>{html.escape(meta.get("sub", ""))}</div>
</div>
<div class="pnav">{nav}</div>
<nav class="toc"><h2>この部分の科段</h2><ol>{toc_html}</ol></nav>
<div class="controls" id="controls">
  <span class="lbl">まとめて開く：</span>
  <button type="button" data-depth="1">第1階層のみ</button>
  <button type="button" data-depth="2">第2階層まで</button>
  <button type="button" data-depth="3">第3階層まで</button>
  <button type="button" data-depth="9">すべて開く</button>
  <button type="button" data-depth="0">すべて閉じる</button>
</div>
<div class="legend-tr"><span>本文（ダルマキールティ）</span><span>和訳</span></div>
<div class="tree">
{chr(10).join(out)}
</div>
<div class="pnav">{nav}</div>
<footer>ダルマキールティ『プラマーナ・ヴィニシュチャヤ』第1・2章 全訳　本文：PVin_text.txt（京都・ハーバード方式の入力テキストをデーヴァナーガリーに機械変換）。（k.N）は偈の番号。</footer>
<script>
(function () {{
  var all = Array.prototype.slice.call(document.querySelectorAll('details.node'));
  function depth(el) {{ var d = 0, p = el; while (p) {{ if (p.matches && p.matches('details.node')) d++; p = p.parentElement; }} return d; }}
  all.forEach(function (el) {{ el.dataset.depth = depth(el); }});
  document.getElementById('controls').addEventListener('click', function (e) {{
    var b = e.target.closest('button[data-depth]'); if (!b) return;
    var n = parseInt(b.dataset.depth, 10);
    all.forEach(function (el) {{ el.open = parseInt(el.dataset.depth, 10) < n; }});
  }});
  function openTo(t) {{ var p = t; while (p) {{ if (p.matches && p.matches('details')) p.open = true; p = p.parentElement; }} t.scrollIntoView({{ block: 'start' }}); }}
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {{
    a.addEventListener('click', function (e) {{
      var t = document.getElementById(a.getAttribute('href').slice(1));
      if (!t || !t.matches('details.node')) return; e.preventDefault(); openTo(t);
      try {{ history.replaceState(null, '', a.getAttribute('href')); }} catch (_) {{}}
    }});
  }});
  if (location.hash.length > 1) {{ var t0 = document.getElementById(location.hash.slice(1)); if (t0 && t0.matches('details.node')) openTo(t0); }}
}})();
</script>
</body>
</html>
'''
    dest = ROOT / f'pvin_zenyaku_{meta["id"]}.html'
    dest.write_text(page, encoding='utf-8')
    print('wrote', dest.name, len(page))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        build(Path(p))
