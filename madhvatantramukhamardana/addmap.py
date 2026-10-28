"""全体の地図に行を追加する。使い方: python3 addmap.py '<grp見出し or ->' '<範囲表示>' '<残り頁>' n|title|pages|desc ..."""
import sys
p = 'parts/01_hero.html'
s = open(p, encoding='utf-8').read()
grp, cur, rest = sys.argv[1], sys.argv[2], sys.argv[3]
rows = ''
if grp != '-':
    rows += f'<tr class="grp"><td colspan="4">{grp}</td></tr>\n'
for a in sys.argv[4:]:
    n, t, pg, d = a.split('|')
    rows += f'<tr><td class="num">§{n}</td><td class="k"><a href="#s{n}">{t}</a></td><td class="num">{pg}</td><td>{d}</td></tr>\n'
i = s.index('<tr><td class="num">—</td><td class="k">（以下作業中）</td>')
j = s.index('</tr>', i) + 5
tail = f'<tr><td class="num">—</td><td class="k">（以下作業中）</td><td class="num">{rest}</td><td>未着手の部分</td></tr>' if rest != '-' else ''
s = s[:i] + rows + tail + s[j:]
import re
s = re.sub(r'訳注　作業中（現在 [^）]*）', f'訳注　作業中（現在 {cur}）', s)
open(p, 'w', encoding='utf-8').write(s)
