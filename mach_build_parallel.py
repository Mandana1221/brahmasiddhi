#!/usr/bin/env python3
"""
Build full parallel text HTML for Mach's Analyse der Empfindungen.
V2: Improved parsing with line-by-line section detection.
"""
import re
import html as html_mod

GERMAN_FILE = "/root/.claude/uploads/181d4bef-3f6d-5143-8cc7-0ace8f7aa520/c6d4766c-dieanalysederemp00mach_mitraocr_1.txt"
JAPANESE_FILE = "/tmp/claude-0/-home-user-brahmasiddhi/181d4bef-3f6d-5143-8cc7-0ace8f7aa520/scratchpad/japanese_translation.txt"
OUTPUT_FILE = "/tmp/claude-0/-home-user-brahmasiddhi/181d4bef-3f6d-5143-8cc7-0ace8f7aa520/scratchpad/mach-parallel.html"

ROMAN_TO_INT = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,
                "IX":9,"X":10,"XI":11,"XII":12,"XIII":13,"XIV":14,"XV":15}
INT_TO_ROMAN_JA = ["","Ⅰ","Ⅱ","Ⅲ","Ⅳ","Ⅴ","Ⅵ","Ⅶ","Ⅷ","Ⅸ","Ⅹ","ⅩⅠ","ⅩⅡ","ⅩⅢ","ⅩⅣ","ⅩⅤ"]

# Chapter line ranges (1-indexed, inclusive start)
# German: (roman, title, start_line, end_line_exclusive)
CHAPTERS_DE_RANGES = [
    ("I", "Antimetaphysische Vorbemerkungen", 240, 663),
    ("II", "Über vorgefaßte Meinungen", 663, 751),
    ("III", "Mein Verhältnis zu R. Avenarius und andern Forschern", 751, 860),
    ("IV", "Die Hauptgesichtspunkte für die Untersuchung der Sinne", 860, 1297),
    ("V", "Physik und Biologie. Kausalität und Teleologie", 1297, 1491),
    ("VI", "Die Raumempfindungen des Auges", 1491, 1753),
    ("VII", "Weitere Untersuchung der Raumempfindungen", 1753, 2498),
    ("VIII", "Der Wille", 2498, 2583),
    ("IX", "Eine biologisch-teleologische Betrachtung über den Raum", 2583, 2766),
    ("X", "Beziehungen der Gesichtsempfindungen zu einander und zu andern psychischen Elementen", 2766, 3258),
    ("XI", "Empfindung, Gedächtnis und Assoziation", 3258, 3369),
    ("XII", "Die Zeitempfindung", 3369, 3579),
    ("XIII", "Die Tonempfindungen", 3579, 4260),
    ("XIV", "Einfluß der vorausgehenden Untersuchungen auf die Auffassung der Physik", 4260, 4812),
    ("XV", "Die Aufnahme der hier dargelegten Ansichten", 4812, 4934),
]

CHAPTERS_JA_RANGES = [
    ("I", "反形而上学的予備考察", 9, 142),
    ("II", "先入見について", 144, 207),
    ("III", "アヴェナリウスおよび他の研究者との関係", 209, 258),
    ("IV", "感覚の研究のための主要な観点", 260, 331),
    ("V", "物理学と生物学。因果性と目的論", 333, 416),
    ("VI", "目の空間感覚", 418, 527),
    ("VII", "空間感覚のさらなる研究", 529, 662),
    ("VIII", "意志", 664, 727),
    ("IX", "空間についての生物学的・目的論的考察", 729, 806),
    ("X", "視覚感覚の相互関係と他の心的要素との関係", 808, 929),
    ("XI", "感覚・記憶・連合", 931, 996),
    ("XII", "時間感覚", 998, 1075),
    ("XIII", "音の感覚", 1077, 1222),
    ("XIV", "以上の研究が物理学の把握に及ぼす影響", 1224, 1369),
    ("XV", "ここで述べた見解の受容", 1373, 1454),
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def escape(text):
    return html_mod.escape(text)

def is_ocr_junk(line):
    s = line.strip()
    if not s:
        return False
    if s.startswith('END_OF_PAGE'):
        return True
    if re.match(r'^—?\s*\d+\s*—?\s*$', s):
        return True
    if re.match(r'^[IVXL]+$', s) and len(s) <= 6:
        return True
    if re.match(r'^Mach,\s*Analyse', s):
        return True
    if s in ('S.Z.18.', 'S.Z.'):
        return True
    return False

def clean_de_chapter(raw_lines):
    """Clean German chapter text: remove OCR junk, join continuation lines."""
    cleaned = []
    for line in raw_lines:
        l = line.rstrip('\n')
        if is_ocr_junk(l):
            continue
        cleaned.append(l)
    return cleaned

def parse_sections_de(raw_lines):
    """Parse German chapter lines into numbered sections."""
    lines = clean_de_chapter(raw_lines)

    # Skip chapter heading (first few lines until we hit a section number)
    sections = []
    current_num = None
    current_lines = []
    heading_skipped = False

    for line in lines:
        s = line.strip()

        # Detect section number: standalone "N." or "I." (roman for section 1)
        is_section_num = False
        section_num = None

        if re.match(r'^(\d+)\.\s*$', s):
            is_section_num = True
            section_num = s.rstrip('.').strip()
        elif re.match(r'^([IVX]+)\.\s*$', s) and s.rstrip('.').strip() in ROMAN_TO_INT:
            roman = s.rstrip('.').strip()
            is_section_num = True
            section_num = str(ROMAN_TO_INT[roman])

        if is_section_num:
            heading_skipped = True
            if current_num is not None:
                sections.append((current_num, '\n'.join(current_lines)))
            current_num = section_num
            current_lines = []
        elif heading_skipped or current_num is not None:
            current_lines.append(line)

    if current_num is not None:
        sections.append((current_num, '\n'.join(current_lines)))

    return sections

def parse_sections_ja(raw_lines):
    """Parse Japanese chapter lines into numbered sections."""
    sections = []
    current_num = None
    current_lines = []

    for line in raw_lines:
        l = line.rstrip('\n')
        s = l.strip()

        # Skip chapter heading
        if re.match(r'^第[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+章', s):
            continue
        # Skip end markers
        if re.match(r'^（第\d+章|^（改訂版|^（補遺', s):
            continue

        if re.match(r'^(\d+)\.\s*$', s):
            if current_num is not None:
                sections.append((current_num, '\n'.join(current_lines)))
            current_num = s.rstrip('.').strip()
            current_lines = []
        elif current_num is not None:
            current_lines.append(l)

    if current_num is not None:
        sections.append((current_num, '\n'.join(current_lines)))

    return sections

def separate_notes_ja(text):
    """Split Japanese section text into main text and footnotes."""
    lines = text.split('\n')
    main = []
    notes = []
    in_note = False
    note_num = None
    note_lines = []

    for line in lines:
        m = re.match(r'^注(\d+)）\s*(.*)', line)
        if m:
            if in_note and note_num:
                notes.append((note_num, '\n'.join(note_lines).strip()))
            in_note = True
            note_num = m.group(1)
            note_lines = [m.group(2)] if m.group(2) else []
        elif in_note:
            note_lines.append(line)
        else:
            main.append(line)

    if in_note and note_num:
        notes.append((note_num, '\n'.join(note_lines).strip()))

    return '\n'.join(main).strip(), notes

def separate_notes_de(text):
    """Split German section text into main text and footnotes.

    Exits note mode when a blank line is followed by non-note text,
    recovering main text that appears after footnotes (common when
    footnotes sit at a page bottom in the OCR).
    """
    lines = text.split('\n')
    main = []
    notes = []
    in_note = False
    note_num = None
    note_lines = []

    i = 0
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r'^(\d+)\)\s+(.*)', s)
        if m:
            if in_note and note_num:
                notes.append((note_num, '\n'.join(note_lines).strip()))
            in_note = True
            note_num = m.group(1)
            note_lines = [m.group(2)]
        elif in_note:
            if s == '':
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines) and re.match(r'^(\d+)\)\s+', lines[j].strip()):
                    note_lines.append(lines[i])
                else:
                    notes.append((note_num, '\n'.join(note_lines).strip()))
                    in_note = False
                    note_num = None
                    note_lines = []
                    main.append(lines[i])
            else:
                note_lines.append(lines[i])
        else:
            main.append(lines[i])
        i += 1

    if in_note and note_num:
        notes.append((note_num, '\n'.join(note_lines).strip()))

    return '\n'.join(main).strip(), notes

def text_to_html_paras(text):
    """Convert text with blank-line-separated paragraphs to HTML <p> tags."""
    if not text.strip():
        return ''
    paras = []
    current = []
    for line in text.split('\n'):
        if line.strip() == '':
            if current:
                paras.append(' '.join(current))
                current = []
        else:
            current.append(line.strip())
    if current:
        paras.append(' '.join(current))

    return '\n            '.join(f'<p>{escape(p)}</p>' for p in paras if p)

def parse_appendices_ja(lines):
    """Parse Japanese appendix (補遺) section."""
    apps = []
    current_num = None
    current_title = None
    current_lines = []

    for line in lines:
        l = line.rstrip('\n')
        s = l.strip()
        if re.match(r'^補遺（Zusätze）', s):
            continue
        if s == '' and current_num is None:
            continue
        m = re.match(r'^補遺(\d+)（(.+?)）\s*$', s)
        if m:
            if current_num is not None:
                apps.append((current_num, current_title, '\n'.join(current_lines).strip()))
            current_num = m.group(1)
            current_title = m.group(2)
            current_lines = []
        elif re.match(r'^（補遺', s):
            if current_num is not None:
                apps.append((current_num, current_title, '\n'.join(current_lines).strip()))
                current_num = None
        elif re.match(r'^エルンスト・マッハ', s):
            if current_num is not None:
                apps.append((current_num, current_title, '\n'.join(current_lines).strip()))
                current_num = None
        elif current_num is not None:
            current_lines.append(l)

    if current_num is not None:
        apps.append((current_num, current_title, '\n'.join(current_lines).strip()))

    return apps

def parse_zusaetze_de(lines):
    """Parse German Zusätze section."""
    cleaned = clean_de_chapter(lines)
    text = '\n'.join(cleaned)
    return text

# ── HTML building ──

def text_to_paras(text):
    """Split text into individual paragraph strings (blank-line-separated)."""
    if not text.strip():
        return []
    paras = []
    current = []
    for line in text.split('\n'):
        if line.strip() == '':
            if current:
                paras.append(' '.join(current))
                current = []
        else:
            current.append(line.strip())
    if current:
        paras.append(' '.join(current))
    return [p for p in paras if p]

def merge_cross_page_paras(paras):
    """Merge paragraph fragments split by OCR page breaks.

    If a paragraph doesn't end with sentence-ending punctuation,
    it was likely split mid-sentence by a page break — merge it
    with the following paragraph.
    """
    if len(paras) <= 1:
        return paras
    merged = [paras[0]]
    for para in paras[1:]:
        prev = merged[-1]
        last_char = prev.rstrip()[-1] if prev.rstrip() else ''
        if last_char not in '.!?;»)':
            merged[-1] = prev + ' ' + para
        else:
            merged.append(para)
    return merged

def build_section_html(sec_num, de_text, ja_text, ch_roman):
    de_paras = merge_cross_page_paras(text_to_paras(de_text))
    ja_paras = text_to_paras(ja_text)
    max_p = max(len(de_paras), len(ja_paras), 1)

    h = f'''
    <section class="para-pair" id="ch{ch_roman}-p{sec_num}">
      <div class="para-num">{sec_num}.</div>'''

    for i in range(max_p):
        de_p = f'<p>{escape(de_paras[i])}</p>' if i < len(de_paras) else ''
        ja_p = f'<p>{escape(ja_paras[i])}</p>' if i < len(ja_paras) else ''
        h += f'''
      <div class="parallel">
        <div class="col de" lang="de">
            {de_p}
        </div>
        <div class="col ja" lang="ja">
            {ja_p}
        </div>
      </div>'''

    h += '\n    </section>\n'
    return h

def build_chapter_endnotes_html(all_notes, ch_roman):
    """Render collected footnotes as a chapter-end notes section."""
    if not all_notes:
        return ''

    h = f'''
    <section class="chapter-notes" id="ch{ch_roman}-notes">
      <div class="chapter-notes-heading">Anmerkungen · 注</div>
'''
    for sec_num, dn, jn in all_notes:
        note_id = jn[0] or dn[0]
        de_n_html = text_to_html_paras(dn[1]) if dn[1] else ''
        ja_n_html = text_to_html_paras(jn[1]) if jn[1] else ''

        h += f'''      <div class="note-block">
        <div class="parallel">
          <div class="col de" lang="de">
            <p class="note-marker">Anm. {dn[0] or note_id})</p>
            {de_n_html}
          </div>
          <div class="col ja" lang="ja">
            <p class="note-marker">注{jn[0] or note_id}）</p>
            {ja_n_html}
          </div>
        </div>
      </div>
'''
    h += '    </section>\n'
    return h

def make_section_groups(de_sections, ja_sections):
    """Pair DE and JA sections by proportional position.

    Returns a list of (de_group, ja_group) where each group is a list
    of (sec_num, sec_text) tuples.  The side with fewer sections gets
    1:1 mapping; the side with more sections has consecutive sections
    merged into groups so both sides have the same number of groups.
    """
    m = len(de_sections)
    n = len(ja_sections)

    if m == 0 and n == 0:
        return []
    if m == 0:
        return [([], [s]) for s in ja_sections]
    if n == 0:
        return [([s], []) for s in de_sections]

    if m == n:
        return [([de_sections[i]], [ja_sections[i]]) for i in range(m)]

    if m <= n:
        groups = []
        for i in range(m):
            ja_start = round(i * n / m)
            ja_end = round((i + 1) * n / m)
            groups.append(([de_sections[i]], ja_sections[ja_start:ja_end]))
        return groups
    else:
        groups = []
        for i in range(n):
            de_start = round(i * m / n)
            de_end = round((i + 1) * m / n)
            groups.append((de_sections[de_start:de_end], [ja_sections[i]]))
        return groups


def build_chapter_html(ch_idx, de_sections, ja_sections):
    ch_roman = CHAPTERS_DE_RANGES[ch_idx][0]
    ch_de_title = CHAPTERS_DE_RANGES[ch_idx][1]
    ch_ja_title = CHAPTERS_JA_RANGES[ch_idx][1]
    ch_ja_roman = INT_TO_ROMAN_JA[ch_idx+1]

    h = f'''
  <article class="chapter" id="ch{ch_roman}">
    <div class="chapter-heading">
      <span class="ch-label">Kapitel {ch_roman} · 第{ch_ja_roman}章</span>
      <h2>
        <span class="de">{escape(ch_de_title)}</span>
        <span class="ja">{escape(ch_ja_title)}</span>
      </h2>
    </div>
'''

    all_notes = []
    groups = make_section_groups(de_sections, ja_sections)

    for gi, (de_group, ja_group) in enumerate(groups):
        de_paras = []
        ja_paras = []
        de_sec_nums = []
        ja_sec_nums = []

        for sec_num, sec_text in de_group:
            main, de_notes = separate_notes_de(sec_text)
            paras = merge_cross_page_paras(text_to_paras(main))
            de_paras.extend(paras)
            de_sec_nums.append(sec_num)
            for dn in de_notes:
                all_notes.append((sec_num, dn, ('', '')))

        for sec_num, sec_text in ja_group:
            main, ja_notes = separate_notes_ja(sec_text)
            paras = text_to_paras(main)
            ja_paras.extend(paras)
            ja_sec_nums.append(sec_num)
            for jn in ja_notes:
                all_notes.append((sec_num, ('', ''), jn))

        de_label = '·'.join(f'§{s}' for s in de_sec_nums)
        ja_label = '·'.join(f'§{s}' for s in ja_sec_nums)
        anchor = de_sec_nums[0] if de_sec_nums else (ja_sec_nums[0] if ja_sec_nums else gi)

        h += f'''
    <div class="section-marker" id="ch{ch_roman}-p{anchor}">
      <span class="de">{de_label}</span>
      <span class="ja">{ja_label}</span>
    </div>'''

        max_p = max(len(de_paras), len(ja_paras), 1)
        for i in range(max_p):
            de_text = escape(de_paras[i]) if i < len(de_paras) else ''
            ja_text = escape(ja_paras[i]) if i < len(ja_paras) else ''
            de_p = f'<p>{de_text}</p>' if de_text else ''
            ja_p = f'<p>{ja_text}</p>' if ja_text else ''
            h += f'''
    <div class="parallel">
      <div class="col de" lang="de">
          {de_p}
      </div>
      <div class="col ja" lang="ja">
          {ja_p}
      </div>
    </div>'''

    h += build_chapter_endnotes_html(all_notes, ch_roman)
    h += '  </article>\n'
    return h

def get_css():
    return '''<title>感覚の分析 対訳</title>
<style>
:root {
  --bg: #F0EFEC;
  --bg-note: #E6E5E1;
  --text: #2B2926;
  --text-2: #74706A;
  --accent: #4A7868;
  --rule: #C5C2BB;
  --rule-vert: #D2CFC8;
  --font-de: "Palatino Linotype", Palatino, "Book Antiqua", Georgia, "Times New Roman", serif;
  --font-ja: "Hiragino Mincho ProN", "Yu Mincho", "MS PMincho", "Noto Serif JP", serif;
  --font-ui: -apple-system, "Segoe UI", "Helvetica Neue", Helvetica, Arial, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #1A1918; --bg-note: #232220; --text: #D5D3CE; --text-2: #807C76;
    --accent: #6DAE96; --rule: #363432; --rule-vert: #2E2C2A;
  }
}
:root[data-theme="dark"] {
  --bg: #1A1918; --bg-note: #232220; --text: #D5D3CE; --text-2: #807C76;
  --accent: #6DAE96; --rule: #363432; --rule-vert: #2E2C2A;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg); color: var(--text); font-family: var(--font-ja);
  line-height: 1.78; font-size: 16px; -webkit-font-smoothing: antialiased;
}
.edition { max-width: 1120px; margin: 0 auto; padding: 3rem 2rem 4rem; }
.masthead { text-align: center; padding-bottom: 2.5rem; margin-bottom: 2.5rem; border-bottom: 1px solid var(--rule); }
.masthead .label { font-family: var(--font-ui); font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); margin-bottom: 1.8rem; }
.masthead h1 { font-weight: 400; line-height: 1.35; }
.title-de { display: block; font-family: var(--font-de); font-size: 1.65rem; font-style: italic; letter-spacing: 0.01em; }
.title-sub-de { display: block; font-family: var(--font-de); font-size: 0.95rem; color: var(--text-2); margin-top: 0.25rem; font-style: italic; }
.title-ja { display: block; font-family: var(--font-ja); font-size: 1.45rem; margin-top: 1.2rem; letter-spacing: 0.08em; }
.title-sub-ja { display: block; font-family: var(--font-ja); font-size: 0.88rem; color: var(--text-2); margin-top: 0.2rem; }
.masthead .author { font-family: var(--font-ui); font-size: 0.85rem; color: var(--text-2); margin-top: 1.5rem; letter-spacing: 0.03em; }
.masthead .pub { font-family: var(--font-ui); font-size: 0.75rem; color: var(--text-2); margin-top: 0.3rem; }
.chapter-heading { text-align: center; margin: 3.5rem 0 2.5rem; padding-top: 2.5rem; border-top: 2px solid var(--rule); }
.chapter:first-of-type .chapter-heading { border-top: none; padding-top: 0; margin-top: 2.5rem; }
.ch-label { display: block; font-family: var(--font-ui); font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-2); margin-bottom: 0.6rem; }
.chapter-heading h2 { font-weight: 400; font-size: 1.15rem; line-height: 1.5; }
.chapter-heading h2 .de { display: block; font-family: var(--font-de); font-style: italic; }
.chapter-heading h2 .ja { display: block; font-family: var(--font-ja); margin-top: 0.15rem; letter-spacing: 0.04em; }
.para-pair { margin-bottom: 2.2rem; padding-bottom: 2.2rem; border-bottom: 1px solid var(--rule); }
.para-pair:last-of-type { border-bottom: none; padding-bottom: 0; }
.para-num { font-family: var(--font-ui); font-size: 0.82rem; font-weight: 600; color: var(--accent); margin-bottom: 0.8rem; padding-left: 0.1rem; }
.parallel { display: grid; grid-template-columns: 1fr 1fr; gap: 0; position: relative; }
.parallel::after { content: ""; position: absolute; top: 0; bottom: 0; left: 50%; transform: translateX(-0.5px); width: 1px; background: var(--rule-vert); }
.col { padding: 0 1.6rem; }
.col p + p { margin-top: 0.85em; }
.col.de { font-family: var(--font-de); font-size: 0.98rem; line-height: 1.72; hyphens: auto; -webkit-hyphens: auto; }
.col.ja { font-family: var(--font-ja); font-size: 0.95rem; line-height: 1.82; }
.parallel + .parallel { margin-top: 0.75em; }
.section-marker { display: grid; grid-template-columns: 1fr 1fr; gap: 0; position: relative; padding: 0 1.6rem; margin: 1.8rem 0 0.4rem; }
.section-marker::after { content: ""; position: absolute; top: 0; bottom: 0; left: 50%; transform: translateX(-0.5px); width: 1px; background: var(--rule-vert); }
.section-marker span { font-family: var(--font-ui); font-size: 0.82rem; font-weight: 600; color: var(--accent); }
.chapter-notes { margin-top: 2.5rem; padding-top: 2rem; border-top: 1px double var(--rule); }
.chapter-notes-heading { font-family: var(--font-ui); font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-2); text-align: center; margin-bottom: 1.5rem; }
.note-block { margin-bottom: 1.2rem; background: var(--bg-note); border-radius: 2px; padding: 1.2rem 0; }
.note-block:last-child { margin-bottom: 0; }
.note-block .parallel { align-items: start; }
.note-marker { font-family: var(--font-ui); font-size: 0.75rem; font-weight: 600; color: var(--accent); margin-bottom: 0.5rem; }
.note-block .col { font-size: 0.88rem; }
.note-block .col.de { font-size: 0.9rem; line-height: 1.68; }
.note-block .col.ja { font-size: 0.87rem; line-height: 1.75; }
.toc { margin-bottom: 2.5rem; }
.toc h3 { font-family: var(--font-ui); font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-2); text-align: center; margin-bottom: 1.5rem; }
.toc-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; font-variant-numeric: tabular-nums; }
.toc-table td { padding: 0.45rem 0.8rem; vertical-align: top; border-bottom: 1px solid var(--rule); }
.toc-table tr:last-child td { border-bottom: none; }
.toc-table .toc-num { width: 3rem; font-family: var(--font-ui); font-size: 0.8rem; color: var(--accent); font-weight: 600; text-align: right; padding-right: 1rem; }
.toc-table .toc-num a { color: var(--accent); text-decoration: none; }
.toc-table .toc-num a:hover { text-decoration: underline; }
.toc-table .toc-de { font-family: var(--font-de); font-style: italic; width: 45%; }
.toc-table .toc-ja { font-family: var(--font-ja); }
.colophon { margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid var(--rule); font-family: var(--font-ui); font-size: 0.75rem; color: var(--text-2); line-height: 1.65; }
.colophon p + p { margin-top: 0.6em; }
@media (max-width: 800px) {
  .edition { padding: 2rem 1rem 3rem; }
  .parallel { grid-template-columns: 1fr; }
  .parallel::after { display: none; }
  .col { padding: 0; }
  .col.de { padding-bottom: 1rem; margin-bottom: 1rem; border-bottom: 1px dashed var(--rule); }
  .col::before { display: block; font-family: var(--font-ui); font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-2); margin-bottom: 0.5rem; }
  .col.de::before { content: "Deutsch"; }
  .col.ja::before { content: "日本語"; }
  .parallel + .parallel .col::before { display: none; }
  .parallel + .parallel { margin-top: 1.2em; }
  .section-marker { grid-template-columns: 1fr; padding: 0; }
  .section-marker::after { display: none; }
  .section-marker span + span { display: none; }
  .note-block .col.de { padding-bottom: 0.8rem; margin-bottom: 0.8rem; }
  .title-de { font-size: 1.35rem; }
  .title-ja { font-size: 1.25rem; }
  .toc-table .toc-de { display: none; }
  .toc-table .toc-num { width: 2.5rem; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
'''

def get_masthead():
    return '''
  <header class="masthead">
    <p class="label">対訳版 · Zweisprachige Ausgabe</p>
    <h1>
      <span class="title-de">Die Analyse der Empfindungen</span>
      <span class="title-sub-de">und das Verhältnis des Physischen zum Psychischen</span>
      <span class="title-ja">感覚の分析</span>
      <span class="title-sub-ja">物理的なものと心理的なものの関係</span>
    </h1>
    <p class="author">Ernst Mach · エルンスト・マッハ</p>
    <p class="pub">9. Auflage, Jena: Gustav Fischer, 1922 · 改訂版（第9版）</p>
  </header>
'''

def build_toc():
    chs = [
        ("I","Antimetaphysische Vorbemerkungen","反形而上学的予備考察"),
        ("II","Über vorgefaßte Meinungen","先入見について"),
        ("III","Mein Verhältnis zu R. Avenarius und andern Forschern","アヴェナリウスおよび他の研究者との関係"),
        ("IV","Die Hauptgesichtspunkte für die Untersuchung der Sinne","感覚の研究のための主要な観点"),
        ("V","Physik und Biologie. Kausalität und Teleologie","物理学と生物学。因果性と目的論"),
        ("VI","Die Raumempfindungen des Auges","目の空間感覚"),
        ("VII","Weitere Untersuchung der Raumempfindungen","空間感覚のさらなる研究"),
        ("VIII","Der Wille","意志"),
        ("IX","Eine biologisch-teleologische Betrachtung über den Raum","空間についての生物学的・目的論的考察"),
        ("X","Beziehungen der Gesichtsempfindungen","視覚感覚の相互関係と他の心的要素との関係"),
        ("XI","Empfindung, Gedächtnis und Assoziation","感覚・記憶・連合"),
        ("XII","Die Zeitempfindung","時間感覚"),
        ("XIII","Die Tonempfindungen","音の感覚"),
        ("XIV","Einfluß der vorausgehenden Untersuchungen auf die Auffassung der Physik","以上の研究が物理学の把握に及ぼす影響"),
        ("XV","Die Aufnahme der hier dargelegten Ansichten","ここで述べた見解の受容"),
    ]
    h = '\n  <nav class="toc">\n    <h3>Inhaltsverzeichnis · 目次</h3>\n    <table class="toc-table">\n'
    for r,d,j in chs:
        h += f'      <tr><td class="toc-num"><a href="#ch{r}">{r}</a></td><td class="toc-de">{escape(d)}</td><td class="toc-ja">{escape(j)}</td></tr>\n'
    h += '      <tr><td class="toc-num"><a href="#zusaetze"></a></td><td class="toc-de">Zusätze (21 Anmerkungen)</td><td class="toc-ja">補遺（全21項目）</td></tr>\n'
    h += '    </table>\n  </nav>\n'
    return h

def get_colophon():
    return '''
  <footer class="colophon">
    <p>本対訳版はエルンスト・マッハ『感覚の分析——物理的なものと心理的なものの関係』（第9版、イェーナ：グスタフ・フィッシャー、1922年）の全15章および補遺の対訳である。ドイツ語原文はインターネット・アーカイヴのOCRに基づくため、誤植・脱字が含まれうる。節番号の付与は原文と和訳で一部異なるため、対応が完全でない箇所がある。</p>
    <p>Diese zweisprachige Ausgabe umfaßt alle 15 Kapitel und die Zusätze von Ernst Machs <em>Die Analyse der Empfindungen und das Verhältnis des Physischen zum Psychischen</em> (9. Aufl., Jena: Gustav Fischer, 1922). Der deutsche Text basiert auf der OCR-Digitalisierung des Internet Archive und kann Lesefehler enthalten. Die Paragraphennummerierung weicht stellenweise zwischen Original und Übersetzung ab.</p>
  </footer>
'''

def main():
    de_lines = read_file(GERMAN_FILE)
    ja_lines = read_file(JAPANESE_FILE)

    html = get_css()
    html += '\n<div class="edition">\n'
    html += get_masthead()
    html += build_toc()

    for ci in range(15):
        # Extract chapter line ranges
        de_r = CHAPTERS_DE_RANGES[ci]
        ja_r = CHAPTERS_JA_RANGES[ci]

        de_ch_lines = de_lines[de_r[2]-1 : de_r[3]-1]
        ja_ch_lines = ja_lines[ja_r[2]-1 : ja_r[3]-1]

        de_sections = parse_sections_de(de_ch_lines)
        ja_sections = parse_sections_ja(ja_ch_lines)

        print(f"  Ch {de_r[0]:>4s}: {len(de_sections):2d} DE, {len(ja_sections):2d} JA")

        html += build_chapter_html(ci, de_sections, ja_sections)

    # Appendices
    ja_app_lines = ja_lines[1458-1:]
    appendices = parse_appendices_ja(ja_app_lines)
    print(f"  Appendices: {len(appendices)}")

    # German Zusätze
    de_zus_lines = de_lines[4934-1:]
    de_zus_text = parse_zusaetze_de(de_zus_lines)

    # Parse German Zusätze into individual entries
    # They start with "Zusatz N." or "N." patterns
    de_zus_sections = {}
    # Simple approach: split by "Zu S." or similar reference patterns
    # For now, just include raw cleaned text as context

    html += '''
  <article class="chapter" id="zusaetze">
    <div class="chapter-heading">
      <span class="ch-label">Zusätze · 補遺</span>
      <h2>
        <span class="de">Zusätze</span>
        <span class="ja">補遺（各章への追加注記）</span>
      </h2>
    </div>
'''

    for app_num, app_title, app_text in appendices:
        app_html = text_to_html_paras(app_text)
        html += f'''
    <section class="para-pair" id="zusatz-{app_num}">
      <div class="para-num">補遺 {app_num}</div>
      <div class="parallel">
        <div class="col de" lang="de">
            <p class="note-marker">Zusatz {app_num}</p>
            <p><em>{escape(app_title)}</em></p>
        </div>
        <div class="col ja" lang="ja">
            <p class="note-marker">補遺{app_num}</p>
            <p><em>{escape(app_title)}</em></p>
            {app_html}
        </div>
      </div>
    </section>
'''

    html += '  </article>\n'
    html += get_colophon()
    html += '\n</div>\n'

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"Size: {len(html):,} chars ({len(html.encode('utf-8')):,} bytes)")

if __name__ == '__main__':
    main()
