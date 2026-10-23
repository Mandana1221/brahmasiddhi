#!/usr/bin/env python3
"""NBh 全訳の目次ページ nbh_index.html を作る（nbh_src/partXX.txt の見出しから）。"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / 'nbh_src' / 'style.css.part').read_text(encoding='utf-8')
CHAP = {'01': '第1章', '02': '第1章', '03': '第2章', '04': '第2章', '05': '第3章', '06': '第3章',
        '07': '第4章', '08': '第4章', '09': '第5章', '10': '第5章'}
HEAD = re.compile(r'^#\s+(\S+)\s*\|\s*([^|]*?)\s*(?:\|\s*(.*))?$')


def main():
    blocks = []
    seen = set()
    for p in sorted((ROOT / 'nbh_src').glob('part*.txt')):
        meta, secs = {}, []
        for line in p.read_text(encoding='utf-8').split('\n'):
            if line.startswith('='):
                k, _, v = line[1:].partition(' ')
                meta[k] = v.strip()
            m = HEAD.match(line)
            if m:
                secs.append((m.group(1), m.group(2), (m.group(3) or '').strip()))
        f = f'nbh_zenyaku_{meta["id"]}.html'
        items = ''.join(
            f'<li><a href="{f}#n{html.escape(n.replace(".", "-"))}"><span class="n">{html.escape(n)}</span>'
            f'{html.escape(t)}</a>{f" <span class=sk>{html.escape(sk)}</span>" if sk.startswith("NS") else ""}</li>'
            for n, t, sk in secs)
        ch = CHAP.get(meta['id'][:2])
        if ch and ch not in seen:
            seen.add(ch)
            blocks.append(f'<h3>{ch}</h3>')
        blocks.append(f'<details class="part"><summary><a href="{f}">{html.escape(meta.get("title", ""))}</a>'
                      f'<span class="rng">{html.escape(meta.get("sub", ""))}</span></summary>'
                      f'<ol class="secs">{items}</ol></details>')
    page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ニヤーヤ・バーシュヤ全訳 目次</title>
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
  <div class="header-devanagari">न्यायभाष्यम्</div>
  <h1>ニヤーヤ・バーシュヤ　全訳</h1>
  <div class="header-sub">Vātsyāyana, Nyāyabhāṣya · Japanese Translation</div>
  <div class="header-jp">ヴァーツヤーヤナ『ニヤーヤ・バーシュヤ』<br>サンスクリット原文・日本語訳対照（科段つき）</div>
</div>
<section>
<h2 class="chapter">この全訳について</h2>
<p>ヴァーツヤーヤナの『ニヤーヤ・バーシュヤ』は、ガウタマ（アクシャパーダ）の『ニヤーヤ・スートラ』に対する現存最古の注釈である。ウッディヨータカラの『ニヤーヤ・ヴァールッティカ』はこの注釈をさらに注釈し、ヴァーチャスパティ・ミシュラの『タートパリヤ・ティーカー』、ウダヤナの『タートパリヤ・パリシュッディ』がそれに続く。</p>
<div class="tbl-wrap"><table>
  <tr><th>要素</th><th>内容</th></tr>
  <tr><td>科段</td><td>スートラごとの節を第1階層とし、その下を訳者が議論の流れに沿って区切った。▸ をクリックすると開く。</td></tr>
  <tr><td>スートラのカード</td><td>デーヴァナーガリーと和訳。</td></tr>
  <tr><td>左右の対訳</td><td>左にヴァーツヤーヤナの本文、右に和訳。<span class="pg" style="font-size:.75rem;border:1px solid var(--rule-light);border-radius:3px;padding:0 .3rem">p.12</span> は刊本の頁の始まり。</td></tr>
  <tr><td>関連箇所</td><td>各スートラの節に、『ヴァールッティカ』対訳（NV）、ヴァーチャスパティの注釈（NVTT 全訳）、ウダヤナの注釈（NVTP 全訳）の該当箇所へのリンクを置いた。</td></tr>
</table></div>
<div class="note"><div class="note-title">底本とおことわり</div>
本文は A. Thakur 校訂『Gautamīyanyāyadarśana with Bhāṣya of Vātsyāyana』（Indian Council of Philosophical Research, 1997）の OCR により、読み取りの誤りを直したもの（脚注の異読は省いた）。頁番号とスートラ番号は同書による。</div>
<p class="sister">関連：<a href="nv/nyayavarttika-index.html">ヴァールッティカ対訳 目次</a>　／　<a href="nvtt_index.html">タートパリヤ・ティーカー全訳 目次</a>　／　<a href="nvtp_index.html">タートパリヤ・パリシュッディ全訳 目次</a></p>
</section>
<section>
<h2 class="chapter">目次</h2>
{"".join(blocks)}
</section>
<footer>ヴァーツヤーヤナ『ニヤーヤ・バーシュヤ』全訳</footer>
</body>
</html>
'''
    (ROOT / 'nbh_index.html').write_text(page, encoding='utf-8')
    print('wrote nbh_index.html', len(page))


if __name__ == '__main__':
    main()
