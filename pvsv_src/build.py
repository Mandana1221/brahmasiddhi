"""Build pvsv_ch1_bilingual.html from PVSV.tex + units/*.py.

Each units/partNNN.py defines UNITS = [dict(...), ...] in text order. A unit covers the
e-text tokens from the end of the previous unit up to and including its `upto` marker, so
the whole text is covered without gaps.  Fields:
  upto   raw e-text words ending the unit ('/' for danda, '//N//' for verse end)
  label  heading;  head  optional section title (starts a new section in the TOC)
  tr     Japanese translation (HTML);  cm  commentary (HTML)
  fixes  [(old, new)] applied to the sandhied HK text (emendations)
  kfull  sandhied HK of a whole karika shown at the top (for karikas split by the vrtti)
"""
import glob, html, importlib.util, os, re, sys
import skt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "pvsv_ch1_bilingual.html")

def norm(words):
    s = " ".join(words)
    s = re.sub(r"//\s*(\d+)\s*//", r" ||\1|| ", s)
    s = s.replace("//", " || ").replace("/", " | ")
    return s.split()

def load_units():
    units = []
    for f in sorted(glob.glob(os.path.join(HERE, "units", "part*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        units.extend(m.UNITS)
    return units

def slice_units(tokens, units):
    pos = 0
    words = [t.w for t in tokens]
    for n, u in enumerate(units):
        mk = norm(u["upto"].split())
        k = len(mk)
        for i in range(pos, len(words) - k + 1):
            if words[i:i + k] == mk:
                end = i + k
                break
        else:
            raise SystemExit("unit %d (%s): marker not found after %s: %r"
                             % (n, u.get("label"), skt.loc(tokens[pos].line), u["upto"]))
        if end - pos > 1500:
            raise SystemExit("unit %d (%s) suspiciously long (%d tokens); check marker"
                             % (n, u.get("label"), end - pos))
        u["_toks"] = tokens[pos:end]
        pos = end
    return pos

KNUM = re.compile(r"^\|\|(\d+)\|\|$")

def render_skt(u):
    """Return HTML for the Sanskrit of one unit."""
    toks = u["_toks"]
    groups = []
    for t in toks:
        if groups and groups[-1][0] == t.verse:
            groups[-1][1].append(t)
        else:
            groups.append((t.verse, [t]))
    fixes = list(u.get("fixes", ()))
    blocks = []       # ('p', [html pieces]) or ('v', html)
    used = set()

    def hk_of(g):
        s = skt.render_hk(g)
        for i, (a, b) in enumerate(fixes):
            if i not in used and a in s:
                s = s.replace(a, b, 1); used.add(i)
        return s

    def hk_lines(g):
        # the fixes were matched on the whole verse group; apply them to each half-verse too
        s = skt.render_hk(g)
        for a, b in fixes:
            if a in s:
                s = s.replace(a, b, 1)
        return s

    for verse, g in groups:
        s = hk_of(g)
        nwords = len([t for t in g if not t.w.startswith("|")])
        if verse and (nwords >= 4 or any(KNUM.match(t.w) for t in g)):
            # split verse group into source lines (half-verses)
            lines, cur, curline = [], [], None
            for t in g:
                if curline is not None and t.line != curline and cur:
                    lines.append(cur); cur = []
                cur.append(t); curline = t.line
            if cur:
                lines.append(cur)
            if len(lines) > 1:
                parts = [hk_lines(l) for l in lines]
            else:
                parts = [s]
            isk = any(KNUM.match(t.w) for t in g)
            blocks.append(("v", isk, parts))
        elif verse:
            if blocks and blocks[-1][0] == "p":
                blocks[-1][1].append('<b class="prat">%s</b>' % html.escape(skt.dev(s)))
            else:
                blocks.append(("p", ['<b class="prat">%s</b>' % html.escape(skt.dev(s))]))
        else:
            if blocks and blocks[-1][0] == "p":
                blocks[-1][1].append(html.escape(skt.dev(s)))
            else:
                blocks.append(("p", [html.escape(skt.dev(s))]))
    missing = [fixes[i] for i in range(len(fixes)) if i not in used]
    if missing:
        raise SystemExit("unit %s: fixes not applied: %r" % (u.get("label"), missing))
    out = []
    if u.get("kfull"):
        out.append('<div class="skt karika full">%s</div>' % "".join(
            '<span class="pada">%s</span>' % html.escape(skt.dev(l)) for l in u["kfull"].split("\n")))
    for b in blocks:
        if b[0] == "p":
            out.append('<div class="skt prose">%s</div>' % " ".join(b[1]))
        else:
            _, isk, parts = b
            cls = "karika" if isk and not u.get("kfull") and not u.get("kshown") else "verse"
            out.append('<div class="skt %s">%s</div>' % (cls, "".join(
                '<span class="pada">%s</span>' % html.escape(skt.dev(p)) for p in parts)))
    return "\n".join(out)

def main():
    tokens = skt.load()
    units = load_units()
    end = slice_units(tokens, units)
    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    body, toc = [], []
    for n, u in enumerate(units):
        uid = "u%d" % (n + 1)
        a, b = u["_toks"][0].line, u["_toks"][-1].line
        loc = skt.loc(a) if a == b else "%s–%s" % (skt.loc(a), skt.loc(b) if a[:3] != b[:3] else skt.loc(b))
        if u.get("head"):
            toc.append('<li class="toc-head"><a href="#%s">%s</a></li>' % (uid, u["head"]))
            body.append('<h2 class="sec" id="s%d">%s</h2>' % (n + 1, u["head"]))
        knums = [KNUM.match(t.w).group(1) for t in u["_toks"] if KNUM.match(t.w)]
        if knums:
            toc.append('<li class="toc-k"><a href="#%s">%s</a></li>' % (uid, "・".join(knums)))
        cls = "unit"
        body.append("""
<section class="%s" id="%s">
  <div class="unit-head"><span class="unit-label">%s</span><span class="unit-loc">Gnoli %s</span></div>
  %s
  <div class="block tr"><div class="block-title">和訳</div>%s</div>
  %s
</section>""" % (cls, uid, u["label"], loc, render_skt(u), u["tr"],
                 ('<div class="block cm"><div class="block-title">解説</div>%s</div>' % u["cm"]) if u.get("cm") else ""))
    last = skt.loc(units[-1]["_toks"][-1].line)
    done = end >= len(tokens)
    tmpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    page = (tmpl.replace("{{CSS}}", css)
                .replace("{{TITLE_DEV}}", skt.dev("pramANavArttikasvavRttiH"))
                .replace("{{RANGE}}", "全訳" if done else "Gnoli 1,1–%s（翻訳継続中）" % last)
                .replace("{{TOC}}", "\n".join(toc))
                .replace("{{BODY}}", "".join(body))
                .replace("{{FOOT}}", "第1章　了" if done else "ここまで（Gnoli %s）。以下、翻訳継続中。" % last))
    open(OUT, "w", encoding="utf-8").write(page)
    print("units:", len(units), "covered to", last, "tokens %d/%d" % (end, len(tokens)))

if __name__ == "__main__":
    main()
