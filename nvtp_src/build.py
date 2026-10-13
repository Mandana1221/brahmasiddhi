#!/usr/bin/env python3
"""NVTP 全訳 HTML のビルド。

nvtp_src/partXX.txt（科段・訳文・本文の行番号）と NVTP_text.txt（本文）から
nvtp_zenyaku_XX.html を作る。刊本の脚注（異読）は出力しない。

partXX.txt の書式（1 行 1 指示）:
  =id 01a
  =title 第1章第1日課（1）
  =sub 説明文
  =range 1–60
  # 1 | 見出し | skt            第1階層（# の数＝階層）
  L 12-18                      本文の行番号（NVTP_text.txt）。散文として左右対訳に
  V 20-23                      偈・スートラのカード（ローマ字付き）
  J 和訳                        直前の L / V の訳（複数行可、空行で段落）
  N ノート                      ノート
  G 要旨                        節の要旨
"""
import html
import re
import sys
from pathlib import Path

from indic_transliteration import sanscript

ROOT = Path(__file__).resolve().parent.parent
TEXT = (ROOT / 'NVTP_text.txt').read_text(encoding='utf-8').split('\n')
CSS = (ROOT / 'nvtp_src' / 'style.css.part').read_text(encoding='utf-8')

FOOT = re.compile(r'^[०-९]{1,2}\s*\.|[A-Za-z]')
PAGE = re.compile(r'^\[p\. (\d+)\]$')


def src_lines(a, b):
    """行番号 a..b（1 始まり、両端含む）の本文。脚注は落とし、頁は 〔p.N〕 に。"""
    out = []
    for ln in TEXT[a - 1:b]:
        s = ln.strip()
        if not s:
            continue
        m = PAGE.match(s)
        if m:
            out.append(('page', m.group(1)))
            continue
        if FOOT.search(s):
            continue
        out.append(('text', s))
    return out


def join(items, verse=False):
    parts = []
    buf = ''
    for kind, s in items:
        if kind == 'page':
            buf += f'\x00{s}\x00'
            continue
        if verse:
            buf += ('\n' if buf and not buf.endswith('\x00') else '') + s
        elif buf.endswith('-'):
            buf = buf[:-1] + s
        else:
            buf += (' ' if buf and not buf.endswith('\x00') else '') + s
    return buf


def render_sa(txt):
    t = html.escape(txt)
    t = re.sub(r'\x00(\d+)\x00', r'<span class="pg">p.\1</span>', t)
    return t.replace('\n', '<br>')


def iast(txt):
    t = re.sub(r'\x00\d+\x00', '', txt)
    t = t.replace('॰', '°')
    t = re.sub(r'(?<![०-९])०(?![०-९])', '°', t)
    return html.escape(sanscript.transliterate(t, sanscript.DEVANAGARI, sanscript.IAST)).replace('\n', '<br>')


def ja(lines):
    paras = '\n'.join(lines).strip().split('\n\n')
    return ''.join(f'<p>{p.strip()}</p>' for p in paras if p.strip())


def build(part):
    meta = {}
    nodes = []          # (level, num, title, sk)
    out = []
    stack = []          # open levels
    cur = None          # current block: dict(kind, lines/a,b, ja=[])
    toc = []

    def flush():
        nonlocal cur
        if not cur:
            return
        k = cur['kind']
        if k in 'LV':
            items = src_lines(cur['a'], cur['b'])
            if k == 'L':
                out.append(f'<div class="seg"><div class="seg-sa dev">{render_sa(join(items))}</div>'
                           f'<div class="seg-ja">{ja(cur["ja"])}</div></div>')
            else:
                raw = join(items, verse=True)
                out.append(f'<div class="sutra"><div class="sutra-text">{render_sa(raw)}</div>'
                           f'<div class="sutra-iast">{iast(raw)}</div>'
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
        m = re.match(r'^([LV])\s+(\d+)-(\d+)\s*$', line)
        if m:
            flush()
            cur = {'kind': m.group(1), 'a': int(m.group(2)), 'b': int(m.group(3)), 'ja': []}
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
<title>{html.escape(meta.get("htitle", "タートパリヤ・パリシュッディ全訳"))}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
{CSS}
<style>
.pg {{ font-family: 'Cormorant Garamond', serif; font-size: 0.75rem; color: var(--muted); border: 1px solid var(--rule-light); border-radius: 3px; padding: 0 0.3rem; margin: 0 0.2rem; white-space: nowrap; }}
.seg-ja p, .sutra-jp p, .tnote p {{ margin-bottom: 0.5rem; }}
.pnav {{ display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; font-size: 0.9rem; margin: 1rem 0; }}
</style>
</head>
<body>
<div class="header">
  <div class="header-devanagari">न्यायवार्त्तिकतात्पर्यपरिशुद्धिः</div>
  <h1>タートパリヤ・パリシュッディ　全訳</h1>
  <div class="header-sub">Udayana, Nyāyavārttikatātparyapariśuddhi · Japanese Translation</div>
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
<div class="legend-tr"><span>本文（ウダヤナ）</span><span>和訳</span></div>
<div class="tree">
{chr(10).join(out)}
</div>
<div class="pnav">{nav}</div>
<footer>ウダヤナ『タートパリヤ・パリシュッディ』全訳（試訳）　本文：A. Thakur 校訂本（1996）の OCR による。脚注の異読は省略。</footer>
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
    dest = ROOT / f'nvtp_zenyaku_{meta["id"]}.html'
    dest.write_text(page, encoding='utf-8')
    print('wrote', dest.name, len(page))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        build(Path(p))
