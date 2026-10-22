#!/usr/bin/env python3
"""ヴァーツヤーヤナ『ニヤーヤ・バーシュヤ』全訳 HTML のビルド。

nbh_src/partXX.txt（科段・訳文・本文の行番号）と NBh_text.txt（Thakur 校訂本の OCR を
nbh_src/prep.py で daṇḍa ごとに 1 行にしたもの）から nbh_zenyaku_XX.html を作る。
書式は NVTT 全訳（nvtt_src/build.py）と同じ。本文はもとからデーヴァナーガリー。
「@」で始まる行（NV・NVTT・NVTP の対応頁の注記）は表示しない（関連箇所のリンクで示す）。
  R ファイル#アンカー | 表示名   参照リンク
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'xref'))
import links  # noqa: E402  NV・NVTT・NVTP の関連箇所リンク

ROOT = Path(__file__).resolve().parent.parent
PREFIX = 'nbh'
TEXT = (ROOT / 'NBh_text.txt').read_text(encoding='utf-8').split('\n')
CSS = (ROOT / 'nbh_src' / 'style.css.part').read_text(encoding='utf-8')

NYS = re.compile(r'^nys_\S+:\s*')


def src_lines(a, b):
    """行番号 a..b（1 始まり、両端含む）の本文。"""
    out = []
    for ln in TEXT[a - 1:b]:
        s = ln.strip()
        if s and not s.startswith('@'):
            out.append(NYS.sub('', s))
    return out


def join(items, verse=False):
    return ('\n' if verse else ' ').join(items)


def deva(txt):
    """表示用に整える（スートラの末尾「//」を「॥」に）。"""
    return re.sub(r'\s*//\s*$', ' ॥', txt, flags=re.M)


def render_sa(txt):
    """[p. N] を頁の印にして、本文をデーヴァナーガリーで示す。"""
    parts = re.split(r'\[p\. (\d+)\]', txt)
    out = html.escape(deva(parts[0]))
    for k in range(1, len(parts), 2):
        out += f'<span class="pg">p.{parts[k]}</span>' + html.escape(deva(parts[k + 1]))
    return out.replace('\n', '<br>')


def ja(lines):
    paras = '\n'.join(lines).strip().split('\n\n')
    return ''.join(f'<p>{p.strip().replace(chr(10), "<br>")}</p>' for p in paras if p.strip())


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
                           f'<div class="sutra-jp">{ja(cur["ja"])}</div></div>')
        elif k == 'N':
            out.append(f'<div class="tnote"><span class="tnote-h">ノート</span>{ja(cur["ja"])}</div>')
        elif k == 'R':
            href, _, label = cur['ja'][0].partition('|')
            out.append(f'<div class="xref"><span class="xref-h">参照</span>'
                       f'<a href="{html.escape(href.strip())}">{html.escape(label.strip())} →</a></div>')
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
            xr = links.for_section(f'{PREFIX}_zenyaku_{meta.get("id", "")}.html', nid, ['nv', 'nvtt', 'nvtp'])
            if xr:
                out.append(xr)
            stack.append(lv)
            if lv == 1:
                toc.append((nid, num, ttl))
            continue
        m = re.match(r'^([LV])\s+(\d+)-(\d+)\s*$', line)
        if m:
            flush()
            cur = {'kind': m.group(1), 'a': int(m.group(2)), 'b': int(m.group(3)), 'ja': []}
            continue
        m = re.match(r'^([JNGR])\s?(.*)$', line)
        if m and (cur is None or m.group(1) != 'J' or cur['kind'] in 'LV'):
            if m.group(1) in 'NGR':
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
<title>{html.escape(meta.get("htitle", "ニヤーヤ・バーシュヤ全訳"))}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
{CSS}
<style>
.pg {{ font-family: 'Cormorant Garamond', serif; font-size: 0.75rem; color: var(--muted); border: 1px solid var(--rule-light); border-radius: 3px; padding: 0 0.3rem; margin: 0 0.2rem; white-space: nowrap; }}
.seg-ja p, .sutra-jp p, .tnote p {{ margin-bottom: 0.5rem; }}
.xref {{ font-size: 0.85rem; margin: 0.4rem 0 0.8rem; padding: 0.35rem 0.7rem; border-left: 3px solid #5B4A9E; background: rgba(91,74,158,0.07); }}
.xref-h {{ color: #5B4A9E; font-weight: 600; margin-right: 0.6rem; }}
.pnav {{ display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; font-size: 0.9rem; margin: 1rem 0; }}
</style>
</head>
<body>
<div class="header">
  <div class="header-devanagari">न्यायभाष्यम्</div>
  <h1>ニヤーヤ・バーシュヤ　全訳</h1>
  <div class="header-sub">Vātsyāyana, Nyāyabhāṣya · Japanese Translation</div>
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
<div class="legend-tr"><span>本文（ヴァーツヤーヤナ）</span><span>和訳</span></div>
<div class="tree">
{chr(10).join(out)}
</div>
<div class="pnav">{nav}</div>
<footer>ヴァーツヤーヤナ『ニヤーヤ・バーシュヤ』全訳　本文：A. Thakur 校訂『Gautamīyanyāyadarśana with Bhāṣya of Vātsyāyana』（1997）の OCR による（脚注の異読は省いた）。頁番号（p.1 など）とスートラ番号は同書による。</footer>
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
    dest = ROOT / f'nbh_zenyaku_{meta["id"]}.html'
    dest.write_text(page, encoding='utf-8')
    print('wrote', dest.name, len(page))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        build(Path(p))
