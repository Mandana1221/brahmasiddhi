# -*- coding: utf-8 -*-
# mitra OCR（節番号の基準）と Gemini OCR（文字の基準）を節ごとに対応づける
import re, sys, json
from difflib import SequenceMatcher

M_PATH, G_PATH, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

# ---- mitra: 節ごと ----
m = {}
started = False
for line in open(M_PATH, encoding="utf-8"):
    line = line.rstrip("\n")
    if "ப்ரதமப்ரகரணம்." == line.strip():
        started = True
    if not started:
        continue
    mm = re.match(r"^(\d{1,3})\.?\s+(.*)$", line)
    if mm:
        n = int(mm.group(1))
        if 1 <= n <= 463 and n not in m:
            m[n] = mm.group(2).strip()

# ---- Gemini: 単位に分割 ----
lines = open(G_PATH, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("【3ページ】"))
units, cur, page = [], None, 3
JUNK = re.compile(r"^(Srivacanabhusanam\.pdf|他 \d+ 件|http://acharya\.org|\d+〜\d+ページ目.*|Gemini.*|全30ページ.*)$")
HEAD = re.compile(r"(வசன|வசந|வாசன).{0,3}பூஷ.*(ப்ரகரண|ப்ரக)|ஸ்ரீமல்லோக|ராமாநுஜாய|^ஸ்ரீ\s*[:ஃ]?\s*$|^ஸ்ரீரஸ்து")
def flush():
    global cur
    if cur and cur["text"].strip():
        units.append(cur)
    cur = None
for l in lines[start:]:
    s = l.strip()
    pm = re.match(r"^【(\d+)ページ】", s)
    if pm:
        flush(); page = int(pm.group(1)); continue
    if not s or JUNK.match(s):
        flush(); continue
    if HEAD.search(s) and not re.match(r"^\d", s):
        flush(); continue
    if re.fullmatch(r"\d{1,2}", s):
        flush(); continue
    nm = re.match(r"^(\d{1,3})\s*[.,]?\s*(.*)$", s)
    if nm and nm.group(2):
        flush(); cur = {"num": int(nm.group(1)), "text": nm.group(2), "page": page}; continue
    if cur is None:
        cur = {"num": None, "text": s, "page": page}
    else:
        # 行末で切れた語をつなぐ
        cur["text"] += s if not cur["text"].endswith(" ") else s
flush()

def norm(x):
    return re.sub(r"[\s\d.,;:!?'\"“”‘’()\[\]\-–—|]", "", x)

# ---- 対応づけ（単調） ----
res, j = {}, 0
for n in range(1, 464):
    a = norm(m.get(n, ""))
    best = (0, None, None)
    for skip in range(0, 5):
        for span in range(1, 4):
            s0, s1 = j + skip, j + skip + span
            if s1 > len(units): break
            cand = "".join(norm(u["text"]) for u in units[s0:s1])
            if not cand: continue
            r = SequenceMatcher(None, a, cand, autojunk=False).ratio()
            # 長すぎる結合を少し減点
            if r > best[0] + 0.02 or (best[1] is None):
                best = (r, s0, s1)
    r, s0, s1 = best
    if s0 is not None and r >= 0.45:
        g = " ".join(u["text"] for u in units[s0:s1])
        res[n] = {"m": m.get(n, ""), "g": g, "score": round(r, 3), "page": units[s0]["page"]}
        j = s1
    else:
        res[n] = {"m": m.get(n, ""), "g": "", "score": round(r, 3), "page": None}
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
sc = [v["score"] for v in res.values()]
low = [k for k, v in res.items() if v["score"] < 0.6]
print("mitra sutras:", len(m), "units:", len(units))
print("matched>=0.45:", sum(1 for v in res.values() if v["g"]), "low<0.6:", len(low), low[:60])
