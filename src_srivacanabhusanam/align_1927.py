# -*- coding: utf-8 -*-
# タミル文字の校合テキスト（acharya.org 版）と、1927年刊テルグ文字版（Gemini OCR）を節ごとに対応づける
# 使い方: python3 -I align_1927.py <tamil_collated.txt> <GeminiOCR.txt> <出力.json>
import re, sys, json
from difflib import SequenceMatcher
TAM, TEL, OUT = sys.argv[1:4]

# インド系文字は Unicode のブロック内の並びが共通なので、ブロック内の位置で比べる。
# タミル文字には有声音・帯気音がないので、各行（varga）を無声無気音にまとめる。
COLLAPSE = {}
for base in (0x15, 0x1A, 0x1F, 0x24, 0x2A):      # ka, ca, ṭa, ta, pa の各行
    for k in range(4):
        COLLAPSE[base + k] = base
def key(s, block):
    out = []
    for ch in s:
        o = ord(ch) - block
        if 0 <= o < 0x80:
            o = COLLAPSE.get(o, o)
            if o in (0x4D,):            # virāma は無視
                continue
            if 0x66 <= o <= 0x6F:       # 数字は無視
                continue
            out.append(chr(0x100 + o))
    return "".join(out)

# タミル側：節ごと
tam = {}
for line in open(TAM, encoding="utf-8"):
    m = re.match(r"^(\d+)\. (.*)$", line.strip())
    if m:
        tam[int(m.group(1))] = re.sub(r"〔.*?〕", "", m.group(2))

# テルグ側：行ごと（ノイズ行は除く）
L = open(TEL, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(L) if i > 1229 and l.strip() == "ప్రథమ ప్రకరణమ్.")
JUNK = re.compile(r"(\.pdf$|ページ|^Gemini|^以下は|^OCRして|^※|వచన ?భూషణ|ప్రకరణ|తిరువడి|శ్రీమల్లోక|^శ్రీమతే)")
units = []
for i in range(start, len(L)):
    s = L[i].strip()
    if not s or JUNK.search(s):
        continue
    k = key(s, 0x0C00)
    if len(k) < 3:
        continue
    units.append((i + 1, s, k))

res, j, miss = {}, 0, 0
for n in range(1, 464):
    a = key(tam[n], 0x0B80)
    best = (0, None, None)
    for skip in range(0, min(8 + 40 * miss, 200)):
        for span in range(1, 9):
            s0, s1 = j + skip, j + skip + span
            if s1 > len(units): break
            cand = "".join(u[2] for u in units[s0:s1])
            if len(cand) > 2.2 * len(a) + 20: break
            r = SequenceMatcher(None, a, cand, autojunk=False).ratio()
            if r > best[0]:
                best = (r, s0, s1)
    r, s0, s1 = best
    if s0 is not None and r >= 0.5:
        res[n] = {"score": round(r, 3), "lines": [units[s0][0], units[s1 - 1][0]],
                  "tel": " ".join(u[1] for u in units[s0:s1])}
        j = s1; miss = 0
    else:
        miss += 1
        res[n] = {"score": round(r, 3), "lines": None, "tel": ""}
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
ok = [n for n, v in res.items() if v["tel"]]
print("matched", len(ok), "of 463; weak(<0.6):", [n for n, v in res.items() if v["tel"] and v["score"] < 0.6][:40])
print("unmatched:", [n for n, v in res.items() if not v["tel"]][:80])
