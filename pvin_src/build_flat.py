#!/usr/bin/env python3
"""PVin 全訳を、Hetubindu 対訳と同じ 1 カラムの読み物スタイル（アコーディオンなし）で出力する。

入力はアコーディオン版と同じ pvin_src/partXX.txt。出力は章ごとに pvin_taiyaku_1.html（第1章）と pvin_taiyaku_2.html（第2章）・pvin_taiyaku_3.html（第3章）。
  # 見出し     → 節（§番号つきの大見出し）
  ## / ###     → 小見出し
  G 要旨       → 節の冒頭の導入文
  L / V        → 原文ブロック（V は偈）
  N ノート     → 直前の原文ブロックの「解説」欄。原文ブロックの直後でなければ囲み
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import kh  # noqa: E402

ROOT = build.ROOT
CSS = (ROOT / 'pvin_src' / 'flat_style.css.part').read_text(encoding='utf-8')
# (章番号, 章名, サンスクリット名, part, 導入文, 「まず30秒で」の内容)
CHAPTERS = [
    (1, '直接知覚', 'pratyakṣapariccheda', ['01a', '01b', '01c'],
     '正しい認識（認識手段）は<strong>直接知覚と推論の二つだけ</strong>である。第1章では、そのうち直接知覚を「<strong>分別を離れ、錯誤のない</strong>」知と定義し、感官の知に言葉が入りこまないことを論証したうえで、意による知覚・自己認識・ヨーガ行者の知覚、そして認識手段と結果の関係、唯識の立場へと進みます。',
     '分別を離れた知、意による知覚、自己認識、ヨーガ行者の知覚、手段と結果、唯識'),
    (2, '自分のための推論', 'svārthānumānapariccheda', ['02a', '02b', '02c'],
     '第2章では、<strong>三相をそなえた徴表</strong>による推論を論じます。推論は錯誤でありながら正しい認識であること、徴表は<strong>自性・結果・非認識</strong>の三種だけであること、そして自性因の例として刹那滅を、結果因の例として煙と火を詳しく検討します。',
     '三相、三種の徴表、非認識、聖典批判、刹那滅論証、結果因'),
    (3, '他人のための推論', 'parārthānumānapariccheda', ['03a', '03b', '03c', '03d', '03e', '03f', '03g', '03h'],
     '第3章では、<strong>言葉によって他人に理解させる推論</strong>を論じます。ディグナーガの定義「自分が見た対象を明らかにすること」の解説から始まり、<strong>主張（宗）</strong>の条件、<strong>理由（因）</strong>の分類（九句因）、<strong>似因</strong>（誤った理由）、<strong>喩例</strong>、そして<strong>論破</strong>へと、討論の作法を順に検討します。',
     '他人のための推論の定義、主張の条件、九句因と三種の正しい理由、似因、喩例、論破'),
]

TEXTINFO = {
    1: {'src': 'Steinkellner 校訂本（2007）<br><small>E. Steinkellner, <i>Dharmakīrti\'s Pramāṇaviniścaya, Chapters 1 and 2. Critically edited.</i> (Sanskrit Texts from the Tibetan Autonomous Region 2) Beijing–Vienna 2007。Steinkellner の訂正表（2008・2013・2018）を反映した</small>',
        'num': '',
        'col': '',
        'foot': '原典：E. Steinkellner, <i>Dharmakīrti\'s Pramāṇaviniścaya, Chapters 1 and 2. Critically edited.</i> (Sanskrit Texts from the Tibetan Autonomous Region 2) Beijing–Vienna 2007。訂正表：E. Steinkellner, „Miszellen zur erkenntnistheoretisch-logischen Schule des Buddhismus X: Corrigenda 2 et addenda to Dharmakīrti\'s Pramāṇaviniścaya. Chapters 1 and 2.“ <i>WZKS</i> 51 (2007–2008), 207–208；E. Steinkellner, „Corrigenda 3 et addenda to Dharmakīrti\'s Pramāṇaviniścaya. Chapters 1 and 2. Critically edited by Ernst Steinkellner. Beijing–Vienna 2007“ (2.1.2013, online)；E. Steinkellner, <i>Dharmakīrti\'s Pramāṇaviniścaya, Chapters 1 and 2. Critically edited 2007 (STTAR 2): Further and Last Corrigenda and Addenda</i> (November 2018) を本文に反映した。',
        'ed': 'Steinkellner 2007'},
    3: {'src': 'Hugon &amp; Tomabechi 校訂本（2011）<br><small>校訂本の頁画像から書き起こした。偈番号・節番号は校訂本に従う。写本の異読や記号は省いた</small>',
        'num': '各ブロック左上の <span class="ia">p.12,3</span> は校訂本の頁・行（そのブロックの始まり）。節見出しの <span class="pg">pp.1–10</span> はその節の頁範囲',
        'col': '頁',
        'foot': '原文は P. Hugon &amp; T. Tomabechi, <i>Dharmakīrti\'s Pramāṇaviniścaya, Chapter 3</i> (Beijing–Vienna 2011) の本文を頁画像から書き起こしたもの。書き起こしの誤りがありうるので、必ず校訂本で確認されたい。節の区分と見出しは同書の Analysis（pp.139–162）による。',
        'ed': 'Hugon &amp; Tomabechi 2011'},
}


def ref_label(ref):
    """'14:1-4' → '14.1–4'、'18-19' → '18–19'。第3章は校訂本の頁・行（'p.12,3'）。"""
    loc = build.loc(ref)
    if loc:
        return 'p.' + loc
    return ref.replace(':', '.').replace('-', '–')


def renum(num, sec_no):
    """part ファイル内の科段番号 '3.1.2' の先頭を通し節番号に置き換える。第3章（I.2.1 など校訂本の番号）はそのまま。"""
    if re.match(r'[IVX]+(\.|$)', num):
        return num
    return '.'.join([str(sec_no)] + num.split('.')[1:])


def parse(pid):
    """part ファイルを [(kind, data)] の列にする。"""
    items = []
    cur = None
    build.set_text()
    for raw in (ROOT / 'pvin_src' / f'part{pid}.txt').read_text(encoding='utf-8').split('\n'):
        line = raw.rstrip()
        if line.startswith('='):
            if line.startswith('=src '):
                build.set_text(line[5:].strip())
            continue
        m = re.match(r'^(#+)\s+(\S+)\s*\|\s*([^|]*?)\s*(?:\|\s*(.*))?$', line)
        if m:
            cur = None
            items.append(('H', {'lv': len(m.group(1)), 'num': m.group(2), 'ttl': m.group(3),
                                'sk': (m.group(4) or '').strip()}))
            continue
        m = re.match(r'^([LV])\s+(\S+)\s*$', line)
        if m:
            cur = {'ref': m.group(2), 'ja': []}
            items.append((m.group(1), cur))
            continue
        m = re.match(r'^([JNGSR])\s?(.*)$', line)
        if m and (cur is None or m.group(1) != 'J' or 'ref' in cur):
            if m.group(1) in 'NGSR':
                cur = {'ja': [m.group(2)]}
                items.append((m.group(1), cur))
            else:
                cur['ja'].append(m.group(2))
            continue
        if cur is not None:
            cur['ja'].append(line)
    return items


def mula(kind, d, uid, notes):
    lines = build.src(d['ref'])
    if kind == 'V':
        src = build.render_verse(lines, kh.dev)
        ia = ''
        cls = 'mula sutra'
    else:
        src = build.render_sa(lines)
        ia = ''
        cls = 'mula'
    exp = ''
    nn = [build.ja(t) for k, t in notes if k == 'N']
    if notes:
        exp = '<div class="exp">'
        if nn:
            exp += '<span class="lbl">解説</span>' + ''.join(nn)
        first = not nn
        for sk in build.SCHOLARS:
            ss = [build.ja(t) for k, t in notes if k == sk]
            if ss:
                exp += ('<div class="stk first">' if first else '<div class="stk">') + \
                       f'<span class="lbl">{build.SCHOLARS[sk]}</span>' + ''.join(ss) + '</div>'
                first = False
        exp += '</div>'
    ref = f'<span class="ref">{ref_label(d["ref"])}</span>' if build.loc(d['ref']) else ''   # 第1・2章は番号を出さない
    return (f'<div class="{cls}" id="{uid}">\n  {ref}\n'
            f'  <div class="src deva" lang="sa">{src}</div>{ia}\n'
            f'  <div class="tr">{build.ja(d["ja"])}</div>{exp}\n</div>')


def build_chapter(chno, name, sk_name, parts, lead, facts):
    nav = []
    maprows = []
    body = []
    sec_no = 0
    for pid in parts:
        items = parse(pid)
        i = 0
        open_sec = False
        while i < len(items):
            kind, d = items[i]
            if kind == 'H' and d['lv'] == 1:
                if open_sec:
                    body.append('</section>')
                sec_no += 1
                sid = f's{sec_no}'
                # 節の範囲（本文の行）
                refs = []
                j = i + 1
                while j < len(items) and not (items[j][0] == 'H' and items[j][1]['lv'] == 1):
                    if items[j][0] in 'LV':
                        refs.append(int(re.match(r'\d+', items[j][1]['ref']).group()))
                    j += 1
                rng = ''
                if refs and build.LOC[min(refs) - 1]:          # 第3章は校訂本の頁で示す
                    p0, p1 = (build.LOC[x - 1].split(',')[0] for x in (min(refs), max(refs)))
                    rng = f'pp.{p0}–{p1}' if p0 != p1 else f'p.{p0}'
                gist = ''
                if i + 1 < len(items) and items[i + 1][0] == 'G':
                    gist = ' '.join(x.strip() for x in items[i + 1][1]['ja'])
                    i += 1
                short = d['ttl'] if len(d['ttl']) <= 12 else d['ttl'][:11] + '…'
                nav.append(f'<li><a href="#{sid}"><b>{sec_no}</b>{html.escape(short)}</a></li>')
                maprows.append(f'<tr><td class="num">§{sec_no}</td><td class="k"><a href="#{sid}">{html.escape(d["ttl"])}</a>'
                               f'<span class="sm"><i>{html.escape(d["sk"])}</i></span></td>' + (f'<td class="num">{rng}</td>' if rng else '') + '</tr>')
                body.append(f'<section id="{sid}" class="wrap">\n  <div class="sec-head"><span class="sec-no">{sec_no}</span>'
                            f'<h2>{html.escape(d["ttl"])}</h2><span class="sub">'
                            + (f'<span class="pg">{rng}</span>' if rng else '')
                            + f'<i>{html.escape(d["sk"])}</i></span></div>')
                if gist:
                    body.append(f'<p>{gist}</p>')
                open_sec = True
            elif kind == 'H':
                tag = 'h3' if d['lv'] == 2 else 'h4'
                sk = f' <span class="sk"><i>{html.escape(d["sk"])}</i></span>' if d['sk'] else ''
                body.append(f'<{tag} class="sub-h"><span class="snum">{renum(d["num"], sec_no)}</span>{html.escape(d["ttl"])}{sk}</{tag}>')
            elif kind in 'LV':
                notes = []
                while i + 1 < len(items) and items[i + 1][0] in 'NSR':
                    notes.append((items[i + 1][0], items[i + 1][1]['ja']))
                    i += 1
                body.append(mula(kind, d, f'u{pid}-{i}', notes))
            elif kind == 'N':
                body.append(f'<div class="point"><span class="lbl">ノート</span>{build.ja(d["ja"])}</div>')
            elif kind in build.SCHOLARS:
                body.append(f'<div class="point stk-pt"><span class="lbl">{build.SCHOLARS[kind]}</span>{build.ja(d["ja"])}</div>')
            elif kind == 'G':
                body.append(f'<p>{" ".join(x.strip() for x in d["ja"])}</p>')
            i += 1
        if open_sec:
            body.append('</section>')

    others = [c for c in CHAPTERS if c[0] != chno]
    other_link = '・'.join(f'<a href="pvin_taiyaku_{c[0]}.html">第{c[0]}章「{c[1]}」</a>' for c in others)
    if any(c[0] == chno - 1 for c in CHAPTERS):
        nav.insert(0, f'<li><a href="pvin_taiyaku_{chno - 1}.html" class="chp">← 第{chno - 1}章へ</a></li>')
    if any(c[0] == chno + 1 for c in CHAPTERS):
        nav.append(f'<li><a href="pvin_taiyaku_{chno + 1}.html" class="chp">第{chno + 1}章へ →</a></li>')
    tx = TEXTINFO[3 if chno == 3 else 1]
    stk_fact = stk_howto = ''
    if chno == 1:
        stk_fact = ('<div><dt>研究</dt><dd>T. Vetter のドイツ語訳（1966）<br><small><i>Dharmakīrti\'s Pramāṇaviniścayaḥ, 1. Kapitel: Pratyakṣam</i>。'
                    'チベット訳の校訂・サンスクリット断片・独訳と、章全体の思想的位置づけを論じた序論をもつ。序論の議論分析と訳注の要点を、各ブロックの「Vetter の解釈」欄に加えた</small></dd></div>')
        stk_howto = ('<div><b>Vetter の解釈</b>解説欄の下段（解説がない箇所では単独）。（注12）は Vetter 1966 の訳注番号、「序論」はその序論（7–28頁）。'
                     '彼の読みに合わせて訳を改めた箇所はそう明記した</div>')
    if chno == 2:
        stk_fact = ('<div><dt>研究</dt><dd>E. Steinkellner のドイツ語訳注（1979）<br><small><i>Dharmakīrti\'s Pramāṇaviniścayaḥ, Zweites Kapitel: Svārthānumānam, Teil II: Übersetzung und Anmerkungen</i>。'
                    'チベット訳からの全訳と詳しい注。典拠や反論者の特定、ダルマキールティが旧作を書き換えた箇所の指摘などを、各ブロックの「Steinkellner の解釈」欄に加えた</small></dd></div>')
        stk_howto = ('<div><b>Steinkellner の解釈</b>解説欄の下段（解説がない箇所では単独）。（注10）は Steinkellner 1979 の注番号、「チベット訳5,1」などはその校訂本（1973）の頁・行。'
                     '彼の読みに合わせて訳を改めた箇所はそう明記した</div>')
    page = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Pramāṇaviniścaya 対訳 第{chno}章</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@600;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400&family=Noto+Serif+Devanagari:wght@400;600&display=swap">
{CSS}
<style>
.mula.sutra .src.ia.vi,.mula .src.ia.vi{{font-weight:400;font-style:italic;font-size:.98rem;color:var(--muted);line-height:1.7;margin-top:4px;overflow-wrap:anywhere}}
.kno{{font-family:var(--f-ia);font-size:.72rem;font-style:normal;font-weight:700;color:var(--gold);background:var(--gold-soft);border-radius:4px;padding:0 6px;margin:0 4px;white-space:nowrap}}
.mula .tr p,.mula .exp p{{margin:0 0 .6em}}
.mula .tr p:last-child{{margin-bottom:0}}
.sub-h{{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px}}
h4.sub-h{{font-family:var(--f-display);font-size:1.02rem;font-weight:800;margin:1.8em 0 .4em;color:var(--ink)}}
.sub-h .snum{{font-family:var(--f-ia);font-size:.85rem;font-weight:700;color:var(--accent)}}
.sub-h .sk{{font-family:var(--f-ia);font-size:.85rem;font-weight:400;color:var(--muted)}}
.chapter-band{{text-align:center;padding-block:64px 24px}}
.chapter-band .ch-title{{font-size:clamp(1.9rem,6vw,2.6rem);margin-top:.2em}}
.mula .exp .stk.first{{margin-top:0;padding-top:0;border-top:0}}
.point.stk-pt .lbl{{color:var(--accent)}}
nav.toc a.chp{{background:var(--accent);color:var(--card);border-color:var(--accent);font-weight:700}}
</style>
</head>
<body>
<nav class="toc" aria-label="目次">
  <ol>
    <li><a href="#intro">入口</a></li>
    <li><a href="#map">全体の地図</a></li>
    {"".join(nav)}
  </ol>
</nav>

<header class="hero wrap">
  <div class="eyebrow">インド仏教論理学を読む</div>
  <h1>Pramāṇaviniścaya</h1>
  <p class="deva-title" lang="sa">प्रमाणविनिश्चयः</p>
  <p class="sub">Dharmakīrti『量決択』第{chno}章「{name}」（<i>{sk_name}</i>）を、原文・和訳・解説でテキスト順に読む</p>
  <span class="sample">対訳　第{chno}章「{name}」全文</span>
  <p>{lead}</p>
  <p>このページでは、デーヴァナーガリーの原文と和訳を対照させ、必要な箇所に解説を添えました。{other_link}は別のページにあります。</p>
</header>

<main>
<section id="intro" class="first wrap">
  <div class="sec-head"><h2 style="grid-column:1/-1">まず30秒で</h2></div>
  <dl class="facts">
    <div><dt>著者</dt><dd>Dharmakīrti（法称）<br><small>7世紀頃の仏教論理学者。<i>Pramāṇavārttika</i>、<i>Nyāyabindu</i>、<i>Hetubindu</i> などの著者</small></dd></div>
    <div><dt>書名</dt><dd><i>Pramāṇaviniścaya</i>「認識手段の決択」<br><small>主著 <i>Pramāṇavārttika</i> の内容を、偈と散文で整理し直した書。全3章</small></dd></div>
    <div><dt>この章</dt><dd>第{chno}章　{name}<br><small>{facts}</small></dd></div>
    {stk_fact}
    <div><dt>本文</dt><dd>{tx['src']}</dd></div>
  </dl>

  <h3>このページの読み方</h3>
  <div class="howto">
    {f"<div><b>番号</b>{tx['num']}</div>" if tx['num'] else ''}
    <div><b>原文</b>デーヴァナーガリー。偈は金色の線のブロック。<span class="kno">k.4</span> は偈の番号</div>
    <div><b>和訳</b>（　）は訳者の補い。（反論）（答え）は議論の話者の区別</div>
    <div><b>解説</b>ブロック下の灰色の欄。用語や論点の説明</div>
    {stk_howto}
  </div>
</section>

<section id="map" class="wrap">
  <div class="sec-head"><h2 style="grid-column:1/-1">全体の地図</h2><span class="sub">第{chno}章をテキストの順に{sec_no}節に分けた</span></div>
  <div class="tbl">
    <table>
      <thead><tr><th>節</th><th>見出し</th>{f"<th>{tx['col']}</th>" if tx['col'] else ''}</tr></thead>
      <tbody>
{chr(10).join(maprows)}
      </tbody>
    </table>
  </div>
</section>

{chr(10).join(body)}

<footer class="wrap">
  <p><strong>テキストについて</strong>　{tx['foot']}</p>
  <p>和訳は試訳であり、正確な読みは校訂本（{tx['ed']}）で確認されたい。同じ訳文の科段（アコーディオン）版は <a href="pvin_index.html">pvin_index.html</a> から読める。{other_link}へ。</p>
</footer>
</main>
</body>
</html>
'''
    fname = f'pvin_taiyaku_{chno}.html'
    (ROOT / fname).write_text(page, encoding='utf-8')
    print('wrote', fname, len(page), 'sections:', sec_no)


if __name__ == '__main__':
    for c in CHAPTERS:
        if all((ROOT / 'pvin_src' / f'part{pid}.txt').exists() for pid in c[3]):
            build_chapter(*c)
