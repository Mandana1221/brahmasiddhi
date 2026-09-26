#!/usr/bin/env python3
"""ウッディヨータナ『クヴァラヤマーラー』対訳HTMLの生成スクリプト。

体裁はハーラ『サッタサイー』対訳（hala_sattasai/）にならう。
data/p*.txt を読み、../kuvalayamala_1.html を出力する。
データ形式（空行で偈・段落を区切る）:
  section: 1 | 見出し      ウパーディエー版の節番号（§）と見出し
  # 1                     偈番号（節内の通し番号）
  loc: p. 1, l. 2         刊本の頁・行
  pk: プラークリット1行（2行）
  ch: チャーヤー1行（2行）
  ja: 和訳
  n: 見出し | 解説本文（**太字** 可）
"""
import glob, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEVA = re.compile(r'([ऀ-ॿ][ऀ-ॿ\s\-–—()\[\]\'’.,;:?!ऽ०-९]*[ऀ-ॿ)\]])|([ऀ-ॿ])')


def inline(s):
    """エスケープ後、**太字**とデーヴァナーガリーの書体指定を付ける。"""
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return DEVA.sub(lambda m: '<span class="skt">%s</span>' % m.group(0), s)


def parse(path):
    items, cur = [], None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not line.strip():
            continue
        if line.startswith('section:'):
            num, _, title = line[8:].partition('|')
            items.append({'section': (num.strip(), title.strip())})
            continue
        if line.startswith('# '):
            cur = {'num': line[2:].strip(), 'loc': '', 'pk': [], 'ch': [], 'ja': [], 'notes': []}
            items.append(cur)
            continue
        key, _, val = line.partition(':')
        val = val.strip()
        if key == 'loc':
            cur['loc'] = val
        elif key in ('pk', 'ch', 'ja'):
            cur[key].append(val)
        elif key == 'n':
            tag, _, body = val.partition('|')
            cur['notes'].append((tag.strip(), body.strip()))
        else:
            raise ValueError('%s: 不明な行: %s' % (path, line))
    return items


def render_section(num, title):
    return '<h2 class="appendix-head" id="s%s">§ %s<span class="sub">%s</span></h2>' % (
        num, num, inline(title))


def render_verse(v, sec):
    vid = 's%s-%s' % (sec, v['num'])
    label = '§ %s · GĀTHĀ %s' % (sec, v['num']) if v['num'] != '0' else '§ %s · INVOCATION' % sec
    if v['loc']:
        label += ' · %s' % v['loc']
    pk = '\n'.join('        <span class="pada">%s</span>' % html.escape(x) for x in v['pk'])
    ch = '\n'.join('        <span class="pada">%s</span>' % html.escape(x) for x in v['ch'])
    ja = '\n'.join('      <p>%s</p>' % inline(x) for x in v['ja'])
    notes = '\n'.join('    <p>%s%s</p>' % ('<span class="tag">%s</span>' % inline(t) if t else '', inline(b))
                      for t, b in v['notes'])
    chaya = '''
      <div class="verse-chaya">
        <span class="lang-label">Chāyā</span>
%s
      </div>''' % ch if ch else ''
    comm = '''
  <div class="commentary">
    <div class="commentary-title">解説</div>
%s
  </div>''' % notes if notes else ''
    return '''<div class="verse-block" id="%s">
  <div class="verse-number">%s</div>
  <div class="verse-columns">
    <div>
      <span class="lang-label">Prakrit</span>
      <div class="verse-prakrit">
%s
      </div>%s
    </div>
    <div class="verse-divider"></div>
    <div class="verse-japanese">
      <span class="lang-label">和訳</span>
%s
    </div>
  </div>%s
</div>''' % (vid, label, pk, chaya, ja, comm)


INTRO = '''<section class="intro">
  <h2>こ の 対 訳 の 読 み 方</h2>
  <p>『クヴァラヤマーラー』（<span class="skt">कुवलयमाला</span>「青蓮の花環」）は、ジャイナ教の僧<strong>ウッディヨータナスーリ</strong>（<span class="skt">उज्जोयणसूरि</span>）が、奥書によれば779年に完成させたプラークリットの長編物語です。散文と韻文を交えた「チャンプー」の形式で書かれています。</p>
  <p>各偈は<strong>左にプラークリット原文</strong>（マハーラーシュトリー語）、その下に<strong>チャーヤー</strong>（<span class="skt">छाया</span>「影」＝原文を一語ずつサンスクリットに置き換えたもの）、<strong>右に和訳</strong>を置き、下の枠に<strong>解説</strong>を付けました。</p>
  <ul>
    <li>「§」はウパーディエー版の節番号、「p. / l.」は同版の頁と行です。</li>
    <li>刊本にはチャーヤーがないため、<strong>チャーヤーは訳者の試案</strong>です。</li>
    <li>原本はOCRテキストです。明らかな誤読は韻律と脚注の異読（J＝ジャイサルメール写本、P＝プーナ写本）に基づいて直し、各偈の「本文」の項に記しました。</li>
    <li>和訳・解説は試訳です。とくに「推定」「自信がない」とした箇所は、刊本で確認してください。</li>
  </ul>
</section>'''


def build():
    items = [it for f in sorted(glob.glob(os.path.join(HERE, 'data', 'p*.txt'))) for it in parse(f)]
    body, toc, sec = [], [], None
    for it in items:
        if 'section' in it:
            sec = it['section'][0]
            body.append(render_section(*it['section']))
            continue
        if body and not body[-1].startswith('<h2'):
            body.append('<hr class="verse-sep">')
        body.append(render_verse(it, sec))
        if it['num'] != '0':
            toc.append('<a href="#s%s-%s">§%s.%s</a>' % (sec, it['num'], sec, it['num']))
    css = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
    page = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>クヴァラヤマーラー対訳</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
<style>%(css)s</style>
</head>
<body>

<div class="header">
  <div class="header-devanagari">उज्जोयणसूरिविरइया कुवलयमाला</div>
  <h1>Uddyotanasūri's Kuvalayamālā</h1>
  <div class="header-sub">a Campū in Prakrit · ed. A. N. Upadhye, Part I (1959)</div>
  <div class="header-jp">ウッディヨータナスーリ作『クヴァラヤマーラー』<br>プラークリット原文・チャーヤー・和訳・解説　—　見本（§1 冒頭）</div>
</div>

%(intro)s

<nav class="intro"><h2>偈 番 号</h2><div class="toc-grid">%(toc)s</div></nav>

%(body)s

<div class="colophon">
  底本：A. N. Upadhye (ed.), <em>Uddyotanasūri's Kuvalayamālā</em>, Part I, Singhi Jain Series 45, Bombay: Bharatiya Vidya Bhavan, 1959（jainelibrary.org 所収OCRテキスト, No. 002777）。<br>
  チャーヤー・和訳・解説は試訳です。
</div>

</body>
</html>
''' % dict(css=css, intro=INTRO, toc=' '.join(toc), body='\n\n'.join(body))
    out = os.path.join(ROOT, 'kuvalayamala_1.html')
    open(out, 'w', encoding='utf-8').write(page)
    return out, len(toc)


if __name__ == '__main__':
    print('%s: %d 偈' % build())
