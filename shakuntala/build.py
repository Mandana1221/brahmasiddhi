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

from translit import to_deva

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
    'gautamī': 'ガウタミー',
    'śiṣyaḥ': '弟子',
    'kāśyapaḥ': 'カーシャパ',
    'kaṇvaḥ': 'カンヴァ',
    'śārṅgaravaḥ': 'シャールンガラヴァ',
    'śāradvataḥ': 'シャーラドヴァタ',
    'kañcukī': '侍従長',
    'pratīhārī': '女官',
    'vaitālikaḥ': '吟遊詩人',
    'vaitālikau': '二人の吟遊詩人',
    'purohitaḥ': '宮廷祭官',
    'purodhāḥ': '宮廷祭官',
    'ṛṣayaḥ': '苦行者たち',
    'śyālaḥ': '警吏の長',
    'puruṣaḥ': '漁師',
    'rakṣiṇau': '二人の警吏',
    'akṣamālā': 'アクシャマーラー',
    'ceṭī': '侍女',
    'ceṭyau': '二人の侍女',
    'prathamā': '一人目の女',
    'dvitīyā': '二人目の女',
    'mātaliḥ': 'マータリ',
    'bālaḥ': '少年',
    'tāpasī': '女の苦行者',
    'tāpasyau': '二人の女の苦行者',
    'mārīcaḥ': 'マーリーチャ',
    'aditiḥ': 'アディティ',
    'sarve': '一同',
    'haṃsapadikā': 'ハンサパディカー',
    'caturikā': 'チャトゥリカー',
    'bhāguriḥ': 'バーグリ',
    'ṛṣikumārakau': '二人の若い苦行者',
    'śiṣyāḥ': '弟子たち',
    'nākalāsikā': '天の踊り子',
    'cūtamañjarī': 'チュータマンジャリー',
    'lipikārī': '絵師',
    'yavanī': 'ヤヴァナの女',
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
    'indravajrā': 'インドラヴァジュラー',
    'upendravajrā': 'ウペーンドラヴァジュラー',
    'hariṇī': 'ハリニー',
    'pṛthvī': 'プリトヴィー',
    'rathoddhatā': 'ラトーッダター',
    'praharṣiṇī': 'プラハルシニー',
    'aupacchandasika': 'アウパッチャンダシカ',
    'vaitālīya': 'ヴァイターリーヤ',
    'gīti': 'ギーティ',
    'upagīti': 'ウパギーティ',
    'aparavaktra': 'アパラヴァクトラ',
    'śālinī': 'シャーリニー',
    'rucirā': 'ルチラー',
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
    """括弧内のト書きを斜体の span にする（エスケープ済みの文字列を返す）。"""
    s = esc(s)
    if ja:
        return re.sub(r'（([^（）]*)）', r'<span class="sd-in">（\1）</span>', s)
    return re.sub(r'\(([^()]*)\)', r'<span class="sd-in">(\1)</span>', s)


def dual(s, wrap=stage):
    """IAST とデーヴァナーガリーの両方を出力し、表示はCSSで切り替える。"""
    return (f'<span class="t-iast">{wrap(s)}</span>'
            f'<span class="t-deva" lang="sa-Deva">{wrap(to_deva(s))}</span>')


def verse_lines(s):
    """詩節の各句を行に分ける。デーヴァナーガリーでは半詩節末に । 、詩節末に ॥ をつける。"""
    padas = [p.strip() for p in s.split(' / ')]
    n = len(padas)
    iast = ''.join(f'<span class="pada">{stage(p)}</span>' for p in padas)
    deva = []
    for i, p in enumerate(padas):
        d = stage(to_deva(p)).rstrip('।॥ ')
        if i == n - 1:
            d += ' ॥'
        elif (n == 4 and i == 1) or (n == 2 and i == 0) or (n not in (2, 4)):
            d += ' ।'
        deva.append(f'<span class="pada">{d}</span>')
    return (f'<span class="t-iast">{iast}</span>'
            f'<span class="t-deva" lang="sa-Deva">{"".join(deva)}</span>')


def ja_text(s):
    return stage(s, True)


def speaker_html(who):
    if who in (None, '-'):
        return ''
    jp = SPEAKERS.get(who, who)
    return (f'<div class="speaker"><span class="sp-jp">{jp}</span>'
            f'<span class="sp-skt">{dual(who, esc)}</span></div>')


def notes_html(notes):
    if not notes:
        return ''
    body = ''.join(f'<p>{esc(n)}</p>' for n in notes)
    return f'<div class="commentary"><div class="commentary-title">注</div>{body}</div>'


def two_cols(left, right, cls=''):
    return (f'<div class="cols {cls}"><div class="col-l">{left}</div>'
            f'<div class="col-r">{right}</div></div>')


def render_block(b, act_no):
    k, a = b['kind'], b['args']
    if k == 'act':
        return ''  # 幕見出しは render_act で出す
    if k == 'head':
        return (f'<div class="scene-head"><span class="scene-skt">{dual(b["skt"], esc)}</span>'
                f'<span class="scene-jp">{esc(b["ja"])}</span></div>')
    if k in ('sd', 'end'):
        cls = 'row sd' if k == 'sd' else 'row endline'
        return (f'<div class="{cls}">'
                + two_cols(f'<p>{dual(b["skt"])}</p>', f'<p>{ja_text(b["ja"])}</p>')
                + f'{notes_html(b["note"])}</div>')
    if k in ('sp', 'pk'):
        who = a[1] if len(a) > 1 else None
        if k == 'sp':
            left = f'<p class="skt">{dual(b["skt"])}</p>'
        else:
            left = (f'<p class="prakrit">{dual(b["pk"])}</p>'
                    f'<p class="chaya"><span class="lang-label">chāyā</span>{dual(b["ch"], esc)}</p>')
        cont = ' cont' if who == '-' else ''
        return (f'<div class="row speech{cont}">{speaker_html(who)}'
                + two_cols(left, f'<p>{ja_text(b["ja"])}</p>')
                + f'{notes_html(b["note"])}</div>')
    if k in ('v', 'pv'):
        num, who = a[0], a[1]
        meter = a[2] if len(a) > 2 else ''
        mj = METERS.get(meter, '')
        meta = (f'<div class="verse-meta"><span class="verse-no">{num}</span>'
                + (f'<span class="meter">{dual(meter, esc)}<span class="meter-jp">{mj}</span></span>' if meter else '')
                + '</div>')
        if k == 'v':
            left = f'<div class="verse-skt">{verse_lines(b["skt"])}</div>'
        else:
            left = (f'<div class="verse-skt prakrit">{verse_lines(b["pk"])}</div>'
                    f'<div class="verse-chaya chaya"><span class="lang-label">chāyā</span>{verse_lines(b["ch"])}</div>')
        return (f'<div class="row verse" id="v{num}">{speaker_html(who)}{meta}'
                + two_cols(left, f'<p class="verse-ja">{ja_text(b["ja"])}</p>')
                + f'{notes_html(b["note"])}</div>')
    raise ValueError(f'unknown block kind: {k}')


def render_act(blocks):
    head = blocks[0]
    act_no = head['args'][0]
    out = [f'<section class="act" id="act{act_no}">',
           f'<div class="act-header"><div class="act-no">第{"一二三四五六七"[int(act_no)-1]}幕</div>'
           f'<h2>{dual(head["skt"], esc)}</h2>'
           f'<div class="act-jp">{esc(head["ja"].split("　", 1)[-1])}</div></div>']
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
        f'<span class="toc-jp">{esc(h["ja"])}</span><span class="toc-skt">{dual(h["skt"], esc)}</span></a></li>'
        for n, h, _ in acts)
    actnav = ''.join(f'<option value="act{n}">{esc(h["ja"])}</option>' for n, h, _ in acts)
    page = (TEMPLATE.replace('{{TOC}}', toc).replace('{{ACTNAV}}', actnav)
            .replace('{{FRONT}}', FRONT)
            .replace('{{BODY}}', '\n'.join(body for _, _, body in acts)))
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
