"""NVTT 全訳（nvtt_src/partXX.txt）から、Thakur 版の番号つきスートラ一覧（IAST）を作る。"""
import re, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TEXT = (ROOT / 'NVTT_text.txt').read_text(encoding='utf-8').split('\n')
RANGE = re.compile(r'([1-5])\.([12])\.(\d+)(付)?(?:\s*[–-]\s*(?:[1-5]\.[12]\.)?(\d+))?')

def nums(tag):
    out = []
    for m in RANGE.finditer(tag):
        a, b, c = m.group(1), m.group(2), int(m.group(3))
        if m.group(4):
            out.append(f'{a}.{b}.{c}付'); continue
        d = int(m.group(5)) if m.group(5) else c
        out += [f'{a}.{b}.{n}' for n in range(c, d + 1)]
    return out

res = []
for p in sorted((ROOT / 'nvtt_src').glob('part*.txt')):
    want, inblk = [], False
    for line in p.read_text(encoding='utf-8').split('\n'):
        m = re.match(r'^(#+)\s+(\S+)\s*\|\s*([^|]*?)\s*(?:\|\s*(.*))?$', line)
        if m:
            inblk = m.group(2).endswith('.0') and (m.group(4) or '').startswith('NS')
            if inblk:
                want = nums(m.group(4))
            continue
        m = re.match(r'^V\s+(\d+)-(\d+)', line)
        if m and inblk:
            for ln in TEXT[int(m.group(1)) - 1:int(m.group(2))]:
                if ln.startswith('nys_') and want:
                    res.append((want.pop(0), re.sub(r'\[p\. \d+\]', '', ln.split(':', 1)[1]).strip(' /')))
json.dump(res, open(ROOT / 'nbh_src' / 'canon.json', 'w'), ensure_ascii=False, indent=0)
print(len(res))
from collections import Counter
print(Counter(k.rsplit('.',1)[0] for k,_ in res))
print(res[:3], res[-2:])
