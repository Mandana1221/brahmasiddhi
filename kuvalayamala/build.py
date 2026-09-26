#!/usr/bin/env python3
"""ウッディヨータナ『クヴァラヤマーラー』対訳HTMLの生成スクリプト。

体裁はハーラ『サッタサイー』対訳（hala_sattasai/）にならう。
data/NN_*.txt（NN = 巻番号）を読み、../kuvalayamala_N.html を出力する。
データ形式（空行でブロックを区切る）:
  volume: 巻の題 | 内容の要約    各巻の最初のファイルの先頭に置く
  part: 見出し | 副題            物語の区切りの見出し
  # 2.1                   ブロック番号（§2 の 1 番目のブロック）。§ はウパーディエー版の節番号
  loc: p. 1, l. 2         刊本の頁・行（任意）
  pk: プラークリット（散文は1行1段落、韻文は1行1パーダ組）
  ch: チャーヤー（同上）
  ja: 和訳（1行1段落）
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
        if line.startswith(('volume:', 'part:')):
            key, _, val = line.partition(':')
            t, _, sub = val.partition('|')
            items.append({key: (t.strip(), sub.strip())})
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


def label(num):
    sec, _, sub = num.partition('.')
    if sub == '0':
        return '§ %s · INVOCATION' % sec
    return '§ %s%s' % (sec, ' · %s' % sub if sub else '')


def render_block(v):
    vid = 's' + v['num'].replace('.', '-')
    lab = label(v['num']) + (' · %s' % v['loc'] if v['loc'] else '')
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
</div>''' % (vid, lab, pk, chaya, ja, comm)


INTRO_FULL = '''<section class="intro">
  <h2>こ の 対 訳 の 読 み 方</h2>
  <p>『クヴァラヤマーラー』（<span class="skt">कुवलयमाला</span>「青蓮の花環」）は、ジャイナ教の僧<strong>ウッディヨータナスーリ</strong>（<span class="skt">उज्जोयणसूरि</span>）が、奥書によれば779年に完成させたプラークリットの長編物語です。散文と韻文を交えた「チャンプー」の形式で書かれています。怒り・慢心・欺き・貪り・迷妄という五つの煩悩を体現した五人が、出家して天界に生まれ、生まれ変わりながら互いを目覚めさせていく物語です。</p>
  <p>各ブロックは<strong>左にプラークリット原文</strong>（マハーラーシュトリー語が中心）、その下に<strong>チャーヤー</strong>（<span class="skt">छाया</span>「影」＝原文を一語ずつサンスクリットに置き換えたもの）、<strong>右に和訳</strong>を置き、下の枠に<strong>解説</strong>を付けました。</p>
  <ul>
    <li>「§」はウパーディエー版の節番号です。一つの節が長い場合は「§ 2 · 1」「§ 2 · 2」のように分けています。</li>
    <li>刊本にはチャーヤーがないため、<strong>チャーヤーは訳者の試案</strong>です。</li>
    <li>原本はOCRテキストです。明らかな誤読は韻律・文脈と脚注の異読（J＝ジャイサルメール写本、P＝プーナ写本）に基づいて直し、主なものを解説の「本文」の項に記しました。</li>
    <li>和訳・解説は試訳です。とくに「推定」「自信がない」とした箇所は、刊本で確認してください。</li>
  </ul>
</section>'''

INTRO_SHORT = '''<section class="intro">
  <p>左：プラークリット原文とチャーヤー（訳者によるサンスクリット訳の試案）／右：和訳／下：解説。「§」はウパーディエー版の節番号。原文はOCRテキストを韻律・文脈・脚注の異読に基づいて直したものです。読み方の詳しい説明は<a href="kuvalayamala_1.html">第1巻</a>の冒頭を参照。和訳・解説は試訳です。</p>
</section>'''


def volumes():
    vols = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'data', '[0-9][0-9]_*.txt'))):
        vols.setdefault(int(os.path.basename(f)[:2]), []).append(f)
    return vols


def build(n, files, vols, titles):
    items = [it for f in files for it in parse(f)]
    title, summary = next(it['volume'] for it in items if 'volume' in it)
    body, toc, seen = [], [], set()
    for it in items:
        if 'volume' in it:
            continue
        if 'part' in it:
            t, sub = it['part']
            body.append('<h2 class="appendix-head">%s<span class="sub">%s</span></h2>' % (inline(t), inline(sub)))
            continue
        if body and not body[-1].startswith('<h2'):
            body.append('<hr class="verse-sep">')
        body.append(render_block(it))
        sec = it['num'].partition('.')[0]
        if sec not in seen:
            seen.add(sec)
            toc.append('<a href="#s%s">§%s</a>' % (it['num'].replace('.', '-'), sec))
    nav = ' · '.join('<span class="current">第%d巻</span>' % k if k == n else
                     '<a href="kuvalayamala_%d.html" title="%s">第%d巻</a>' % (k, html.escape(titles[k]), k)
                     for k in sorted(vols))
    secs = sorted(int(s) for s in seen)
    css = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
    page = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>クヴァラヤマーラー対訳 第%(n)d巻</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
<style>%(css)s</style>
</head>
<body>

<div class="header">
  <div class="header-devanagari">उज्जोयणसूरिविरइया कुवलयमाला</div>
  <h1>Uddyotanasūri's Kuvalayamālā</h1>
  <div class="header-sub">a Campū in Prakrit · ed. A. N. Upadhye, Part I (1959)</div>
  <div class="header-jp">ウッディヨータナスーリ作『クヴァラヤマーラー』　第%(n)d巻「%(title)s」<br>%(summary)s　—　§%(first)d〜§%(last)d</div>
</div>

<nav class="nav-sataka">%(nav)s</nav>

%(intro)s

<nav class="intro"><h2>節 番 号</h2><div class="toc-grid">%(toc)s</div></nav>

%(body)s

<nav class="nav-sataka" style="margin-top:3rem">%(nav)s</nav>

<div class="colophon">
  底本：A. N. Upadhye (ed.), <em>Uddyotanasūri's Kuvalayamālā</em>, Part I, Singhi Jain Series 45, Bombay: Bharatiya Vidya Bhavan, 1959（jainelibrary.org 所収OCRテキスト, No. 002777）。<br>
  チャーヤー・和訳・解説は試訳です。
</div>

</body>
</html>
''' % dict(n=n, title=html.escape(title), summary=inline(summary), css=css, nav=nav,
           intro=INTRO_FULL if n == 1 else INTRO_SHORT, toc=' '.join(toc),
           body='\n\n'.join(body), first=secs[0], last=secs[-1])
    out = os.path.join(ROOT, 'kuvalayamala_%d.html' % n)
    open(out, 'w', encoding='utf-8').write(page)
    return out, len(secs)


if __name__ == '__main__':
    vols = volumes()
    titles = {}
    for k, fs in vols.items():
        for line in open(fs[0], encoding='utf-8'):
            if line.startswith('volume:'):
                titles[k] = line[7:].partition('|')[0].strip()
                break
    for k, fs in sorted(vols.items()):
        print('%s: %d 節' % build(k, fs, vols, titles))
