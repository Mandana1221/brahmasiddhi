import re, html
from indic_transliteration import sanscript as S

import os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
STYLE = open(D + "style.html").read()
EXTRA = """<style>
.mula .vr{font-size:.74rem;font-weight:700;color:var(--gold);background:var(--gold-soft);border-radius:4px;padding:0 6px;margin-left:6px;letter-spacing:.04em}
.mula .lac{color:var(--muted)}
.crit{margin-top:10px;font-size:.84rem;line-height:1.75;color:var(--muted);border-top:1px dashed var(--line);padding-top:8px}
.crit b{color:var(--ink);font-weight:700}
.crit i{color:var(--ink)}
.mula.vrtti{border-left-color:var(--muted)}
</style>"""

FINAL_CONS = set("kgṅcjñṭḍṇtdnpbmyrlvśṣsh")

def dev(iast):
    """IAST (edition spacing) -> Devanagari: join consonant-final words, punctuation."""
    t = iast.strip()
    t = t.replace("…", " @@ ")
    # join consonant-final word with following word
    toks = t.split(" ")
    out = []
    for w in toks:
        if out and out[-1] and out[-1] not in ("/", "//", "@@") and w not in ("/", "//", "@@") \
           and out[-1][-1] in FINAL_CONS and not out[-1].endswith(("ḥ",)) and w[:1] not in ".,":
            out[-1] = out[-1] + w
        elif out and w.startswith("'"):
            out[-1] = out[-1] + w
        else:
            out.append(w)
    t = " ".join(out)
    t = t.replace("//", "॥").replace("/", "।")
    d = S.transliterate(t, S.IAST, S.DEVANAGARI)
    d = d.replace(".", " ।").replace("–", "—").replace("@@", '<span class="lac">…</span>')
    d = re.sub(r"\s+", " ", d).replace(" ।", " ।")
    return d

def mula(ref, iast, tr, exp, kind="", crit=""):
    cls = "mula" + (" " + kind if kind else "")
    c = f'<div class="crit">{crit}</div>' if crit else ""
    e = f'<div class="exp"><span class="lbl">解説</span>{exp}</div>' if exp else ""
    return f'''<div class="{cls}">
  <span class="ref">{ref}</span>
  <div class="src deva" lang="sa">{(dev(iast).replace(" । ", " ।<br>", 1) if kind == "sutra" else dev(iast))}</div>
  <div class="tr">{tr}</div>{c}{e}
</div>'''

# ------------------------------------------------------------------ content
K = {
1: "pāratantryaṃ hi sambandhaḥ siddhe kā paratantratā / tasmāt sarvasya bhāvasya sambandho nāsti bhāvataḥ // 1",
2: "rūpaśleṣo hi sambandho dvitve sa ca kathaṃ bhavet / tasmāt prakṛtibhinnānāṃ sambandho nāsti bhāvataḥ // 2",
3: "parāpekṣā hi sambandhaḥ so 'san katham apekṣate / saṃś ca sarvanirāśaṃso bhāvaḥ katham apekṣate // 3",
4: "dvayor ekābhisambandhāt sambandho yadi taddvayoḥ / kaḥ sambandho 'navasthā ca na sambandhamatis tathā // 4",
}

sections = []

# ---------------- §0 maṅgala + purpose
s0 = []
s0.append(mula("SP 3,1 / SPV 11,2",
  "namo vītarāgāya // vastubhūtaṃ sambandhaṃ nirākartum āha – pāratantryam ityādi.",
  "離欲者（<i>vītarāga</i>）に帰命する。——実在としての関係を退けるために、「従属とは…」云々と言う。",
  "<p>帰敬はカーリカー部の写本冒頭のもの。続く一文は Vṛtti の導入で、校訂者の分析では全体の目的（0. „the refutation of relation as real“, 11,2）に当たる。</p>"
  "<p>否定の対象は <i>vastubhūta</i> な関係、つまり実在の側に立てられた関係に限定されている。第1偈 Vṛtti の結び <i>vikalpanirmitasyāpratiṣedhaḥ</i> と対をなし、本書全体が二諦的な枠組みで書かれていることを最初に示す。<i>sambandha</i> は分別によって構成され、言語活動（<i>vyavahāra</i>）で用いられるかぎりでは否定されない（第5–6偈）。</p>",
  crit="<b>本文</b>　<i>vastubhūtaṃ sambandhaṃ nirākartum</i> : <i>vastubhūta+ sambandha+ nirākartum</i> Ms（校訂者による補正）。"))
sections.append(("s0", "0", "帰敬と目的", "SP 3 / SPV 11,2", "実在としての関係の否定という全体の目的", "".join(s0)))

# ---------------- §1 k.1
s1 = []
s1.append(mula("SP 3 / k.1", K[1],
  "関係とは、他への従属（<i>pāratantrya</i>）にほかならない。〔しかし〕すでに成立しているものに、どんな他への従属があろうか。それゆえ、いかなる存在にも、実在としての関係はない。",
  "", kind="sutra",
  crit="<b>異読</b>　1d <i>bhāvataḥ</i> Ms, TR（Tib. <i>yaṅ dag ñid du</i>）: <i>tattvataḥ</i> TŚV, AS, PKM, NKC, SVR, VR, F。Jaina 系の引用と Frauwallner の再構成はすべて <i>tattvataḥ</i>。Ms の読みは Vṛtti の注 <i>bhāvato vastutaḥ</i>（11,11f）によって支持される。"))
s1.append(mula("SPV 11,4–7",
  "pāratantryaṃ parāyattatā. sā sambandhaḥ sambandhinaḥ siddhasyāsiddhasya vā bhavet. asiddhasyābhāvarūpatvān na vastubhūtaḥ sambandhaḥ. siddhe 'pi sambandhini kā paratantratā. naivety asambandhaḥ.",
  "「従属」とは他に依存していること（<i>parāyattatā</i>）である。関係であるそれは、すでに成立した関係項にあるか、成立していない関係項にあるかのどちらかであろう。成立していないものは非存在を本質とするので、〔その場合〕関係は実在ではない。成立した関係項についても、どんな従属があろうか。まったくない。だから無関係である。",
  "<p>論法は単純な両刀論法である。関係を「関係項 x が他に従属していること」と定義すると、その述定の主語 x は (a) 未成立か (b) 既成立かのどちらかである。(a) 未成立の x は <i>abhāvarūpa</i>、すなわち何ものでもないので、それに属性としての従属は帰属できない。(b) 既成立の x は、自らの存在のために他を必要としないので、従属する余地がない。</p>"
  "<p>前提になっているのは、存在するものは自らの原因から完成した姿で生じる、という Dharmakīrti の存在論である。PVSV 第1章でも、生じた事物は「その状態について他に依存しない」（<i>jātasya tadbhāve 'nyānapekṣaṇāt</i>、PVSV 100,2）と言われ、消滅無因論の根拠になっていた。従属は生成の局面にしか場所をもたず、しかも生成の局面には従属の主語がまだない。この構図が第3偈と第7–9偈でも繰り返される。</p>",
  kind="vrtti",
  crit="<b>本文</b>　6 <i>naivety</i> : <i>nevety</i> Ms。冒頭 <i>pāratantryaṃ parāyattatā. sā sambandhaḥ … bhavet</i> は Bhāsarvajña, <i>Nyāyabhūṣaṇa</i> 503,13 に引用（Cie）。"))
s1.append(mula("SPV 11,8–10",
  "siddhasyāpi kiñcid asiddham astīti [cet]. tatsiddhau pāratantryam api na saṅgacchate, siddhāsiddhabhāvidoṣavikalpānatikramāt. na caikasya niṣpannāniṣpanne rūpe staḥ.",
  "〔反論〕「成立したものにも、何か未成立の〔部分〕がある」〔と言うなら〕。〔答論〕その〔部分〕の成立に関しても、従属は成り立たない。成立したもの・未成立のものに伴う過失という二者択一を免れないからである。また、一つのものに、完成した姿と未完成の姿〔の二つ〕があるのではない。",
  "<p>反論者は、x の一部が未完成で、その部分が他に依存すると考えて (a)(b) の間をすり抜けようとする。Devendrabuddhi は二段で答える。第一に、その「部分」についても同じ両刀論法がそのまま繰り返される（<i>vikalpānatikramāt</i>）。第二に、一つのものに完成・未完成の二つの姿はない。後者は、矛盾する属性をもてば別の事物である（<i>viruddhadharmādhyāsa</i> による差異の規準）という原則の適用である。</p>"
  "<p><i>siddhāsiddhabhāvidoṣa</i> は「成立・未成立〔のそれぞれ〕に生じる過失」と解した。</p>"
  "<p>Steinkellner（2022, 試訳）は <i>tatsiddhau</i> の <i>tat</i> を「未成立の面をもつその存在」と取り、「それが成立しているときにも従属は成り立たない」と解する。ここでは <i>tat</i> を直前の <i>kiñcid asiddham</i>（未成立の部分）と取った。続く「二者択一を免れない」という理由は、問題の部分そのものに既成立・未成立の両刀論法が再適用される、という構図に合うからである。どちらに取っても論の帰結は変わらない。</p>",
  kind="vrtti",
  crit="<b>本文</b>　8 <i>tatsiddhau</i> : <i>tatsiddho</i> Ms。<i>iti</i> の後の <i>cet</i> は訳で補った。"))
s1.append(mula("SPV 11,10–12",
  "yata evaṃ na niṣpannasyetarasya vā pāratantryam, tasmāt sarvasya bhāvasya sambandho nāsti bhāvato vastutaḥ. vikalpanirmitasyāpratiṣedho 'vastutvāt.",
  "このように、完成したものにもそうでないものにも従属はないので、それゆえ、いかなる存在にも、<b>実在として</b>（<i>bhāvataḥ</i>）、すなわち実在の上で（<i>vastutaḥ</i>）関係はない。分別によって作られた〔関係〕は否定しない。〔それは〕実在ではないからである。",
  "<p>最後の一文が本書の射程を決める。否定されるのは実在の関係だけで、分別が構成する関係は、実在でないという理由で否定の対象にならない。否定とは、実在に何かがあるという主張を退けることだからである。この「分別による関係」の積極的な説明は第5偈（<i>tān miśrayati kalpanā</i>）と第6偈（言語の行為・行為者の語）で与えられる。</p>"
  "<p>この一文は、PV 第1章が論証因の根拠として説く本質的結合（<i>svabhāvapratibandha</i>）との整合という問題にも答えている。結合は二項間の実在の関係ではない。結果の本性が原因の本性に依って生じている、という一項ごとの本性の事実を、分別が「関係」として構成したものにすぎない。第16偈の <i>bhāve bhāvini tadbhāvo bhāva eva ca bhāvitā</i> がその定式である。</p>",
  kind="vrtti",
  crit="<b>本文</b>　10 <i>°syetarasya</i> : <i>°syaitarasya</i> Ms。11f <i>nāsti bhāvato vastutaḥ</i> rec.（SPVt <i>yaṅ dag ñid du dṅos por med</i>）: <i>nāsti bhā . . . . . taḥ</i> Ms。12 <i>°nirmitasyāpratiṣedho</i> rec.（T <i>mi dgag</i>）: <i>°ni+mitasyā.r . . . . dho</i> Ms。<i>'vastutvāt</i> rec.（SPVt <i>dṅos po med pa'i phyir</i>）: <i>'va . . tvāt</i> Ms。最後の二文の大部分は写本の欠損をチベット訳から復元した読み。"))
fig1 = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 270" style="min-width:560px;width:100%" role="img" aria-label="第1偈の両刀論法。関係を他への従属と定義すると、関係項は未成立か既成立かで、どちらでも従属は成り立たない">
    <defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <rect x="180" y="10" width="300" height="52" rx="10" class="s-band"/>
    <text x="330" y="33" text-anchor="middle" font-size="14" font-weight="700" class="s-ink">関係＝関係項 x の他への従属</text>
    <text x="330" y="52" text-anchor="middle" font-size="12" class="ia s-muted" font-style="italic">pāratantrya = parāyattatā</text>
    <path d="M280 62 L170 98" class="st-muted" stroke-width="1.5" marker-end="url(#m1)"/>
    <path d="M380 62 L490 98" class="st-muted" stroke-width="1.5" marker-end="url(#m1)"/>
    <rect x="40" y="100" width="260" height="70" rx="10" class="s-jatisoft"/>
    <text x="170" y="124" text-anchor="middle" font-size="13.5" font-weight="700" class="s-jati">x は未成立（asiddha）</text>
    <text x="170" y="145" text-anchor="middle" font-size="12" class="s-ink">非存在を本質とする（abhāvarūpa）</text>
    <text x="170" y="162" text-anchor="middle" font-size="12" class="s-ink">→ 従属の担い手がない</text>
    <rect x="360" y="100" width="260" height="70" rx="10" class="s-jatisoft"/>
    <text x="490" y="124" text-anchor="middle" font-size="13.5" font-weight="700" class="s-jati">x は既成立（siddha）</text>
    <text x="490" y="145" text-anchor="middle" font-size="12" class="s-ink">自らの姿は完成している</text>
    <text x="490" y="162" text-anchor="middle" font-size="12" class="s-ink">→ 従属の余地がない</text>
    <path d="M490 170 V196" class="st-muted" stroke-width="1.5" marker-end="url(#m1)"/>
    <rect x="360" y="198" width="260" height="62" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="490" y="220" text-anchor="middle" font-size="12" class="s-muted">反論：一部は未成立である</text>
    <text x="490" y="240" text-anchor="middle" font-size="12" class="s-ink">→ その部分に同じ二者択一が再来</text>
    <text x="490" y="255" text-anchor="middle" font-size="11" class="s-muted">一つのものに完成・未完成の二姿はない</text>
    <rect x="40" y="198" width="260" height="62" rx="10" class="s-anssoft"/>
    <text x="170" y="222" text-anchor="middle" font-size="13" font-weight="700" class="s-ans">実在としての関係はない</text>
    <text x="170" y="244" text-anchor="middle" font-size="12" class="s-ink">分別が作る関係は否定しない</text>
  </svg>
  </div>
  <figcaption><b>図1　第1偈の両刀論法。</b>Vṛtti 11,4–12 の論の運び。右下の反論（11,8–10）は二者択一を部分に移しても同じ形で反復されるだけだ、という形で処理される。</figcaption>
</figure>'''
s1.insert(2, fig1)
sections.append(("s1", "1", "従属としての関係の否定", "k.1 / SPV 11,4–12", "関係＝他への従属（pāratantrya）", "".join(s1)))

# ---------------- §2 k.2
s2 = []
s2.append(mula("SP 3 / k.2", K[2],
  "〔反論〕関係とは、姿の融合（<i>rūpaśleṣa</i>）である。〔答論〕〔関係項が〕二つであるとき、それがどうしてありえようか。それゆえ、本性において別々のもの（<i>prakṛtibhinna</i>）どうしには、実在としての関係はない。",
  "", kind="sutra",
  crit="<b>異読</b>　2a <i>rūpaśleṣo</i> : <i>rūpeśleṣo</i> VR。2b <i>sa ca</i> : <i>sati</i> ĪPVV。2d <i>bhāvataḥ</i> Ms, TR : <i>tattvataḥ</i> TŚV, PKM, NKC, SVR, VR, F（第1偈と同じ分布）。"))
s2.append(mula("SPV 12,3–6",
  "rūpaśleṣo hi sambandhaḥ, na pāratantryam iti cet, tan na. dvitve sambandhinoḥ sva … sa svarūpaśleṣaḥ svabhāvaikātmyalakṣaṇaḥ kathaṃ bhavet. naiva bhavet. aikye 'pi tayoḥ sambandhinor abhāvāt kaḥ sambandhaḥ, dviṣṭhatvād asya.",
  "「関係とは姿の融合であって、従属ではない」と言うなら、そうではない。関係項が二つであるとき、〔それぞれが自らの姿をもっているのだから（欠損部、チベット訳による）〕、本性が一体であることを特徴とするその自らの姿の融合が、どうしてありえようか。決してありえない。〔逆に〕一体になったとしても、二つの関係項がなくなるので、どんな関係があろうか。これ（関係）は二つのものにあるからである。",
  "<p>第二の定義は、関係を二項の姿が溶け合うこととみなす。Vṛtti はこれを <i>svabhāvaikātmya</i>、すなわち本性の同一化と解し、二者択一にかける。二であれば融合はなく、一であれば関係項が二つないので関係はない。関係は定義上二項にある（<i>dviṣṭha</i>）からである。</p>"
  "<p><i>dviṣṭha</i> という要件は、第7偈（因果関係は継起するので二項に同時に立たない）と第11偈（<i>dviṣṭho hi kaścit sambandhaḥ</i>）でも論の支点になる。本書は全体として、「関係は二項に同時に立つ実在でなければならない」という対論者の前提を逆手に取っている。</p>",
  kind="vrtti",
  crit="<b>本文</b>　3 <i>rūpaśleṣo hi sambandhaḥ</i> rec.（PKM 516,1; SPVt <i>ṅo bo 'dres pa 'brel pa yin gyi</i>）: 欠損 Ms。4 <i>sva . . . . .</i>：写本の欠損。SPVt は <i>'brel pa can gñis kyi ṅo bo yin na</i>（二つの関係項の姿であるなら）と訳しており、訳はこれで補った。5 <i>aikye 'pi</i> rec.（SPVt <i>gcig tu gyur na yaṅ</i>）: <i>ekya yi</i> Ms。5f <i>aikye … asya</i> は NKC 305,19–20 に並行（cf.）。"))
s2.append(mula("SPV 12,7–11",
  "syād etat – naikasvābhāvyaṃ śleṣaḥ. kiṃ tarhi. nairantaryam iti. bhavatu. kaḥ pratiṣedhaḥ. kevalaṃ nairantaryam antarābhāva iti vastubhūtaḥ sambandho na syāt. yadi ca nairantaryaṃ sambandhaḥ, sāntaratā kiṃ na sambandha iṣyate, ubhayatrāpi sambandhinoḥ svabhāvasthiter abhedāt. prāptyādayo 'pi nairantaryārthasamāveśina ity anudghoṣyāḥ.",
  "こう言うかもしれない。「融合とは本性が一つであることではない。では何か。間がないこと（<i>nairantarya</i>）である」と。それでよい。何を否定しようか。ただ、間がないことは間の欠如にすぎないので、実在としての関係ではないことになろう。また、もし間がないことが関係なら、間があること（<i>sāntaratā</i>）はなぜ関係と認められないのか。どちらの場合も、関係項が自らの本性にとどまっていることに違いはないからである。到達（<i>prāpti</i>）なども、間がないという意味に含まれるので、〔実在の関係として〕言い立てるべきではない（<i>anudghoṣya</i>）。",
  "<p>「融合」を緩めて「間がないこと」（隣接）と読み替える反論。Devendrabuddhi はこれを否定しない（<i>bhavatu</i>）。ただし <i>nairantarya</i> を分析すれば <i>antarābhāva</i>、つまり〔第三のものの〕非存在であり、非存在は実在ではないので、隣接は実在の関係にならない。</p>"
  "<p>続く対称性の議論が要点である。隣接していても離れていても、各項はそれぞれの本性にとどまっていて、項の側には何の違いもない（<i>svabhāvasthiter abhedāt</i>）。項の内在的なあり方に差を生まないものを実在の関係と呼ぶなら、離れていることも関係でなければならない。関係が実在であるための条件は、関係項に実在的な差を生むことだ、という基準がここで暗に用いられている。</p>"
  "<p><i>prāpti</i> は「到達・接触」の意で、隣接と同類の空間的関係として一括される。Steinkellner（2022, 試訳, n.1）は、<i>prāpti</i> と定義される関係が Vātsyāyana の <i>Nyāyabhāṣya</i> 87,16–88,14（NSū 2.1.52–54 への注）で論駁されていることを指摘する。<i>anudghoṣyāḥ</i> も同氏に従い、対論者が〔実在の関係として〕主張すべきではない、の意に取った。</p>",
  kind="vrtti",
  crit="<b>本文</b>　8 <i>naira&lt;nta&gt;ryam</i> em. : <i>nairaryam</i> Ms。11 <i>nairantaryā°</i> : <i>nerantaryā°</i> Ms。"))
s2.append(mula("SPV 12,11–14",
  "yata evaṃ na rūpaśleṣalakṣaṇo 'pi sambandhaḥ, tasmāt prakṛtibhinnānāṃ sarvabhāvānāṃ sambandho nāsti bhāvato 'nyatra kalpanāsamāropitāt.",
  "このように、姿の融合を特徴とする関係もないので、本性において別々のあらゆる存在には、分別によって付託された〔関係〕以外に、実在としての関係はない。",
  "<p>第1偈 Vṛtti の結論と同じ型の結び。ここでは <i>kalpanāsamāropita</i>（分別による付託）という語が使われる。<i>prakṛtibhinna</i> は、各存在が本性においてすでに別々であることを言い、第5偈 <i>sarve te svātmani sthitāḥ</i> の先取りになっている。</p>",
  kind="vrtti"))
sections.append(("s2", "2", "融合としての関係の否定", "k.2 / SPV 12,3–14", "関係＝姿の融合（rūpaśleṣa）、隣接（nairantarya）", "".join(s2)))

# ---------------- §3 k.3
s3 = []
s3.append(mula("SP 3 / k.3", K[3],
  "〔反論〕関係とは、他者の依存（<i>parāpekṣā</i>）である。〔答論〕それ（関係項）が存在しないなら、どうして依存しようか。また、存在するなら、いかなるものにも期待をもたない（<i>sarvanirāśaṃsa</i>）存在が、どうして依存しようか。",
  "<p><i>parāpekṣā</i> は通常「他への依存」と読める複合語だが、Vṛtti は <i>parasyāpekṣamāṇasyāpekṣayā</i>（依存する他者の依存によって、13,4）と分析し、<i>para</i> を依存の主体（属格）と取る。Steinkellner（2022, 試訳）もこれに従って „reliance of another“ と訳す。一方の項から見た「他者」、つまりもう一方の関係項がこちらを当てにすること、が関係だという定義である。訳はこの Vṛtti の分析に従った。</p>",
  kind="sutra",
  crit="<b>異読</b>　3a <i>parāpekṣā hi</i> : <i>parāpekṣādi</i> TŚV : <i>parāpekṣā yadi</i> ĪPVV。3b <i>so 'san</i> : <i>so sat</i> TŚV。3d <i>apekṣate</i> : <i>apekṣyate</i> TŚV。"))
s3.append(mula("SPV 13,3–6",
  "atha parāpekṣā hi sambandho na rūpaśleṣa iti. atrāpi parasyāpekṣamāṇasyāpekṣayā sambandhitve 'pekṣamāṇaḥ san vā 'pekṣate 'san vā. yady asan so 'san katham apekṣate. svayam anabhinirvṛttasvabhāvasya bhāvasyāpekṣā na dharmaḥ syād iti kaḥ kasya sambandhaḥ.",
  "では、「関係とは他者の依存であって、姿の融合ではない」と言うなら。この場合も、依存する他者の依存によって〔ものが〕関係項となるとき、依存するものは、存在していて依存するのか、存在せずに依存するのか。もし存在しないなら、存在しないそれがどうして依存しようか。自らの本性がまだ生じていない存在には、依存は属性としてありえないので、何が何の関係であろうか。",
  "<p>第三の定義 <i>apekṣā</i> は、第1偈の <i>pāratantrya</i> と内容的にはほぼ同じで、Vṛtti も最後に「残りは従属の場合と同様」と言う。違いは、<i>apekṣā</i> が「何かを当てにする・期待する」という志向的な語で、偈が <i>nirāśaṃsa</i>（期待をもたない）という擬人的な語で応じている点にある。</p>"
  "<p>未成立の側の処理は第1偈と同じだが、ここでは <i>dharma</i> の語が明示される。依存はある基体の属性でなければならないが、基体の本性がまだ成立していない（<i>anabhinirvṛttasvabhāva</i>）なら、属性の担い手がない。</p>",
  kind="vrtti",
  crit="<b>本文</b>　4 <i>'pekṣamāṇaḥ</i> : <i>'pekṣyamāṇaḥ</i> Ms。"))
s3.append(mula("SPV 13,7–8",
  "saṃś ca sarvanirāśaṃsaḥ sarvasvabhāvabhāvānapekṣo bhāvaḥ katham apekṣate yenāpekṣā sambandhaḥ syāt. śeṣaṃ pāratantryavad vācyam.",
  "また、存在するなら、「いかなるものにも期待をもたない」、すなわち自らの本性のすべてがすでに生じているので〔何ものにも〕依存しない（<i>sarvasvabhāvabhāvānapekṣa</i>）存在が、どうして依存しようか。それによって依存が関係となるような〔依存が〕。残りは従属の場合と同様に述べるべきである。",
  "<p>Ms の複合語 <i>sarvasvabhāvasvabhāvānapekṣa</i> は解しにくい。校訂者は Ms の読みを採り、チベット訳 SPVt が <i>raṅ gi ṅo bo thams cad skyes pa (!) bltos pa med pa'i</i>（自らの姿のすべてが生じていて、依存しない）と訳していることを注記し、Vinītadeva の <i>Sambandhaparīkṣāṭīkā</i>（T）5a8–5b3 の説明を参照させている。Steinkellner（2022, 試訳）の序文は、二つ目の <i>svabhāva</i> を <i>bhāva</i> と改める Eltschinger の提案を記す。<i>°bhāva°</i> は SPVt の <i>skyes pa</i>（生じた）にそのまま対応し、校訂者が „(!)“ を付した齟齬が解ける。ここではこの提案を採り、「本性のすべてが生じていること（<i>sarvasvabhāvabhāva</i>）によって〔他に〕依存しない」と解した。既成立の存在には生じるべき部分が残っていない、という第1偈 Vṛtti の論点（11,8–10）の言い換えになる。</p>"
  "<p>既成立の存在は何ものにも依存しない、というこの論点は、PVSV で消滅の原因を退けたときの論法と同じである。そこでは、何もしないもの（<i>akiṃcitkara</i>）は依存されない（<i>nāpekṣyate</i>）と言われていた（PVSV 100,13f、第196偈）。依存（<i>apekṣā</i>）が成り立つのは助けるもの（<i>upakārin</i>）に対してだけで、すでに完成したものを助けることはできない。本書第9偈（<i>upakārī hy apekṣyaḥ syāt</i>）でこの論点が因果関係に適用される。</p>",
  kind="vrtti",
  crit="<b>本文</b>　7 <i>°nirāśaṃsaḥ</i> : <i>°nirāśa+saḥ</i> Ms。<i>sarvasvabhāvabhāvānapekṣo</i> em.（Eltschinger の提案（Steinkellner 2022 序文）; cf. SPVt <i>skyes pa</i>）: <i>sarvasvabhāvasvabhāvānapekṣo</i> Ms, ed.（校訂者は SPVt の訳に „(!)“ を付す）。"))
sections.append(("s3", "3", "依存としての関係の否定", "k.3 / SPV 13,3–8", "関係＝他者の依存（parāpekṣā）", "".join(s3)))

# ---------------- §4 k.4
s4 = []
s4.append(mula("SP 3 / k.4", K[4],
  "もし二つのものに、一つの〔第三のもの〕との結合によって関係がある（<i>ekābhisambandha</i>）とするなら、その〔一つのもの〕と二つとの関係は何か。また、無限遡及（<i>anavasthā</i>）になる。そうであれば、関係の観念も〔実在に即したものでは〕ない。",
  "", kind="sutra",
  crit="<b>異読</b>　4a <i>°sambandhāt</i> : <i>°sambandhā°</i> SVR。4a–b <i>ekābhisambandhāt sambandho</i> : <i>ekābhisambandho</i> Ms（Ms の脱文）。4b <i>taddvayoḥ</i> TŚV, PKM, SVR : <i>tad dvayoḥ</i> F。"))
s4.append(mula("SPV 14,3–9",
  "mā prāpad ayaṃ doṣa iti. dvayoḥ sambandhinor ekābhisambandhāt – ekenārthāntareṇa guṇākhyena saṃyogenānarthāntareṇa vā dharmeṇāvācyena vā vastubhūtena sambandhāt kāraṇāt – sambandho yadīṣyate, tadā 'narthāntarapakṣe sambandhinau kevalau kalpitau syātām iti na kaścit sambandhaḥ. tato 'pi vā sambandhāt sambandhinor avyatirekeṇaikatvāc ca, vastubhūtasyāvācyasyāpi nyāyato 'rthāntarānarthāntaravikalpānatikramāt. anarthāntarapakṣe na sambandhaḥ sambandhī vā kaścit.",
  "この過失が及ばないように、と〔考えて〕、二つの関係項に一つのものとの結合によって——すなわち、性質（<i>guṇa</i>）と呼ばれる結合（<i>saṃyoga</i>）のような、別個の一つのものとの結合、あるいは、〔関係項と〕別でない属性（<i>dharma</i>）との結合、あるいは、〔同とも異とも〕言い表せない（<i>avācya</i>）実在との結合、という原因によって——関係があると認めるなら、そのとき、別でないとする立場では、関係項二つだけが想定されたことになり、何の関係もない。あるいはまた、その関係と別でないので、二つの関係項が一つになってしまうからでもある。実在であるなら、言い表せないものであっても、道理上、別か別でないかという二者択一を免れないからである。別でないとする立場では、関係も関係項も何もない。",
  "<p>第1–3偈で、二項だけで関係を立てる案が尽きた。そこで対論者は第三項を立てる。Vṛtti はその第三項に三つの型を挙げる。</p>"
  "<ul><li><b>別個のもの</b>（<i>arthāntara</i>）：Vaiśeṣika の <i>saṃyoga</i> のように、二つの実体に同時に属する性質（<i>guṇa</i>）としての関係。</li>"
  "<li><b>別でないもの</b>（<i>anarthāntara</i>）：関係項と別でない属性（<i>dharma</i>）。</li>"
  "<li><b>言い表せないもの</b>（<i>avācya</i>）：関係項と同とも異とも言えない実在。</li></ul>"
  "<p>校訂本は <i>dharmeṇāvācyena vastubhūtena</i> と印刷し、<i>avācya</i> を「別でない属性」の限定と読ませるが、Steinkellner（2022, 試訳）の序文はこれを訂正して <i>°āvācyena vā</i> を em.（TŚV, T による）とし、試訳も三つの選択肢として訳す。ここでもこの訂正に従った。続く文が <i>avācya</i> を別・別でないの二者択一に回収する（<i>vastubhūtasyāvācyasyāpi …</i>）のも、それが独立の第三の選択肢として立てられていたからである。</p>"
  "<p>まず別でない場合を処理する。関係が項と別でないなら、立っているのは結局二つの項だけで、関係を立てなかったのと同じである（その場合の過失は第1–3偈で述べた）。また、二項がともにその一つの関係と別でないなら、二項どうしも同一になり、関係項の二性が失われる。「言い表せない」という逃げ道については、実在であるかぎり、同か異かの二者択一を免れないとして退ける。</p>"
  "<p><i>avācya</i> な第三項を誰が説いたのかは、ここでは示されていない。同一・別異のどちらとも言えないとする立場は、Jaina の論者などに見られるが、ここでの同定は保留する。なお、第4偈とその Vṛtti は Jaina の Vidyānanda（TŚV 148,26）と Prabhācandra（PKM 505,27–29）に引用されている。</p>",
  kind="vrtti",
  crit="<b>本文</b>　5 <i>°āvācyena vā</i> em.（TŚV, T; Steinkellner 2022 序文の訂正）: <i>°āvācyena</i> Ms, ed.。3f <i>sambandhinor</i> : <i>sambambinor</i> Ms。<i>ekābhisambandhād</i> : 一部判読不能 Ms。6 <i>sambandhinau</i> : <i>sambandhandhinau</i> Ms。<i>kalpitau</i> : <i>kalpito</i> Ms。9 <i>°vikalpānatikramāt</i> : <i>°vikalpanatikramāt</i> Ms。<i>sambandhī</i> : <i>sambandhā</i> Ms。<i>ekenārthāntareṇa … sambandhāt</i> は TŚV 148,26 に引用（Cie）。"))
tbl4 = '''<div class="tbl min"><table>
<thead><tr><th>第三項の型</th><th>例</th><th>Vṛtti の処理</th><th>帰結</th></tr></thead>
<tbody>
<tr><td class="k">別でない（<i>anarthāntara</i>）</td><td>関係項と別でない属性（<i>dharma</i>）</td><td>別でないなら、立つのは二項だけ</td><td><span class="pill j">二項だけの関係</span>（第1–3偈の過失）／二項の同一化</td></tr>
<tr><td class="k">言い表せない（<i>avācya</i>）</td><td>関係項と同とも異とも言えない実在</td><td>実在なら同・異の二者択一を免れない</td><td>別でない場合か別個の場合のどちらかに帰着</td></tr>
<tr><td class="k">別個（<i>arthāntara</i>）</td><td>性質（<i>guṇa</i>）としての結合（<i>saṃyoga</i>）</td><td>第三項と二項との関係が改めて問われる</td><td><span class="pill j">無関係</span> または <span class="pill j">無限遡及</span></td></tr>
</tbody></table></div>'''
s4.append(tbl4)
s4.append(mula("SPV 14,9–14",
  "bhavatu vā sambandho 'rthāntaram anyo vā, tathā taddvayoḥ kaḥ sambandhaḥ, tenaikena dvayoḥ sambandhinoḥ kaḥ sambandhaḥ. naiva. yathā sambandhinor yathoktadoṣān na sambandhaḥ, tathā 'nenāpi sambandhinor asambandhaḥ. anyathā kevalayoḥ sambandhinoḥ sambandhe kaḥ pratiṣedha iti.",
  "あるいは、関係が別個のものであれ、もう一方〔の選択肢〕であれ、そうであっても「それと二つとのどんな関係か」、すなわち、その一つのものと二つの関係項とには、どんな関係があるのか。まったくない。関係項どうしに、上述の過失のゆえに関係がないのと同じく、これ（第三のもの）と関係項とにも関係はない。さもなければ、関係項二つだけの関係に、何の否定があろうか。",
  "<p>別個の第三項 R を立てた場合。R と a、R と b の間の関係は、a と b の間の関係と同じ問題を抱える。第1–3偈の論証は「二つの実在のあいだの関係」一般に対するものなので、a–R、R–b にもそのまま当てはまる。逆に、もし R が a・b と直接に関係しうるなら、a と b も直接に関係しうるはずで、R を立てる意味がなくなる（<i>anyathā … kaḥ pratiṣedhaḥ</i>）。</p>"
  "<p>これは Vaiśeṣika の <i>saṃyoga</i> が、<i>guṇa</i> として実体に <i>samavāya</i> によって内属する、という二重構造への批判として読める。<i>samavāya</i> そのものの批判は第19–21偈で行われる。</p>",
  kind="vrtti",
  crit="<b>本文</b>　10 <i>tathā</i> : <i>tathā {dvai}</i> Ms。<i>bhavatu … asambandhaḥ</i> は PKM 505,27–29 に引用（Cie）。<i>yathā … 'nenāpi</i> は NKC 306,11 に並行（cf.）。"))
fig4 = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 230" style="min-width:560px;width:100%" role="img" aria-label="第4偈の無限遡及。aとbの関係に第三項Rを立てると、aとRの関係にさらに第四項が必要になる">
    <g font-size="13">
      <circle cx="90" cy="150" r="30" class="s-accsoft"/><text x="90" y="155" text-anchor="middle" font-weight="700" class="s-acc ia">a</text>
      <circle cx="570" cy="150" r="30" class="s-accsoft"/><text x="570" y="155" text-anchor="middle" font-weight="700" class="s-acc ia">b</text>
      <rect x="290" y="128" width="80" height="44" rx="10" class="s-goldsoft"/><text x="330" y="155" text-anchor="middle" font-weight="700" class="s-gold ia">R</text>
      <line x1="120" y1="150" x2="290" y2="150" class="st-muted" stroke-width="1.5" stroke-dasharray="5 4"/>
      <line x1="370" y1="150" x2="540" y2="150" class="st-muted" stroke-width="1.5" stroke-dasharray="5 4"/>
      <rect x="170" y="62" width="70" height="38" rx="9" class="s-jatisoft"/><text x="205" y="86" text-anchor="middle" font-weight="700" class="s-jati ia">R₁</text>
      <rect x="420" y="62" width="70" height="38" rx="9" class="s-jatisoft"/><text x="455" y="86" text-anchor="middle" font-weight="700" class="s-jati ia">R₂</text>
      <line x1="205" y1="100" x2="205" y2="146" class="st-jati" stroke-width="1.2"/>
      <line x1="455" y1="100" x2="455" y2="146" class="st-jati" stroke-width="1.2"/>
      <text x="205" y="40" text-anchor="middle" font-size="12" class="s-muted">a–R の関係は？</text>
      <text x="455" y="40" text-anchor="middle" font-size="12" class="s-muted">R–b の関係は？</text>
      <text x="205" y="56" text-anchor="middle" font-size="12" class="s-jati">さらに R₁₁ …</text>
      <text x="455" y="56" text-anchor="middle" font-size="12" class="s-jati">さらに R₂₁ …</text>
      <text x="330" y="205" text-anchor="middle" font-size="12" class="s-ink">一つのもの（<tspan class="ia" font-style="italic">ekārtha</tspan>）との結合で関係を立てると、その結合ごとに新たな一つのものが要る</text>
    </g>
  </svg>
  </div>
  <figcaption><b>図2　第4偈の無限遡及（<i>anavasthā</i>）。</b>Vṛtti 14,15–20。どこかで第三項なしの関係を認めれば、最初の a–b にも第三項は不要になる（14,20–22）。どちらの場合も、第三項による関係の基礎づけは成功しない。</figcaption>
</figure>'''
s4.append(fig4)
s4.append(mula("SPV 14,15–20",
  "kiñ ca. yady ekārthasambandhāt sambandha iṣyate, tadā sambandhasambandhinor apy ekārthasambandhena bhavitavyam. tathā sambandhābhyupagamāt punas tatraikārthābhisambandha ity anavasthā bhavet. tataś ca kvacin naikārthasambandhaḥ sidhyati. asambandhe sarvatra na sambandhamatis tathā. na vastvanupātinī sambandhabuddhir anavasthāyāṃ satyām.",
  "さらに、もし一つのものとの結合によって関係を認めるなら、そのときは関係と関係項の間にも、一つのものとの結合がなければならない。そうして関係を認めると、またそこにも一つのものとの結合が〔必要になる〕ので、無限遡及になるであろう。そしてそれゆえ、どこにおいても一つのものとの結合は成立しない。どこにも関係がないので、「そうであれば関係の観念もない」。無限遡及がある以上、関係の知は実在に従うものではない。",
  "<p>偈の <i>na sambandhamatis tathā</i> を Vṛtti は <i>na vastvanupātinī sambandhabuddhiḥ</i> と言い換える。関係の観念が存在しないと言うのではない。その観念が実在に即した（<i>vastvanupātin</i>）ものではない、というのである。これは第1偈 Vṛtti の「分別が作った関係は否定しない」と整合する。関係の知は現にあるが、その対象は分別の構成物である。</p>"
  "<p>遡及の論法は、関係を「関係項とは別の実在」として立てるかぎり、関係項と関係のあいだにもまた関係が要る、という構造にもとづく。対論者が遡及を止めるには、どこかで自分自身によって関係する関係（自己結合的な関係）を認めるしかない。それが次の一文で塞がれる。Steinkellner（2022, 試訳, n.3）は、同じ無限遡及の論法が Mokṣākaragupta の <i>Tarkabhāṣā</i> 7,2–6（Iyengar 版） にも見られることを指摘する。</p>",
  kind="vrtti",
  crit="<b>本文</b>　16 <i>ekārtha°</i> n.e. T。17 <i>a&lt;navasthā</i> em. : <i>a///vasthā</i> Ms。"))
s4.append(mula("SPV 14,20–23",
  "kvacid ekārthābhisambandham antareṇa sambandhakalpanāyāṃ prathamayor api sambandhinor ekārthasambandhāt sambandho mā bhūt. kevalayor api sambandhe doṣa uktaḥ. etena nairantaryāder dharmāntarakalpanāpi pratyuktā.",
  "〔遡及の〕どこかで、一つのものとの結合なしに関係を想定するなら、最初の二つの関係項についても、一つのものとの結合によって関係がある、ということはなくてよいことになる。そして、関係項二つだけの関係についても、過失はすでに述べた。これによって、間がないことなどを別の属性として想定することも退けられた。",
  "<p>遡及を止める手は、第三項なしの関係をどこかで認めることである。しかしそれを認めるなら、最初の a–b の段階でそうすればよく、第三項は不要になる。そして二項だけの関係はすでに第1–3偈で否定済みである。こうして第三項案は二つの角のどちらでも失敗する。</p>"
  "<p>最後の一文は第2偈 Vṛtti の <i>nairantarya</i> に戻る。隣接を、関係項とは別の属性（<i>dharmāntara</i>）として実体化する案も、第三項案の一種として同じく退けられる。校訂者の分析ではここまでが「一般的な否定」の第1部（1.1–1.4）で、第5偈の要約へと続く。</p>",
  kind="vrtti",
  crit="<b>本文</b>　21 <i>kalpanāyāṃ prathamayor api sambandhinor</i> rec.（T <i>rtog na ni 'brel pa can daṅ po gñis la yaṅ</i>）: <i>ka . . . . . yor api sambandhinor</i> Ms。21f <i>°sambandhāt sambandho</i> rec.（SPVt <i>'brel pa'i phyir 'brel pa</i>）: 欠損 Ms。22f <i>nairantaryāder</i> : <i>nairanta{{ranta}}ryāder</i> Ms。"))
sections.append(("s4", "4", "第三項による関係の否定", "k.4 / SPV 14,3–23", "関係＝一つのものとの結合（ekābhisambandha）、無限遡及", "".join(s4)))

# summary table of k.1–4
summ = '''<section id="sum4" class="wrap">
  <div class="sec-head"><span class="sec-no">✓</span><h2>第1–4偈のまとめ</h2><span class="sub">関係の四つの定義と、それぞれの否定</span></div>
  <div class="tbl min"><table>
  <thead><tr><th>偈</th><th>関係の定義</th><th>二者択一の軸</th><th>否定の要点</th><th>Vṛtti</th></tr></thead>
  <tbody>
  <tr><td class="num">1</td><td class="k">従属<span class="sm"><i>pāratantrya</i> = <i>parāyattatā</i></span></td><td>関係項は既成立か未成立か</td><td>未成立なら担い手がなく、既成立なら従属の余地がない</td><td class="num">11,4–12</td></tr>
  <tr><td class="num">2</td><td class="k">姿の融合<span class="sm"><i>rūpaśleṣa</i>（→ <i>nairantarya</i>）</span></td><td>関係項は二か一か</td><td>二なら融合せず、一なら関係項がない。隣接は間の非存在にすぎない</td><td class="num">12,3–14</td></tr>
  <tr><td class="num">3</td><td class="k">他者の依存<span class="sm"><i>parāpekṣā</i></span></td><td>関係項は存在するかしないか</td><td>非存在は依存せず、存在は何も期待しない</td><td class="num">13,3–8</td></tr>
  <tr><td class="num">4</td><td class="k">第三項との結合<span class="sm"><i>ekābhisambandha</i></span></td><td>第三項は関係項と別か別でないか</td><td>別でなければ二項に戻り、別なら無関係か無限遡及</td><td class="num">14,3–23</td></tr>
  </tbody></table></div>
  <div class="point"><span class="lbl">四つの論証に共通する前提</span>
  <p>(1) 実在の関係は、二項に同時に属する（<i>dviṣṭha</i>）実在でなければならない。(2) 実在は自らの本性において完結している（<i>svātmani sthita</i>、第5偈）。(3) 実在であるものは、同か異かの二者択一を免れない。偈と Vṛtti はこの三つを対論者と共有できる前提として扱い、(1) と (2) が両立しないことを示す。関係の語と観念は、分別が作るものとして残される（11,12; 14,19f）。</p></div>
</section>'''

# ------------------------------------------------------------------ agent sections
import os, importlib.util
AFTER = []
for nm in ("secA", "secB", "secC"):
    fp = D + nm + ".py"
    if os.path.exists(fp):
        spec = importlib.util.spec_from_file_location(nm, fp); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        AFTER += m.sections(mula, dev, K)
# renumber agent sections sequentially from 5
AFTER = [(f"s{i+5}", str(i+5), t, pg, sub, c) for i, (_sid, _no, t, pg, sub, c) in enumerate(AFTER)]
TERMS_EXTRA = ""
for nm in ("secA", "secB", "secC"):
    fp = D + nm + "_terms.html"
    if os.path.exists(fp): TERMS_EXTRA += open(fp).read()

# ------------------------------------------------------------------ page
MAP = [
("0", "帰敬・目的", "—", "11,2", "実在としての関係の否定"),
("1.1", "従属（pāratantrya）", "1", "11,4–12", "既成立・未成立の両刀論法", "s1"),
("1.2", "姿の融合（rūpaśleṣa）", "2", "12,3–14", "二か一か。隣接（nairantarya）は間の非存在", "s2"),
("1.3", "他者の依存（parāpekṣā）", "3", "13,3–8", "非存在は依存せず、存在は期待しない", "s3"),
("1.4", "第三項との結合（ekābhisambandha）", "4", "14,3–23", "第三項は無関係か無限遡及", "s4"),
("1.5", "要約：存在は自らに立つ。混ぜるのは分別", "5–6", "15,3–16,7", "関係の語は他者からの区別（anyāpoha）を伝えるために用いられる"),
("2.1.1–4", "因果関係（kāryakāraṇabhāva）", "7–10", "17,3–20,7", "継起するので二項に立たない。助けるもの（upakārin）は存在しないときに助けない"),
("2.1.5", "存在・非存在を限定とする結合", "11–15", "21,3–25,9", "因果の知は存在・非存在の観察の内容。「結果」の語は便宜のための約定"),
("2.1.5.3", "因果関係の成立", "16–18", "26,3–28,13", "bhāve bhāvini tadbhāvaḥ…。分別が別々のものを結合したかのように示す"),
("2.2.1", "結合（saṃyoga）・内属（samavāya）", "19–22", "29,3–32,11", "相互に助けないので関係項ではない。Sāṃkhya の関係も同様"),
("2.2.2", "適合性（yogyatā）", "23–24", "33,3–34,6", "結合によって不適合なものが適合するのは矛盾"),
("(2.2)/(1.)", "総括", "25", "35,3–13", "刹那ごとに生じる存在の本性の差異。あらゆる存在は無関係"),
]
def _sid_for(k):
    try: k0 = int(str(k).split("–")[0])
    except ValueError: return None
    for sid, no, t, pg, sub, c in AFTER:
        m = re.search(r"k\.(\d+)", pg)
        if m and int(m.group(1)) <= k0:
            last = sid
    return last if k0 >= 5 else None
map_rows = ""
for r in MAP:
    no, ttl, k, pg, cont = r[:5]
    tgt = r[5] if len(r) > 5 else _sid_for(k)
    link = f'<a href="#{tgt}">{ttl}</a>' if tgt else ttl
    here = ""
    map_rows += f'<tr{here}><td class="num">{no}</td><td class="k">{link}</td><td class="num">{k}</td><td class="num">{pg}</td><td>{cont}</td></tr>\n'

nav = '<li><a href="#intro">入口</a></li><li><a href="#map">全体の構成</a></li>' + "".join(
    f'<li><a href="#{sid}"><b>{no}</b>{ttl[:9]}</a></li>' for sid, no, ttl, *_ in sections + AFTER) + \
    '<li><a href="#terms">用語集</a></li>'

body_secs = ""
for sid, no, ttl, pg, sub, content in sections:
    body_secs += f'''
<section id="{sid}" class="wrap">
  <div class="sec-head"><span class="sec-no">{no}</span><h2>{ttl}</h2><span class="sub"><span class="pg">{pg}</span>{sub}</span></div>
{content}
</section>
'''

after_secs = ""
for sid, no, ttl, pg, sub, content in AFTER:
    after_secs += f'''
<section id="{sid}" class="wrap">
  <div class="sec-head"><span class="sec-no">{no}</span><h2>{ttl}</h2><span class="sub"><span class="pg">{pg}</span>{sub}</span></div>
{content}
</section>
'''
page = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Sambandhaparīkṣā 対訳</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@600;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400&family=Noto+Serif+Devanagari:wght@400;600&display=swap">
{STYLE}
{EXTRA}
</head>
<body>
<nav class="toc" aria-label="目次"><ol>{nav}</ol></nav>

<header class="hero wrap">
  <div class="eyebrow">DHARMAKĪRTI 小品対訳</div>
  <h1>Sambandhaparīkṣā</h1>
  <p class="deva-title" lang="sa">सम्बन्धपरीक्षा</p>
  <p class="sub">Dharmakīrti『関係の考察』と Devendrabuddhi の注（<i>Vṛtti</i>）を、原文・和訳・解説でテキスト順に読む</p>
  <span class="sample">対訳　全文（帰敬から第25偈・奥書まで）</span>
  <p>Dharmakīrti は、実在としての関係（<i>sambandha</i>）を一切認めない。二項のあいだに立つ実在の関係は、従属・融合・依存・第三項との結合のどの形で定義しても成り立たず、関係の語と観念は分別（<i>kalpanā</i>）が作るものにすぎない。<i>Sambandhaparīkṣā</i> は、この主張を25偈で論じ、とくに因果関係（第7–18偈）と、Vaiśeṣika の結合・内属（第19–22偈）を詳しく検討する小品である。</p>
  <p>このページは、Steinkellner による写本にもとづく新校訂本の本文（Dharmakīrti の偈と、弟子 Devendrabuddhi の注 <i>Sambandhaparīkṣāvṛtti</i>）を、デーヴァナーガリーと和訳で対照させ、各ブロックに解説と校訂上の注記を付ける。帰敬から第25偈と奥書までの全文を、校訂者の分析に従って節に分けて収めた。</p>
</header>

<main>
<section id="intro" class="first wrap">
  <div class="sec-head"><h2 style="grid-column:1/-1">テキストと注記の基礎</h2></div>
  <dl class="facts">
    <div><dt>著作</dt><dd><i>Sambandhaparīkṣā</i>（SP）25偈<br><small>カーリカー部奥書 <i>kṛtir ācāryadharmakīrtipādānām</i>。PV 以後の小品とされる</small></dd></div>
    <div><dt>注</dt><dd>Devendrabuddhi『<i>Sambandhaparīkṣāvṛtti</i>』（SPV）<br><small>Dharmakīrti の直弟子で、PV 第2–4章の注釈（<i>Pramāṇavārttikapañjikā</i>）の著者。写本奥書 <i>kṛtir ācāryadevendrabuddheḥ</i> による。チベット訳（SPVt）の奥書は Dharmakīrti 作とする</small></dd></div>
    <div><dt>本文</dt><dd>E. Steinkellner (ed.), <i>Dharmakīrti's Sambandhaparīkṣā and Devendrabuddhi's Sambandhaparīkṣāvṛtti</i>. China Tibetology Publishing House / Austrian Academy of Sciences Press<br><small>SP は写本 Ms（1b–2b）、SPV は Ms（2b4–9a）。欠損部は校訂者がチベット訳（SPVt）、Vinītadeva の注釈 <i>Sambandhaparīkṣāṭīkā</i>（T）、引用から復元（rec.）している</small></dd></div>
    <div><dt>頁・行</dt><dd>SP 3–7（偈）、SPV 11–35（Vṛtti）<br><small>ブロック左上の「SPV 11,4–7」は校訂本 Vṛtti の頁・行。構成表の番号は校訂者の Analysis による</small></dd></div>
    <div><dt>引用者</dt><dd>Jaina・Śaiva の論書に多数<br><small>Vidyānanda TŚV、Prabhācandra PKM・NKC、Vādideva SVR、Abhinavagupta ĪPVV、Utpaladeva <i>Sambandhasiddhi</i>（SS）など。異読注に反映</small></dd></div>
    <div><dt>範囲</dt><dd>帰敬・第1–25偈・奥書<br><small>Vṛtti は SPV 11,2–35,15 の全文</small></dd></div>
  </dl>

  <h3>このページの読み方</h3>
  <div class="howto">
    <div><b>偈</b>金色の枠。偈の下の小字は異読（校訂本の apparatus から主要なものを抜粋）</div>
    <div><b>Vṛtti</b>灰色の枠。デーヴァナーガリーは校訂本の IAST から機械的に転写し、連声は校訂本の分かち書きに従う。<span class="lac">…</span> は写本の欠損</div>
    <div><b>和訳</b>〔　〕は訳者の補い。〔反論〕〔答論〕は訳者の付けた標識</div>
    <div><b>本文注記</b>各ブロックの点線の下。em. は校訂者の訂正、rec. はチベット訳などからの復元、Ms は写本の読み</div>
    <div><b>解説</b>灰色の欄。論証の構造、前提、Dharmakīrti の他著作との関係を扱う</div>
  </div>
</section>

<section id="map" class="wrap">
  <div class="sec-head"><h2 style="grid-column:1/-1">全体の構成</h2><span class="sub">校訂者の Analysis にもとづく。主題をクリックすると該当の節へ移る</span></div>
  <p>本書は二部に分かれる。第1–6偈は関係一般の否定で、関係の定義を四つ取り上げて退け（第1–4偈）、関係は分別が作るという結論を述べる（第5–6偈）。第7–25偈は個別の関係の否定で、因果関係（第7–18偈）、Vaiśeṣika の結合・内属と適合性（第19–24偈）を扱い、第25偈で全体を総括する。</p>
  <div class="tbl min"><table>
    <thead><tr><th>分析</th><th>主題</th><th>偈</th><th>SPV</th><th>要点</th></tr></thead>
    <tbody>
{map_rows}
    </tbody>
  </table></div>
</section>
{body_secs}
{summ}
{after_secs}

<section id="terms" class="wrap">
  <div class="sec-head"><h2 style="grid-column:1/-1">用語集</h2><span class="sub">本文に出る主な術語</span></div>
  <dl class="gloss">
    <dt>sambandha / sambandhin</dt><dd>関係／関係項</dd>
    <dt>vastubhūta / bhāvataḥ</dt><dd>実在としての／実在の上で（Vṛtti は <i>vastutaḥ</i> と注す）</dd>
    <dt>pāratantrya / parāyattatā</dt><dd>他への従属／他に依存していること（第1偈）</dd>
    <dt>siddha / asiddha</dt><dd>既成立／未成立。niṣpanna / aniṣpanna（完成／未完成）とも</dd>
    <dt>rūpaśleṣa</dt><dd>姿の融合。Vṛtti は本性の一体化（svabhāvaikātmya）と解する（第2偈）</dd>
    <dt>nairantarya / sāntaratā</dt><dd>間がないこと（隣接）／間があること</dd>
    <dt>prāpti</dt><dd>到達・接触。隣接に含まれるとされる</dd>
    <dt>parāpekṣā / nirāśaṃsa</dt><dd>他者の依存（Vṛtti は <i>para</i> を依存の主体と分析）／期待をもたない（第3偈）</dd>
    <dt>ekābhisambandha</dt><dd>一つの〔第三の〕ものとの結合（第4偈）</dd>
    <dt>arthāntara / anarthāntara</dt><dd>別個のもの／別でないもの</dd>
    <dt>avācya</dt><dd>同とも異とも言い表せないもの</dd>
    <dt>saṃyoga / guṇa</dt><dd>結合／性質（Vaiśeṣika の範疇）</dd>
    <dt>anavasthā</dt><dd>無限遡及</dd>
    <dt>dviṣṭha</dt><dd>二項に立つ。関係の要件</dd>
    <dt>kalpanā / vikalpa</dt><dd>分別。関係の観念を作るもの</dd>
    <dt>kalpanāsamāropita / vikalpanirmita</dt><dd>分別によって付託された／作られた</dd>
{TERMS_EXTRA}
  </dl>
</section>

<footer class="wrap">
  <p><strong>テキストについて</strong>　原文は、E. Steinkellner 校訂 <i>Dharmakīrti's Sambandhaparīkṣā and Devendrabuddhi's Sambandhaparīkṣāvṛtti</i>（China Tibetology Research Center / Austrian Academy of Sciences）の OCR テキストに拠る。OCR は複数回分を照合し、明らかな誤認識（ș/ṣ、ņ/ṇ など）を正した。デーヴァナーガリーは校訂本の IAST から機械的に転写したもので、子音で終わる語と次の語を連結し、句読点を ।・॥ に置き換えた。頁・行番号と分析番号は校訂本による。</p>
  <p>本文注記の略号は校訂本のもの（Ms＝写本、SPVt＝Vṛtti のチベット訳、T＝Vinītadeva の <i>Sambandhaparīkṣāṭīkā</i>（チベット訳のみ現存、P 5735。Steinkellner 2022 試訳の Ṭ）、F＝Frauwallner による再構成、TŚV, PKM, NKC, SVR, AS, TR, VR, ĪPVV, NBhūṣ, SS＝引用・並行文献）。和訳は試訳であり、解説の PVSV への言及は Gnoli 版の頁・行による。和訳と解説は E. Steinkellner, <i>Dharmakīrti's Investigation of Relation (Sambandhaparīkṣā) with Devendrabuddhi's Commentary (Sambandhaparīkṣāvṛtti). A trial translation</i>（2022；本文中「Steinkellner（2022, 試訳）」）と照合した。同書序文に挙げられた校訂本の訂正と Eltschinger の提案は本文注記に反映し、解釈が異なる箇所は解説に記した。</p>
</footer>
</main>
</body>
</html>'''
open(D + "../sambandhapariksa_taiyaku.html", "w").write(page)
print("ok", len(page))
