#!/usr/bin/env python3
"""Parse Rāmāyaṇa plain-text and generate per-kāṇḍa bilingual HTML shells."""

import re, sys, html as H
from pathlib import Path
from collections import OrderedDict

SRC = Path(__file__).parent / "sa_rAmAyaNa_2.txt"

KANDA_NAMES = {
    1: ("バーラカーンダ", "Bālakāṇḍa"),
    2: ("アヨーディヤーカーンダ", "Ayodhyākāṇḍa"),
    3: ("アーラニヤカーンダ", "Āraṇyakāṇḍa"),
    4: ("キシュキンダーカーンダ", "Kiṣkindhākāṇḍa"),
    5: ("スンダラカーンダ", "Sundarakāṇḍa"),
    6: ("ユッダカーンダ", "Yuddhakāṇḍa"),
    7: ("ウッタラカーンダ", "Uttarakāṇḍa"),
}

CSS = """\
  :root {
    --ground: #f5f2e8; --ground-deep: #ece8da; --surface: #e6e1d1;
    --text: #2b2922; --text-secondary: #6b6455;
    --accent: #4e6e52; --accent-light: #dce5dc; --accent-muted: #7a9a7e;
    --ref: #9b8968; --border: #c4b898; --border-light: #d8d0bb;
    --verse-bg: #edeade;
    --header-bg: #2e3830; --header-text: #e8e4d6; --header-sub: #a8b8a4;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --ground: #1a1d1a; --ground-deep: #141714; --surface: #232823;
      --text: #d4d0c4; --text-secondary: #8a857a;
      --accent: #7aab7e; --accent-light: #2a3a2c; --accent-muted: #5e8a62;
      --ref: #b8a47a; --border: #3e4a3e; --border-light: #2e382e;
      --verse-bg: #1e231e;
      --header-bg: #0e120e; --header-text: #d4d0c4; --header-sub: #6e8a6e;
    }
  }
  :root[data-theme="dark"] {
    --ground: #1a1d1a; --ground-deep: #141714; --surface: #232823;
    --text: #d4d0c4; --text-secondary: #8a857a;
    --accent: #7aab7e; --accent-light: #2a3a2c; --accent-muted: #5e8a62;
    --ref: #b8a47a; --border: #3e4a3e; --border-light: #2e382e;
    --verse-bg: #1e231e;
    --header-bg: #0e120e; --header-text: #d4d0c4; --header-sub: #6e8a6e;
  }
  :root[data-theme="light"] {
    --ground: #f5f2e8; --ground-deep: #ece8da; --surface: #e6e1d1;
    --text: #2b2922; --text-secondary: #6b6455;
    --accent: #4e6e52; --accent-light: #dce5dc; --accent-muted: #7a9a7e;
    --ref: #9b8968; --border: #c4b898; --border-light: #d8d0bb;
    --verse-bg: #edeade;
    --header-bg: #2e3830; --header-text: #e8e4d6; --header-sub: #a8b8a4;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Yu Mincho', 'Hiragino Mincho ProN', 'Noto Serif JP', serif;
    background: var(--ground); color: var(--text); line-height: 1.7;
  }
  header {
    background: var(--header-bg); color: var(--header-text);
    padding: 3em 1.5em 2.4em; text-align: center;
  }
  header h1 { font-size: 1.9em; letter-spacing: 0.18em; font-weight: 700; margin-bottom: 0.25em; }
  header .skt-title {
    font-family: Georgia, 'DejaVu Serif', serif; font-style: italic;
    font-size: 1.05em; color: var(--header-sub); letter-spacing: 0.06em; margin-bottom: 0.6em;
  }
  header .meta { font-size: 0.82em; color: var(--header-sub); opacity: 0.7; margin-top: 0.8em; }
  .kanda-label {
    background: var(--ground-deep); border-bottom: 1px solid var(--border-light);
    padding: 1em 1.5em; text-align: center; font-size: 0.85em;
    color: var(--text-secondary); letter-spacing: 0.15em;
  }
  .sarga-header {
    display: flex; align-items: center; gap: 1em;
    padding: 1.2em 2em; background: var(--accent-light);
    border-bottom: 2px solid var(--accent-muted);
  }
  .sarga-header .sarga-num {
    font-family: Georgia, 'DejaVu Serif', serif; font-size: 1.6em;
    font-weight: 700; color: var(--accent); line-height: 1; flex-shrink: 0;
  }
  .sarga-header .sarga-info { display: flex; flex-direction: column; gap: 0.15em; }
  .sarga-header .sarga-info .ja { font-size: 1.05em; font-weight: 700; color: var(--accent); }
  .sarga-header .sarga-info .skt {
    font-family: Georgia, 'DejaVu Serif', serif; font-style: italic;
    font-size: 0.88em; color: var(--text-secondary);
  }
  .wrap { max-width: 1200px; margin: 0 auto; padding: 0 0 4em; }
  table { width: 100%; border-collapse: collapse; }
  tr.verse-row { border-bottom: 1px solid var(--border-light); }
  tr.verse-row:last-child { border-bottom: none; }
  td { vertical-align: top; padding: 1em 1.8em; width: 50%; }
  td.skt-cell { border-right: 2px solid var(--border); }
  .verse-num {
    display: block; font-family: Georgia, 'DejaVu Serif', serif;
    font-size: 0.72em; color: var(--ref); letter-spacing: 0.05em; margin-bottom: 0.5em;
  }
  .skt-verse {
    font-family: Georgia, 'DejaVu Serif', serif;
    font-size: 0.94em; line-height: 1.85; color: var(--text);
  }
  .skt-verse .pada { display: block; }
  .skt-verse .pada + .pada { margin-top: 0.15em; }
  .jpn-verse { font-size: 0.92em; line-height: 1.95; color: var(--text); }
  footer {
    text-align: center; padding: 2em 1.5em; font-size: 0.78em;
    color: var(--text-secondary); border-top: 1px solid var(--border-light); margin: 0 2em;
  }
  @media (max-width: 800px) {
    header h1 { font-size: 1.4em; }
    td { display: block; width: 100%; border-right: none !important; padding: 0.8em 1.2em; }
    td.skt-cell { border-bottom: 1px dashed var(--border-light); }
    .sarga-header { padding: 1em 1.2em; }
  }
"""

REF_RE = re.compile(r'\s+(R_(\d+),(\d+)\.(\d+)([a-h])?)\s*$')


def parse(src_path):
    """Return {kanda_num: {sarga_num: [(verse_num, [padas])]} }"""
    data = OrderedDict()
    text = src_path.read_text(encoding='utf-8')

    in_text = False
    current_lines = []
    for raw_line in text.split('\n'):
        line = raw_line.rstrip()
        if not in_text:
            if line.strip() == '# Text':
                in_text = True
            continue

        if line == '':
            if current_lines:
                last = current_lines[-1]
                m = REF_RE.search(last)
                if m:
                    ref_full = m.group(1)
                    k = int(m.group(2))
                    s = int(m.group(3))
                    v = int(m.group(4))
                    cleaned_last = last[:m.start()].strip()
                    padas = []
                    for cl in current_lines[:-1]:
                        padas.append(cl.strip())
                    if cleaned_last:
                        padas.append(cleaned_last)
                    data.setdefault(k, OrderedDict()).setdefault(s, []).append((v, padas))
                current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        last = current_lines[-1]
        m = REF_RE.search(last)
        if m:
            k = int(m.group(2))
            s = int(m.group(3))
            v = int(m.group(4))
            cleaned_last = last[:m.start()].strip()
            padas = []
            for cl in current_lines[:-1]:
                padas.append(cl.strip())
            if cleaned_last:
                padas.append(cleaned_last)
            data.setdefault(k, OrderedDict()).setdefault(s, []).append((v, padas))

    return data


def render_kanda(kanda_num, sargas, out_path):
    ja_name, skt_name = KANDA_NAMES[kanda_num]
    total_verses = sum(len(vs) for vs in sargas.values())
    total_sargas = len(sargas)

    parts = []
    parts.append(f'<title>ラーマーヤナ 第{kanda_num}巻 対訳 — Rāmāyaṇa {kanda_num} {skt_name}</title>')
    parts.append(f'<style>{CSS}</style>')
    parts.append(f'<header>')
    parts.append(f'  <h1>ラーマーヤナ 第{kanda_num}巻 対訳</h1>')
    parts.append(f'  <div class="skt-title">Vālmīki-Rāmāyaṇa — {skt_name} — Bilingual Edition</div>')
    parts.append(f'  <div class="meta">全{total_sargas}章・{total_verses}詩節</div>')
    parts.append(f'</header>')
    parts.append(f'<div class="wrap">')
    parts.append(f'<div class="kanda-label">第{kanda_num}巻　{ja_name} ― {skt_name}</div>')

    for sarga_num, verses in sargas.items():
        parts.append(f'<div class="sarga-header">')
        parts.append(f'  <div class="sarga-num">{sarga_num}</div>')
        parts.append(f'  <div class="sarga-info">')
        parts.append(f'    <span class="ja">第{sarga_num}章</span>')
        parts.append(f'    <span class="skt">Sarga {sarga_num}</span>')
        parts.append(f'  </div>')
        parts.append(f'</div>')
        parts.append(f'<table>')

        for verse_num, padas in verses:
            ref_display = f'R {kanda_num}.{sarga_num}.{verse_num}'
            ref_short = f'{kanda_num}.{sarga_num}.{verse_num}'
            pada_html = ''.join(f'<span class="pada">{H.escape(p)}</span>' for p in padas)

            parts.append(f'<tr class="verse-row">')
            parts.append(f'<td class="skt-cell">')
            parts.append(f'  <span class="verse-num">{H.escape(ref_display)}</span>')
            parts.append(f'  <div class="skt-verse">{pada_html}</div>')
            parts.append(f'</td>')
            parts.append(f'<td class="jpn-cell">')
            parts.append(f'  <span class="verse-num">{H.escape(ref_short)}</span>')
            parts.append(f'  <div class="jpn-verse">【未訳】</div>')
            parts.append(f'</td>')
            parts.append(f'</tr>')

        parts.append(f'</table>')

    parts.append(f'</div>')
    parts.append(f'<footer>')
    parts.append(f'  底本：GRETIL — Göttingen Register of Electronic Texts in Indian Languages<br>')
    parts.append(f'  Data entry: Muneo Tokunaga / Contribution: John Smith / CC BY-NC-SA 4.0')
    parts.append(f'</footer>')

    out_path.write_text('\n'.join(parts), encoding='utf-8')
    return total_sargas, total_verses


def main():
    data = parse(SRC)
    out_dir = Path(__file__).parent
    for k, sargas in data.items():
        fname = f"ramayana_k{k}_bilingual.html"
        out_path = out_dir / fname
        ns, nv = render_kanda(k, sargas, out_path)
        print(f"  {fname}: {ns} sargas, {nv} verses")
    print(f"Done — {len(data)} files generated.")


if __name__ == '__main__':
    main()
