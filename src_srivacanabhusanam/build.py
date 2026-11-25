# -*- coding: utf-8 -*-
# データファイル d*.py と overview.py から srivacanabhusanam_kadan.html を組み立てる
# 使い方: python3 -I build.py <srcdir> <css元HTML> <出力HTML>
import os, re, sys, glob, html

SRC, CSS_FROM, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

# ---------- 図表ヘルパー ----------
def fig(cap, body, note=None):
    n = f'\n  <div class="cap2">{note}</div>' if note else ''
    return f'<figure class="fig">\n  <figcaption>{cap}</figcaption>\n{body}{n}\n</figure>\n'

def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = []
    for r in rows:
        if isinstance(r, str):
            tr.append(f'<tr class="grp"><td colspan="{len(head)}">{r}</td></tr>')
        else:
            tr.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return f'<div class="tscroll"><table class="t"><thead><tr>{th}</tr></thead><tbody>{"".join(tr)}</tbody></table></div>'

def flow(nodes, arrows=None):
    out = []
    for i, nd in enumerate(nodes):
        cls, inner = nd if isinstance(nd, tuple) else ("", nd)
        out.append(f'<div class="node {cls}">{inner}</div>')
        if i < len(nodes) - 1:
            lab = arrows[i] if arrows else ""
            if lab:
                out.append(f'<div class="arr lbl"><span class="ac">→</span><span>{lab}</span></div>')
            else:
                out.append('<div class="arr"><span class="ac">→</span></div>')
    return '<div class="flow">' + "".join(out) + '</div>'

KS, SS, FS = [], {}, {}
OV = {}
def K(num, title, a, b): KS.append((num, title, a, b))
def S(no, tr, ex=None, chk=False):
    assert no not in SS, f"duplicate §{no}"
    SS[no] = (tr, ex, chk)
def F(no, h): FS.setdefault(no, []).append(h)
def OVERVIEW(h): OV["html"] = h
NT = {}
def N(no, txt): NT[no] = txt

ns = dict(K=K, S=S, F=F, N=N, fig=fig, table=table, flow=flow, OVERVIEW=OVERVIEW)
for p in sorted(glob.glob(os.path.join(SRC, "d*.py"))) + [os.path.join(SRC, "overview.py")]:
    if os.path.exists(p):
        exec(compile(open(p, encoding="utf-8").read(), p, "exec"), ns)

def lvl(num): return num.count(".") + 1
def ref_of(n):
    best = None
    for num, t, a, b in KS:
        if a <= n <= b and (best is None or lvl(num) >= lvl(best)):
            best = num
    return best or "—"
def rng(a, b): return f"{a}" if a == b else f"{a}–{b}"

# ---------- 検査 ----------
done = sorted(SS)
problems = []
for num, t, a, b in KS:
    # 子の範囲が親に収まるか
    par = num.rsplit(".", 1)[0] if "." in num else None
    if par:
        pk = [k for k in KS if k[0] == par]
        if not pk: problems.append(f"親なし {num}")
        elif not (pk[0][2] <= a and b <= pk[0][3]): problems.append(f"範囲外 {num}")
for n in done:
    if ref_of(n) == "—": problems.append(f"科段なし §{n}")
if problems: print("PROBLEMS:", problems)

# ---------- CSS ----------
src = open(CSS_FROM, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
css += """
  .edmark{margin:26px 0 6px;font-size:13px;color:var(--sub);border-top:2px dotted var(--line);padding-top:6px}
  .edmark b{color:var(--accent)}
  .kd .row .t i{font-style:italic}
"""

# ---------- 出力 ----------
tops = [k for k in KS if lvl(k[0]) == 1]
H = []
H.append(f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="iast-fonts.css">
<title>シュリーヴァチャナブーシャナム科段</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <div class="kicker">Piḷḷai Lokācārya 作　科段・和訳・図解</div>
  <h1>『シュリーヴァチャナブーシャナム』<i>Śrīvacanabhūṣaṇam</i><br>科段と解説</h1>
  <p>節の番号（§）は acharya.org 刊タミル文字版（全463節）によります。本文は二つの OCR を照合した校合テキストに基づきます。術語は IAST で記しています。</p>
  <p style="margin-top:8px">初めての方は <a href="srivacanabhusanam_nyumon.html" style="color:#fff">『シュリーヴァチャナブーシャナム』入門</a>（大学1年生向け）からどうぞ。</p>
  <p style="margin-top:8px"><a href="index.html" style="color:#fff">← 原典研究の書庫（リンク集）へ</a></p>
</header>
""")
toc = ['<li><a href="#whole">全体の科段</a></li>', '<li><a href="#zukai">図解：全体の見取り図</a></li>']
for num, t, a, b in tops:
    toc.append(f'<li><a href="#kd{num}">詳しい科段 {num}（§{rng(a,b)}）</a></li>')
for num, t, a, b in tops:
    if any(a <= n <= b for n in done):
        toc.append(f'<li><a href="#exp{num}">解説 {num}：{t}</a></li>')
H.append('<nav class="card toc"><b>目次</b><ol>' + "".join(toc) + '</ol></nav>\n')

# 全体の科段
H.append('<h2 id="whole">全体の科段</h2>\n<div class="kd">')
for num, t, a, b in KS:
    if lvl(num) <= 2:
        cls = "lv2" if lvl(num) == 1 else "lv3"
        H.append(f'  <div class="row {cls}"><span class="n">{num}</span><span class="t">{t}</span><span class="s">{rng(a,b)}</span></div>')
H.append('</div>')
H.append(f'<p class="note">和訳・解説は現在 {len(done)} 節（全463節中）。</p>\n')

# 図解
H.append('<h2 id="zukai">図解：全体の見取り図</h2>\n' + OV.get("html", "") + "\n")

# 詳しい科段
for num0, t0, a0, b0 in tops:
    H.append(f'<h2 id="kd{num0}">詳しい科段 {num0}（§{rng(a0,b0)}）</h2>\n<div class="kd">')
    for num, t, a, b in KS:
        if num == num0 or num.startswith(num0 + "."):
            cls = {1: "lv1", 2: "lv2", 3: "lv3", 4: "lv4"}.get(lvl(num), "lv5")
            H.append(f'  <div class="row {cls}"><span class="n">{num}</span><span class="t">{t}</span><span class="s">{rng(a,b)}</span></div>')
    H.append('</div>\n')

# 解説
ED = {1: "第1章（<i>prathama-prakaraṇa</i>）", 115: "第2章（<i>dvitīya-prakaraṇa</i>）", 244: "第3章（<i>tṛtīya-prakaraṇa</i>）", 381: "第4章（<i>caturtha-prakaraṇa</i>）"}
for n in done:
    for num, t, a, b in KS:
        if a == n and lvl(num) == 1:
            H.append(f'<h2 id="exp{num}">解説 {num}：{t}（§{rng(a,b)}）</h2>\n')
    for num, t, a, b in KS:
        if a == n and lvl(num) == 2:
            H.append(f'<h3><span class="h3n">{num}</span>{t}（§{rng(a,b)}）</h3>\n')
    if n in ED:
        H.append(f'<div class="edmark">この版の <b>{ED[n]}</b> はここから始まります。</div>\n')
    for f in FS.get(n, []):
        H.append(f)
    tr, ex, chk = SS[n]
    if n in NT:
        ex = (ex + " " if ex else "") + NT[n]
    tag = '<span class="chk">要確認</span>' if chk else ''
    exh = f'\n  <div class="ex"><p>{ex}</p></div>' if ex else ''
    H.append(f'<div class="sutra" id="s{n}">\n  <div class="hd"><span class="no">§{n}</span><span class="ref">科段 {ref_of(n)}</span>{tag}</div>\n  <div class="tr">{tr}</div>{exh}\n</div>\n')

H.append("""
<div class="card note">
  <b>注意</b><br>
  本文は acharya.org 刊タミル文字版を二つの OCR（Gemini・mitra-surya）で読み、節ごとに照合した<a href="srivacanabhusanam_tamil_collated.txt">校合テキスト（タミル文字、全463節）</a>に基づきます。OCR の乱れがある節や、訳・解釈に特に自信がない節には「要確認」の印を付けました。「要確認」の節はすべて、1927年刊テルグ文字版（<i>Aṇṇaṅgarācārya</i> 校訂）の OCR と照合しました（<a href="srivacanabhusanam_telugu1927_aligned.txt">1927年版の節ごとの本文</a>）。
  科段と解説は、本書の讃頌（<i>taniyan</i>）が挙げる六つの主題と伝統的な注釈（<i>Maṇavāḷa Māmuni</i>）の理解を参考にまとめたもので、注釈そのものと一節ずつ照合したものではありません。
</div>
</div>
</body>
</html>
""")
open(OUT, "w", encoding="utf-8").write("\n".join(H))
print("sutras:", len(done), "outline:", len(KS), "figures:", sum(len(v) for v in FS.values()))
