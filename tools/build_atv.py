#!/usr/bin/env python3
"""Build atmatattvaviveka_zenyaku.html from the sources in atv/.

atv/outline.txt   科段: one node per line, "num | 見出し | sk | ページ | (第1階層のみ) 章の副題"
atv/text/*.txt    対訳とノート: blocks that start with "@node <num>"

Block syntax (inside @node):
  gist: 要旨
  verse: ラベル        -> 偈のカード (続けて sa: / ia: / ja:)
  seg:                 -> 左右の対訳 (続けて sa: / ja:)
  sa: / ia: / ja:      -> 本文 / ローマ字 / 和訳
  note:                -> ノート (続けて "- " で始まる項目)
  ほかの行は直前の項目の続き。**x** は太字。HTML はそのまま通す。
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATV = ROOT / "atv"
OUT = ROOT / "atmatattvaviveka_zenyaku.html"


def inline(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s.strip())


def read_outline():
    nodes = []
    for ln in (ATV / "outline.txt").read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        f = [x.strip() for x in ln.split("|")]
        f += [""] * (5 - len(f))
        num, title, sk, refs, sub = f[:5]
        nodes.append(dict(num=num, title=title, sk=sk, refs=refs, sub=sub,
                          depth=num.count(".") + 1, children=[]))
    roots, stack = [], []
    for n in nodes:
        while stack and stack[-1]["depth"] >= n["depth"]:
            stack.pop()
        (stack[-1]["children"] if stack else roots).append(n)
        stack.append(n)
    return roots, {n["num"]: n for n in nodes}


def read_text():
    blocks = {}
    for p in sorted((ATV / "text").glob("*.txt")):
        cur = None
        for ln in p.read_text(encoding="utf-8").splitlines():
            if ln.startswith("#"):
                continue
            m = re.match(r"@node\s+(\S+)", ln)
            if m:
                cur = blocks.setdefault(m.group(1), [])
                continue
            if cur is None or not ln.strip():
                continue
            m = re.match(r"(gist|verse|seg|sa|ia|ja|note):\s?(.*)", ln)
            if m:
                cur.append([m.group(1), m.group(2)])
            elif ln.startswith("- "):
                cur.append(["li", ln[2:]])
            elif cur:
                cur[-1][1] += " " + ln.strip()
    return blocks


def render_block(items):
    out, i = [], 0
    while i < len(items):
        k, v = items[i]
        if k == "gist":
            out.append(f'<p class="gist">{inline(v)}</p>')
            i += 1
        elif k == "verse":
            d = {}
            i += 1
            while i < len(items) and items[i][0] in ("sa", "ia", "ja"):
                d[items[i][0]] = items[i][1]
                i += 1
            out.append(
                f'<div class="sutra"><div class="sutra-head"><span class="sutra-num">{inline(v)}</span></div>'
                f'<div class="sutra-text">{inline(d.get("sa", ""))}</div>'
                f'<div class="sutra-iast">{inline(d.get("ia", ""))}</div>'
                f'<div class="sutra-jp">{inline(d.get("ja", ""))}</div></div>')
        elif k == "seg":
            d = {}
            i += 1
            while i < len(items) and items[i][0] in ("sa", "ja"):
                d[items[i][0]] = items[i][1]
                i += 1
            out.append(f'<div class="seg"><div class="seg-sa dev">{inline(d.get("sa", ""))}</div>'
                       f'<div class="seg-ja">{inline(d.get("ja", ""))}</div></div>')
        elif k == "note":
            lis = []
            i += 1
            while i < len(items) and items[i][0] == "li":
                lis.append(f"<li>{inline(items[i][1])}</li>")
                i += 1
            out.append('<div class="tnote"><div class="tnote-h">ノート</div><ol>' + "".join(lis) + "</ol></div>")
        else:
            sys.exit(f"unexpected '{k}:' outside verse/seg: {v[:40]}")
    return "\n".join(out)


def has_text(n, blocks):
    return n["num"] in blocks or any(has_text(c, blocks) for c in n["children"])


def render_node(n, blocks):
    d = n["depth"]
    cls = ["node"]
    if d <= 2:
        cls.append(f"lv{d}")
    leaf = not n["children"] and n["num"] not in blocks
    if leaf:
        cls.append("leaf")
    nid = "n" + n["num"].replace(".", "-")
    sk = f' <span class="sk">{html.escape(n["sk"])}</span>' if n["sk"] else ""
    refs = "".join(f'<span class="ref">{html.escape(r.strip())}</span>' for r in n["refs"].split(",") if r.strip())
    if leaf and d >= 3:
        refs += '<span class="ref mi">未訳</span>'
    opened = " open" if d == 1 or (d == 2 and has_text(n, blocks)) else ""
    s = (f'<details class="{" ".join(cls)}" id="{nid}"{opened}>\n'
         f'<summary><span class="num">{n["num"]}</span><span class="ttl">{inline(n["title"])}{sk}</span>'
         f'<span class="refs">{refs}</span></summary>\n')
    if leaf:
        return s + "</details>\n"
    body = render_block(blocks[n["num"]]) if n["num"] in blocks else ""
    kids = "".join(render_node(c, blocks) for c in n["children"])
    return s + f'<div class="body">\n{body}\n{kids}</div></details>\n'


def main():
    roots, index = read_outline()
    blocks = read_text()
    missing = [k for k in blocks if k not in index]
    if missing:
        sys.exit(f"@node not in outline: {missing}")
    done = [n for n in index.values()
            if any(k in ("seg", "verse") for k, _ in blocks.get(n["num"], []))]
    pages = [int(p) for n in done for p in re.findall(r"\d+", n["refs"])]
    progress = f"p.1–{max(pages)}（全452ページ）" if pages else "未着手"
    parts = [(ATV / "template_head.html").read_text(encoding="utf-8"),
             (ATV / "intro.html").read_text(encoding="utf-8").replace("{{PROGRESS}}", progress)]
    for i, r in enumerate(roots):
        parts.append(f'<section class="stabaka" id="st{r["num"]}">\n'
                     f'<h2 class="chapter">{inline(r["title"])}</h2>\n'
                     f'<p class="chapter-sub">{inline(r["sub"])}</p>\n'
                     f'<div class="legend-tr"><span>本文（ウダヤナ）</span><span>和訳</span></div>\n'
                     f'<div class="tree">\n{render_node(r, blocks)}</div>\n</section>\n')
    parts.append("<footer>アートマタットヴァ・ヴィヴェーカ　対訳と解説</footer>\n")
    parts.append((ATV / "template_script.html").read_text(encoding="utf-8"))
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {OUT.name}: {len(index)} nodes, {len(blocks)} with text, progress {progress}")


if __name__ == "__main__":
    main()
