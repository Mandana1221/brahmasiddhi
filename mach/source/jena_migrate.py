#!/usr/bin/env python3
"""Migrate an old-format chapter file (kapitel_N_complete.txt) to the
Jena-aligned format (kapitel_N.txt) and report every German difference
against the Jena 1922 OCR (jena1922_ocr.txt).

Usage: python3 jena_migrate.py N            -> writes kapitel_N.txt + report
The German text is NOT replaced automatically: differences are listed in
the report and decided by hand (the OCR has its own errors).
"""
import re, sys, os, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
OCR = os.path.join(HERE, 'jena1922_ocr.txt')
JP = re.compile(r'[぀-ヿ一-鿿]')
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
         'XI', 'XII', 'XIII', 'XIV', 'XV']
# first line (1-based) of each chapter in the OCR; 2185 = "Zusätze."
OCR_START = {1: 178, 2: 376, 3: 418, 4: 463, 5: 589, 6: 687, 7: 802, 8: 1085,
             9: 1141, 10: 1203, 11: 1424, 12: 1475, 13: 1579, 14: 1878, 15: 2104, 16: 2185}
FN_RE = re.compile(r'(\*|\d{1,2})\)')


# ---------------------------------------------------------------- OCR side
def read_ocr(n):
    lines = open(OCR, encoding='utf-8').read().split('\n')
    chunk = lines[OCR_START[n] - 1: OCR_START[n + 1] - 1]
    title = chunk[0].strip()
    nums = [int(m.group(1)) for l in chunk for m in [re.match(r'^— (\d+) —$', l.strip())] if m]
    page = nums[0] - 1
    stream = [('\x00P%d\x00' % page)]
    notes, figs = [], []
    pending_page = None
    for l in chunk[1:]:
        s = l.strip()
        m = re.match(r'^— (\d+) —$', s)
        if m:
            page = int(m.group(1)); pending_page = page; continue
        if (not s or s.startswith('END_OF_PAGE') or s.startswith('OCR done') or re.match(r'^\d+\*?$', s)
                or s.startswith('Mach, Analyse') or re.match(r'^\.?\s*[\dIl]{1,2}\.$', s)):
            continue
        fm = re.match(r'^Fig\. (\d+)\.?$', s)
        if fm:
            figs.append((int(fm.group(1)), page, len(stream))); continue
        if re.match(r'^(\d{1,2}|\*)\) ', s):
            notes.append((page, s)); continue
        if pending_page is not None:
            stream.append('\x00P%d\x00' % pending_page); pending_page = None
        stream.append(s)
    text = '\n'.join(stream)
    # rejoin words hyphenated at a line or page end
    text = re.sub(r'([a-zäöüß])-\n(\x00P\d+\x00\n)?([a-zäöüß])',
                  lambda m: m.group(1) + (m.group(2) or '').strip() + m.group(3), text)
    text = text.replace('\n', ' ')
    return title, text, notes, figs


def tokenize_ocr(text):
    """-> tokens (marker-free) and {token_index: [(page, char_offset)]}"""
    toks, pbs = [], {}
    for raw in text.split():
        if re.fullmatch(r'\x00P\d+\x00', raw):
            pbs.setdefault(len(toks), []).append((int(raw[2:-1]), 0)); continue
        m = re.search(r'\x00P(\d+)\x00', raw)
        if m:
            pbs.setdefault(len(toks), []).append((int(m.group(1)), m.start()))
            raw = raw[:m.start()] + raw[m.end():]
        toks.append(raw)
    return toks, pbs


def norm(t):
    t = t.replace('„', '"').replace('“', '"').replace('”', '"').replace('»', '"').replace('«', '"')
    t = re.sub(r'(?<=[^\d\s(])(\*|\d{1,2})\)', '', t)   # attached footnote marker
    return t


# ------------------------------------------------------------ source side
def read_source(n):
    path = os.path.join(HERE, 'kapitel_%d_complete.txt' % n)
    lines = open(path, encoding='utf-8').read().split('\n')
    title_de, title_jp = lines[1].strip(), lines[2].strip()
    text = '\n'.join(lines[3:])
    parts = re.split(r'\n(?:Anmerkungen[^\n]*)\n', text, maxsplit=1)
    body, anm = parts[0], (parts[1] if len(parts) > 1 else '')
    blocks = [b.strip() for b in re.split(r'\n\s*\n', body) if b.strip()]
    items, last_sec, issues = [], None, []
    for b in blocks:
        for sub in b.split('\n') if re.match(r'^§\d+', b) else [b]:
            sub = sub.strip()
            if not sub:
                continue
            if re.fullmatch(r'§\s*\d+', sub):
                k = int(re.sub(r'\D', '', sub))
                if k != last_sec:
                    items.append(['sec', k]); last_sec = k
                continue
            sub = re.sub(r'^【[移補]】', '', sub).strip()
            if JP.search(sub):
                if items and items[-1][0] == 'pair':
                    items[-1][2].append(sub)
                else:
                    items.append(['pair', '', [sub]]); issues.append('JP ohne DE: ' + sub[:40])
            else:
                if items and items[-1][0] == 'pair' and not items[-1][2]:
                    issues.append('DE ohne JP: ' + items[-1][1][:60])
                items.append(['pair', sub, []])
    notes = []
    for line in anm.split('\n'):
        s = line.strip()
        if not s:
            continue
        m = re.match(r'^Anm\.\s*(\d+|\*)?\s*\)?\s*(\[?zu §\s*\d+\]?)?\s*(.*)$', s)
        if m and s.startswith('Anm'):
            notes.append(['', ''])
            s = m.group(3).strip()
            if not s:
                continue
        s = re.sub(r'^【[補移]】', '', s).strip()
        s = re.sub(r'^注\s*(\d+|\*)?\s*[）)]\s*', '', s).strip()
        s = re.sub(r'^\[?§\s*\d+\s*に対して\]?\s*', '', s).strip()
        if not s:
            continue
        if not notes:
            notes.append(['', ''])
        if JP.search(s):
            notes[-1][1] = (notes[-1][1] + ' ' + s).strip()
        else:
            if notes[-1][1]:            # German after Japanese -> malformed, new note
                notes.append(['', ''])
            notes[-1][0] = (notes[-1][0] + ' ' + s).strip()
    notes = [x for x in notes if x[0] or x[1]]
    # superscript markers in German -> n)
    sup = str.maketrans('¹²³⁴⁵⁶⁷⁸⁹⁰', '1234567890')
    for it in items:
        if it[0] == 'pair':
            it[1] = re.sub(r'\s?([¹²³⁴⁵⁶⁷⁸⁹⁰]+)[⁾)]', lambda m: m.group(1).translate(sup) + ')', it[1])
    return title_de, title_jp, items, notes, issues


# ---------------------------------------------------------- helpers
ABBR = r'(?<!\bz\. B)(?<!\bd\. h)(?<!\bS)(?<!\bBd)(?<!\bvgl)(?<!\bVgl)(?<!\bu\. s\. w)(?<!\bu)(?<!\bs)(?<!\bw)(?<!\bf)(?<!\bff)(?<!\bp)(?<!\bAufl)(?<!\bJahrg)(?<!\bNr)(?<!\bDr)(?<!\bProf)(?<!\bFig)(?<!\bca)(?<!\betc)(?<!\bbzw)(?<!\bResp)(?<!\bvergl)(?<!\bSt)(?<!\bHr)(?<!\b[A-Z])'


def de_sentences(s):
    parts = re.split(ABBR + r'(?<=[.?!:])(["“]?(?:\[\^\d+\])?)\s+(?=[„"A-ZÄÖÜ(—–])', s)
    out, i = [], 0
    while i < len(parts):
        seg = parts[i] + (parts[i + 1] if i + 1 < len(parts) else '')
        out.append(seg); i += 2
    return [x for x in out if x.strip()]


def split_de(de, jps):
    """split German into len(jps) parts at sentence ends, proportional to JP length"""
    if len(jps) <= 1:
        return [de]
    sents = de_sentences(de)
    if len(sents) < len(jps):
        return [de] + [''] * (len(jps) - 1)
    total_j = sum(len(j) for j in jps)
    cum_targets, acc = [], 0
    for j in jps[:-1]:
        acc += len(j); cum_targets.append(acc / total_j)
    lens = [len(s) for s in sents]; total_d = sum(lens)
    cuts, acc, k = [], 0, 0
    cumd = []
    for L in lens:
        acc += L; cumd.append(acc / total_d)
    prev = 0
    for t in cum_targets:
        best = min(range(prev + 1, len(sents) - (len(cum_targets) - len(cuts)) + 1),
                   key=lambda c: abs(cumd[c - 1] - t))
        cuts.append(best); prev = best
    pieces, start = [], 0
    for c in cuts + [len(sents)]:
        pieces.append(' '.join(sents[start:c])); start = c
    return pieces


def place_jp_refs(de, jp, refs):
    """insert [^k] into Japanese at the sentence proportional to the German position"""
    if not refs:
        return jp
    jsents = re.split(r'(?<=。)', jp)
    jsents = [x for x in jsents if x]
    dsents = de_sentences(de)
    inserts = {}
    for r in refs:
        di = next((i for i, s in enumerate(dsents) if '[^%s]' % r in s), len(dsents) - 1)
        ji = min(len(jsents) - 1, round((di + 0.5) / max(len(dsents), 1) * len(jsents) - 0.5))
        inserts.setdefault(max(ji, 0), []).append(r)
    out = []
    for i, s in enumerate(jsents):
        if i in inserts:
            mark = ''.join('[^%s]' % r for r in inserts[i])
            s = s[:-1] + mark + '。' if s.endswith('。') else s + mark
        out.append(s)
    return ''.join(out)


# ---------------------------------------------------------------- main
MARK = re.compile(r'^(.*?[^\d\s(])((?:\d{1,2}|\*)\))(.*)$')


def strip_src_markers(de):
    """remove the old footnote markers from source German (keep real parentheses)"""
    out, last = [], 0
    for m in re.finditer(r'\s?(?<![\d(])(?:\*|\d{1,2})\)(?=[\s.,;:!?“"—)]|$)', de):
        before = de[:m.start()]
        if before.count('(') > before.count(')'):
            continue
        out.append(de[last:m.start()]); last = m.end()
    out.append(de[last:])
    return ''.join(out)


KEEP_HYPHEN_NEXT = {'und', 'oder', 'bis', 'als', 'sowie', 'resp.', 'bzw.', 'noch', 'wie'}


def autofix(items, otoks, note_texts, log):
    """Pre-pass: repair hyphenation debris in the old German and insert
    passages that exist only in the Jena text."""
    stoks, sref = [], []
    for ii, it in enumerate(items):
        if it[0] == 'pair':
            for t in it[1].split():
                stoks.append(t); sref.append(ii)
    A = [norm(t) for t in otoks]
    Ai = [i for i, t in enumerate(A) if t and not re.fullmatch(r'(\*|\d{1,2})\)', t)]
    B = [norm(t) for t in stoks]
    sm = difflib.SequenceMatcher(None, [A[i] for i in Ai], B, autojunk=False)
    repl = {}           # source token index -> replacement string ('' = drop)
    inserts = []        # (after_source_token_index, ocr text)
    notes_flat = norm(' '.join(note_texts))
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        oseg = [otoks[Ai[k]] for k in range(a1, a2)]
        sseg = stoks[b1:b2]
        ojoin, sjoin = norm(''.join(oseg)), norm(''.join(sseg))
        # 1) hyphenation debris in the source ("ge-ringerem", "Vor- stellungen")
        if (sseg and oseg and '\\' not in ojoin and '-' in sjoin
                and sjoin.replace('-', '') == ojoin.replace('-', '')
                and not any(t.endswith('-') and i + 1 < len(sseg) and sseg[i + 1] in KEEP_HYPHEN_NEXT
                            for i, t in enumerate(sseg))):
            for k in range(b1, b2):
                repl[k] = ''
            repl[b1] = ' '.join(oseg)
            log.append('Silbentrennung behoben: „%s“ → „%s“' % (' '.join(sseg), ' '.join(oseg)))
            continue
        # 2) passage present only in Jena
        if a2 - a1 >= 8 and (b2 - b1) <= 2 and '\\' not in ''.join(oseg):
            text = ' '.join(oseg)
            probe = norm(' '.join(oseg[: min(12, len(oseg))]))
            probe2 = norm(' '.join(oseg[1: min(13, len(oseg))]))
            if probe and (probe in notes_flat or probe2 in notes_flat):
                log.append('Fußnotenüberlauf im OCR ignoriert: „%s …“' % text[:60]); continue
            # keep the source tokens of a 'replace' (usually the paragraph's last word)
            inserts.append((b1 - 1 if b1 > 0 else 0, text, b2 - b1))
            log.append('FEHLTE in der alten Fassung, aus Jena eingefügt (%d Wörter): „%s …“' % (a2 - a1, text[:80]))
    if not repl and not inserts:
        return items
    # rebuild items
    per_item = {}
    for j, t in enumerate(stoks):
        r = repl.get(j, t)
        if r:
            per_item.setdefault(sref[j], []).append(r)
    new_items, extra = [], {}
    for after, text, nsrc in inserts:
        ii = sref[after] if stoks else 0
        extra.setdefault(ii, []).append(text)
    for ii, it in enumerate(items):
        if it[0] != 'pair':
            new_items.append(it); continue
        new_items.append(['pair', ' '.join(per_item.get(ii, [])), it[2]])
        for text in extra.get(ii, []):
            new_items.append(['pair', text, ['〔未訳〕']])
    return new_items


def migrate(n):
    title, otext, onotes, ofigs = read_ocr(n)
    otoks, opbs = tokenize_ocr(otext)
    tde, tjp, items, snotes, issues = read_source(n)
    titlenote = bool(re.search(r'[a-zäöü]\d\)\.?$', title))
    for it in items:
        if it[0] == 'pair':
            it[1] = strip_src_markers(it[1])
    fixlog = []
    src_all = [it[1] for it in items if it[0] == 'pair'] + [d for d, _ in snotes]
    items = autofix(items, otoks, [s for _, s in onotes] + src_all, fixlog)

    stoks, sref = [], []
    for ii, it in enumerate(items):
        if it[0] == 'pair':
            for ti, t in enumerate(it[1].split()):
                stoks.append(t); sref.append((ii, ti))
    A = [norm(t) for t in otoks]
    B = [norm(t) for t in stoks]
    Ai = [i for i, t in enumerate(A) if t and not re.fullmatch(r'(\*|\d{1,2})\)', t)]
    Bi = [j for j, t in enumerate(B) if t]
    sm = difflib.SequenceMatcher(None, [A[i] for i in Ai], [B[j] for j in Bi], autojunk=False)
    ops = sm.get_opcodes()
    pos_a = {i: k for k, i in enumerate(Ai)}

    def map_ocr(i_ocr):
        ia = next((pos_a[i] for i in range(i_ocr, len(A)) if i in pos_a), len(Ai))
        for op, a1, a2, b1, b2 in ops:
            if a1 <= ia < a2:
                if op == 'equal':
                    return Bi[b1 + ia - a1], True
                return (Bi[b1] if b1 < len(Bi) else len(stoks) - 1), False
        return len(stoks) - 1, False

    report_pos = []
    inserts = {}            # source token j -> list of (kind, value, offset)
    first_page = None
    for i, lst in sorted(opbs.items()):
        for page, off in lst:
            if first_page is None:
                first_page = page; continue
            if i >= len(otoks):
                continue
            j, exact = map_ocr(i)
            if not exact:
                report_pos.append('S. %d: Umbruchposition unsicher bei „%s“' % (page, ' '.join(otoks[i:i + 4])))
            inserts.setdefault(j, []).append(('pb', page, off if exact else 0))
    last_page = max(p for l in opbs.values() for p, _ in l)

    # footnote references from the OCR body
    k = 1 if titlenote else 0
    for i, t in enumerate(otoks):
        m = MARK.match(t)
        if not m:
            continue
        k += 1
        j, exact = map_ocr(i)
        if not exact:
            report_pos.append('Anm. %d: Verweisposition unsicher bei „%s“' % (k, ' '.join(otoks[max(i - 2, 0):i + 2])))
        inserts.setdefault(j, []).append(('fn', k, len(m.group(1))))
    n_refs = k

    new_tokens = {}
    for j, t in enumerate(stoks):
        ii, _ = sref[j]
        pbs = [x for x in inserts.get(j, []) if x[0] == 'pb']
        fns = [x for x in inserts.get(j, []) if x[0] == 'fn']
        for _, num, off in fns:
            core = re.match(r'^(.*?)([.,;:!?“"‘’)\]—]*)$', t)
            t = core.group(1) + '[^%d]' % num + core.group(2)
        for _, page, off in pbs:
            if 0 < off < len(t) and '[^' not in t[:off]:
                t = t[:off] + '{%d}' % page + t[off:]
            else:
                t = '{%d}' % page + t
        new_tokens.setdefault(ii, []).append(t)

    # notes: German from the OCR, Japanese from the best-matching old note
    used = set()
    notes_out, note_rep = [], []
    for idx, (pg, s) in enumerate(onotes, 1):
        o = re.sub(r'^(\d{1,2}|\*)\)\s*', '', s).strip()
        best, br = None, 0.0
        for si, (sde, sjp) in enumerate(snotes):
            if si in used or not sde:
                continue
            r = difflib.SequenceMatcher(None, norm(o), norm(sde), autojunk=False).ratio()
            if r > br:
                best, br = si, r
        if best is not None and br >= 0.55:
            used.add(best)
            sde, sjp = snotes[best]
            de = sde if (br >= 0.9 or len(sde) >= len(o)) else o
            notes_out.append((de, re.sub(r'【[補移]】', '', sjp) or '〔未訳〕'))
            if norm(o).split() != norm(sde).split():
                note_rep.append('- Anm. %d (S. %d, Ähnlichkeit %.2f)\n  OCR: %s\n  SRC: %s' % (idx, pg, br, o[:600], sde[:600]))
        else:
            notes_out.append((o, '〔未訳〕'))
            note_rep.append('- Anm. %d (S. %d): KEINE Übersetzung gefunden\n  OCR: %s' % (idx, pg, o[:600]))
    for si, (sde, sjp) in enumerate(snotes):
        if si not in used:
            note_rep.append('- Alte Anm. nicht zugeordnet:\n  DE: %s\n  JP: %s' % (sde[:300], sjp[:200]))

    lines = ['@chapter %d | %s | %s | %s | %d–%d' % (n, ROMAN[n], tde, tjp, first_page, last_page)]
    if titlenote:
        lines.append('@titlenote 1')
    lines.append('')
    cur_page = first_page
    figs = list(ofigs)
    n_par = 0
    for ii, it in enumerate(items):
        if it[0] == 'sec':
            lines += ['§%d' % it[1], '']; continue
        de = ' '.join(new_tokens.get(ii, []))
        jps = [re.sub(r'【[補移]】|\s?[¹²³⁴⁵⁶⁷⁸⁹⁰]+[⁾)）]', '', j) for j in it[2]] or ['〔未訳〕']
        for d, j in zip(split_de(de, jps), jps):
            refs = re.findall(r'\[\^(\d+)\]', d)
            lines += [d if d else '〔—〕', '', place_jp_refs(d, j, refs), '']
            n_par += 1
            pages = [int(p) for p in re.findall(r'\{(\d+)\}', d)]
            if pages:
                cur_page = pages[-1]
        for f in list(figs):
            if f[1] <= cur_page:
                lines += ['@fig Fig. %d (S. %d) | 図%d（原書 S. %d）' % (f[0], f[1], f[0], f[1]), '']
                figs.remove(f)
    for f in figs:
        lines += ['@fig Fig. %d (S. %d) | 図%d（原書 S. %d）' % (f[0], f[1], f[0], f[1]), '']
    lines += ['==Anmerkungen==', '']
    for i, (de, jp) in enumerate(notes_out, 1):
        lines += ['[^%d]' % i, de, jp, '']
    open(os.path.join(HERE, 'kapitel_%d.txt' % n), 'w', encoding='utf-8').write('\n'.join(lines).rstrip() + '\n')

    rep = ['# Kapitel %d — %s' % (n, title), '',
           'Absätze: %d | Anm. (OCR): %d | Verweise (OCR-Text, inkl. Titel): %d | alte Anm.: %d'
           % (n_par, len(onotes), n_refs, len(snotes))]
    rep += ['Struktur: ' + x for x in issues] + ['Position: ' + x for x in report_pos]
    rep += ['Autofix: ' + x for x in fixlog]
    rep += ['', '## Textdifferenzen (OCR | Quelle)']
    for op, a1, a2, b1, b2 in ops:
        if op == 'equal':
            continue
        oa = ' '.join(otoks[Ai[max(a1 - 3, 0)]: (Ai[a2 + 1] if a2 + 1 < len(Ai) else len(otoks))])
        sb = ' '.join(stoks[Bi[max(b1 - 3, 0)]: (Bi[b2 + 1] if b2 + 1 < len(Bi) else len(stoks))])
        rep.append('- [%s] OCR: %s\n         SRC: %s' % (op, oa[:500], sb[:500]))
    rep += ['', '## Anmerkungen'] + note_rep
    open(os.path.join(HERE, '..', 'review', 'kapitel_%d_report.md' % n), 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
    print('Kap. %2d: %3d Abs., %3d Diffs, Anm OCR %2d / Verweise %2d / alt %2d, unsicher %d' % (
        n, n_par, sum(1 for o in ops if o[0] != 'equal'), len(onotes), n_refs, len(snotes), len(report_pos)))


if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, '..', 'review'), exist_ok=True)
    for a in sys.argv[1:]:
        migrate(int(a))
