"""Read the Gnoli PVSV e-text and render Sanskrit with sandhi restored (Harvard-Kyoto -> Devanagari)."""
import re
from indic_transliteration import sanscript

SRC_DEFAULT = __file__.rsplit("/", 1)[0] + "/PVSV.tex"

# Stems with genuine vrddhi ai/au word-internally (not a+i / a+u junctions).
VRDDHI = ("ekaik", "pauruSey", "vaiphaly", "vaikaly", "vaiyarthy", "nairAtmy", "trailoky", "paurvApary",
          "vaidharmy", "vaizeS", "naiyAyik", "saugat", "vailakSaNy", "vaicitry", "vaiSamy",
          "vaiziSTy", "vaiyadhikaraNy", "vaisAdRzy", "vaisadRzy", "laukik", "vaidik", "jaimin",
          "bauddh", "kautuk", "vaijAty", "taimir", "saukSmy", "maitr", "caitr", "aindr", "aikAnt",
          "aikAntik", "aikya", "kaumAr", "dhaurty", "aizvary", "vaipar", "vaiyAkaraN", "sauv",
          "vaizvarUpy", "vaimaty", "vaiparItya", "vairUpy", "gaurav", "lAghav", "pauruS", "vairAgy",
          "naiSphaly", "naiyamik", "vaikalpik", "naizcaly", "dvaividhy", "traividhy", "vaidhurya",
          "vaizadya", "vaizady", "bhautik", "kaivaly", "vaidy", "vaiyAtya", "sauks", "aupacArik",
          "aupAdhik", "naimittik", "aupAdAnik", "vaisAdRzy", "vaiyAkhy", "vaipulya", "vaiSayik",
          "aikadez", "aikArth", "vairAgy", "vaiSamya", "nair", "pauna", "gaura", "kaumud", "jaiminI",
          "mauna", "vaiSNav", "zaiv", "rauravA")

# Indeclinables ending in a/A/i/u: a line ending with one of these is a separate word.
INDECL = set("""yadi pUrvatra paratra uttaratra sa ta ya ka ca na eva iva tatra atra yatra kutra sarvatra anyatra ekatra ubhayatra iha ha sma Aha
vA yathA tathA sadA tadA yadA kadA kva api iti hi tu nu punaH bhavati asti nAsti syAt kila khalu
nanu atha tAvat sarvathA anyathA ekadA ubhayathA iva kevalam yataH tataH ataH tAvan na-""".split())

def _junction_vowels(tok):
    """Convert e-text a+u -> o / a+i -> e markers ('au','ai' inside a word)."""
    tok = re.sub(r"(?<=.)(AA|aA|Aa)", "A", tok)
    tok = tok.replace("cz", "cch")
    tok = re.sub(r"(?<=.)Au", "o", tok)
    tok = re.sub(r"(?<=.)Ai", "e", tok)
    def fix(m):
        i = m.start()
        rest = tok[i:]
        for v in VRDDHI:
            # genuine if a vrddhi stem starts at the consonant(s) just before this ai/au
            for k in (0, 1, 2, 3):
                if i - k >= 0 and tok[i - k:].startswith(v):
                    return m.group(0)
        return {"ai": "e", "au": "o"}[m.group(0)]
    # only word-internal, followed by a consonant that is not a word-final ending
    out = []
    pos = 0
    for m in re.finditer(r"a[iu]", tok):
        i = m.start()
        if i == 0 or tok[i - 1] == "a" or i + 2 >= len(tok):
            continue
        if not any(ch in "aAiIuUReoL" for ch in tok[:i]) and not tok.startswith(("svau", "svai")):
            continue   # word-initial consonant cluster + ai/au: genuine vrddhi
        tail = tok[i + 2:]
        if tail in ("H", "z", "s", "r", "S", "M", "m") or re.fullmatch(r"[HzsrSMm]", tail):
            continue
        if tail[0] in "aAiIuUReo":
            continue
        out.append((i, fix(m)))
    if out:
        t = list(tok)
        for i, rep in reversed(out):
            t[i:i + 2] = list(rep)
        tok = "".join(t)
    tok = re.sub(r"(?<=.)ae", "ai", tok)   # e-text marks a+e as 'ae'
    tok = re.sub(r"(?<=.)Ae", "ai", tok)
    tok = re.sub(r"(?<=.)uu", "U", tok)
    tok = re.sub(r"(?<=.)ii", "I", tok)
    tok = re.sub(r"(?<=.)Ao", "au", tok)
    return tok

VOW = "aAiIuURLeo"
def _first_vowel(w):
    if w.startswith(("ai", "au")):
        return w[:2]
    return w[0] if w and w[0] in VOW else None

# a-final words whose -a is underlying (so a+V sandhi applies). Other -a before a vowel
# in the e-text is hiatus (from -aH / -e) and must stay separate.
A_WORDS = set("saha nAma atha ca na eva iva atra tatra yatra kutra sarvatra anyatra ekatra ubhayatra iha ha sma Aha "
              "uta yena tena kena anena ena".split())
AA_WORDS = set("tathA yathA sadA tadA yadA kadA sarvathA anyathA ubhayathA ekadA vA mA vinA sahA "
               "sA yA kA eSA saiSA".split())

def _a_underlying(w):
    if w in A_WORDS:
        return True
    return w.endswith(("ena", "eNa", "sya"))

def _aa_underlying(w):
    if w in AA_WORDS:
        return True
    return w.endswith(("yA", "tA", "nA", "NA", "dhA", "kA", "tvA", "tmA")) and len(w) > 2

FUNC = set(("iti ity eva api apy iva ca na hi tu vA cet punaH punar tathA yathA ced iha atra tatra kila khalu "
            "Aha AhuH ayam ayaM iyam iyaM idam idaM anena asya asau eSa etat etad evam evaM atha anyathA anyatra "
            "ataH asti santi").split())

def _free_word(w):
    """Next-line word that is clearly a separate word (not the tail of a compound)."""
    return w in FUNC or w.endswith(("te", "nte", "ti", "nti", "yAt", "tAm", "eta"))

def _vsandhi(a, b, force=False, last=None):
    """Vowel sandhi between a and b. force=True for compound junctions (line breaks)."""
    fb = _first_vowel(b)
    if fb is None or not a:
        return None
    if a.endswith(("ai", "au")):
        if a.endswith("au") and not force:
            return a[:-2] + "Av " + b
        return None
    la = a[-1]
    last = last or a
    if la == "a" and (force or _a_underlying(last)) or la == "A" and (force or _aa_underlying(last)):
        m = {"a": "A", "A": "A", "i": "e", "I": "e", "u": "o", "U": "o", "R": "ar",
             "e": "ai", "ai": "ai", "o": "au", "au": "au"}.get(fb)
        if m:
            return a[:-1] + m + b[len(fb):]
    if la in "oe" and fb == "a":
        return a + "'" + b[1:]
    if la in "iI" and fb in ("i", "I"):
        return a[:-1] + "I" + b[1:]
    if la in "uU" and fb in ("u", "U"):
        return a[:-1] + "U" + b[1:]
    if la == "i" or (force and la == "I"):
        return a[:-1] + "y" + b
    if la == "u" or (force and la == "U"):
        return a[:-1] + "v" + b
    return None

VOICED = set("gjDdbnmyrlvhGJN") | set(VOW)
def _visarga(a, b):
    """Visarga sandhi before b (e-text sometimes leaves H across line/verse breaks)."""
    if not a.endswith("H") or len(a) < 2:
        return None
    v = a[-2]
    f = b[0]
    if a.endswith("aH") and not a.endswith(("AH",)):
        if f == "a":
            return a[:-2] + "o'" + b[1:]
        if f in VOW:
            return a[:-1] + " " + b
        if f in VOICED:
            return a[:-2] + "o " + b
    if a.endswith("AH"):
        if f in VOICED:
            return a[:-1] + " " + b
    if f in "tT" or f == "c":
        return a[:-1] + {"t": "s", "T": "S", "c": "z"}[f] + " " + b
    if a.endswith("AH"):
        return None
    if f in VOICED:
        if f == "r":
            return a[:-2] + {"i": "I", "u": "U"}.get(v, v) + " " + b
        return a[:-1] + ("r" + b if f in VOW else "r" + b)
    return None

def _tfinal(a, b):
    """Final t/d of a before b (only if e-text left it unassimilated)."""
    if not a or a[-1] not in "td":
        return None
    f = b[0]
    base = a[:-1]
    if f == "z":
        return base + "cch" + b[1:]
    if f == "c":
        return base + "c" + b
    if f == "j":
        return base + "j" + b
    if f == "l":
        return base + "l" + b
    if f in "nm":
        return base + "n" + b
    if f == "h":
        return base + "ddh" + b[1:]
    if f in VOICED:
        return base + "d" + b
    return base + "t" + b

CONS = "kgcjTDtdnpbmlrsSzhGJNyv"
H_GEM = {"d": "ddh", "g": "ggh", "b": "bbh", "D": "DDh", "j": "jjh"}

def _stem_like(w):
    """Heuristic for a line-final token: compound member (join without space)?"""
    if w in INDECL or w in A_WORDS or w in AA_WORDS:
        return False
    if w[-1] in "aiuR" and not w.endswith(("sya", "ena", "eNa", "ati", "Ni", "ini", "au", "ai", "Ani", "Ini", "Uni", "Aya", "Su")):
        return True
    return False

class Token:
    __slots__ = ("w", "line", "verse", "bol")
    def __init__(self, w, line, verse, bol):
        self.w, self.line, self.verse, self.bol = w, line, verse, bol

# verse lines that lack the leading tab in the e-text
EXTRA_VERSE_LINES = {"03405", "03406"}

def load(path=SRC_DEFAULT):
    toks = []
    for raw in open(path, encoding="utf-8"):
        m = re.match(r"^(\d{5}) (.*)$", raw.rstrip("\n"))
        if not m:
            continue
        num, body = m.groups()
        verse = body.startswith("\t") or num in EXTRA_VERSE_LINES
        body = re.sub(r"//\s*(\d+)\s*/(?!/)", r"//\1//", body)   # e-text slip: '//63 /'
        body = re.sub(r"//\s*(\d+)\s*//", r" ||\1|| ", body)
        body = body.replace("//", " || ").replace("/", " | ")
        for k, w in enumerate(body.split()):
            toks.append(Token(w, num, verse, k == 0))
    return toks

def loc(line):
    return "%d,%d" % (int(line[:3]), int(line[3:]))

def render_hk(tokens, fixes=()):
    """Join a run of tokens into sandhied HK text."""
    res = []          # output words (space separated)
    last = None       # last raw word merged into res[-1]
    for t in tokens:
        w = t.w
        if w.startswith("|"):
            if res and res[-1].endswith("M"):
                res[-1] = res[-1][:-1] + "m"
            if res and res[-1][-1:] in "gdDb":
                res[-1] = res[-1][:-1] + {"g": "k", "d": "t", "D": "T", "b": "p"}[res[-1][-1]]
            res.append(w); last = w; continue
        w = _junction_vowels(w)
        if not res or res[-1].startswith("|"):
            res.append(w); last = w; continue
        prev = res[-1]
        compound = t.bol and not _free_word(w) and _stem_like(last)
        j = _vsandhi(prev, w, force=compound, last=last)
        if j is None:
            j = _visarga(prev, w)
        if j is None and prev[-1] in "td":
            j = _tfinal(prev, w)
        if j is not None:
            res[-1:] = j.split(" ")
        elif prev[-1] == "n" and len(prev) > 1 and prev[-2] in "aiu" and w[0] in VOW:
            res[-1] = prev + "n" + w          # san eva -> sanneva
        elif prev[-1] == "M" and w[0] in VOW:
            res[-1] = prev[:-1] + "m" + w
        elif prev[-1] == "m" and w[0] not in VOW:
            res[-1] = prev[:-1] + "M"
            res.append(w)
        elif prev[-1] in CONS:
            if w[0] == "h" and prev[-1] in "kgcjTDtdpb":
                if prev[-1] in H_GEM:
                    res[-1] = prev[:-1] + H_GEM[prev[-1]] + w[1:]
                else:
                    res.append(w)
            elif prev[-1] == "c" and w[0] == "z":
                res[-1] = prev + "ch" + w[1:]
            else:
                res[-1] = prev + w
        elif compound:
            res[-1] = prev + w
        else:
            res.append(w)
        last = w
    out = " ".join(res)
    for a, b in fixes:
        if a not in out:
            raise ValueError("fix not found: %r in %r" % (a, out[:80]))
        out = out.replace(a, b, 1)
    return out

def dev(hk):
    return sanscript.transliterate(hk, sanscript.HK, sanscript.DEVANAGARI)
