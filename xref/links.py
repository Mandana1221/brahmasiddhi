"""xref/xmap.json（xref/xmap.py が作る対応表）から、NV・NVTT・NVTP 相互の関連箇所リンクを作る。"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_P = ROOT / 'xref' / 'xmap.json'
MAP = json.loads(_P.read_text(encoding='utf-8')) if _P.exists() else {}

# 各ページの節（file#id）が受け持つスートラ
OWN = {'nvtt': {}, 'nvtp': {}}
for _s, _v in MAP.items():
    for _k in ('nvtt', 'nvtp'):
        if _v[_k]:
            OWN[_k].setdefault(f'{_v[_k]["file"]}#{_v[_k]["id"]}', []).append(_s)


def span(ss):
    """['3.1.19', '3.1.20'] → '3.1.19–20'。"""
    if not ss:
        return ''
    a, b = ss[0], ss[-1]
    return a if a == b else f'{a}–{b.split(".")[-1]}'


def _uniq(items):
    seen, out = set(), []
    for it in items:
        k = (it['file'], it['id'])
        if k not in seen:
            seen.add(k)
            out.append(it)
    return out


def nv_items(ss):
    return _uniq([e for s in ss for e in MAP.get(s, {}).get('nv', [])])


def nv_label(e):
    n = e['file'].split('-')[1]
    return f'NV対訳 {n} §{e["sec"]} {e["title"]}（{e["ref"]}）'


def sec_items(ss, key):
    return _uniq([MAP[s][key] for s in ss if MAP.get(s, {}).get(key)])


def sec_label(e, key):
    name = 'NVTT 全訳' if key == 'nvtt' else 'NVTP 全訳'
    return f'{name} {e["num"]} {e["title"]}'


def href(e):
    return ('nv/' if e['file'].startswith('nyayavarttika') else '') + e['file']


def links(items, label):
    return '、'.join(f'<a href="{html.escape(href(e))}#{e["id"]}">{html.escape(label(e))}</a>' for e in items)


def rows(ss, keys):
    """keys の順に（'nv' / 'nvtt' / 'nvtp'）関連箇所の行を作る。"""
    head = {'nv': 'ヴァールッティカ', 'nvtt': 'ヴァーチャスパティの注釈', 'nvtp': 'ウダヤナの注釈'}
    out = []
    for k in keys:
        it = nv_items(ss) if k == 'nv' else sec_items(ss, k)
        if it:
            lab = nv_label if k == 'nv' else (lambda e, k=k: sec_label(e, k))
            out.append(f'<div class="xref xref-{k}"><span class="xref-h">{head[k]}</span>{links(it, lab)}</div>')
    return ''.join(out)


def for_section(page, nid, keys):
    """全訳ページ page の節 nid が受け持つスートラについて、関連箇所の行を作る。"""
    key = 'nvtt' if page.startswith('nvtt') else 'nvtp'
    ss = OWN[key].get(f'{page}#{nid}')
    return rows(ss, keys) if ss else ''
