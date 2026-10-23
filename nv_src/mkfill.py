#!/usr/bin/env python3
"""NV 対訳ページの省略を補う「補完ファイル」nv_src/fill/NN.txt の下書きを作る。

  python3 nv_src/mkfill.py NN [NN ...]

各省略について、前後の文脈（< と >）、OCR から取り出した原文（S）、和訳を書く欄（J）を並べる。
S が「=」の項目は、刊本そのものの省略（スートラなどを冒頭と末尾だけで示すもの）で、補わない。
すでにファイルがあれば作らない。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gaps  # noqa: E402

FILL = gaps.ROOT / 'nv_src' / 'fill'


def tidy(t):
    """OCR の本文を対訳ページの書き方に揃える。"""
    t = re.sub(r'\[p\. \d+\]', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s*([।॥?])\s*', r' \1 ', t)
    t = re.sub(r'॥ ([०-९।]+) ॥', r'॥\1॥', t)
    return re.sub(r'^[।॥?,\s]+', '', t.strip())


def main():
    for a in sys.argv[1:]:
        out = FILL / f'{int(a):02d}.txt'
        if out.exists():
            print('exists', out)
            continue
        f = gaps.PAGES / f'nyayavarttika-{int(a)}-taiyaku.html'
        lines = [f'# NV 対訳 {a} の省略の補完。S = 補う原文（= は刊本どおりの省略で補わない）、J = 和訳。', '']
        for g in gaps.gaps_of(f):
            lines.append(f'@ {g["block"]} {g["gap"]}  pp.{g["pp"]}')
            lines.append('< ' + re.sub(r'<[^>]+>', ' ', g['left']).strip())
            lines.append('> ' + re.sub(r'<[^>]+>', ' ', g['right']).strip())
            t = g.get('text')
            if t is None:
                lines.append('S ?')
            elif re.search(r'\.\.\.|…', t) and len(gaps.norm(t)[0]) < 60:
                lines.append('S =')
            else:
                lines.append('S ' + tidy(t))
            lines.append('J ')
            lines.append('')
        out.write_text('\n'.join(lines), encoding='utf-8')
        print('wrote', out)


if __name__ == '__main__':
    main()
