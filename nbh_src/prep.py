#!/usr/bin/env python3
"""ヴァーツヤーヤナ『ニヤーヤ・バーシュヤ』（Thakur 校訂本 OCR）から NBh_text.txt を作る。

OCR は頁ごとに END_OF_PAGE_NNN で区切られ、刊本の pp.1–50, 149–320, 索引, 51–148 の順に並んでいる。
これを刊本の頁順に並べ、柱（頁の見出し）・行番号・脚注・脚注番号を落とし、
本文を daṇḍa（।）ごとに 1 行にする。
  [p. N]                頁の始まり（行頭）
  nys_a,b.c: … //       スートラ（番号は Thakur 版。位置は nbh_src/canon.json と照合して決める）
  @ [वा पृः …; टी पृः …; प पृः …]   NV・NVTT・NVTP の対応頁（刊本の注記）
  @@ …प्रकरणम्           論題の見出し
訂正は nbh_src/corrections.txt（書式は NVTT と同じ）を最後に当てる。
使い方: python3 nbh_src/prep.py OCR.txt
"""
import bisect
import difflib
import json
import re
import sys
from pathlib import Path

from indic_transliteration import sanscript

ROOT = Path(__file__).resolve().parent.parent
DIG = str.maketrans('०१२३४५६७८९', '0123456789')
DEVA = r'ऀ-ॣ॰-ॿ'      # 文字（数字 ०–९ を除く）
MARKRE = r'॥(?=(?:[\s।]*[०-९]){3})[\s।०-९]{3,14}॥'      # スートラの印（OCR で区切りが崩れたものも）

raw = Path(sys.argv[1]).read_text(encoding='utf-8')
pages = re.split(r'END_OF_PAGE_\d+\n?', raw)
# 刊本の頁順：OCR の 0–49（pp.1–50）、271–319・322–370（pp.51–148。320–321 は pp.98–99 の重複）、
# 50–154（pp.149–253）、185–186（pp.254–255。OCR では p.285 の後に入っている）、155–184・187–221（pp.256–320）
order = (list(range(0, 50)) + list(range(271, 320)) + list(range(322, 371)) + list(range(50, 155))
         + [185, 186] + list(range(155, 185)) + list(range(187, 222)))
assert len(order) == 320


def clean_page(text):
    out, body = [], False
    for ln in text.split('\n'):
        s = ln.strip()
        if not body:            # 柱：頁番号・書名・[सूत्र・「1.1.1] 論題名 頁」
            if not s:
                continue
            if (re.match(r'^[०-९]+\s*$', s) or ('न्यायदर्शनम्' in s and len(s) < 60)
                    or s.startswith('[सूत्र') or re.match(r'^[०-९]+\.[०-९]+\.[०-९]+\s*\]', s)
                    or s == 'सवात्स्यायनभाष्यं'):
                continue
            body = True
        out.append(ln)
    # 脚注：最後の「१. 」で始まる行から後
    fn = None
    for i, ln in enumerate(out):
        if re.match(r'^\s*१\.\s', ln):
            fn = i
    if fn is not None:
        out = out[:fn]
    while out and re.match(r'^\s*(पृ:\s*[०-९]+)?\s*$', out[-1]):
        out.pop()
    body = '\n'.join(out)
    return re.sub(r'(?m)^\s*(?:५|१०|१५|२०|२५|३०)\s+(?=\S)', '', body)      # 行番号


def norm(t):
    t = re.sub(rf'(?<=[{DEVA}]):', 'ः', t)                  # 「:」の visarga
    t = t.replace('।।', '॥').replace('||', '॥').replace('॰', '०')
    t = re.sub(r'॥\s*([०-९]+)\s*।\s*([०-९]+)\s*।\s*([०-९]+)\s*॥', r'॥\1।\2।\3॥', t)
    # OCR で崩れたスートラの印：「॥१॥ २॥१३॥」「॥४१॥ ४१॥」→「॥१।२।१३॥」「॥४।१।४१॥」
    t = re.sub(r'॥\s*([०-९])\s*॥\s*([०-९])\s*॥\s*([०-९]+)\s*॥', r'॥\1।\2।\3॥', t)
    t = re.sub(r'॥\s*([०-९])([०-९])\s*॥\s*([०-९]+)\s*॥', r'॥\1।\2।\3॥', t)
    t = re.sub(r'॥\s*([०-९])\s*॥\s*([०-९])\s*।\s*([०-९]+)\s*॥', r'॥\1।\2।\3॥', t)      # 「॥१॥ १।५॥」
    # 脚注番号：語に付いた数字（॥…॥ や [ … ] の参照は残す）
    t = re.sub(rf'(?<=[{DEVA}ऽ])[०-९]+(?=[\s।॥,;?—\-)]|$)', '', t)
    t = re.sub(rf'(?<=[\s(—])[०-९]+(?=[{DEVA}])', '', t)
    t = re.sub(r'(?m)^[०-९]+(?=[अ-ह])', '', t)
    # 行の途中に残った行番号（「प्रियं ५ स्वाध्यायं」「देहेन्द्रिय- २० बुद्धि」「२] 20」）
    t = re.sub(r'-\s+(?:५|१०|१५|२०|२५|३०)\s+(?=\S)', '-', t)
    t = re.sub(r'(?<=[।?])\s+(?:५|१०|१५|२०|२५|३०)\s+(?=[^\s०-९])', ' ', t)
    t = re.sub(r'(?<=[^\s\[।०-९])\s+(?:५|१०|१५|२०|२५|३०|5|10|15|20|25|30)(?=\s+[^\s\]।०-९]|\s*$)', '', t, flags=re.M)
    return t


def join(lines):
    s = ''
    for ln in lines:
        if s.endswith('-'):
            s = s[:-1] + ln
        elif s:
            s += ' ' + ln
        else:
            s = ln
    return s


# ---- 頁を並べて段落にする ----
paras = []
for pg, k in enumerate(order, 1):
    first, cur = True, []
    for ln in norm(clean_page(pages[k])).split('\n'):
        s = ln.strip()
        if not s:
            if cur:
                paras.append(cur)
                cur = []
            continue
        if first:
            s, first = f'[p. {pg}]' + s, False
        cur.append(s)
    if cur:
        paras.append(cur)
    paras.append(None)              # 頁末

# 頁をまたぐ段落をつなぐ：頁末の段落が文の途中（। ॥ ? ] で終わらない）なら次の段落に続ける
merged, i = [], 0
while i < len(paras):
    p = paras[i]
    if p is None:
        i += 1
        continue
    while (i + 2 < len(paras) and paras[i + 1] is None and paras[i + 2]
           and not re.search(r'[।॥?\]]\s*$', p[-1])
           and not re.sub(r'^\[p\. \d+\]', '', paras[i + 2][0]).startswith('[')):
        p = p + paras[i + 2]
        i += 2
    merged.append(p)
    i += 1

S = '\n\n'.join(re.sub(r'[ \t]+', ' ', join(p)).strip() for p in merged)

# ---- スートラの位置：NVTT 全訳の Thakur 版スートラ一覧（nbh_src/canon.json）と照合 ----
CANON = json.loads((ROOT / 'nbh_src' / 'canon.json').read_text(encoding='utf-8'))
KEEP = re.compile(r'[अ-हा-्ंःॠ-ॣ]')
idx = [i for i, ch in enumerate(S) if KEEP.match(ch)]
N = ''.join(S[i] for i in idx)                  # 文字だけにした本文
MARK = list(re.finditer(MARKRE, S))


def nrm(dev):
    return ''.join(ch for ch in dev if KEEP.match(ch))


def npos(i):
    return bisect.bisect_left(idx, i)


spans, ptr, miss = [], 0, []
for num, iast in CANON:
    if num.endswith('付'):
        continue                        # Thakur 版のバーシュヤではスートラに数えない
    dev = nrm(sanscript.transliterate(iast.replace("'", ''), sanscript.IAST, sanscript.DEVANAGARI))
    L, best = len(dev), None
    for m in MARK:                      # 1) スートラの印（॥a।b।c॥）の直前
        if m.start() < ptr:
            continue
        e = npos(m.start())
        if e - npos(ptr) > 6000:
            break
        w0 = max(0, e - L - 12)
        win = N[w0:e]
        sm = difflib.SequenceMatcher(None, win, dev, autojunk=False)
        blocks = [b for b in sm.get_matching_blocks() if b.size]
        hit = sum(b.size for b in blocks)
        if blocks and hit >= 0.8 * L:
            best = (w0 + max(0, blocks[0].a - blocks[0].b), e, m.end())
            break
    if best is None:                    # 2) 印がなければ本文中を探す
        lo = npos(ptr)
        seg = N[lo:lo + 8000]
        head = dev[:min(12, L)]
        k = seg.find(head)
        while k >= 0:
            if difflib.SequenceMatcher(None, seg[k:k + L], dev, autojunk=False).ratio() > 0.85:
                best = (lo + k, lo + k + L, None)
                break
            k = seg.find(head, k + 1)
    if best is None:
        miss.append(num)
        continue
    st, en, mend = best
    s0 = max(idx[min(st, len(idx) - 1)], ptr)
    s1 = mend if mend else idx[min(en, len(idx)) - 1] + 1
    spans.append((num, s0, s1))
    ptr = s1
# 2 回目：見つからなかったスートラを、前後のスートラの間で緩く探す（スートラ一覧が連声を分けて書く場合など）
order = [k for k, _ in CANON if not k.endswith('付')]
found = {n: (a, b) for n, a, b in spans}
for num in list(miss):
    j = order.index(num)
    lo = next((found[order[x]][1] for x in range(j - 1, -1, -1) if order[x] in found), 0)
    hi = next((found[order[x]][0] for x in range(j + 1, len(order)) if order[x] in found), len(S))
    dev = nrm(sanscript.transliterate(dict(CANON)[num].replace("'", ''), sanscript.IAST, sanscript.DEVANAGARI))
    a, b = npos(lo), npos(hi)
    region = N[a:b]
    bestr = None
    for k in range(0, max(1, len(region) - len(dev) // 2), 3):
        win = region[k:k + len(dev) + 8]
        r = difflib.SequenceMatcher(None, win, dev, autojunk=False).ratio()
        if bestr is None or r > bestr[0]:
            bestr = (r, k)
    if bestr and bestr[0] > 0.7:
        k = bestr[1]
        win = region[k:k + len(dev) + 8]
        bl = [x for x in difflib.SequenceMatcher(None, win, dev, autojunk=False).get_matching_blocks() if x.size]
        st, en = a + k + bl[0].a, a + k + bl[-1].a + bl[-1].size
        s0, s1 = idx[st], idx[en - 1] + 1
        m = re.match(r'\s*' + MARKRE, S[s1:s1 + 30])
        if m:
            s1 += m.end()
        spans.append((num, s0, s1))
        found[num] = (s0, s1)
        miss.remove(num)
# 3 回目：読みが大きく違うもの（例 4.2.21 शब्दसंयोगविभवाच्च）は、前後のスートラの間にある番号どおりの印から、
# 直前の文の切れ目までをスートラとする
for num in list(miss):
    j = order.index(num)
    lo = next((found[order[x]][1] for x in range(j - 1, -1, -1) if order[x] in found), 0)
    hi = next((found[order[x]][0] for x in range(j + 1, len(order)) if order[x] in found), len(S))
    want = num.replace('.', '')
    for m in MARK:
        if lo <= m.start() < hi and re.sub(r'\D', '', m.group().translate(DIG)) == want:
            b = max(S.rfind(c, lo, m.start()) for c in '।॥\n')
            s0 = max(lo, b + 1)
            while S[s0].isspace():
                s0 += 1
            spans.append((num, s0, m.end()))
            found[num] = (s0, m.end())
            miss.remove(num)
            break
spans.sort(key=lambda x: x[1])
if miss:
    print('照合できないスートラ:', ' '.join(miss), file=sys.stderr)

# ---- 出力 ----
out = []


def emit_text(seg):
    for para in seg.split('\n\n'):
        para = para.strip()
        if not para:
            continue
        pm = re.match(r'^(\[p\. \d+\])?\s*\[\s*(वा\s*पृ.*?)\]\s*(.*)$', para)
        if pm:
            if pm.group(1):
                out.append(pm.group(1))
            out.append('@ [' + re.sub(r'\s+', ' ', pm.group(2)).strip() + ']')
            para = pm.group(3).strip()
        # 段落の途中の対応頁の注記「[वा पृः …]」も別の行に（前の「[सूत」などの柱の残りは落とす）
        para = re.sub(r'(?:\[सूत्?र?\s*)?\[\s*(वा\s*पृ[^\]]*)\]',
                      lambda m: '\n@ [' + re.sub(r'\s+', ' ', m.group(1)).strip() + ']\n', para)
        para = re.sub(r'\[\s*([^\]\[]*प्रकरणम्)\s*\]', lambda m: '\n@@ ' + m.group(1).replace('-', '') + '\n', para)
        for chunk in para.split('\n'):
            chunk = chunk.strip()
            if chunk.startswith('@'):
                out.append(chunk)
                continue
            # 参照「[ १ । १ । ४१ ]」の中の । では切らない
            chunk = re.sub(r'\[[^\]\[]*\]', lambda m: re.sub(r'\s*।\s*', '\x01', m.group()), chunk)
            for piece in re.findall(r'.*?(?:॥[^॥]*॥|।|\?|$)', chunk):
                piece = piece.strip().replace('\x01', '।')
                if piece:
                    out.append(piece)
        out.append('')


pos = 0
for num, s0, s1 in spans:
    emit_text(S[pos:s0])
    a, b, c = num.split('.')
    body = S[s0:s1]
    pre = ''.join(re.findall(r'\[p\. \d+\]', body))
    body = re.sub(r'\[p\. \d+\]', '', body)
    body = re.sub(MARKRE, '', body)
    body = re.sub(r'\s+', ' ', body).strip()
    out += ['', f'nys_{a},{b}.{c}: {pre}{body} //', '']
    pos = s1
emit_text(S[pos:])
out = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip().split('\n')

# ---- 訂正表 ----
cf = ROOT / 'nbh_src' / 'corrections.txt'
bad = []
if cf.exists():
    for cl in cf.read_text(encoding='utf-8').split('\n'):
        if not cl.strip() or cl.startswith('#'):
            continue
        no, old, new = cl.split('\t')
        i = int(no) - 1
        if old == '*':
            out[i] = ''
        elif old == '+':
            if out[i].strip():
                bad.append(f'{no} + (空行ではない)')
            else:
                out[i] = new
        elif old in out[i]:
            out[i] = out[i].replace(old, new, 1)
        else:
            bad.append(f'{no} {old}')
if bad:
    sys.exit('訂正できない:\n' + '\n'.join(bad))
(ROOT / 'NBh_text.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out), 'lines;', sum(1 for x in out if x.startswith('nys_')), 'sūtras')
