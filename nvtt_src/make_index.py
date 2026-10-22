#!/usr/bin/env python3
"""NVTT 全訳の目次ページ nvtt_index.html を作る（nvtt_src/partXX.txt の見出しから）。"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / 'nvtt_src' / 'style.css.part').read_text(encoding='utf-8')
HEAD = re.compile(r'^#\s+(\S+)\s*\|\s*([^|]*?)\s*(?:\|\s*(.*))?$')


def main():
    blocks = []
    for p in sorted((ROOT / 'nvtt_src').glob('part*.txt')):
        meta, secs = {}, []
        for line in p.read_text(encoding='utf-8').split('\n'):
            if line.startswith('='):
                k, _, v = line[1:].partition(' ')
                meta[k] = v.strip()
            m = HEAD.match(line)
            if m:
                secs.append((m.group(1), m.group(2), (m.group(3) or '').strip()))
        f = f'nvtt_zenyaku_{meta["id"]}.html'
        items = ''.join(
            f'<li><a href="{f}#n{html.escape(n.replace(".", "-"))}"><span class="n">{html.escape(n)}</span>'
            f'{html.escape(t)}</a>{f" <span class=sk>{html.escape(sk)}</span>" if sk.startswith("NS") else ""}</li>'
            for n, t, sk in secs)
        blocks.append(f'<details class="part"><summary><a href="{f}">{html.escape(meta.get("title", ""))}</a>'
                      f'<span class="rng">{html.escape(meta.get("sub", ""))}</span></summary>'
                      f'<ol class="secs">{items}</ol></details>')
    page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>タートパリヤ・ティーカー全訳 目次</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
{CSS}
<style>
details.part {{ border-top: 1px solid var(--rule-light); padding: 0.6rem 0; }}
details.part > summary {{ cursor: pointer; font-size: 1.05rem; }}
details.part > summary .rng {{ display: block; font-size: 0.82rem; color: var(--muted); margin-left: 1.2rem; }}
ol.secs {{ list-style: none; padding-left: 1.2rem; margin: 0.5rem 0; font-size: 0.92rem; }}
ol.secs li {{ margin: 0.15rem 0; }}
ol.secs .n {{ display: inline-block; min-width: 2.6rem; color: var(--muted); font-family: 'Cormorant Garamond', serif; }}
ol.secs .sk {{ font-size: 0.78rem; color: var(--muted); }}
.sister {{ font-size: 0.92rem; }}
</style>
</head>
<body>
<div class="header">
  <div class="header-devanagari">न्यायवार्त्तिकतात्पर्यटीका</div>
  <h1>タートパリヤ・ティーカー　全訳</h1>
  <div class="header-sub">Vācaspatimiśra, Nyāyavārttikatātparyaṭīkā · Japanese Translation</div>
  <div class="header-jp">ヴァーチャスパティ・ミシュラ『ニヤーヤ・ヴァールッティカ・タートパリヤ・ティーカー』<br>サンスクリット原文・日本語訳対照（科段つき）</div>
</div>
<section>
<h2 class="chapter">この全訳について</h2>
<p>ヴァーチャスパティ・ミシュラ（10世紀）の『タートパリヤ・ティーカー』は、ウッディヨータカラの『ニヤーヤ・ヴァールッティカ』に対する注釈である。ウダヤナの『タートパリヤ・パリシュッディ』はさらにこの書への注釈にあたる。</p>
<div class="tbl-wrap"><table>
  <tr><th>要素</th><th>内容</th></tr>
  <tr><td>科段</td><td>スートラ（またはスートラのまとまり）ごとの節を第1階層とし、その下を訳者が議論の流れに沿って区切った。▸ をクリックすると開く。</td></tr>
  <tr><td>スートラのカード</td><td>デーヴァナーガリーと和訳。</td></tr>
  <tr><td>左右の対訳</td><td>左にヴァーチャスパティの本文、右に和訳。<span class="pg" style="font-size:.75rem;border:1px solid var(--rule-light);border-radius:3px;padding:0 .3rem">p.12</span> は刊本の頁の始まり。</td></tr>
  <tr><td>関連箇所</td><td>各スートラの節に、『ヴァールッティカ』対訳（NV）とウダヤナの注釈（NVTP 全訳）の該当箇所へのリンクを置いた。</td></tr>
</table></div>
<div class="note"><div class="note-title">底本とおことわり</div>
本文は GRETIL の電子テキスト（Sansknet Project 入力）を、Anantalal Thakur 校訂本（Indian Council of Philosophical Research, 1996）の OCR と照合して直したもの。頁番号とスートラ番号は Thakur 校訂本による。</div>
<p class="sister">関連：<a href="nv/nyayavarttika-index.html">ヴァールッティカ対訳 目次</a>　／　<a href="nvtp_index.html">タートパリヤ・パリシュッディ全訳 目次</a></p>
</section>
<section>
<h2 class="chapter">目次</h2>
{"".join(blocks)}
</section>
<footer>ヴァーチャスパティ・ミシュラ『タートパリヤ・ティーカー』全訳</footer>
</body>
</html>
'''
    (ROOT / 'nvtt_index.html').write_text(page, encoding='utf-8')
    print('wrote nvtt_index.html', len(page))


if __name__ == '__main__':
    main()
