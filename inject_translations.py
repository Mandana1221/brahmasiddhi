#!/usr/bin/env python3
"""Inject Japanese translations into bilingual HTML files.

Usage: python3 inject_translations.py <html_file> <translations_tsv>

TSV format: ref<TAB>japanese_translation
  e.g.: 1.1.1\t苦行と聖典の学習に専心し……
"""

import sys, re, html as H
from pathlib import Path


def inject(html_path, tsv_path):
    translations = {}
    for line in Path(tsv_path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t', 1)
        if len(parts) == 2:
            translations[parts[0].strip()] = parts[1].strip()

    content = Path(html_path).read_text(encoding='utf-8')

    count = 0
    for ref, jpn in translations.items():
        old = f'<span class="verse-num">{H.escape(ref)}</span>\n  <div class="jpn-verse">【未訳】</div>'
        new = f'<span class="verse-num">{H.escape(ref)}</span>\n  <div class="jpn-verse">{H.escape(jpn)}</div>'
        if old in content:
            content = content.replace(old, new, 1)
            count += 1

    Path(html_path).write_text(content, encoding='utf-8')
    print(f"Injected {count}/{len(translations)} translations into {html_path}")
    remaining = content.count('【未訳】')
    print(f"Remaining untranslated: {remaining}")


if __name__ == '__main__':
    inject(sys.argv[1], sys.argv[2])
