#!/usr/bin/env python3
"""『シャクンタラー』対訳HTMLを生成する。

使い方: python3 build.py
act*.txt（幕ごとのデータ）を読み込み、リポジトリ直下に
shakuntala_bilingual.html を書き出す。
"""
import glob
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'shakuntala_bilingual.html')

# 話者名（IAST の主格形 → 日本語表示）
SPEAKERS = {
    'sūtradhāraḥ': '座頭',
    'naṭī': '女優',
    'rājā': '王',
    'sūtaḥ': '御者',
    'tapasvī': '苦行者',
    'tāpasaḥ': '苦行者',
    'sakhyau': '二人の友',
    'ubhe': '二人',
    'śakuntalā': 'シャクンタラー',
    'priyaṃvadā': 'プリヤンヴァダー',
    'anasūyā': 'アナスーヤー',
    'nepathye': '舞台裏で',
    'vidūṣakaḥ': '道化',
    'dauvārikaḥ': '門番',
    'senāpatiḥ': '将軍',
    'parijanaḥ': 'お供の者たち',
    'tāpasau': '二人の苦行者',
    'ṛṣī': '二人の苦行者',
    'ubhau': '二人',
    'prathamaḥ': '一人目',
    'dvitīyaḥ': '二人目',
    'karabhakaḥ': 'カラバカ',
}

METERS = {
    'śloka': 'シュローカ',
    'āryā': 'アーリヤー',
    'vasantatilakā': 'ヴァサンタティラカー',
    'śārdūlavikrīḍita': 'シャールドゥーラヴィクリーディタ',
    'sragdharā': 'スラグダラー',
    'śikhariṇī': 'シカリニー',
    'mandākrāntā': 'マンダークラーンター',
    'mālinī': 'マーリニー',
    'vaṃśastha': 'ヴァンシャスタ',
    'puṣpitāgrā': 'プシュピターグラー',
    'upajāti': 'ウパジャーティ',
    'drutavilambita': 'ドルタヴィランビタ',
    'viyoginī': 'ヴィヨーギニー',
}


def parse(path):
    """データファイルを読み、ブロックのリストを返す。"""
    blocks, cur, key = [], None, None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if line.startswith('#') or not line.strip():
            continue
        if line.startswith('=== '):
            parts = line[4:].split()
            cur = {'kind': parts[0], 'args': parts[1:], 'note': []}
            blocks.append(cur)
            key = None
            continue
        m = re.match(r'^(skt|pk|ch|ja|note): ?(.*)$', line)
        if m:
            key, val = m.group(1), m.group(2)
            if key == 'note':
                cur['note'].append(val)
            else:
                cur[key] = val
        elif key:  # 継続行
            if key == 'note':
                cur['note'][-1] += line
            else:
                cur[key] += line
    return blocks


def esc(s):
    return html.escape(s, quote=False)


def stage(s, ja=False):
    """括弧内のト書きを斜体の span にする。"""
    s = esc(s)
    if ja:
        return re.sub(r'（([^（）]*)）', r'<span class="sd-in">（\1）</span>', s)
    return re.sub(r'\(([^()]*)\)', r'<span class="sd-in">(\1)</span>', s)


def lines(s, ja=False):
    return ''.join(f'<span class="pada">{stage(p.strip(), ja)}</span>'
                   for p in s.split(' / '))


def speaker_html(who):
    if who in (None, '-'):
        return ''
    jp = SPEAKERS.get(who, who)
    return (f'<div class="speaker"><span class="sp-skt">{esc(who)}</span>'
            f'<span class="sp-jp">{jp}</span></div>')


def notes_html(notes):
    if not notes:
        return ''
    body = ''.join(f'<p>{esc(n)}</p>' for n in notes)
    return f'<div class="commentary"><div class="commentary-title">注</div>{body}</div>'


def render_block(b, act_no):
    k, a = b['kind'], b['args']
    if k == 'act':
        return ''  # 幕見出しは render_act で出す
    if k == 'head':
        return (f'<div class="scene-head"><span class="scene-skt">{esc(b["skt"])}</span>'
                f'<span class="scene-jp">{esc(b["ja"])}</span></div>')
    if k in ('sd', 'end'):
        cls = 'row sd' if k == 'sd' else 'row endline'
        return (f'<div class="{cls}"><div class="cols">'
                f'<div class="col-l"><p>{stage(b["skt"])}</p></div><div class="divider"></div>'
                f'<div class="col-r"><p>{stage(b["ja"], True)}</p></div></div>'
                f'{notes_html(b["note"])}</div>')
    if k in ('sp', 'pk'):
        who = a[1] if len(a) > 1 else None
        if k == 'sp':
            left = f'<p class="skt">{stage(b["skt"])}</p>'
        else:
            left = (f'<p class="prakrit">{stage(b["pk"])}</p>'
                    f'<p class="chaya"><span class="lang-label">chāyā</span>{esc(b["ch"])}</p>')
        return (f'<div class="row">{speaker_html(who)}<div class="cols">'
                f'<div class="col-l">{left}</div><div class="divider"></div>'
                f'<div class="col-r"><p>{stage(b["ja"], True)}</p></div></div>'
                f'{notes_html(b["note"])}</div>')
    if k in ('v', 'pv'):
        num, who = a[0], a[1]
        meter = a[2] if len(a) > 2 else ''
        mj = METERS.get(meter, '')
        meta = (f'<div class="verse-number">詩節 {num}'
                + (f'<span class="meter">{esc(meter)}（{mj}）</span>' if meter else '')
                + '</div>')
        if k == 'v':
            left = f'<div class="verse-skt">{lines(b["skt"])}</div>'
        else:
            left = (f'<div class="verse-skt prakrit">{lines(b["pk"])}</div>'
                    f'<div class="verse-chaya"><span class="lang-label">chāyā</span>{lines(b["ch"])}</div>')
        return (f'<div class="row verse" id="v{num}">{speaker_html(who)}{meta}<div class="cols">'
                f'<div class="col-l">{left}</div><div class="divider"></div>'
                f'<div class="col-r"><p class="verse-ja">{stage(b["ja"], True)}</p></div></div>'
                f'{notes_html(b["note"])}</div>')
    raise ValueError(f'unknown block kind: {k}')


def render_act(blocks):
    head = blocks[0]
    act_no = head['args'][0]
    out = [f'<section class="act" id="act{act_no}">',
           f'<div class="act-header"><h2>{esc(head["skt"])}</h2>'
           f'<div class="act-jp">{esc(head["ja"])}</div></div>']
    out += [render_block(b, act_no) for b in blocks[1:]]
    out.append('<a class="back-top" href="#top">↑ 目次へ</a></section>')
    return act_no, head, '\n'.join(out)


FRONT = open(os.path.join(HERE, 'front.html'), encoding='utf-8').read()
TEMPLATE = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()


def main():
    acts = []
    for path in sorted(glob.glob(os.path.join(HERE, 'act*.txt'))):
        acts.append(render_act(parse(path)))
    toc = ''.join(
        f'<li><a href="#act{n}"><span class="toc-num">{n}</span>'
        f'<span class="toc-skt">{esc(h["skt"])}</span><span>{esc(h["ja"])}</span></a></li>'
        for n, h, _ in acts)
    page = (TEMPLATE.replace('{{TOC}}', toc)
            .replace('{{FRONT}}', FRONT)
            .replace('{{BODY}}', '\n'.join(body for _, _, body in acts)))
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
