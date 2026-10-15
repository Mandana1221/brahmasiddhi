"""京都・ハーバード方式（KH）のローマ字をデーヴァナーガリーと IAST に変換する。"""
import re

VOW = [('RR', 'ॠ', 'ṝ', 'ॄ'), ('lR', 'ऌ', 'ḷ', 'ॢ'), ('ai', 'ऐ', 'ai', 'ै'), ('au', 'औ', 'au', 'ौ'),
       ('a', 'अ', 'a', ''), ('A', 'आ', 'ā', 'ा'), ('i', 'इ', 'i', 'ि'), ('I', 'ई', 'ī', 'ी'),
       ('u', 'उ', 'u', 'ु'), ('U', 'ऊ', 'ū', 'ू'), ('R', 'ऋ', 'ṛ', 'ृ'), ('e', 'ए', 'e', 'े'),
       ('o', 'ओ', 'o', 'ो')]
CON = [('kh', 'ख', 'kh'), ('gh', 'घ', 'gh'), ('ch', 'छ', 'ch'), ('jh', 'झ', 'jh'), ('Th', 'ठ', 'ṭh'),
       ('Dh', 'ढ', 'ḍh'), ('th', 'थ', 'th'), ('dh', 'ध', 'dh'), ('ph', 'फ', 'ph'), ('bh', 'भ', 'bh'),
       ('k', 'क', 'k'), ('g', 'ग', 'g'), ('G', 'ङ', 'ṅ'), ('c', 'च', 'c'), ('j', 'ज', 'j'), ('J', 'ञ', 'ñ'),
       ('T', 'ट', 'ṭ'), ('D', 'ड', 'ḍ'), ('N', 'ण', 'ṇ'), ('t', 'त', 't'), ('d', 'द', 'd'), ('n', 'न', 'n'),
       ('p', 'प', 'p'), ('b', 'ब', 'b'), ('m', 'म', 'm'), ('y', 'य', 'y'), ('r', 'र', 'r'), ('l', 'ल', 'l'),
       ('v', 'व', 'v'), ('Z', 'श', 'ś'), ('z', 'श', 'ś'), ('S', 'ष', 'ṣ'), ('s', 'स', 's'), ('h', 'ह', 'h')]
OTH = [('M', 'ं', 'ṃ'), ('H', 'ः', 'ḥ'), ("'", 'ऽ', "'")]
TOK = sorted([(k, 'V', d, i, s) for k, d, i, s in VOW] + [(k, 'C', d, i, '') for k, d, i in CON]
             + [(k, 'O', d, i, '') for k, d, i in OTH], key=lambda x: -len(x[0]))
KMARK = re.compile(r'\((k\.[^)]*)\)')


def _tokens(s):
    i = 0
    while i < len(s):
        for k, kind, d, ia, sign in TOK:
            if s.startswith(k, i):
                yield kind, d, ia, sign
                i += len(k)
                break
        else:
            yield 'X', s[i], s[i], ''
            i += 1


def _dev(s):
    out = []
    prev_c = False
    for kind, d, _, sign in _tokens(s):
        if kind == 'C':
            if prev_c:
                out.append('्')
            out.append(d)
            prev_c = True
            continue
        if kind == 'V':
            out.append(sign if prev_c else d)
        else:
            if prev_c:
                out.append('्')
            out.append({'.': '।', '?': '।'}.get(d, d) if kind == 'X' else d)
        prev_c = False
    if prev_c:
        out.append('्')
    return ''.join(out)


def _iast(s):
    return ''.join(ia for _, _, ia, _ in _tokens(s))


def _split(s):
    """(k.N) の偈番号を変換対象から外す。"""
    parts = []
    pos = 0
    for m in KMARK.finditer(s):
        parts.append(('t', s[pos:m.start()]))
        parts.append(('k', m.group(1)))
        pos = m.end()
    parts.append(('t', s[pos:]))
    return parts


def dev(s, kfmt='({})'):
    return ''.join(_dev(t) if k == 't' else kfmt.format(t) for k, t in _split(s))


def iast(s, kfmt='({})'):
    return ''.join(_iast(t) if k == 't' else kfmt.format(t) for k, t in _split(s))
