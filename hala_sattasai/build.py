#!/usr/bin/env python3
"""ハーラ『サッタサイー』対訳HTMLの生成スクリプト。

data/sN_*.txt（N = 百頌番号）を読み、../hala_sattasai_N.html を出力する。
データ形式（空行で偈を区切る）:
  # 6                     偈番号（パトワルダン版）
  w: 7                    ヴェーバー版番号
  poet: मयरंदसेहरस्स | マカランダシェーカラ
  pk: プラークリット1行（2行）
  ch: チャーヤー1行（2行）
  ja: 和訳
  n: 見出し | 解説本文（**太字** 可）
  q: 引用（デーヴァナーガリー） || 引用の和訳
  appendix: 見出し | 副題    （以降の偈を付録として扱う）
"""
import glob, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SATAKA = {
    1: ('पढमं सयं', '第一百頌'), 2: ('बीयं सयं', '第二百頌'),
    3: ('तइयं सयं', '第三百頌'), 4: ('चउत्थं सयं', '第四百頌'),
    5: ('पंचमं सयं', '第五百頌'), 6: ('छट्ठं सयं', '第六百頌'),
    7: ('सत्तमं सयं', '第七百頌'),
}
DEVA = re.compile(r'([ऀ-ॿ][ऀ-ॿ\s\-–—()\[\]\'’.,;:?!ऽ०-९]*[ऀ-ॿ)\]])|([ऀ-ॿ])')


def dev_num(n):
    return ''.join('०१२३४५६७८९'[int(c)] for c in str(n))


def inline(s):
    """エスケープ後、**太字**とデーヴァナーガリーの書体指定を付ける。"""
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return DEVA.sub(lambda m: '<span class="skt">%s</span>' % m.group(0), s)


def parse(path):
    verses, cur, appendix = [], None, None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not line.strip():
            continue
        if line.startswith('appendix:'):
            t, _, sub = line[9:].partition('|')
            appendix = (t.strip(), sub.strip())
            continue
        if line.startswith('# '):
            cur = {'num': line[2:].strip(), 'w': '', 'poet': None, 'pk': [], 'ch': [],
                   'ja': [], 'notes': [], 'appendix': appendix}
            appendix = None
            verses.append(cur)
            continue
        key, _, val = line.partition(':')
        val = val.strip()
        if key == 'w':
            cur['w'] = val
        elif key == 'poet':
            cur['poet'] = [x.strip() for x in val.split('|')]
        elif key in ('pk', 'ch', 'ja'):
            cur[key].append(val)
        elif key == 'n':
            tag, _, body = val.partition('|')
            cur['notes'].append(('n', tag.strip(), body.strip()))
        elif key == 'q':
            src, _, tr = val.partition('||')
            cur['notes'].append(('q', src.strip(), tr.strip()))
        else:
            raise ValueError('%s: 不明な行: %s' % (path, line))
    return verses


def render_verse(v, sataka):
    num = v['num']
    is_app = num.startswith('A')
    vid = ('a%s' % num[1:]) if is_app else 'g%s' % num
    label = ('付録 %s' % num[1:]) if is_app else 'GĀTHĀ %s' % num
    if v['w']:
        label += ' · W %s' % v['w']
    poet = ''
    if v['poet']:
        skt, jp = (v['poet'] + [''])[:2]
        poet = '<span class="poet">作者：%s（<span class="skt">%s</span>）</span>' % (html.escape(jp), html.escape(skt))
    pk = '\n'.join('        <span class="pada">%s</span>' % html.escape(x) for x in v['pk'])
    ch = '\n'.join('        <span class="pada">%s</span>' % html.escape(x) for x in v['ch'])
    ja = '\n'.join('      <p>%s</p>' % inline(x) for x in v['ja'])
    notes = []
    for kind, a, b in v['notes']:
        if kind == 'n':
            tag = '<span class="tag">%s</span>' % inline(a) if a else ''
            notes.append('    <p>%s%s</p>' % (tag, inline(b)))
        else:
            tr = '<br>「%s」' % inline(b) if b else ''
            notes.append('    <p class="quote"><span class="skt">%s</span>%s</p>' % (html.escape(a), tr))
    out = []
    if v['appendix']:
        t, sub = v['appendix']
        out.append('<h2 class="appendix-head" id="appendix">%s<span class="sub">%s</span></h2>' % (inline(t), inline(sub)))
    chaya = ''
    if ch:
        chaya = '''
      <div class="verse-chaya">
        <span class="lang-label">Chāyā</span>
%s
      </div>''' % ch
    comm = ''
    if notes:
        comm = '''
  <div class="commentary">
    <div class="commentary-title">解説 · Bhuvanapāla</div>
%s
  </div>''' % '\n'.join(notes)
    out.append('''<div class="verse-block" id="%s">
  <div class="verse-number">%s%s</div>
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
</div>''' % (vid, label, poet, pk, chaya, ja, comm))
    return '\n'.join(out)


INTRO_FULL = '''<section class="intro">
  <h2>こ の 対 訳 の 読 み 方</h2>
  <p>各偈は<strong>左にプラークリット原文</strong>（マハーラーシュトリー語）、その下に<strong>チャーヤー</strong>（<span class="skt">छाया</span>「影」＝原文を一語ずつサンスクリットに置き換えたもの）、<strong>右に和訳</strong>を置き、下の枠にブヴァナパーラ注に基づく<strong>解説</strong>を付けました。</p>
  <p>ブヴァナパーラはジャイナ教徒の注釈者で（注の冒頭が <span class="skt">ओं नमो जिनाय</span>「ジナに帰命す」）、注釈名『チェーコークティ・ヴィチャーラ・リーラー』は「洒落た言葉（<span class="skt">छेकोक्ति</span>）を吟味する遊び」の意です。各偈に作者名を付し、使われている修辞（<span class="skt">अलंकार</span>）の名を挙げ、表向きの意味の裏にある「隠れた意図」を読み解くのが特徴です。</p>
  <ul>
    <li>偈番号はパトワルダン版、「W」はヴェーバー版（1881）の番号です。</li>
    <li>チャーヤーは原則として注釈中の <span class="skt">[ ]</span> 内の文を採りました。原本はOCRテキストのため、明らかな誤読は修正しています。</li>
    <li>和訳・解説は試訳です。とくに「推定」「要確認」とした箇所は刊本で確認してください。</li>
  </ul>
</section>'''

INTRO_SHORT = '''<section class="intro">
  <p>左：プラークリット原文とチャーヤー（サンスクリット訳）／右：和訳／下：ブヴァナパーラ注に基づく解説。偈番号はパトワルダン版、「W」はヴェーバー版の番号。読み方の詳しい説明は<a href="hala_sattasai_1.html">第一百頌</a>の冒頭を参照。和訳・解説は試訳です。</p>
</section>'''


def build(sataka):
    files = sorted(glob.glob(os.path.join(HERE, 'data', 's%d_*.txt' % sataka)))
    if not files:
        return None
    verses = [v for f in files for v in parse(f)]
    skt, jp = SATAKA[sataka]
    nav = []
    for k, (_, j) in SATAKA.items():
        if k == sataka:
            nav.append('<span class="current">%s</span>' % j)
        elif glob.glob(os.path.join(HERE, 'data', 's%d_*.txt' % k)):
            nav.append('<a href="hala_sattasai_%d.html">%s</a>' % (k, j))
        else:
            nav.append('<span>%s</span>' % j)
    main = [v for v in verses if not v['num'].startswith('A')]
    first, last = main[0]['num'], main[-1]['num']
    toc = ' '.join('<a href="#g%s">%s</a>' % (v['num'], v['num']) for v in main)
    if any(v['num'].startswith('A') for v in verses):
        toc += ' <a href="#appendix">付録</a>'
    body = '\n<hr class="verse-sep">\n\n'.join(render_verse(v, sataka) for v in verses)
    css = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
    page = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>サッタサイー対訳 %(jp)s</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Devanagari:wght@400;600&family=Shippori+Mincho:wght@400;600&display=swap">
<style>%(css)s</style>
</head>
<body>

<div class="header">
  <div class="header-devanagari">गाहाकोसो · %(skt)s</div>
  <h1>Hāla's Gāhākosa (Sattasaī)</h1>
  <div class="header-sub">with the commentary <span>Chekoktivicāralīlā</span> of Bhuvanapāla · ed. M. V. Patwardhan (1980)</div>
  <div class="header-jp">ハーラ編『ガーハーコーサ（サッタサイー／七百頌）』%(jp)s<br>ブヴァナパーラ注に基づく対訳　—　第%(first)s〜%(last)s偈</div>
</div>

<nav class="nav-sataka">%(nav)s</nav>

%(intro)s

<nav class="intro"><h2>偈 番 号</h2><div class="toc-grid">%(toc)s</div></nav>

%(body)s

<nav class="nav-sataka" style="margin-top:3rem">%(nav)s</nav>

<div class="colophon">
  底本：M. V. Patwardhan (ed.), <em>Hāla's Gāhākosa (Gāthāsaptaśatī) with the Sanskrit Commentary of Bhuvanapāla</em>, Part I, Prakrit Text Series 21, Ahmedabad 1980（jainelibrary.org 所収OCRテキスト）。<br>
  和訳・解説は試訳です。
</div>

</body>
</html>
''' % dict(jp=jp, skt=skt, css=css, nav=' · '.join(nav), first=first, last=last,
           intro=INTRO_FULL if sataka == 1 else INTRO_SHORT, toc=toc, body=body)
    out = os.path.join(ROOT, 'hala_sattasai_%d.html' % sataka)
    open(out, 'w', encoding='utf-8').write(page)
    return out, len(verses)


if __name__ == '__main__':
    for k in SATAKA:
        r = build(k)
        if r:
            print('%s: %d 偈' % r)
