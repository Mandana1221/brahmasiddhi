# -*- coding: utf-8 -*-
# 1927年刊テルグ文字版（Gemini OCR）から『シュリーヴァチャナブーシャナム』の節を取り出す
# 使い方: python3 -I extract_1927.py <GeminiOCR.txt> <出力.json>
import re, sys, json
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
tel = str.maketrans("౦౧౨౩౪౫౬౭౮౯", "0123456789")
start = next(i for i, l in enumerate(L) if i > 1229 and l.strip() == "ప్రథమ ప్రకరణమ్.")
JUNK = re.compile(r"(\.pdf$|ページ|^Gemini|^以下は|^OCRして|^※|^[0-9]{1,3}$|వచన ?భూషణ|ప్రకరణ|తిరువడి|శ్రీమల్లోక|^శ్రీమతే|^\.\.$|^\(|^（)")
res, cur, notes = {}, 0, []
for i in range(start, len(L)):
    s = L[i].strip()
    if not s or JUNK.search(s):
        continue
    m = re.match(r"^([౦-౯0-9]{1,3})\s*[.,౹।]\s*(.*)$", s)
    if m:
        n = int(m.group(1).translate(tel))
        # OCR の数字の読み誤りに備え、直前の番号から近いものだけを新しい節とみなす
        if cur < n <= cur + 4:
            cur = n; res[n] = m.group(2).strip(); continue
        if n != cur:
            notes.append((i + 1, n, cur))
            # 番号が読めない場合：次の節とみなす
            cur += 1; res[cur] = m.group(2).strip(); continue
    if cur:
        res[cur] = res.get(cur, "") + " " + s
json.dump(res, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
missing = [n for n in range(1, 464) if n not in res]
print("found", len(res), "last", max(res), "missing", missing[:80])
print("renumbered lines", notes[:30])
