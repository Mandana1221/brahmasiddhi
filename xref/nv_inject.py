#!/usr/bin/env python3
"""NV（ヴァールッティカ）対訳ページを nv/ に写し、スートラ番号を Thakur 版に揃え（xref/thakur.py）、
各ブロックの解説欄に NVTT（ヴァーチャスパティ）・NVTP（ウダヤナ）の関連箇所を加える。

  python3 xref/nv_inject.py NV対訳のディレクトリ

元のページ（vidhiviveka リポジトリ）は変更しない。元が更新されたら、xref/xmap.py と
このスクリプトを実行し直せばよい。
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import links  # noqa: E402
import thakur  # noqa: E402
from xmap import sutras  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'nv'
CSS = ('.mula .exp .xr{margin-top:10px;padding-top:10px;border-top:1px dashed var(--line);font-size:.92em}'
       '.mula .exp .xr .lbl{color:#5B4A9E}.mula .exp .xr p{margin:0 0 .3em}')

SISTER = ('<p class="sub">関連：<a href="../nbh_index.html">ニヤーヤ・バーシュヤ全訳 目次</a>　／　'
          '<a href="../nvtt_index.html">タートパリヤ・ティーカー全訳 目次</a>　／　'
          '<a href="../nvtp_index.html">タートパリヤ・パリシュッディ全訳 目次</a></p>\n')


def close_of(t, i):
    """t[i] で始まる <div …> に対応する </div> の位置。"""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', t[i:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return i + m.start()
    raise ValueError('unclosed div')


def box(ss):
    rows = []
    for key, name in (('nbh', 'ヴァーツヤーヤナの注解（NBh 全訳）'), ('nvtt', 'ヴァーチャスパティの注釈（NVTT 全訳）'), ('nvtp', 'ウダヤナの注釈（NVTP 全訳）')):
        it = links.sec_items(ss, key)
        if it:
            a = '、'.join(f'<a href="../{html.escape(e["file"])}#{e["id"]}">{html.escape(e["num"])} '
                         f'{html.escape(e["title"])}</a>' for e in it)
        else:
            a = '<span class="muted">この箇所への注釈はない</span>'
        rows.append(f'<p>{name}：{a}</p>')
    return (f'<div class="xr"><span class="lbl">関連箇所（スートラ {html.escape(links.span(ss))}）</span>'
            + ''.join(rows) + '</div>')


def inject(src):
    t = thakur.convert_html(src.read_text(encoding='utf-8'), src.name)   # スートラ番号を Thakur 版に
    t = t.replace('</style>', CSS + '\n</style>', 1)
    out, pos = [], 0
    for m in re.finditer(r'<div class="mula[^"]*" id="u\d+">\s*<span class="ref">([^<]*)</span>', t):
        ref = html.unescape(m.group(1))
        if 'NS' not in ref:
            continue
        ss = sutras(ref.split('NS', 1)[1])
        end = close_of(t, m.start())
        blk = t[m.start():end]
        k = blk.find('<div class="exp">')
        if k >= 0:
            at = close_of(t, m.start() + k)
            piece = box(ss)
        else:
            at = end
            piece = f'<div class="exp">{box(ss)}</div>'
        out.append(t[pos:at])
        out.append(piece)
        pos = at
    out.append(t[pos:])
    return ''.join(out)


def main():
    src = Path(sys.argv[1])
    OUT.mkdir(exist_ok=True)
    n = 0
    for f in sorted(src.glob('nyayavarttika-*.html')):
        if f.name == 'nyayavarttika-index.html':
            t = thakur.convert_html(f.read_text(encoding='utf-8'), f.name)
            t = t.replace('</header>', SISTER + '</header>', 1)
            (OUT / f.name).write_text(t, encoding='utf-8')
            continue
        (OUT / f.name).write_text(inject(f), encoding='utf-8')
        n += 1
    print('wrote', n, 'pages to', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
