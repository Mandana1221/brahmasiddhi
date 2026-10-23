#!/usr/bin/env python3
"""NVTP 全訳の目次ページ nvtp_index.html を作る。"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / 'nvtp_src' / 'style.css.part').read_text(encoding='utf-8')

# (ファイルid, 範囲, 見出し, 含む論題)
PARTS = [
    ('01a', '第1章第1日課', 'pp.1–36', '1. 対象・目的・関係の論題（1）'),
    ('01b', '第1章第1日課', 'pp.37–117', '1. 対象・目的・関係の論題（2）'),
    ('01c', '第1章第1日課', 'pp.118–230', '2. 認識手段の定義の論題'),
    ('01d', '第1章第1日課', 'pp.230–306', '3. 認識対象の定義　4. 論証の前段　5. 論証の基盤（定説）　6. 論証　7. 論証の後段'),
    ('02', '第1章第2日課', 'pp.307–334', '8. 論議　9. 疑似理由　10. 詭弁　11. 人の無能力の標識'),
    ('03', '第2章第1日課', 'pp.335–389', '12. 疑いの吟味 〜 20. 特殊な言葉の吟味'),
    ('04', '第2章第2日課', 'pp.390–422', '21. 認識手段は四つか 〜 24. 語の対象'),
    ('05', '第3章第1日課', 'pp.423–461', '25. 感官と別の自己 〜 33. 対象の吟味'),
    ('06', '第3章第2日課', 'pp.462–498', '34. 知の無常 〜 40. 身体は不可見力によって作られる'),
    ('07', '第4章第1日課', 'pp.499–540', '41. 付随して成立したものの吟味 〜 54. 解脱の吟味'),
    ('08', '第4章第2日課', 'pp.541–558', '55. 過失の原因 〜 60. 真理の知を守る'),
    ('09', '第5章第1日課', 'pp.559–585', '61. 対立論証を示すことの擬似 〜 77. 六主張（擬似の議論）'),
    ('10', '第5章第2日課', 'pp.586–601', '78. 主張に関わる五つの敗北の立場 〜 84. 自説からの逸脱・疑似理由'),
]


def main():
    rows = []
    for pid, ah, rng, cont in PARTS:
        f = ROOT / f'nvtp_zenyaku_{pid}.html'
        if f.exists():
            link = f'<a href="nvtp_zenyaku_{pid}.html">{html.escape(ah)}（{rng}）</a>'
            st = '公開'
        else:
            link = f'{html.escape(ah)}（{rng}）'
            st = '翻訳中'
        rows.append(f'<tr><td>{link}</td><td>{html.escape(cont)}</td><td class="c">{st}</td></tr>')
    page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>タートパリヤ・パリシュッディ全訳 目次</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
{CSS}
</head>
<body>
<div class="header">
  <div class="header-devanagari">न्यायवार्त्तिकतात्पर्यपरिशुद्धिः</div>
  <h1>タートパリヤ・パリシュッディ　全訳</h1>
  <div class="header-sub">Udayana, Nyāyavārttikatātparyapariśuddhi · Japanese Translation</div>
  <div class="header-jp">ウダヤナ『ニヤーヤ・ヴァールッティカ・タートパリヤ・パリシュッディ』<br>サンスクリット原文・日本語訳対照（科段つき）</div>
</div>
<section>
<h2 class="chapter">この全訳について</h2>
<p>ウダヤナ（10〜11世紀）の『タートパリヤ・パリシュッディ』は、ヴァーチャスパティ・ミシュラの『ニヤーヤ・ヴァールッティカ・タートパリヤ・ティーカー』に対する注釈である。ニヤーヤ・スートラ、ヴァーツヤーヤナのバーシュヤ、ウッディヨータカラの『ヴァールッティカ』、ヴァーチャスパティの『ティーカー』と重なる注釈の層の最上部にあたり、「ニヤーヤ四注釈（ニヤーヤ・チャトゥルグランティカー）」の一つに数えられる。</p>
<div class="tbl-wrap"><table>
  <tr><th>要素</th><th>内容</th></tr>
  <tr><td>科段</td><td>刊本の論題（プラカラナ）を第1階層とし、その下を訳者が議論の流れに沿って区切った。▸ をクリックすると開く。</td></tr>
  <tr><td>偈・スートラのカード</td><td>デーヴァナーガリー・ローマ字（IAST）・和訳。</td></tr>
  <tr><td>左右の対訳</td><td>左にウダヤナの本文、右に和訳。<span class="pg" style="font-size:.75rem;border:1px solid var(--rule-light);border-radius:3px;padding:0 .3rem">p.12</span> は刊本の頁の始まり。スマホでは上下に並ぶ。</td></tr>
  <tr><td>「〜」と言う</td><td>本書は『ティーカー』の語句を見出しとして引き、それを解説する。かぎ括弧内の多くはその見出し語の訳。</td></tr>
  <tr><td>（　）・ノート</td><td>（　）は訳者の補い。ノートは理解のための説明。</td></tr>
</table></div>
<div class="note"><div class="note-title">底本とおことわり</div>
底本は Anantalal Thakur 校訂本（Indian Council of Philosophical Research, 1996）。本文は OCR から起こしたもので、刊本の脚注（写本の異読）は収めていない。</div>
<p>関連：<a href="nbh_index.html">ニヤーヤ・バーシュヤ全訳 目次</a>　／　<a href="nvtt_index.html">タートパリヤ・ティーカー全訳 目次</a>　／　<a href="nv/nyayavarttika-index.html">ヴァールッティカ対訳 目次</a></p>
</section>
<section>
<h2 class="chapter">目次</h2>
<div class="tbl-wrap"><table>
<tr><th>ファイル</th><th>収める論題</th><th class="c">状態</th></tr>
{"".join(rows)}
</table></div>
</section>
<footer>ウダヤナ『タートパリヤ・パリシュッディ』全訳</footer>
</body>
</html>
'''
    (ROOT / 'nvtp_index.html').write_text(page, encoding='utf-8')
    print('wrote nvtp_index.html')


if __name__ == '__main__':
    main()
