#!/usr/bin/env python3
"""Build the bilingual HTML edition from kapitel_N.txt (Jena-1922-aligned format).

Source format (kapitel_N.txt):
  @chapter N | ROMAN | German title | Japanese title | first–last page
  @titlenote K                      (optional: footnote K belongs to the title)
  §k                                (section)
  German paragraph                  ({201} = Jena page break, [^3] = footnote 3)
  Japanese paragraph
  @fig German caption | Japanese caption
  ==Anmerkungen==  then  [^k] / German note / Japanese note
  ==Korrekturen==  then  DE | position | old | new   or   JP | position | text
"""
import re, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'html')
JP = re.compile(r'[぀-ヿ一-鿿]')
RJP = {1: 'Ⅰ', 2: 'Ⅱ', 3: 'Ⅲ', 4: 'Ⅳ', 5: 'Ⅴ', 6: 'Ⅵ', 7: 'Ⅶ', 8: 'Ⅷ', 9: 'Ⅸ', 10: 'Ⅹ',
       11: 'ⅩⅠ', 12: 'ⅩⅡ', 13: 'ⅩⅢ', 14: 'ⅩⅣ', 15: 'ⅩⅤ'}
EMPTY_DE = '〔—〕'


def esc(s):
    return html.escape(s, quote=False)


def parse(path):
    text = open(path, encoding='utf-8').read()
    body, _, rest = text.partition('==Anmerkungen==')
    anm, _, korr = rest.partition('==Korrekturen==')
    meta, items, notes, corr = {}, [], {}, {'de': [], 'jp': []}
    sec, pending = None, None
    for b in [x.strip() for x in re.split(r'\n\s*\n', body) if x.strip()]:
        if b.startswith('@chapter'):
            n, rom, de, jp, pages = [x.strip() for x in b.split('\n')[0][8:].split('|')]
            meta.update(num=int(n), rom=rom, de=de, jp=jp, pages=pages,
                        first=(int(re.match(r'\d+', pages).group()) if pages[:1].isdigit() else re.match(r'[IVXL]+', pages).group()))
            for l in b.split('\n')[1:]:
                if l.startswith('@titlenote'):
                    meta['titlenote'] = l.split()[1]
            continue
        if b.startswith('@titlenote'):
            meta['titlenote'] = b.split()[1]; continue
        if re.fullmatch(r'§\d+', b):
            sec = int(b[1:]); items.append(('sec', sec, '§ %d' % sec)); continue
        if b.startswith('@sec '):
            sid, _, lab = b[5:].partition('|')
            sec = sid.strip(); items.append(('sec', sec, lab.strip())); continue
        if b.startswith('@fig'):
            de, jp = [x.strip() for x in b[4:].split('|')]
            items.append(('fig', de, jp)); continue
        if b == EMPTY_DE:
            pending = ''; continue
        if JP.search(b) or b == '〔未訳〕':
            items.append(('pair', sec, pending, b)); pending = None
        else:
            pending = b
    for m in re.finditer(r'\[\^(\d+)\]\n(.+?)\n(.+?)(?=\n\s*\n|\Z)', anm, re.S):
        notes[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    for l in korr.split('\n'):
        p = [x.strip() for x in l.split('|')]
        if p[0] == 'DE' and len(p) == 4:
            corr['de'].append(p[1:])
        elif p[0] == 'JP' and len(p) == 3:
            corr['jp'].append(p[1:])
    return meta, items, notes, corr


def inline(s):
    if s in ('', EMPTY_DE, '〔未訳〕'):
        return '<span class="missing">%s</span>' % (s or EMPTY_DE)
    s = esc(s)
    s = re.sub(r'\{(\d+|[IVXL]+)\}', r'<span class="pb" title="Jena 1922, S. \1">\1</span>', s)
    s = re.sub(r'\[\^(\d+)\]', r'<a class="fr" href="#n\1">\1</a>', s)
    return s


def note_html(ids, notes):
    rows = []
    for i in ids:
        de, jp = notes.get(i, ('', '〔注なし〕'))
        rows.append('<li id="n%s"><span class="nn">%s</span><p class="de" lang="de">%s</p>'
                    '<p class="jp" lang="ja">%s</p></li>' % (i, i, esc(de), esc(jp)))
    return '<ol class="notes">' + ''.join(rows) + '</ol>' if rows else ''


def fname(n):
    return {0: 'vorwort.html', 16: 'zusaetze.html'}.get(n, 'kapitel_%02d.html' % n)


def label(n):
    return {0: '序文', 16: '補遺'}.get(n, '第%s章' % RJP.get(n, ''))


def kicker(meta):
    n = meta['num']
    if n == 0: return 'VORWORTE · 序文'
    if n == 16: return 'ZUSÄTZE · 補遺'
    return 'KAPITEL %s · 第%s章' % (meta['rom'], RJP[n])


def short(s, l):
    if isinstance(s, int): return '§%d' % s
    m = re.match(r'z(\d+)(b?)$', s)
    if m: return 'Z%s%s' % (m.group(1), '′' if m.group(2) else '')
    return l.split('·')[-1].strip().replace('への序文', '').replace('への付記', '')


def zlink(h, n):
    """Link references to the Zusätze (S. Z. n. / （補遺n参照）) to zusaetze.html."""
    def zid(k):
        return 'z18b' if (n == 13 and k == '18') else 'z' + k
    h = re.sub(r'S\. Z\. (\d+)\.', lambda m: '<a class="zref" href="zusaetze.html#s%s">S. Z. %s.</a>' % (zid(m.group(1)), m.group(1)), h)
    h = re.sub(r'（補遺(\d+)参照）', lambda m: '（<a class="zref" href="zusaetze.html#s%s">補遺%s</a>参照）' % (zid(m.group(1)), m.group(1)), h)
    return h


def build(meta, items, notes, corr):
    out, k, page = [], 0, meta['first']
    for it in items:
        if it[0] == 'sec':
            k = 0
            out.append('<h2 class="sec" id="s%s"><a href="#s%s">%s</a></h2>' % (it[1], it[1], esc(it[2])))
        elif it[0] == 'fig':
            out.append('<figure class="fig"><span lang="de">%s</span><span lang="ja">%s</span>'
                       '<em>図版・譜例は原書を参照</em></figure>' % (esc(it[1]), esc(it[2])))
        else:
            _, sec, de, jp = it
            de = de or ''
            k += 1
            pid = '%s.%d' % (sec, k) if sec is not None else str(k)
            starts = [int(p) if p.isdigit() else p for p in re.findall(r'\{(\d+|[IVXL]+)\}', de)]
            pages = starts if de.startswith('{') else [page] + starts
            page = pages[-1]
            refs = list(dict.fromkeys(re.findall(r'\[\^(\d+)\]', de + jp)))
            pg = ''.join('<span>S.&nbsp;%s</span>' % p for p in dict.fromkeys(pages))
            out.append('<article class="row" id="p%s">\n  <aside class="mg"><a class="pid" href="#p%s">%s</a>'
                       '<span class="pg">%s</span></aside>\n  <p class="de" lang="de">%s</p>\n'
                       '  <p class="jp" lang="ja">%s</p>\n  %s\n</article>'
                       % (pid, pid, pid, pg, zlink(inline(de), meta['num']), zlink(inline(jp), meta['num']), note_html(refs, notes)))
    n = meta['num']
    tn = meta.get('titlenote')
    secs = [(it[1], it[2]) for it in items if it[0] == 'sec']
    nav = ''.join('<a href="#s%s">%s</a>' % (s, esc(short(s, l))) for s, l in dict.fromkeys(secs))
    prev = '<a href="%s">← %s</a>' % (fname(n - 1), label(n - 1)) if n > 0 else '<a href="index.html">← 目次</a>'
    nxt = '<a href="%s">%s →</a>' % (fname(n + 1), label(n + 1)) if n < 16 else '<a href="index.html">目次 →</a>'
    corr_block = ''
    if corr['de'] or corr['jp']:
        rows = ''.join('<tr><td>%s</td><td lang="de">%s</td><td lang="de">%s</td></tr>' % tuple(map(esc, r)) for r in corr['de'])
        lis = ''.join('<li><b>%s</b> %s</li>' % tuple(map(esc, r)) for r in corr['jp'])
        corr_block = ('<details class="corr">\n  <summary>校訂注（Jena 1922 版との照合）</summary>\n'
                      + ('  <p>ドイツ語本文は Jena 第9版（1922）に一致させた。旧テキストから改めた箇所：</p>\n'
                         '  <div class="tw"><table><thead><tr><th>位置</th><th>旧テキスト</th><th>Jena 1922（採用）</th>'
                         '</tr></thead><tbody>%s</tbody></table></div>\n' % rows if rows else '')
                      + ('  <p>和訳の主な改訂：</p>\n  <ul>%s</ul>\n' % lis if lis else '')
                      + '</details>')
    title_note = ('<sup><a class="fr" href="#n%s">%s</a></sup>' % (tn, tn)) if tn else ''
    return TEMPLATE.format(chlabel=label(n), kicker=kicker(meta), rom=meta['rom'], rjp=RJP.get(n, ''), de=esc(meta['de']), jp=esc(meta['jp']),
                           pages=meta['pages'], title_note=title_note,
                           tnote=note_html([tn], notes) if tn else '',
                           nav=nav, body='\n'.join(out), corr_block=corr_block, prev=prev, next=nxt)


TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{chlabel} {jp}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+JP:wght@400;600&display=swap">
<style>
:root {{
  --paper:#fbf8f1; --ink:#2b2721; --muted:#7a7266; --rule:#ddd3bd;
  --de:#8b6f2e; --de-bg:#f6f0e2; --jp:#5a7a99; --jp-bg:#eef3f7;
  --note-bg:#f4efe4; --bar:#fbf8f1ee; --hl:#f3e2b0;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper:#1c1a17; --ink:#e3ded4; --muted:#9d958a; --rule:#3a352d;
    --de:#cfa95c; --de-bg:#26221b; --jp:#8fb0cf; --jp-bg:#1f242a;
    --note-bg:#23201b; --bar:#1c1a17ee; --hl:#4a3f22;
  }}
}}
:root[data-theme="dark"] {{
  --paper:#1c1a17; --ink:#e3ded4; --muted:#9d958a; --rule:#3a352d;
  --de:#cfa95c; --de-bg:#26221b; --jp:#8fb0cf; --jp-bg:#1f242a;
  --note-bg:#23201b; --bar:#1c1a17ee; --hl:#4a3f22;
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; scroll-padding-top:4.5rem; }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior:auto; }} }}
body {{ margin:0; background:var(--paper); color:var(--ink);
  font-family:"Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif; line-height:1.9; }}
a {{ color:inherit; }}
:focus-visible {{ outline:2px solid var(--de); outline-offset:2px; }}
[lang="de"] {{ font-family:"EB Garamond","Garamond","Times New Roman",serif; hyphens:auto; }}

.bar {{ position:sticky; top:0; z-index:5; background:var(--bar); backdrop-filter:blur(6px);
  border-bottom:1px solid var(--rule); }}
.bar-in {{ max-width:78rem; margin:0 auto; padding:.5rem 1rem; display:flex; gap:1rem; align-items:center; flex-wrap:wrap; font-size:.82rem; }}
.bar .ch {{ text-decoration:none; font-weight:600; letter-spacing:.06em; white-space:nowrap; }}
.seg {{ display:inline-flex; border:1px solid var(--rule); border-radius:999px; overflow:hidden; }}
.seg button {{ font:inherit; background:none; color:var(--muted); border:0; padding:.2rem .8rem; cursor:pointer; }}
.seg button[aria-pressed="true"] {{ background:var(--de); color:var(--paper); }}
.secnav {{ display:flex; gap:.15rem; overflow-x:auto; margin-left:auto; scrollbar-width:none; }}
.secnav a {{ text-decoration:none; color:var(--muted); padding:.1rem .45rem; border-radius:4px; white-space:nowrap; }}
.secnav a:hover {{ color:var(--de); background:var(--de-bg); }}

header.title {{ max-width:78rem; margin:0 auto; padding:3rem 1rem 1.5rem; text-align:center; }}
.kicker {{ font-size:.8rem; letter-spacing:.3em; color:var(--muted); }}
h1 {{ margin:.4rem 0 .2rem; font-size:2rem; font-weight:600; letter-spacing:.15em; }}
h1 + .de-title {{ font-size:1.35rem; font-style:italic; color:var(--de); }}
h1 sup a {{ font-size:.55em; color:var(--de); text-decoration:none; }}
.source {{ margin-top:1rem; font-size:.78rem; color:var(--muted); }}
.title .notes {{ max-width:60rem; margin:1.2rem auto 0; text-align:left; }}

main {{ max-width:78rem; margin:0 auto; padding:0 1rem 4rem; }}
h2.sec {{ font-size:1rem; font-weight:600; color:var(--de); letter-spacing:.12em;
  margin:3rem 0 .6rem; padding-bottom:.3rem; border-bottom:1px solid var(--rule); }}
h2.sec a {{ text-decoration:none; }}

.row {{ display:grid; grid-template-columns:4.2rem 1fr 1fr; column-gap:1.6rem;
  padding:1rem 0; border-bottom:1px dotted var(--rule); }}
.row:target {{ background:linear-gradient(90deg,var(--hl),transparent 70%); }}
.mg {{ font-size:.72rem; color:var(--muted); display:flex; flex-direction:column; gap:.1rem; padding-top:.3rem;
  font-variant-numeric:tabular-nums; }}
.pid {{ font-weight:600; color:var(--de); text-decoration:none; font-size:.8rem; }}
.pg {{ display:flex; flex-direction:column; }}
.row > p {{ margin:0; }}
.row > .de {{ font-size:1.08rem; line-height:1.75; text-align:justify; }}
.row > .jp {{ font-size:.95rem; text-align:justify; }}
.pb {{ display:inline-block; font-family:"Noto Serif JP",serif; font-size:.62rem; line-height:1;
  color:var(--de); border:1px solid var(--de); border-radius:3px; padding:.08rem .25rem; margin:0 .15rem;
  vertical-align:.25em; opacity:.8; }}
.pb::before {{ content:"S. "; }}
a.fr {{ font-size:.68em; vertical-align:super; line-height:0; text-decoration:none; color:var(--de);
  font-weight:600; padding:0 .1em; font-family:"Noto Serif JP",serif; }}
.jp a.fr {{ color:var(--jp); }}
a.zref {{ color:inherit; text-decoration:underline; text-decoration-thickness:1px; text-underline-offset:2px; }}
a.zref:hover {{ color:var(--accent, inherit); }}

.notes {{ grid-column:2 / 4; list-style:none; margin:.8rem 0 0; padding:.6rem .9rem; background:var(--note-bg);
  border-radius:4px; display:grid; gap:.5rem; font-size:.8rem; line-height:1.65; }}
.notes li {{ display:grid; grid-template-columns:1.8rem 1fr 1fr; column-gap:1.2rem; }}
.notes li:target {{ outline:2px solid var(--hl); outline-offset:3px; }}
.notes .nn {{ color:var(--de); font-weight:600; }}
.notes p {{ margin:0; }}
.notes .de {{ font-size:.92rem; }}

.fig {{ grid-column:1/-1; margin:1rem 0 1rem 5.8rem; padding:.8rem 1rem; border:1px dashed var(--de);
  border-radius:4px; display:flex; flex-wrap:wrap; gap:.3rem 1.5rem; font-size:.82rem; color:var(--muted); }}
.missing {{ color:var(--muted); font-style:italic; }}
.fig em {{ font-style:normal; margin-left:auto; font-size:.72rem; }}

body.only-de .row > .jp, body.only-de .notes .jp, body.only-jp .row > .de, body.only-jp .notes .de {{ display:none; }}
body.only-de .row, body.only-jp .row {{ grid-template-columns:4.2rem minmax(0,44rem); }}
body.only-de .notes li, body.only-jp .notes li {{ grid-template-columns:1.8rem 1fr; }}
body.only-de .notes, body.only-jp .notes {{ grid-column:2; }}
body.no-notes .row .notes {{ display:none; }}

details.corr {{ max-width:78rem; margin:2rem auto; padding:0 1rem; font-size:.85rem; }}
details.corr summary {{ cursor:pointer; color:var(--de); font-weight:600; }}
.corr .tw {{ overflow-x:auto; }}
.corr table {{ border-collapse:collapse; margin:.8rem 0; min-width:32rem; }}
.corr td, .corr th {{ border-bottom:1px solid var(--rule); padding:.3rem .8rem; text-align:left; vertical-align:top; }}
.corr th {{ color:var(--muted); font-weight:400; font-size:.75rem; }}
.corr ul {{ padding-left:1.2rem; }}
.pager {{ max-width:78rem; margin:0 auto; padding:1.5rem 1rem 3rem; display:flex; justify-content:space-between;
  border-top:1px solid var(--rule); font-size:.85rem; }}
.pager a {{ color:var(--de); text-decoration:none; }}

@media (max-width: 760px) {{
  .row, body.only-de .row, body.only-jp .row {{ grid-template-columns:1fr; row-gap:.6rem; }}
  .mg {{ flex-direction:row; gap:.8rem; padding:0; }}
  .pg {{ flex-direction:row; gap:.5rem; }}
  .row > .jp {{ padding-top:.6rem; border-top:1px solid var(--rule); }}
  .notes, body.only-de .notes, body.only-jp .notes {{ grid-column:1; }}
  .notes li {{ grid-template-columns:1.6rem 1fr; }}
  .notes li .jp {{ grid-column:2; margin-top:.3rem; }}
  .fig {{ margin-left:0; }}
  .secnav {{ margin-left:0; width:100%; }}
}}
</style>
</head>
<body>
<div class="bar"><div class="bar-in">
  <a class="ch" href="index.html" title="目次">{chlabel}</a>
  <span class="seg" role="group" aria-label="表示言語">
    <button type="button" data-v="both" aria-pressed="true">対訳</button>
    <button type="button" data-v="only-de" aria-pressed="false">独</button>
    <button type="button" data-v="only-jp" aria-pressed="false">日</button>
  </span>
  <span class="seg" role="group" aria-label="注">
    <button type="button" data-n="show" aria-pressed="true">注あり</button>
    <button type="button" data-n="no-notes" aria-pressed="false">注なし</button>
  </span>
  <nav class="secnav" aria-label="節">{nav}</nav>
</div></div>

<header class="title">
  <div class="kicker">{kicker}</div>
  <h1>{jp}{title_note}</h1>
  <div class="de-title" lang="de">{de}</div>
  <div class="source">底本：E. Mach, <i lang="de">Die Analyse der Empfindungen</i>, 9. Aufl., Jena: G. Fischer 1922, S. {pages}　｜　本文中の <span class="pb">201</span> は底本の改頁位置</div>
  {tnote}
</header>

<main>
{body}
</main>

{corr_block}

<nav class="pager">{prev}<a href="index.html">目次</a>{next}</nav>

<script>
(function(){{
  var b=document.body;
  function store(k,v){{ try{{localStorage.setItem(k,v);}}catch(e){{}} }}
  function load(k){{ try{{return localStorage.getItem(k);}}catch(e){{return null;}} }}
  function setV(v){{ b.classList.remove('only-de','only-jp'); if(v!=='both') b.classList.add(v);
    document.querySelectorAll('[data-v]').forEach(function(x){{x.setAttribute('aria-pressed',x.dataset.v===v);}}); store('mach-view',v); }}
  function setN(n){{ b.classList.toggle('no-notes',n==='no-notes');
    document.querySelectorAll('[data-n]').forEach(function(x){{x.setAttribute('aria-pressed',x.dataset.n===n);}}); store('mach-notes',n); }}
  document.querySelectorAll('[data-v]').forEach(function(x){{x.addEventListener('click',function(){{setV(x.dataset.v);}});}});
  document.querySelectorAll('[data-n]').forEach(function(x){{x.addEventListener('click',function(){{setN(x.dataset.n);}});}});
  setV(load('mach-view')||'both'); setN(load('mach-notes')||'show');
}})();
</script>
</body>
</html>
'''


INDEX_STYLE = '<style>\n:root {\n  --bg: #f7f4ed;\n  --text: #2a2722;\n  --muted: #6b6560;\n  --accent: #8b7332;\n  --card-bg: #f0ece3;\n  --border: #d4cfc4;\n}\n@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {\n    --bg: #1e1d1a;\n    --text: #d8d4cc;\n    --muted: #9a958d;\n    --accent: #c4a54a;\n    --card-bg: #28261f;\n    --border: #3d3a32;\n  }\n}\n:root[data-theme="dark"] {\n  --bg: #1e1d1a;\n  --text: #d8d4cc;\n  --muted: #9a958d;\n  --accent: #c4a54a;\n  --card-bg: #28261f;\n  --border: #3d3a32;\n}\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody {\n  font-family: "Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", serif;\n  background: var(--bg); color: var(--text); line-height: 1.7;\n  padding: 2.5em 1.2em 3em; max-width: 640px; margin: 0 auto;\n}\nheader { text-align: center; margin-bottom: 2.4em; padding-bottom: 1.6em; border-bottom: 1px solid var(--border); }\n.book-title-jp { font-size: 1.5em; font-weight: 600; letter-spacing: 0.12em; margin-bottom: 0.15em; }\n.book-title-de { font-size: 1.15em; font-style: italic; color: var(--accent); margin-bottom: 0.15em; }\n.book-subtitle { font-size: 0.82em; color: var(--muted); margin-bottom: 0.6em; }\n.book-meta { font-size: 0.75em; color: var(--muted); letter-spacing: 0.05em; }\n.toc-label { font-size: 0.72em; font-weight: 600; color: var(--accent); letter-spacing: 0.15em;\n  margin-bottom: 1em; padding-bottom: 0.5em; border-bottom: 1px solid var(--border); }\n.toc { display: flex; flex-direction: column; }\n.ch { display: grid; grid-template-columns: 2.8em 1fr; padding: 0.7em 0; border-bottom: 1px solid var(--border);\n  text-decoration: none; color: var(--text); transition: background 0.15s; }\n.ch:first-child { border-top: 1px solid var(--border); }\n.ch:hover { background: var(--card-bg); }\n.ch:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }\n.ch-num { font-size: 0.78em; font-weight: 600; color: var(--accent); padding-top: 0.15em; text-align: right; padding-right: 0.8em; }\n.ch-titles { display: flex; flex-direction: column; gap: 0.1em; }\n.ch-jp { font-size: 0.92em; line-height: 1.5; }\n.ch-de { font-size: 0.78em; font-style: italic; color: var(--muted); line-height: 1.4; }\nfooter { margin-top: 2em; padding-top: 1em; border-top: 1px solid var(--border); font-size: 0.72em; color: var(--muted); line-height: 1.6; }\nfooter p + p { margin-top: 0.3em; font-style: italic; }\n</style>'
INDEX_HEAD = '<header>\n  <div class="book-title-jp">感覚の分析</div>\n  <div class="book-title-de">Die Analyse der Empfindungen</div>\n  <div class="book-subtitle">und das Verhältnis des Physischen zum Psychischen</div>\n  <div class="book-meta">Ernst Mach &#x7C; 第9版 (1922) &#x7C; 独日対訳</div>\n</header>\n\n<div class="toc-label">目次 INHALTSVERZEICHNIS</div>\n\n'
INDEX_FOOT = '<footer>\n  <p>エルンスト・マッハ『感覚の分析——物理的なものと心理的なものの関係』第9版（イェーナ：グスタフ・フィッシャー、1922年）序文・全15章・補遺の独日対訳。ドイツ語本文は同版に照合して校訂した。</p>\n  <p>Ernst Mach, Die Analyse der Empfindungen und das Verhältnis des Physischen zum Psychischen, 9. Aufl., Jena: Gustav Fischer, 1922.</p>\n</footer>\n'


def build_index(metas):
    rows = []
    for m in metas:
        rows.append('  <a class="ch" href="%s">\n    <span class="ch-num">%s</span>\n'
                    '    <span class="ch-titles">\n      <span class="ch-jp">%s</span>\n'
                    '      <span class="ch-de">%s</span>\n    </span>\n  </a>'
                    % (fname(m['num']), {0: '序', 16: '補'}.get(m['num'], RJP.get(m['num'])), esc(m['jp']), esc(m['de'])))
    return ('<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Mach 感覚の分析 目次</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600&display=swap">\n'
            + INDEX_STYLE + '\n</head>\n<body>\n' + INDEX_HEAD
            + '<nav class="toc">\n' + '\n'.join(rows) + '\n</nav>\n\n' + INDEX_FOOT + '</body>\n</html>\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    metas = []
    for n in range(0, 17):
        src = {0: 'vorwort.txt', 16: 'zusaetze.txt'}.get(n, 'kapitel_%d.txt' % n)
        path = os.path.join(HERE, src)
        if not os.path.exists(path):
            print('SKIPPED: %s not found' % src); continue
        meta, items, notes, corr = parse(path)
        metas.append(meta)
        out = os.path.join(OUT, fname(n))
        open(out, 'w', encoding='utf-8').write(build(meta, items, notes, corr))
        print('Created: %s (%d paragraphs, %d notes)' % (fname(n), sum(1 for i in items if i[0] == 'pair'), len(notes)))
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(build_index(metas))
    print('Created: index.html')


if __name__ == '__main__':
    main()
