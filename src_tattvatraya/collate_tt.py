# -*- coding: utf-8 -*-
# Gemini OCR（テルグ文字、1927年版）から『タットヴァトラヤ』全202節を取り出す
# 使い方: python3 -I collate_tt.py <GeminiOCR.txt> <出力.txt>
import re, sys
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
OUT = sys.argv[2]
tel = str.maketrans("౦౧౨౩౪౫౬౭౮౯", "0123456789")
JUNK = re.compile(r"(\.pdf$|ページ目|^Gemini|^以下は|^OCRして|^※|^[0-9]+$|^తత్త్వ ?త్య?్?ర ?యమ్\.?$|^(చిత్|అచిత్|ఈశ్వర) ?ప్రకరణమ్\.?$|ముట్రిట్రు|సమాప్తమ్|తిరువడి|^\[|^తత్త్వత్రయమ్ —|శ్రీమల్లోక|^శ్రీమతే)")

def extract(a, b):
    """行 a..b（1始まり）から節を取り出す。番号のない行は直前の節の続きとする。"""
    res, cur, cont = {}, None, {}
    for i in range(a - 1, b):
        s = L[i].strip()
        if not s or JUNK.search(s):
            continue
        m = re.match(r"^([౦-౯]{1,3})\s*[.,]\s*(.*)$", s)
        if m:
            cur = int(m.group(1).translate(tel)); res[cur] = m.group(2).strip(); continue
        if cur is not None:
            res[cur] += " " + s; cont.setdefault(cur, []).append(i + 1)
    return res, cont

main, cont = extract(864, 1210)
dup, _ = extract(742, 776)
# ページ先頭の続き行は、実際には前のページの最後の節の続き（番号の前に置かれた行）
# 例：行 1195 付近は §186 の続き。extract は直前の節に足すので、そのまま正しく連結される。
missing = [n for n in range(1, 203) if n not in main]
print("main:", len(main), "missing:", missing)
print("continuations appended to:", sorted(cont))

SECT = {1: "చిత్ప్రకరణమ్（第1章 魂）", 77: "అచిత్ప్రకరణమ్（第2章 物質）", 141: "ఈశ్వరప్రకరణమ్（第3章 神）"}
out = ["తత్త్వత్రయమ్ — Tattvatraya（Piḷḷai Lokācārya）",
       "校合テキスト：1927年刊テルグ文字版（Aṇṇaṅgarācārya 校訂）の Gemini OCR による。",
       "ページをまたぐ節はつなぎ合わせた。§187–202 は OCR 内の重複部分と照合した。〔 〕は注記。", ""]
diff = []
for n in range(1, 203):
    if n in SECT:
        out += ["", "== " + SECT[n] + " ==", ""]
    if n not in main and n in dup:
        main[n] = dup.pop(n)
    t = re.sub(r"\s+", " ", main.get(n, "〔欠〕"))
    if n in dup:
        d = re.sub(r"\s+", " ", dup[n])
        if d.replace(" ", "") != t.replace(" ", ""):
            diff.append(n)
            # 長い方（途中で切れていない方）を本文にし、もう一方を注記
            if len(d) > len(t) + 5:
                t, d = d, t
            t += " 〔別出：" + d + "〕"
    out.append(f"{n}. {t}")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("dup differs:", diff)
