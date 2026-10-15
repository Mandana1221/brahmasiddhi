"""Repeatedly build; drop fix tuples reported as 'not applied' (obsolete after sandhi-rule changes)."""
import subprocess, re, glob, ast
for _ in range(40):
    r = subprocess.run(["python3", "build.py"], capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r"fixes not applied: (\[.*\])", out)
    if not m:
        print(out.strip()); break
    bad = ast.literal_eval(m.group(1))
    for f in glob.glob("units/part*.py"):
        s = open(f).read()
        t = s
        for a, b in bad:
            pat = "(%r, %r)" % (a, b)
            pat2 = '("%s", "%s")' % (a, b)
            for p in (pat, pat2):
                t = t.replace(p + ", ", "").replace(", " + p, "").replace("  fixes=[" + p + "],\n", "")
        if t != s:
            open(f, "w").write(t); print("pruned", bad, "in", f)
