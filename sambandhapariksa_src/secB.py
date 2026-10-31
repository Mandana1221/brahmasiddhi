# -*- coding: utf-8 -*-
# k.11–18 with Devendrabuddhi's Vṛtti (SPV 21–28); analysis 2.1.5
KB = {
11: "dviṣṭho hi kaścit sambandho nāto 'nyat tasya lakṣaṇam / bhāvābhāvopadhir yogaḥ kāryakāraṇatā yadi // 11",
12: "yogopādhī na tāv eva kāryakāraṇatātra kim / bhedāc cen nanv ayaṃ śabdo niyoktāraṃ samāśritaḥ // 12",
13: "paśyann ekam adṛṣṭasya darśane tadadarśane / apaśyan kāryam anveti vināpy ākhyātṛbhir janaḥ // 13",
14: "darśanādarśane muktvā kāryabuddher asambhavāt / kāryādiśrutir apy atra lāghavārthaṃ niveśitā // 14",
15: "tadbhāvabhāvāt tatkāryagatir yāpy anuvarṇyate / saṅketaviṣayākhyā sā sāsnāder gogatir yathā // 15",
16: "bhāve bhāvini tadbhāvo bhāva eva ca bhāvitā / prasiddhe hetuphalate pratyakṣānupalambhataḥ // 16",
17: "etāvanmātratattvārthāḥ kāryakāraṇagocarāḥ / vikalpā darśayanty arthān mithyārthā ghaṭitān iva // 17",
18: "bhinne kā ghaṭanā 'bhinne kāryakāraṇatāpi kā / bhāve hy anyasya viśliṣṭau śliṣṭau syātāṃ kathaṃ ca tau // 18",
}


def sections(mula, dev, K):
    out = []

    # ---------------- §10 k.11–12
    s = []
    s.append(mula("SP 5 / k.11", KB[11],
      "関係とは、なにか二つのものに立つもの（<i>dviṣṭha</i>）である。これ以外に、その特徴はない。〔反論〕もし因果関係（<i>kāryakāraṇatā</i>）が、存在・非存在を限定とする結合（<i>bhāvābhāvopadhir yogaḥ</i>）であるとするなら、",
      "", kind="sutra",
      crit="<b>異読</b>　apparatus に異読の記載はない。第11偈全体は TŚV 149,18f+33; PKM 510,7f; SVR 815,5+11 に引用（Ci）。11c の <i>upadhi</i> は Vṛtti では <i>upādhi</i> の形で注される。"))
    s.append(mula("SPV 21,3–7",
      "na yena kenacid ekena sambandhāt sambandhaḥ, kin tarhi sambandhalakṣaṇenaikeneti cet, tan na. dviṣṭho hi kaścit padārthaḥ sambandhaḥ. nāto 'rthadvayābhisambandhino 'rthād anyat tasya sambandhasya lakṣaṇam upapadyate, yena saṅkhyādes tasya viśeṣo vyavasthāpyeta.",
      "〔反論〕「どんな一つのものとの結合によってでも関係がある、というのではない。そうではなく、関係を特徴とする一つのもの〔との結合〕によってである」と言うなら、〔答論〕そうではない。関係とは、なにか二つのものに立つ事物（<i>padārtha</i>）である。これ、すなわち二つの対象と結合している対象であること以外に、その関係の特徴は成り立たない。〔もし成り立つなら〕それによって、数（<i>saṅkhyā</i>）などからのその〔関係の〕区別が確立されるであろうが、〔そうした特徴はない〕。",
      "<p>反論は第10偈を受ける。第10偈 Vṛtti では、一つのものとの結合によって関係を立てると、共通の属性をもつあらゆるものが関係していることになる、と退けられた（校訂者の分析 2.1.4）。反論者はそこで、結合の相手となる「一つのもの」を、関係を特徴とするもの（<i>sambandhalakṣaṇa</i>）に限定する。</p>"
      "<p>答論は、関係の特徴として挙げうるのは「二つに立つ」ことだけだ、と指摘する。しかし二つに立つものは関係に限らない。数（<i>saṅkhyā</i>）、たとえば Vaiśeṣika の性質としての二性も二つの実体に属する。したがって「関係を特徴とする一つのもの」は、数などから区別できる固有の特徴をもたず、限定として働かない。校訂者の分析ではここから 2.1.5（存在・非存在を限定とする結合の否定、第11–17偈）が始まる。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>ekena</i> n.e. T。5 <i>'rthadvayābhi°</i> rec.（SPVt <i>don gñis daṅ mṅon par</i>, PKM）: <i>. . . . yābhi°</i> Ms。<i>arthād</i> n.e. T。6 <i>upapadyate</i> em.（T <i>'thad na</i>）: <i>upalabhyate</i> Ms。21,3–10 は PKM 507,11–14 に並行（cf.）。4f <i>dviṣṭho … lakṣaṇam</i> は SVR 815,6–7 に並行（cf.）。"))
    s.append(mula("SPV 21,8–10",
      "kasyacid bhāve bhāvo 'bhāve 'bhāvaḥ, tayor bhavator abhavatoś ca yau bhāvau 'bhāvau tāv upādhir viśeṣaṇaṃ yasya yogasya sambandhasyāsau bhāvābhāvopādhir yogaḥ kāryakāraṇatā yadi, na sarvaḥ sambandhaḥ,",
      "〔反論〕あるもの〔A〕があるとき〔B が〕あり、ないときにはない。それら二つが存在し、また存在しないときの二つの存在と二つの非存在、それらが限定（<i>upādhi</i>）すなわち限定要素（<i>viśeṣaṇa</i>）となっている結合すなわち関係、それが「存在・非存在を限定とする結合」である。もし〔そのような結合が〕因果関係であって、あらゆる関係が〔そうなのでは〕ない、とするなら、——",
      "<p>偈の後半は対論者の新しい提案である。関係一般ではなく因果関係に限って、それを存在・非存在によって限定された実在の結合（<i>yoga</i>）として立てる。A があるとき B があり、A がないとき B がない、という二組の存在・非存在が限定要素となり、この結合を数などから区別する。前段の「関係に固有の特徴がない」という批判に答える形になっている。</p>"
      "<p>文は次頁の <i>tadā</i>（第12偈 Vṛtti）に続く。「もし…なら、そのとき…」の構文で、偈の <i>yadi</i>（11d）と、Vṛtti が第12偈の冒頭に補う <i>tadā</i> が対応する。</p>",
      kind="vrtti",
      crit="<b>本文</b>　8f <i>yau bhāvau &lt;'bhāvau&gt; tāv</i> em.（SPVt <i>yod pa daṅ med pa gaṅ yin pa de'i</i>）: <i>yau bhāvau tāv</i> Ms。9 <i>upādhir</i> em. : <i>upādhi°</i> Ms。10 <i>sambandhaḥ</i> n.e. T。"))
    s.append(mula("SP 5 / k.12", KB[12],
      "〔答論〕結合の限定であるそれら二つ〔存在と非存在〕こそが、ここで因果関係なのではないか。〔反論〕〔両者は〕別々であるから〔一つの語では表せない〕と言うなら、〔答論〕この語は、適用する者（<i>niyoktṛ</i>）に依拠しているではないか。",
      "", kind="sutra",
      crit="<b>異読</b>　12c <i>nanv</i> : <i>na tv</i> TŚV。第12偈は TŚV 149,19f; PKM 510,9f; SVR 815,12f に引用（Ci）。"))
    s.append(mula("SPV 22,3–4",
      "tadā yau tau yogopādhī bhāvābhāvau tāv eva kāryakāraṇatātra na kim, yenāsato 'phalasya sambandhasya kalpanā.",
      "そのとき、結合の限定である存在と非存在、その二つこそが、ここで因果関係なのではないのか。〔そうでないとする〕ために、存在せず効果もない関係が想定されることになるのである。",
      "<p>反駁は簡潔である。結合を限定し区別する存在・非存在が与えられているなら、因果関係としてはそれで足りる。その上に結合という別の実在を立てても、それは存在せず（<i>asat</i>）、何の働きもない（<i>aphala</i>）。存在・非存在だけで因果の知と言語活動が説明できるなら、結合を想定する理由がない、という節約の論法である。</p>"
      "<p><i>yena</i> 以下は、存在・非存在を因果関係と認めないことの帰結として訳した。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>tadā</i> em.（PKM, T <i>de'i tshe</i>）: <i>yadā</i> Ms。22,3–9 は PKM 507,17–22 に並行（cf.）。"))
    s.append(mula("SPV 22,4–9",
      "bhedāc cet, syād etat – bhāve bhāvo 'bhāve 'bhāva iti bahavo 'bhidheyāḥ, kāryakāraṇateti caikārthābhidhāyinā śabdena vācyās tadviṣayā ayuktā iti bhāvābhāvau na kāryakāraṇateṣyate. nanv ayaṃ śabdo niyoktāraṃ puruṣaṃ samāśrita iti niyoktṛsamāśrayād yaṃ śabdam asau yathā prayuṅkte sa tathā prāhety anekatrāpy ekā śrutir ity aparihāra eva.",
      "「別々であるから」と言うなら、〔つまり〕こう言うかもしれない。「『あるときにあり、ないときにはない』というように、表示されるべきものは多数である。それらが、一つの対象を表示する『因果関係』という語によって、その〔語の〕対象として表示されるのは不適切である。それゆえ、存在・非存在は因果関係とは認められない」と。〔答論〕しかし、この語は適用する人（<i>niyoktṛ puruṣa</i>）に依拠している。適用する者に依拠しているので、その人がある語をどのように用いても、その〔語〕はそのとおりに言う。だから、多数のものについても一つの語がありうる。それゆえ〔その反論は〕まったく答えになっていない。",
      "<p>対論者の再反論は言語の側から来る。存在・非存在は少なくとも四つ（A の存在・非存在、B の存在・非存在）に分かれ、多数である。「因果関係」という単数の語には、それに対応する一つの対象がなければならない。だから語の対象は、存在・非存在とは別の一つのもの、つまり結合である、というのである。</p>"
      "<p>答論は、語と対象の結びつきは語を適用する人に依る、と答える。語が一つであることは、対象が一つであることを保証しない。多数のものに一つの語を当てることは、使用者がそう用いれば成り立つ。語が実在の構造を写すのではなく、使用者の約定によって対象に当てられるという考え方は、第14–15偈で、「結果」などの語は簡便のための約定（<i>saṅketa</i>）である、という形で展開される。</p>",
      kind="vrtti",
      crit="<b>本文</b>　apparatus にこの部分の訂正の記載はない。9 <i>aparihāra</i> の途中で Ms は 6a に移る。"))
    tbl = '''<div class="tbl min"><table>
<thead><tr><th>SPV</th><th>対論者の提案</th><th>答論</th></tr></thead>
<tbody>
<tr><td class="num">21,3–7</td><td class="k">関係を特徴とする一つのものとの結合<span class="sm"><i>sambandhalakṣaṇenaikena</i></span></td><td>関係の特徴は「二つに立つ」ことだけで、数などから区別できない</td></tr>
<tr><td class="num">21,8–10</td><td class="k">存在・非存在を限定とする結合<span class="sm"><i>bhāvābhāvopādhir yogaḥ</i></span></td><td>限定である存在・非存在そのものが因果関係である。結合は存在せず効果もない（22,3–4）</td></tr>
<tr><td class="num">22,4–7</td><td class="k">存在・非存在は多数で、一語「因果関係」の対象にならない<span class="sm"><i>bhedāt</i></span></td><td>語は適用者に依拠する。多数のものに一語を当てることはできる（22,7–9）</td></tr>
</tbody></table></div>'''
    s.append(tbl)
    out.append(("s10", "10", "存在・非存在を限定とする結合", "k.11–12 / SPV 21,3–22,9",
                "因果関係＝bhāvābhāvopādhir yogaḥ の否定。語は適用者に依る", "".join(s)))

    # ---------------- §11 k.13
    s = []
    s.append(mula("SP 5 / k.13", KB[13],
      "一方を見ていて、〔それまで〕見えなかったものが見えるとき、そして、その〔一方〕が見えないとき〔もう一方を〕見ないとき、人は、説明する者がいなくても、結果を理解する。",
      "", kind="sutra",
      crit="<b>異読</b>　13d <i>vināpy ākhyātṛbhir</i> : <i>vinā vyākhyātṛbhir</i> PKM。第13偈は TŚV 149,20f; PKM 510,11f; SVR 816,1f に、第13–14偈は ĪPVV 1.199,18–21 に引用（Ci）。"))
    s.append(mula("SPV 23,3–7",
      "tasmāt tāv eva bhāvābhāvau kāryakāraṇatā yuktā. yasmāt paśyann ekaṃ kāraṇābhimatam upalabdhilakṣaṇaprāptasyādṛṣṭasya kāryākhyasya darśane sati yat paśyan dṛṣṭavāṃs tadadarśane saty apaśyan kāryābhimataṃ kāryam anvetīdam ato bhavatīti pratipadyate vināpy ākhyātṛbhir janaḥ, ata idaṃ bhavatīty ākhyātāram antareṇa janaḥ.",
      "それゆえ、その存在と非存在こそが因果関係であるのが正しい。なぜなら、原因と見なされる一方を見ていて、知覚の条件を満たしていながら（<i>upalabdhilakṣaṇaprāpta</i>）〔それまで〕見えなかった、結果と呼ばれるものが見えるとき、また、見ていて〔すでに〕見たもの〔原因〕が見えないとき〔結果と見なされるものを〕見ないとき、人は、結果と見なされる「結果を理解する」、すなわち「これはあれから生じる」と知るからである。「説明する者がいなくても」、すなわち「これはあれから生じる」と説明する人なしに、人は〔そう知る〕。",
      "<p>偈は、因果関係がどのようにして知られるかを述べ、その知の内容が存在・非存在の観察以外のものではないことを示す。手順は三つに分かれる。(1) 原因と見なされる A を見る。そのとき、知覚可能でありながらまだ見えていなかった B が見えるようになる。(2) A が見えなくなると、B も見えない。(3) そこから「B は A から生じる」と知る。<i>upalabdhilakṣaṇaprāpta</i> の限定は、B が見えないことが単なる見落としではなく、B の非存在を示すための条件である。</p>"
      "<p>「説明する者がいなくても」は、因果の知が他人の教示や約定に由来するものではなく、観察から直接に生じることを言う。つまり、因果の知の内容は観察された存在・非存在そのものである。これが次の段（23,8–12）の論点になる。<i>yasmāt … pratipadyate</i> について、apparatus は PVSV 22,2–3 を挙げている。</p>",
      kind="vrtti",
      crit="<b>本文</b>　5 <i>apaśyan</i> : <i>apasyan</i> Ms。<i>tadadarśane</i> : <i>tadaśarśane</i> Ms。3–6 <i>yasmāt … pratipadyate</i> について PVSV 22,2–3（apparatus の符号は OCR では Ce'e）。3–7 は PKM 507,23–508,2; SVR 816,3–6 に並行（cf.）。"))
    fig = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 250" style="min-width:560px;width:100%" role="img" aria-label="第13偈の因果の知。原因Aを見ていて結果Bが見えるようになり、Aが見えないときBも見えない。そこからBはAから生じると知る">
    <defs><marker id="mB10" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <text x="70" y="70" text-anchor="middle" font-size="13" font-weight="700" class="s-ink">原因 A</text>
    <text x="70" y="130" text-anchor="middle" font-size="13" font-weight="700" class="s-ink">結果 B</text>
    <text x="210" y="30" text-anchor="middle" font-size="12" class="s-muted">(1) 以前</text>
    <text x="370" y="30" text-anchor="middle" font-size="12" class="s-muted">(1) A を見ているとき</text>
    <text x="530" y="30" text-anchor="middle" font-size="12" class="s-muted">(2) A が見えないとき</text>
    <rect x="150" y="48" width="120" height="36" rx="9" class="s-card st-line" stroke-width="1"/>
    <text x="210" y="71" text-anchor="middle" font-size="12" class="s-muted">—</text>
    <rect x="310" y="48" width="120" height="36" rx="9" class="s-accsoft"/>
    <text x="370" y="71" text-anchor="middle" font-size="12.5" font-weight="700" class="s-acc">見える</text>
    <rect x="470" y="48" width="120" height="36" rx="9" class="s-card st-line" stroke-width="1"/>
    <text x="530" y="71" text-anchor="middle" font-size="12.5" class="s-muted">見えない</text>
    <rect x="150" y="108" width="120" height="36" rx="9" class="s-card st-line" stroke-width="1"/>
    <text x="210" y="124" text-anchor="middle" font-size="12" class="s-muted">見えない</text>
    <text x="210" y="139" text-anchor="middle" font-size="10.5" class="s-muted">（知覚可能なのに）</text>
    <rect x="310" y="108" width="120" height="36" rx="9" class="s-accsoft"/>
    <text x="370" y="131" text-anchor="middle" font-size="12.5" font-weight="700" class="s-acc">見える</text>
    <rect x="470" y="108" width="120" height="36" rx="9" class="s-card st-line" stroke-width="1"/>
    <text x="530" y="131" text-anchor="middle" font-size="12.5" class="s-muted">見えない</text>
    <path d="M370 150 V176" class="st-muted" stroke-width="1.5" marker-end="url(#mB10)"/>
    <path d="M530 150 L420 178" class="st-muted" stroke-width="1.5" marker-end="url(#mB10)"/>
    <rect x="200" y="180" width="340" height="56" rx="10" class="s-anssoft"/>
    <text x="370" y="203" text-anchor="middle" font-size="13" font-weight="700" class="s-ans">「これはあれから生じる」</text>
    <text x="370" y="223" text-anchor="middle" font-size="11.5" class="s-ink">説明する者なしに知られる。内容は存在・非存在だけ</text>
  </svg>
  </div>
  <figcaption><b>図10　第13偈の因果の知。</b>Vṛtti 23,3–7。知覚と非知覚（<i>pratyakṣānupalambha</i>、第16偈）による因果の確立の手順。知の内容は観察された存在・非存在以外のものではない（23,8–12）。</figcaption>
</figure>'''
    s.append(fig)
    s.append(mula("SPV 23,8–12",
      "saṅketād anvetīty api vārttaḥ. tathā hi na bhāvābhāvābhyām anyat saṅkete 'pi pratipadyate. tasmād yatpratipattau yatpratipattiḥ, sa tasyārthaḥ. tad yathā śuklapaṭapratipattau śuklapratipatteḥ śauklyam. bhāvābhāvau ca pratipadyamānaḥ kāryakāraṇatāṃ pratipadyata iti bhāvābhāvau kāryakāraṇatāpratipatter arthaḥ, nānyaḥ.",
      "〔反論〕「約定（<i>saṅketa</i>）によって理解する」〔と言う〕のも、取るに足りない。なぜなら、約定においても、存在・非存在と別のものは理解されないからである。それゆえ、あるものが理解されるときにある理解が生じるなら、そのものがその〔理解〕の対象（<i>artha</i>）である。たとえば、白い布が理解されるとき、「白い」という理解の〔対象〕は白さである。そして、存在・非存在を理解している人が因果関係を理解しているのだから、存在・非存在が因果関係の理解の対象であり、ほかのものではない。",
      "<p>想定される反論は、因果関係の知は観察ではなく、「これが原因、これが結果」という約定を教わることから得られる、というものである。そうであれば、知の対象は観察された存在・非存在とは別のものでありうる。答論は、約定の場面でも理解されるのは存在・非存在だけだ、と応じる。約定は、存在・非存在の観察に言葉を当てるだけで、新しい対象を加えない。</p>"
      "<p>ここで用いられる基準は、「X が理解されるときに Y の理解が生じるなら、X が Y の対象である」というものである。白い布の例では、布を見て「白い」と理解するとき、その理解の対象は布の白さである。同じように、存在・非存在を理解していることがそのまま因果関係を理解していることなのだから、因果関係の理解の対象は存在・非存在である。校訂者の分析 2.1.5.2.1。</p>",
      kind="vrtti"))
    s.append(mula("SPV 23,13–16",
      "syād etat – bhāvābhāvau sādhanam anyā kāryakāraṇatā sādhyā. anyā cet, kin na tasyā rūpaṃ nirdiśyate. utpādyotpādakabhāvas tarhi rūpam. tat kiṃ nāmāntarād arthabhedo yenaivam ucyate. tathā hy utpādyotpādakabhāvo janyajanakabhāvaḥ kāryakāraṇabhāva ity evamādayaḥ paryāyāḥ.",
      "こう言うかもしれない。「存在・非存在は論証するもの（<i>sādhana</i>）であり、〔それとは〕別の因果関係が論証されるもの（<i>sādhya</i>）である」と。〔答論〕別であるなら、どうしてその姿が示されないのか。〔反論〕では、生じられるもの・生じさせるものの関係（<i>utpādyotpādakabhāva</i>）がその姿である。〔答論〕では、名前が違うことから対象が違うのか。そのために、そのように言われるのか。というのも、「生じられるもの・生じさせるものの関係」「生み出されるもの・生み出すものの関係」「結果・原因の関係」などは同義語だからである。",
      "<p>反論は、存在・非存在を論証因とし、因果関係をその論証対象とする。そうであれば、両者は別でなければならない。答論は、別であるならその固有の姿を示せ、と求める。反論者が挙げる「生じられるもの・生じさせるものの関係」は、「因果関係」の言い換えにすぎない。名前が違っても対象が違うことにはならない。こうして、存在・非存在とは別の論証対象としての因果関係は、内容を示されないまま退けられる。校訂者の分析 2.1.5.2.2（後者は前者によって推論されるのではない）。</p>",
      kind="vrtti"))
    out.append(("s11", "11", "因果の知の内容", "k.13 / SPV 23,3–16",
                "知覚・非知覚による因果の理解。その対象は存在・非存在", "".join(s)))

    # ---------------- §12 k.14–15
    s = []
    s.append(mula("SP 5 / k.14", KB[14],
      "見えること・見えないことを離れては、結果の知はありえないので、「結果」などの語も、ここでは簡便のために〔存在・非存在に〕あてがわれたのである。",
      "", kind="sutra",
      crit="<b>異読</b>　14b <i>asambhavāt</i> : <i>na sambhavāt</i> ĪPVV。第14偈は TŚV 149,21; PKM 510,13f; SVR 816,7f に引用（Ci）。校訂者は PV 4.268（= PVin 3.43）を参照させる（cf.）。"))
    s.append(mula("SPV 24,3–6",
      "tasmād darśanādarśane viṣayiṇā viṣayapradarśanād bhāvābhāvau muktvā kāryabuddher asambhavāt kāraṇāt kāryādiśrutir apy atra bhāvābhāvayor mā lokaḥ pratipadam iyantīṃ śabdamālām abhidhād iti vyavahāralāghavārthaṃ niveśiteti.",
      "それゆえ、「見えること・見えないこと」、すなわち——対象をもつもの〔である知〕によって対象を示しているので——存在・非存在を離れては、結果の知はありえない、という理由で、「結果」などの語も、ここでは存在・非存在に対して、「人々が一歩ごとにこれほど長い語の連なりを口にすることのないように」と、言語活動を簡便にするためにあてがわれたのである。",
      "<p>偈の「見えること・見えないこと」（<i>darśanādarśane</i>）を、Vṛtti は存在・非存在と読む。知（<i>viṣayin</i>）を表す語で、その対象（<i>viṣaya</i>）を示しているからである。因果の知の内容は存在・非存在しかないので、「結果」「原因」という語も存在・非存在の言い換えにすぎない。それが用いられるのは、「A があるとき B があり、A がないとき B がない」という長い言い方を毎回しないための便宜である。</p>"
      "<p>第12偈の「語は適用者に依拠する」がここで具体化される。多数の存在・非存在に一つの語を当てることは、対象の側に一つのものがあることを示すのではなく、言語活動（<i>vyavahāra</i>）の簡便さ（<i>lāghava</i>）のための約定である。</p>",
      kind="vrtti",
      crit="<b>本文</b>　5 <i>lokaḥ</i>（PKM, SVR）: <i>loka°</i> Ms。<i>iya&lt;n&gt;tīṃ</i> em.（SVR）: <i>iyatīṃ</i> Ms。<i>abhidhād</i> Ms : <i>abhidadhyād</i> PKM, SVR（Ms は <i>mā</i> にアオリストを続ける形、引用者は願望法）。全体は PKM 508,2–5; SVR 816,9–11 に並行（cf.）。"))
    s.append(mula("SP 5 / k.15", KB[15],
      "「それがあるときにあることから、それの結果であると理解される」と説かれるのも、それは約定の対象の言明である。ちょうど喉の垂れ肉（<i>sāsnā</i>）などから牛を理解するように。",
      "", kind="sutra",
      crit="<b>異読</b>　15b <i>yāpy anuvarṇyate</i> : <i>yasya tu vartate</i> TŚV。第15偈は TŚV 149,22; PKM 510,15f; SVR 816,15f に引用（Ci）。"))
    s.append(mula("SPV 25,3–4",
      "nānyā 'nvayavyatirekābhyāṃ kāryakāraṇatā. nānyā cet, kathaṃ bhāvābhāvābhyāṃ sā prasādhyate.",
      "因果関係は、肯定的随伴と否定的随伴（<i>anvayavyatireka</i>）と別のものではない。〔反論〕別でないなら、どうしてそれ（因果関係）が存在・非存在によって論証されるのか。",
      "<p>第13偈 Vṛtti の結論（因果関係は存在・非存在以外のものではない）を受けて、反論者は論証の形式を盾にとる。論証されるものは論証するものと別でなければならない。もし因果関係が存在・非存在と同じなら、存在・非存在によって因果関係を論証する、という言い方自体が成り立たない。第15偈はこれに答える。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>nānyā 'nvaya°</i> Ms : <i>anvaya°</i>（PKM, SPVt, T）。4 <i>bhāvā&lt;bhāvā&gt;bhyāṃ</i> em.（PKM）: <i>bhāvābhyāṃ</i> Ms。25,3–9 は PKM 508,6–10 に並行（cf.）。"))
    s.append(mula("SPV 25,4–9",
      "tadbhāve bhāvāl liṅgāt tatkāryagatiḥ, yasya bhāve bhāvas tasya kāryasya gatiḥ, yāpy anuvarṇyate asyedaṃ kāryaṃ kāraṇañ ceti, saṅketaviṣayākhyā sā. yad etad anuvarṇanaṃ tadbhāvabhāvitvena kāryakāraṇasaṅketaviṣayākhyānam etad, nārthabhedaḥ. kim iva. sāsnāder gogatir yathā. yathā gaur ayaṃ sāsnādimattvād ity anena govyavahārasya viṣayaḥ pradarśyate.",
      "〔答論〕「それがあるときにあること」という証因（<i>liṅga</i>）から「それの結果であると理解される」、すなわち、あるものがあるときにある〔もの〕について、それの結果であると理解されることが、「これはこれの結果であり、〔これは〕原因である」と「説かれるのも、それは約定の対象の言明である」。この説明は、それがあるときにあるということによって、結果・原因という約定の対象を言明するものであり、対象の違いではない。何のように。「喉の垂れ肉などから牛を理解するように」。「これは牛である、喉の垂れ肉などをもつから」ということによって、「牛」という言語活動の対象が示されるように。",
      "<p>答えは、存在・非存在からの因果の「論証」は、新しい対象を知らせるのではなく、すでに観察された事態に「結果」「原因」という語を当てる約定の対象を示すだけだ、というものである。論証するものと論証されるものの違いは、対象の違い（<i>arthabheda</i>）ではない。</p>"
      "<p>牛の例がこれを示す。喉の垂れ肉などをもつものを見ている人に「これは牛である、喉の垂れ肉などをもつから」と言うとき、知らされるのは新しい事物ではない。目の前のものが「牛」という語の適用対象であること、つまり言語活動（<i>vyavahāra</i>）の対象であることである。同じく「これはこれの結果である、これがあるときにあるから」も、存在・非存在の事実が「結果・原因」の語の適用対象であることを示すにすぎない。校訂者の分析 2.1.5.2.3。</p>",
      kind="vrtti",
      crit="<b>本文</b>　6 <i>yad</i> em.（T <i>gaṅ yaṅ</i>）: <i>tad</i> Ms。4–9 は SVR 816,17–19 に並行（cf.）。"))
    tbl = '''<div class="tbl min"><table>
<thead><tr><th></th><th>牛の例（<i>sāsnāder gogatiḥ</i>）</th><th>因果の例（<i>tatkāryagatiḥ</i>）</th></tr></thead>
<tbody>
<tr><td class="k">証因</td><td>喉の垂れ肉などをもつこと（<i>sāsnādimattva</i>）</td><td>それがあるときにあること（<i>tadbhāvabhāvitva</i>）</td></tr>
<tr><td class="k">言明</td><td>「これは牛である」</td><td>「これはこれの結果であり、これは原因である」</td></tr>
<tr><td class="k">示されるもの</td><td>「牛」という言語活動の対象</td><td>「結果・原因」という約定の対象</td></tr>
<tr><td class="k">新しい対象</td><td><span class="pill j">なし</span></td><td><span class="pill j">なし</span>（<i>nārthabhedaḥ</i>）</td></tr>
</tbody></table></div>'''
    s.append(tbl)
    out.append(("s12", "12", "「結果」の語と約定", "k.14–15 / SPV 24,3–6; 25,3–9",
                "因果の語は簡便のための約定。論証は約定の対象を示すだけ", "".join(s)))

    # ---------------- §13 k.16
    s = []
    s.append(mula("SP 6 / k.16", KB[16],
      "生じるもの（<i>bhāvin</i>）があるとき、それ〔原因〕があること、そして、〔原因があるとき〕存在することこそが、生じるものであること（<i>bhāvitā</i>）である。〔このような〕原因であること・結果であることは、知覚と非知覚（<i>pratyakṣānupalambha</i>）によって確立される。",
      "", kind="sutra",
      crit="<b>異読</b>　apparatus に異読の記載はない。第16偈は TŚV 149,22f; PKM 510,17f; SVR 816,20f に引用（Ci）。16ab について校訂者は ĪPK I 2.9ab を参照させる（cf.）。"))
    s.append(mula("SPV 26,3–6",
      "syād etat – bhāvābhāvayoḥ kāryakāraṇatve kāraṇatvaṃ kevalaṃ kāryatvañ cobhayagatabhāvābhāvāpekṣam. anyathā kathaṃ bhāvamātraṃ kāraṇaṃ kāryaṃ vā. na ca bhavator abhavatoś ca bhāvābhāvāv ubhayagatau kāryatvaṃ kāraṇatvaṃ vā. kāryakāraṇatā tu syād iti.",
      "こう言うかもしれない。「存在・非存在が因果関係であるなら、原因であることだけ、また結果であることも、両者にある存在・非存在に依拠する。そうでなければ、単なる存在がどうして原因あるいは結果であろうか。しかし、存在し、また存在しない二つのものの、両者にある存在・非存在は、結果であることでも原因であることでもない。〔せいぜい〕因果関係ではありえよう」と。",
      "<p>反論は、存在・非存在説が原因性（<i>kāraṇatva</i>）と結果性（<i>kāryatva</i>）を個別に説明できない、と突く。単なる存在（<i>bhāvamātra</i>）はそれだけでは原因でも結果でもないので、原因性・結果性は両項にわたる存在・非存在に依拠するはずである。しかし両項にわたる存在・非存在は、両者を合わせた因果関係（<i>kāryakāraṇatā</i>）ではありえても、一方だけの原因性や結果性にはならない。したがって、個々の項の原因性・結果性のためには、存在・非存在とは別のものが要る、というのである。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>°kāraṇatve</i> : <i>°karaṇatve</i> Ms。5 <i>bhāvābhāvāv</i> em.（T <i>yod pa daṅ med pa</i>）: <i>bhāvāv</i> Ms。"))
    s.append(mula("SPV 26,7–9",
      "tan na. ubhayagatatve 'py uttarabhāvābhāvaviśeṣaṇau pūrvasya bhāvābhāvau kāraṇatvam. pūrvasya bhāvābhāvaviśeṣaṇāv uttarasya bhāvābhāvau kāryatvam.",
      "〔答論〕そうではない。両者にあるとしても、後のものの存在・非存在によって限定された、前のものの存在・非存在が原因であることである。前のものの存在・非存在によって限定された、後のものの存在・非存在が結果であることである。",
      "<p>答論は、存在・非存在が両項にわたることを認めたうえで、どちらを主とし、どちらを限定とするかによって原因性と結果性が分かれる、と言う。前のもの（原因）の存在・非存在を、後のもの（結果）の存在・非存在で限定すれば原因性になる。後のものの存在・非存在を、前のものの存在・非存在で限定すれば結果性になる。存在・非存在のほかに何も加える必要はない。</p>",
      kind="vrtti"))
    s.append(mula("SPV 26,9–13",
      "tathā hi bhāve bhāvini bhavanadharmiṇi bhāve tadbhāvaḥ kāraṇābhimatasya bhāvaḥ. bhāva evetīhāpy avadhāraṇam. anena vyatireka ākṣiptaḥ. kāraṇābhimatasya bhāva eva ca bhāvitā kāryābhimatasya kāryatvam iti prasiddhe pratyakṣānupalambhato hetuphalate. yata evaṃ bhāvābhāvāv eva kāryakāraṇatā, nānyā.",
      "すなわち、「生じるものがあるとき」、つまり生起を属性とする（<i>bhavanadharmin</i>）存在があるとき、「それがあること」、すなわち原因と見なされるものがあること〔が原因であることである〕。ここでも「あることのみ」という限定（<i>avadhāraṇa</i>）がある。これによって否定的随伴（<i>vyatireka</i>）が含意される。「そして」原因と見なされるもの〔があるとき〕に「存在することこそが、生じるものであること」、すなわち結果と見なされるものの結果であることである。このように、原因であること・結果であることは「知覚と非知覚によって確立される」。このように、存在・非存在こそが因果関係であって、ほかのものではない。",
      "<p>偈の前半は、前段の二つの定義を言い換えたものと読める。(a) 原因性：生じるもの（結果）があるとき、原因があること。(b) 結果性（<i>bhāvitā</i>）：原因があるとき、〔結果が〕存在すること。Vṛtti は (b) の <i>eva</i> を (a) にも及ぼす（<i>ihāpi</i>）。結果があるとき原因が必ずあるなら、原因がないとき結果はない。これが否定的随伴を含意する、という意味に訳した。</p>"
      "<p>(b) の <i>kāraṇābhimatasya</i> は属格だが、<i>bhāve</i> を補って「原因と見なされるものがあるときに」と解した。原因・結果が「見なされるもの」（<i>abhimata</i>）と言われるのは、それが実在の性質ではなく、存在・非存在の観察に当てられた名前だからである（第14–15偈）。偈の後半は、この二つの事態が知覚と非知覚によって確立されることを言い、第13偈の手順を受ける。校訂者の分析 2.1.5.3（因果関係の成立）。</p>",
      kind="vrtti",
      crit="<b>本文</b>　10 <i>&lt;bhāvaḥ.&gt; bhāva evetīhāpy</i> em.（SPVt <i>yod pa'o // yod pa ñid do źes 'dir yaṅ</i>; T 17b4）: <i>bhāva eva itīhāpy°</i> Ms（最初の <i>bhāvaḥ.</i> は校訂者の補い）。13 <i>yata evaṃ</i> Ms : T <i>de ltar na</i>（PKM <i>tato</i>）。<i>eva</i>（PKM）: <i>eda</i> Ms。9–13 は PKM 508,10–14 に並行（cf.）。"))
    fig = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 260" style="min-width:560px;width:100%" role="img" aria-label="第16偈の原因性と結果性。前のものの存在非存在を後のもので限定すれば原因性、後のものの存在非存在を前のもので限定すれば結果性">
    <defs><marker id="mB11" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <rect x="40" y="20" width="250" height="56" rx="10" class="s-goldsoft"/>
    <text x="165" y="44" text-anchor="middle" font-size="13.5" font-weight="700" class="s-gold">前のもの A の存在・非存在</text>
    <text x="165" y="64" text-anchor="middle" font-size="11.5" class="s-ink">原因と見なされるもの</text>
    <rect x="370" y="20" width="250" height="56" rx="10" class="s-accsoft"/>
    <text x="495" y="44" text-anchor="middle" font-size="13.5" font-weight="700" class="s-acc">後のもの B の存在・非存在</text>
    <text x="495" y="64" text-anchor="middle" font-size="11.5" class="s-ink">結果と見なされるもの</text>
    <path d="M165 76 V112" class="st-gold" stroke-width="2" marker-end="url(#mB11)"/>
    <path d="M495 76 L190 112" class="st-muted" stroke-width="1.3" stroke-dasharray="5 4" marker-end="url(#mB11)"/>
    <path d="M495 76 V112" class="st-acc" stroke-width="2" marker-end="url(#mB11)"/>
    <path d="M165 76 L470 112" class="st-muted" stroke-width="1.3" stroke-dasharray="5 4" marker-end="url(#mB11)"/>
    <text x="330" y="100" text-anchor="middle" font-size="11" class="s-muted">点線＝限定（viśeṣaṇa）</text>
    <rect x="40" y="114" width="250" height="78" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="165" y="138" text-anchor="middle" font-size="13.5" font-weight="700" class="s-ink">原因性 kāraṇatva</text>
    <text x="165" y="158" text-anchor="middle" font-size="12" class="s-ink">B があるとき A がある（16a）</text>
    <text x="165" y="178" text-anchor="middle" font-size="11.5" class="s-muted">「のみ」の限定 → 否定的随伴</text>
    <rect x="370" y="114" width="250" height="78" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="495" y="138" text-anchor="middle" font-size="13.5" font-weight="700" class="s-ink">結果性 bhāvitā</text>
    <text x="495" y="158" text-anchor="middle" font-size="12" class="s-ink">A があるとき B がある（16b）</text>
    <text x="495" y="178" text-anchor="middle" font-size="11.5" class="s-muted">bhāva eva</text>
    <rect x="150" y="206" width="360" height="44" rx="10" class="s-anssoft"/>
    <text x="330" y="226" text-anchor="middle" font-size="13" font-weight="700" class="s-ans">存在・非存在こそが因果関係</text>
    <text x="330" y="243" text-anchor="middle" font-size="11.5" class="s-ink">知覚と非知覚によって確立される（16cd）</text>
  </svg>
  </div>
  <figcaption><b>図11　第16偈の原因性と結果性。</b>Vṛtti 26,7–13。同じ二組の存在・非存在を、どちらを主としどちらを限定とするかで、原因性と結果性が分かれる（26,7–9）。第三のものは加わらない。</figcaption>
</figure>'''
    s.append(fig)
    out.append(("s13", "13", "因果関係の成立", "k.16 / SPV 26,3–13",
                "bhāve bhāvini tadbhāvaḥ…。原因性・結果性は限定の向きで分かれる", "".join(s)))

    # ---------------- §14 k.17–18
    s = []
    s.append(mula("SP 6 / k.17", KB[17],
      "ただこれだけ〔存在・非存在〕を真実の対象とし、原因・結果を対象領域とする分別（<i>vikalpa</i>）は、偽りの対象をもつもの（<i>mithyārtha</i>）として、〔別々の〕事物を結合したかのように示す。",
      "", kind="sutra",
      crit="<b>異読</b>　17c <i>arthān</i> TŚV, PKM : <i>arthā</i> SVR。17d <i>mithyārthā</i> PKM, F : <i>mithyārthān</i> TŚV, SVR。第17偈は TŚV 149,23f; PKM 510,19f; SVR 817,3f に引用（Ci）。"))
    s.append(mula("SPV 27,3–7",
      "tenaitāvanmātratattvārthāḥ. etāvanmātraṃ bhāvābhāvau. tāv eva tattvaṃ bhūtaṃ yasyārthasyāsāv etāvanmātratattvaḥ. so 'rtho yeṣāṃ vikalpānāṃ ta etāvanmātratattvārthāḥ. kim. etāvanmātrabījāḥ kāryakāraṇagocarāḥ. te darśayanti ghaṭitān iva sambaddhān ivāsambaddhān arthān. evaṃ ghaṭanāc ca mithyārthāḥ.",
      "それゆえ「ただこれだけを真実の対象とする」。「ただこれだけ」とは存在・非存在である。その二つだけが真実、すなわち実在であるような対象、それが「ただこれだけを真実とする〔対象〕」である。それを対象とする分別が「ただこれだけを真実の対象とする」〔分別〕である。どういうことか。ただこれだけを種子とする（<i>etāvanmātrabīja</i>）、原因・結果を対象領域とする〔分別〕である。それらは、結合していない事物を「結合したかのように」、すなわち関係したかのように示す。そして、このように結合させるので「偽りの対象をもつ」。",
      "<p>第16偈までで、因果関係の実在的な内容は存在・非存在だけであることが示された。第17偈は、それにもかかわらず「A が B を生む」「A と B は因果的に結ばれている」と考える分別の身分を定める。分別は二つの面をもつ。一方で、その真実の対象は存在・非存在に尽きる。Vṛtti はこれを「ただこれだけを種子とする」と言い換え、分別が根拠のない虚構ではなく、観察された存在・非存在から生じていることを示す。他方で、分別は別々の事物を結合したかのように示すので、その現れ方において偽りの対象をもつ。</p>"
      "<p>これは第5偈の「存在は自らに立ち、混ぜるのは分別である」と、第1偈 Vṛtti の「分別によって作られた関係は否定しない」を、因果関係の場合に適用したものである。校訂者の分析 2.1.5.3.2。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>etāvanmātra°</i> n.e. T（T 18a7）。全体は PKM 508,14–17 に並行（cf.）。"))
    s.append(mula("SP 6 / k.18", KB[18],
      "別であるなら、何の結合があろうか。別でないなら、因果関係もまた何であろうか。また、他のもの〔関係〕が存在することによって、離れている二つが、どうして結びついたものとなろうか。",
      "", kind="sutra",
      crit="<b>異読</b>　18c <i>bhāve hy anyasya</i> PKM : <i>bhāve vānyasya</i> TŚV : <i>anyasya bhāve</i> SVR。第18偈は TŚV 149,24f; PKM 510,21f; SVR 817,9f に引用（Ci）。"))
    s.append(mula("SPV 28,3–8",
      "kim abhūtaḥ sambandhaḥ pradarśyate tair yena mithyārthāḥ. evam etat. tathā hy atra dvayī kalpanā. sambadhyamānaḥ kāryakāraṇabhūto 'rtho bhinno 'bhinno vā syāt. yadi bhinnaḥ, bhinne kā ghaṭanā. naiva, svasvabhāvavyavasthiteḥ. athābhinnaḥ, abhinne kāryakāraṇatāpi kā. naiva, aniṣpannasya kartavyasya kāraṇād vyatiriktasyābhāvāt. kutaḥ punar dvayor ghaṭanā.",
      "〔問〕それら〔分別〕によって示されるのは実在でない関係であり、そのために〔それらは〕偽りの対象をもつのか。〔答〕そのとおりである。すなわち、ここには二つの選択肢がある。関係づけられる、原因・結果である事物は、別であるか別でないかのどちらかであろう。もし別であるなら、「別であるとき、何の結合があろうか」。まったくない。〔それぞれが〕自らの本性に確立しているからである。また、別でないなら、「別でないとき、因果関係もまた何であろうか」。まったくない。原因から区別される、まだ完成していない、作られるべき〔結果〕がないからである。ましてや、どうして二つのものの結合があろうか。",
      "<p>第18偈は、分別が示す関係が実在でないことを、二者択一で確かめる。別であれば、各項は自らの本性に立っていて（第5偈 <i>svātmani sthitāḥ</i>）、結合の余地がない。別でなければ、原因と区別される結果、つまりまだ作られていない、これから作られるべきものがないので、因果関係が成り立たない。そもそも二つがないので、二つの結合も問題にならない。第2偈の「二か一か」（姿の融合の否定）と同じ型の論法を、因果関係に当てはめたものである。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4f <i>°bhūto 'rtho</i> Ms : T は <i>yaṅ dag pa ma yin pa'i don</i>（実在でない対象）と訳す（T 18b5）。6 <i>athābhinnaḥ</i> em.（SVR 817,13; PKM）: <i>athābhinne</i> Ms。4–7 は PKM 508,18–20 に並行（cf.）。"))
    fig = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 250" style="min-width:560px;width:100%" role="img" aria-label="第18偈の二者択一。原因と結果は別か別でないか。別なら結合がなく、別でないなら因果関係がない。第三の関係を立てても二つは結びつかない">
    <defs><marker id="mB12" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <rect x="180" y="10" width="300" height="46" rx="10" class="s-band"/>
    <text x="330" y="38" text-anchor="middle" font-size="13.5" font-weight="700" class="s-ink">関係づけられる原因・結果</text>
    <path d="M260 56 L130 88" class="st-muted" stroke-width="1.5" marker-end="url(#mB12)"/>
    <path d="M330 56 V88" class="st-muted" stroke-width="1.5" marker-end="url(#mB12)"/>
    <path d="M400 56 L530 88" class="st-muted" stroke-width="1.5" marker-end="url(#mB12)"/>
    <rect x="20" y="90" width="200" height="76" rx="10" class="s-jatisoft"/>
    <text x="120" y="113" text-anchor="middle" font-size="13" font-weight="700" class="s-jati">別（bhinna）</text>
    <text x="120" y="134" text-anchor="middle" font-size="11.5" class="s-ink">自らの本性に確立</text>
    <text x="120" y="152" text-anchor="middle" font-size="11.5" class="s-ink">→ 結合（ghaṭanā）がない</text>
    <rect x="230" y="90" width="200" height="76" rx="10" class="s-jatisoft"/>
    <text x="330" y="113" text-anchor="middle" font-size="13" font-weight="700" class="s-jati">別でない（abhinna）</text>
    <text x="330" y="134" text-anchor="middle" font-size="11.5" class="s-ink">作られるべき結果がない</text>
    <text x="330" y="152" text-anchor="middle" font-size="11.5" class="s-ink">→ 因果関係がない</text>
    <rect x="440" y="90" width="200" height="76" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="540" y="113" text-anchor="middle" font-size="12.5" class="s-muted">反論：関係という第三のもの</text>
    <text x="540" y="134" text-anchor="middle" font-size="11.5" class="s-ink">それがあっても二項は離れたまま</text>
    <text x="540" y="152" text-anchor="middle" font-size="11.5" class="s-ink">→ 第三のものが増えるだけ</text>
    <rect x="130" y="190" width="400" height="50" rx="10" class="s-anssoft"/>
    <text x="330" y="212" text-anchor="middle" font-size="13" font-weight="700" class="s-ans">実在としての関係はない</text>
    <text x="330" y="230" text-anchor="middle" font-size="11.5" class="s-ink">分別が結合したかのように示すだけ（第17偈）</text>
  </svg>
  </div>
  <figcaption><b>図12　第18偈の二者択一と第三項。</b>Vṛtti 28,3–13。左の二つは偈の前半（28,3–8）、右は後半（28,9–13）。右の型は第4偈（<i>ekābhisambandha</i>）の論法を因果関係に当てはめたもの。</figcaption>
</figure>'''
    s.append(fig)
    s.append(mula("SPV 28,9–13",
      "syād etat – na bhinnasyābhinnasya vā kevalasya sambandhaḥ, kin tarhi, sambandhākhyenaikena sambandhād iti. atrāpi bhāve sattāyām anyasya sambandhākhyasya viśliṣṭau kāryakāraṇābhimatau śliṣṭau syātāṃ katham. naiva. sa eva sambandhākhyo 'paraḥ syāt. na punas tadbhāve 'nyasya kasyacit svabhāvasaṃsarga iti kuto bhāvataḥ sambandhaḥ.",
      "こう言うかもしれない。「別であるもの、あるいは別でないもの単独の関係があるのではない。そうではなく、関係と呼ばれる一つのものとの結合によって〔関係がある〕」と。〔答論〕この場合も、「他のもの」すなわち関係と呼ばれるものが「存在すること」、すなわちあることによって、「離れている二つ」すなわち原因・結果と見なされるものが、「どうして結びついたものとなろうか」。まったくならない。関係と呼ばれるその〔第三の〕ものが、別にあるだけであろう。しかし、それがあっても、他の何か〔原因・結果〕の本性が交わる（<i>svabhāvasaṃsarga</i>）ことはない。それゆえ、どうして実在としての関係があろうか。",
      "<p>偈の後半は、第4偈の第三項案（<i>ekābhisambandha</i>）を因果関係について繰り返し退ける。関係という第三のもの R を立てても、R が存在することは、原因と結果それぞれの本性に何も変化を与えない。A と B は R があってもなくても離れたままで、ただ R が一つ増えるだけである。実在の関係であるためには項の本性が交わらなければならない、という第2偈 Vṛtti 以来の基準がここでも用いられている。</p>"
      "<p>校訂者の分析ではここまでが 2.1（因果関係の否定、第7–18偈）で、第19偈からは結合・内属などの他の関係の否定（2.2）に移る。</p>",
      kind="vrtti",
      crit="<b>本文</b>　11 <i>kāryakāraṇābhimata°</i> em.（PKM, T 19b4）: <i>kāryakāraṇatābhimata°</i> Ms（SVR 817,15 も同じ）。12 <i>°ākhyo</i> Ms : T <i>źes bya ba'i ṅo bo</i>（T 19b5）。<i>'paraḥ syāt</i> Ms : T <i>gźan źig yod par zad pa'i phyir</i>（T 19b5f、校訂者は (?) を付す）。13 <i>svabhāva°</i> Ms : T <i>dṅos po</i>（T 19b6）。9–12 は PKM 508,21–509,1 に並行（cf.）。"))
    out.append(("s14", "14", "分別が示す結合", "k.17–18 / SPV 27,3–7; 28,3–13",
                "分別は存在・非存在を種子とし、別々のものを結合したかのように示す", "".join(s)))
    return out
