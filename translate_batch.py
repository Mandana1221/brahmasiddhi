#!/usr/bin/env python3
"""Generate TSV translation files from parsed verse data.
This outputs the Sanskrit with a placeholder for manual/AI translation.

Usage: python3 translate_batch.py <kanda_num> <start_sarga> <end_sarga> <output_tsv>
"""

import re, sys
from pathlib import Path
from collections import OrderedDict

SRC = Path(__file__).parent / "sa_rAmAyaNa_2.txt"
REF_RE = re.compile(r'\s+(R_(\d+),(\d+)\.(\d+)([a-h])?)\s*$')


def parse_kanda(src_path, target_kanda, start_sarga, end_sarga):
    text = src_path.read_text(encoding='utf-8')
    in_text = False
    current_lines = []
    verses = []

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
                    k = int(m.group(2))
                    s = int(m.group(3))
                    v = int(m.group(4))
                    if k == target_kanda and start_sarga <= s <= end_sarga:
                        cleaned_last = last[:m.start()].strip()
                        padas = [cl.strip() for cl in current_lines[:-1]]
                        if cleaned_last:
                            padas.append(cleaned_last)
                        ref = f"{k}.{s}.{v}"
                        skt = ' / '.join(padas)
                        verses.append((ref, skt))
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
            if k == target_kanda and start_sarga <= s <= end_sarga:
                cleaned_last = last[:m.start()].strip()
                padas = [cl.strip() for cl in current_lines[:-1]]
                if cleaned_last:
                    padas.append(cleaned_last)
                ref = f"{k}.{s}.{v}"
                skt = ' / '.join(padas)
                verses.append((ref, skt))

    return verses


if __name__ == '__main__':
    kanda = int(sys.argv[1])
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    out = sys.argv[4]

    verses = parse_kanda(SRC, kanda, start, end)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(f"# Kāṇḍa {kanda}, Sargas {start}-{end}\n")
        f.write(f"# {len(verses)} verses\n")
        for ref, skt in verses:
            f.write(f"# SKT: {skt}\n")
            f.write(f"{ref}\t【未訳】\n")

    print(f"Wrote {len(verses)} verses to {out}")
