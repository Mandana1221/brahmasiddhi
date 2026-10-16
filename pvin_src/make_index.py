#!/usr/bin/env python3
"""PVin 全訳の目次ページ pvin_index.html を作る。"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / 'pvin_src' / 'style.css.part').read_text(encoding='utf-8')

# (ファイルid, 章, 本文の行, 含む論題)
PARTS = [
    ('01a', '第1章 直接知覚（1）', '1–104', '0. 帰敬と序　1. 認識手段は二つ　2. 直接知覚の定義　3. 意による直接知覚'),
    ('01b', '第1章 直接知覚（2）', '105–160', '4. 自己認識　5. ヨーガ行者の直接知覚　6. 似而非の直接知覚'),
    ('01c', '第1章 直接知覚（3）', '161–237', '7. 認識手段と結果　8. 自己認識が結果（唯識）　9. 同時認識の決まり'),
    ('02a', '第2章 自分のための推論（1）', '238–323', '1. 推論の二種　2. 推論は錯誤だが正しい　3. 推論の対象　4. 徴表の三相　5. 「無いところに無い」'),
    ('02b', '第2章 自分のための推論（2）', '324–407', '6. 三種の徴表　7. 非認識の徴表　8. 隔たったものと聖典　9. 二種の非認識'),
    ('02c', '第2章 自分のための推論（3）', '408–521', '10. 自性の徴表　11. 刹那滅　12. 結果の徴表　13. 無常性　14. 単なる不見　15. 否定の証因'),
]


def part3():
    """第3章の part ファイルの =title・=sub から目次の行を作る。"""
    out = []
    for f in sorted((ROOT / 'pvin_src').glob('part03*.txt')):
        meta = dict(ln[1:].partition(' ')[::2] for ln in f.read_text(encoding='utf-8').split('\n') if ln.startswith('='))
        title = meta.get('title', '').replace('　', ' ').replace('（その', '（').replace('）', '）')
        sub = meta.get('sub', '')
        out.append((meta['id'], title, sub))
    return out


def main():
    rows = []
    for pid, ch, rng, cont in PARTS:
        link = f'<a href="pvin_zenyaku_{pid}.html">{html.escape(ch)}</a>'
        rows.append(f'<tr><td>{link}<br><small>本文 {rng} 行</small></td><td>{html.escape(cont)}</td></tr>')
    for pid, ch, sub in part3():
        link = f'<a href="pvin_zenyaku_{pid}.html">{html.escape(ch)}</a>'
        rows.append(f'<tr><td>{link}</td><td>{html.escape(sub)}</td></tr>')
    page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>プラマーナ・ヴィニシュチャヤ全訳 目次</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
{CSS}
</head>
<body>
<div class="header">
  <div class="header-devanagari">प्रमाणविनिश्चयः</div>
  <h1>プラマーナ・ヴィニシュチャヤ　全訳</h1>
  <div class="header-sub">Dharmakīrti, Pramāṇaviniścaya · Japanese Translation</div>
  <div class="header-jp">ダルマキールティ『プラマーナ・ヴィニシュチャヤ（量決択）』第1–3章<br>サンスクリット原文・日本語訳対照（科段つき）</div>
</div>
<section>
<h2 class="chapter">この全訳について</h2>
<p>ダルマキールティ（法称、7世紀）の『プラマーナ・ヴィニシュチャヤ』は、主著『プラマーナ・ヴァールッティカ』の内容を、偈と散文の注を組み合わせて整理し直した認識論・論理学の書である。ここでは全3章、第1章「直接知覚」・第2章「自分のための推論」・第3章「他人のための推論」を訳す。</p>
<div class="tbl-wrap"><table>
  <tr><th>要素</th><th>内容</th></tr>
  <tr><td>科段</td><td>議論の流れに沿って訳者が区切った。▸ をクリックすると開く。</td></tr>
  <tr><td>偈のカード</td><td>デーヴァナーガリー・ローマ字（IAST）・和訳。偈の一部だけが散文の間に置かれている場合も、その部分をカードにした。</td></tr>
  <tr><td>左右の対訳</td><td>左にダルマキールティの本文（デーヴァナーガリー）、右に和訳。スマホでは上下に並ぶ。</td></tr>
  <tr><td>（　）・ノート</td><td>（　）は訳者の補い。（反論）（答え）は議論の話者の区別。ノートは理解のための説明。</td></tr>
</table></div>
<div class="note"><div class="note-title">底本とおことわり</div>
本文は京都・ハーバード方式で入力されたテキスト（PVin_text.txt）を機械的にデーヴァナーガリーとローマ字に変換したもの。明らかな入力の誤り（kalpanāpoḍham、mūḍhaṃ、aniścitāyām）だけを直した。第1章第1偈などテキストに欠落があるらしい箇所は、ノートで注記した。<br>第3章の本文は Hugon &amp; Tomabechi 校訂本（2011）の頁画像から書き起こしたもので、書き起こしの誤りがありうる。番号は校訂本の頁・行。</div>
</section>
<section>
<h2 class="chapter">目次</h2>
<p><a href="pvin_zenyaku_complete.html">▶ 全文を1ファイルで読む（第1–3章）</a><br>▶ 読み物スタイル（Hetubindu 対訳と同じ形式）：<a href="pvin_taiyaku_1.html">第1章</a>／<a href="pvin_taiyaku_2.html">第2章</a>／<a href="pvin_taiyaku_3.html">第3章</a></p>
<div class="tbl-wrap"><table>
<tr><th>ファイル</th><th>収める論題</th></tr>
{"".join(rows)}
</table></div>
</section>
<footer>ダルマキールティ『プラマーナ・ヴィニシュチャヤ』第1–3章 全訳</footer>
</body>
</html>
'''
    (ROOT / 'pvin_index.html').write_text(page, encoding='utf-8')
    print('wrote pvin_index.html')


if __name__ == '__main__':
    main()
