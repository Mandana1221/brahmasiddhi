# -*- coding: utf-8 -*-
# Sections 15–19: k.19–25 with SPV 29–35 and colophon (Analysis 2.2, (2.2), (1.), Colophon)

def sections(mula, dev, K):
    out = []

    # ================================================================ §15 k.19
    s = []
    s.append(mula("SP 6 / k.19",
      "saṃyogisamavāyyādi sarvam etena cintitam / anyonyānupakārāc ca na sambandhī ca tādṛśaḥ // 19",
      "結合するもの（<i>saṃyogin</i>）・内属するもの（<i>samavāyin</i>）など、すべてはこれによって考察された。また、互いに助けない（<i>anupakāra</i>）ので、そのようなものは関係項ではない。",
      "", kind="sutra",
      crit="<b>異読</b>　19c <i>°ānupakārāc ca</i> TŚV, PKM : <i>°ānupakārātma</i> SVR。SP 6 の偈本文は OCR 上 <i>°ānupakārāc can na</i> と読めるが、SPV 29 の偈と Vṛtti（29,7）に従い <i>ca na</i> とした。引用 Ci PKM 510,23f; SVR 817,17f。"))
    s.append(mula("SPV 29,3–5",
      "saṃyogisamavāyyādi. ādigrahaṇena svasvāmyādi. sarvam etenānantaroktena sāmānyena sambandhapratiṣedhakena granthena cintitaṃ na saṃyogādilakṣaṇo vastutaḥ sambandho 'stīti.",
      "「結合するもの・内属するものなど」。「など」の語によって、所有物と所有者〔の関係〕（<i>svasvāmin</i>）などが〔含まれる〕。〔それら〕「すべて」は、「これによって」、すなわち直前に述べた、関係を一般的に否定する論述によって、「考察された」。つまり、結合などを特徴とする関係は、実在としてはない、と。",
      "<p>校訂者の分析では、ここから第2部の後半（2.2「その他の関係の否定」、第19–25偈）に入る。因果関係（第7–18偈）に続いて、Vaiśeṣika の範疇である結合（<i>saṃyoga</i>）と内属（<i>samavāya</i>）が取り上げられ（2.2.1、第19–22偈）、さらに適合性（<i>yogyatā</i>）が検討される（2.2.2、第23–24偈）。</p>"
      "<p>第19偈前半は、これらの関係に新しい論証を立てる必要はないと言う。<i>etena</i> を Vṛtti は「直前に述べた、関係を一般的に否定する論述」と解する。二つの実在のあいだの関係一般に対する論証が、結合・内属にもそのまま当てはまるという趣旨である。<i>ādi</i> に含められる <i>svasvāmin</i>（所有物と所有者）について、校訂者の分析は「Sāṅkhya の関係」とする（2.2.1.1）。Vṛtti 自身はその所属を述べていない。</p>",
      kind="vrtti",
      crit="<b>本文</b>　5 <i>'stīti</i> : <i>stīti</i> Ms。3–5 は PKM 509,2–3 に並行（cf.）。"))
    s.append(mula("SPV 29,6–10",
      "samavāyinas tāvan na sambandhitā, yathā śauklyaṃ guṇaḥ paṭe samavetam. anayor anyonyaṃ parasparam anupakārād ajanyajanakabhāvāt kāraṇāt samavāyilakṣaṇo na sambandhī ca tādṛśo 'nupakāryānupakārakabhūtaḥ. tathā hi yo yena upakāryaḥ sa tam apekṣate, yañ cāpekṣate tena tasya sambandhaḥ. na caivaṃ śuklapaṭayoḥ, svarūpasiddheḥ.",
      "まず、内属するものには関係項であることがない。たとえば、性質（<i>guṇa</i>）である白さが布に内属している場合のように。この二つは「互いに」、すなわち相互に「助けない」、つまり生じられるもの・生じさせるものの関係（<i>janyajanakabhāva</i>）がない、という理由から、内属するものを特徴とする〔関係項〕であって「そのような」、すなわち助けられるものでも助けるものでもないものは、「関係項ではない」。すなわち、あるものによって助けられるべきものは、それに依存する。そして依存する相手と、それとの関係がある。しかし、白いものと布とはそうではない。〔それぞれ〕自らの姿が成立しているからである。",
      "<p>第19偈後半の理由 <i>anyonyānupakārāt</i> を、Vṛtti は <i>ajanyajanakabhāvāt</i> と言い換える。「助けること」（<i>upakāra</i>）は、ここでは生じさせることと同じ意味で用いられている。論の順序は次のとおりである。関係とは依存であり（第3偈）、依存は助けるものに対してのみ成り立ち（第9偈 <i>upakārī hy apekṣyaḥ syāt</i>）、助けるとは生じさせることである。白さと布はどちらも自らの姿がすでに成立している（<i>svarūpasiddhi</i>）。だから一方が他方を生じさせることはなく、依存も関係もない。</p>"
      "<p>例が性質とその基体である実体になっているのは、内属の典型例だからである。<i>svarūpasiddheḥ</i> は第1偈の既成立のものの角（<i>siddhe kā paratantratā</i>）を、内属の二項に当てはめたものである。</p>",
      kind="vrtti",
      crit="<b>本文</b>　6 <i>paṭe</i> em.（SPVt <i>snam bu</i>）: <i>ghaṭe</i> Ms。9 <i>upakāryaḥ</i> em.（T <i>phan gdags par bya ba</i>, T 20b3）: <i>kāryaḥ</i> Ms。7–9 <i>anayor … °bhūtaḥ</i> は PKM 509,4–5 に並行（cf.）。"))
    s.append(mula("SPV 29,11–16",
      "ādhārādheyabhāvo 'pi nākāryakāraṇabhūtayoḥ, kāryakāraṇabhāve ca tadbhāvī doṣaḥ. kāryakāraṇabhāve saty ādhārādheyabhāvāt śuklapaṭayoḥ sambandhakalpanāpy asādhvī. tathā hi na tayor laukika ādhārādheyabhāvo 'sti. janyajanakalakṣaṇe cādhārādheyabhāve sāmānyatadvatoḥ parasparam anupakāryopakārakayoḥ samavāyalakṣaṇaḥ sambandho na syāt.",
      "支えるもの・支えられるものの関係（<i>ādhārādheyabhāva</i>）も、結果・原因でない二つにはない。また、結果・原因の関係があるなら、それ（因果関係）に伴う過失が〔及ぶ〕。結果・原因の関係があるとして、〔それにもとづく〕支えるもの・支えられるものの関係によって白いものと布とに関係を想定することも、正しくない。すなわち、その二つには、世間で〔言われる〕支えるもの・支えられるものの関係はない。また、支えるもの・支えられるものの関係が、生じられるもの・生じさせるものを特徴とするのなら、普遍（<i>sāmānya</i>）とそれをもつもの（<i>tadvat</i>）とは互いに助けられるもの・助けるものでないので、〔その間に〕内属を特徴とする関係はないことになろう。",
      "<p>対論者は、内属の二項は助け合わなくても、支えるもの（基体）と支えられるもの（そこにあるもの）という関係にある、と答えうる。内属を「支えられるもの・支えるものの関係」として説明するのは Vaiśeṣika の通説である。Vṛtti はこれも二者択一で退ける。(a) 二項が因果関係にないなら、支える・支えられるの関係もない。支えることは、そこにあるものを生じさせることに帰着するからである。(b) 因果関係にあるなら、第7–18偈で因果関係に示した過失がそのまま及ぶ（<i>tadbhāvī doṣaḥ</i>）。</p>"
      "<p>さらに二つの点が加えられる。第一に、白さと布のあいだには、世間で言う「支える・支えられる」の関係（器と中身のような関係）が見られない。第二に、支える関係を生じさせる関係と定義すれば、普遍とそれをもつ個物には生じさせる関係がないので、Vaiśeṣika が認める普遍の内属まで成り立たなくなる。11–13 は Arcaṭa の <i>Hetubinduṭīkā</i>（HBT 8,20–24）に並行文がある（校訂者による cf.）。</p>",
      kind="vrtti",
      crit="<b>本文</b>　11 <i>'pi</i> : <i>pi</i> Ms。14 <i>'sti</i> : <i>sti</i> Ms。14 <i>cādhā</i>(Ms 8a)<i>rādheya°</i>：写本の葉替わり。11–13 <i>ādhārādheyabhāvo … asādhvī</i> は HBT 8,20–24 に並行（cf.）。"))
    tbl = '''<div class="tbl min"><table>
<thead><tr><th>対論者の拠りどころ</th><th>例</th><th>Vṛtti の処理</th><th>帰結</th></tr></thead>
<tbody>
<tr><td class="k">関係一般の否定<span class="sm">29,3–5</span></td><td>結合・内属・所有物と所有者（<i>svasvāmin</i>）など</td><td>第1–18偈の論証がそのまま及ぶ（<i>etena cintitam</i>）</td><td><span class="pill j">実在の関係ではない</span></td></tr>
<tr><td class="k">相互の助け（<i>upakāra</i>）<span class="sm">29,6–10</span></td><td>性質である白さと布</td><td>助けとは生じさせること。二項とも自らの姿が成立している</td><td><span class="pill j">依存がなく関係項ではない</span></td></tr>
<tr><td class="k">支える・支えられる（<i>ādhārādheya</i>）<span class="sm">29,11–14</span></td><td>白さと布</td><td>因果でなければ成り立たない。因果なら因果関係の過失が及ぶ。世間的な支える関係もない</td><td><span class="pill j">関係の想定は正しくない</span></td></tr>
<tr><td class="k">支える＝生じさせる<span class="sm">29,14–16</span></td><td>普遍とそれをもつもの</td><td>両者には生じさせる関係がない</td><td><span class="pill j">普遍の内属が成り立たない</span></td></tr>
</tbody></table></div>'''
    s.insert(2, tbl)
    out.append(("s15", "15", "結合・内属と他の関係", "k.19 / SPV 29,3–16", "相互に助けないものは関係項ではない（anyonyānupakāra）", "".join(s)))

    # ================================================================ §16 k.20–21
    s = []
    s.append(mula("SP 6 / k.20",
      "janane 'pi hi kāryasya kenacit samavāyinā / samavāyī tadā nāsau na tato 'tiprasaṅgataḥ // 20",
      "〔反論〕ある内属するものが結果を生じさせるのだとしても、〔答論〕そのとき、それは内属するものではない。〔また〕それ（生じさせること）によって〔関係項なの〕でもない。過大適用（<i>atiprasaṅga</i>）になるからである。",
      "", kind="sutra",
      crit="<b>異読</b>　校訂本に異読の記載はない。カーリカー部の写本はこの偈で Ms 2b の葉が替わる。引用 Ci PKM 510,25f; SVR 818,1f。"))
    s.append(mula("SPV 30,3–7",
      "syād etad – asti kaścit samavāyī yo 'vayavirūpaṃ kāryākhyaṃ janayati. tena nānupakārād asambandhiteti. evañ janane 'pi hi kāryasya kenacit samavāyinābhyupagamyamāne nāsau samavāyī tadā, jananakāle janyasyāniṣpatter dvayor asamavāyāt, niṣpanne 'pi kārye kāraṇasya tirodhānāt, atirobhāve ca samavahitayor upakāryopakārakabhāvābhāvāt.",
      "こう言うかもしれない。「全体（<i>avayavin</i>）の姿をした、結果と呼ばれるものを生じさせる、何らかの内属するものがある。それゆえ、助けないから関係項でない、ということはない」と。〔答論〕このように、「ある内属するものが結果を生じさせる」と認められるとしても、「そのとき、それは内属するものではない」。生じさせる時点では、生じられるものがまだ完成していないので、二つの〔あいだに〕内属がないからである。結果が完成したときには、原因は消え去っている（<i>tirodhāna</i>）からである。また、消え去っていないとしても、ともに現前している二つには、助けられるもの・助けるものの関係がないからである。",
      "<p>第19偈の「互いに助けない」に対する反論。部分（<i>avayava</i>）と全体（<i>avayavin</i>）のように、内属するものの一方が他方を結果として生じさせる場合がある。そこには助ける関係があるのだから、第19偈の理由は成り立たない、というのである。部分が全体の内属因（<i>samavāyikāraṇa</i>）であるとする Vaiśeṣika の説を念頭に置いた反論と見てよい。ただし Vṛtti はその術語を用いていない。</p>"
      "<p>答論は、生じさせることと内属することが同時には成り立たないことを、三つの局面に分けて示す。(1) 生じさせている時点では、結果はまだない。(2) 結果が完成した時点では、原因はもうない。(3) 原因が残っているとしても、ともに成立している二つのあいだに助けはない。(1)(2) は第7偈の論点（因果は継起し、二項に同時には立たない）を内属に当てはめたものである。(3) は第1偈・第3偈の既成立のものの角と同じ論法である。どの局面にも、生じさせる関係と内属とが同じ二項に同時に成り立つ時点がない。(2) の <i>tirodhāna</i> は、原因が結果の生じた時点で滅しているという、Dharmakīrti の側の前提に立った言い方である。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>anupakārād</i> Ms : <i>phan par byed pa'i phyir</i>（＝<i>upakārāt</i>?）T。4 <i>'pi</i> : <i>pi</i> Ms。3–6 <i>asti … janyasyāniṣpatter</i> は PKM 509,6–9 と SVR 817,24f + 818,3f に並行（cf.）。"))
    s.append(mula("SPV 30,8–9",
      "bhavatu vā kaścit samavāyī, na tu tato jananāt kāraṇāt. kiṃ kāraṇam. atiprasaṅgataḥ, kumbhakārāder api ghaṭasya jananāt sambandhitāpatteḥ.",
      "あるいは、何らかの内属するものがあるとしてもよい。しかし、「それによって」、すなわち生じさせることという理由によって、〔関係項なの〕ではない。なぜか。「過大適用になるからである」。陶工なども壺を生じさせるので、〔壺の〕関係項であることになってしまうからである。",
      "<p>偈の後半 <i>na tato 'tiprasaṅgataḥ</i> の説明。内属するものがあることを仮に認めても、それが関係項である根拠を「生じさせること」に求めることはできない。生じさせることを根拠にすれば、壺を作る陶工も壺の関係項（内属するもの）になってしまう。生じさせる関係だけでは、内属するものとそうでないものを区別できないということである。</p>",
      kind="vrtti",
      crit="<b>本文</b>　9 <i>kumbhakārāder</i> Ms（SVR）: <i>°ādi</i> n.e. T（T 22a6）。<i>sambandhitā°</i> Ms : <i>de daṅ 'brel pa can du</i> T（T 22a6f）。9 <i>kumbhakārāder … jananāt</i> は SVR 818,4–5 に並行（cf.）。"))
    s.append(mula("SP 7 / k.21",
      "tayor anupakāre 'pi samavāye paratra vā / sambandho yadi viśvaṃ syāt samavāyi parasparam // 21",
      "もし、その二つが〔互いに〕助けないとしても、また内属において、あるいは他において〔助けがないとしても〕関係があるのなら、全世界が相互に内属するものとなってしまうであろう。",
      "", kind="sutra",
      crit="<b>異読</b>　21a <i>'pi</i> : <i>pi</i> Ms。引用 Ci PKM 510,27f; SVR 818,6f（OCR では第21・22偈の引用の記号が一つずれているが、PKM の行の順から判断した）。"))
    s.append(mula("SPV 31,3–7",
      "atha mā bhūd eṣa doṣa iti tayoḥ samavāyinoḥ parasparam anupakāre 'pi, tābhyāṃ sambandhibhyām anupakāre ca samavāye, nityatvāt tasya, tābhyāṃ samavāye ca paratra vā kvacid anupakāre 'pi, sambandho yadīṣyate, tadā viśvaṃ sarvaṃ jagat parasparāsambaddhaṃ samavāyi parasparam syāt.",
      "では、この過失が及ばないように、と〔考えて〕、「その二つ」すなわち内属する二つが互いに「助けないとしても」、またその二つの関係項によって内属が助けられないとしても——それ（内属）は常住だからである——、さらにその二つに対して内属が、「あるいは他において」何かが、助けないとしても、「関係がある」と認める「のなら」、そのときは「全世界」、すなわちあらゆる世界が、互いに結びついていないのに、「相互に内属するものとなってしまうであろう」。",
      "<p>第20偈で「助ける」角が退けられたので、対論者はもう一方の角を選ぶ。助けがまったくなくても内属は成り立つ、という立場である。Vṛtti は、偈の <i>tayoḥ</i>・<i>samavāye</i>・<i>paratra</i> を、成り立たない三つの助けとして読む。(1) 二つの関係項は互いに助けない。(2) 内属は常住なので、関係項は内属を助けない。(3) 内属も、他の何ものも、関係項を助けない。チベット訳 SPVt も（3）を「その二つも、内属も、他の何ものも助けない」と訳している。</p>"
      "<p>帰謬の形は第2偈 Vṛtti の <i>sāntaratā</i> の議論と同じである。関係項の側に何の違いも生じさせないものを関係と認めるなら、助け合っていないことは世界のどの二つについても同じように言えるので、すべてのものが互いに内属することになる。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>atha mā bhūd eṣa doṣa iti</i> rec.（SPVt <i>skyon 'dir mi 'gyur bar bya ba'i phyir</i>; cf. Ms 5a3）: <i>a(tha mā) . . . . . doṣa iti</i> Ms。4 <i>'pi</i> : <i>pi</i> Ms。5 <i>sa&lt;ma&gt;vāye</i> em. : <i>savāye</i> Ms。5 <i>'pi</i> : <i>pi</i> Ms。3–7 <i>tayoḥ … syāt</i> は PKM 509,10–13 に並行（cf.）。"))
    fig = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 330" style="min-width:560px;width:100%" role="img" aria-label="第20–21偈の両刀論法。内属するものが助ける場合も助けない場合も、内属は成り立たない">
    <defs><marker id="mC20" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <rect x="170" y="10" width="320" height="52" rx="10" class="s-band"/>
    <text x="330" y="33" text-anchor="middle" font-size="14" font-weight="700" class="s-ink">内属する二項のあいだに助けはあるか</text>
    <text x="330" y="52" text-anchor="middle" font-size="12" class="ia s-muted" font-style="italic">upakāra / anupakāra</text>
    <path d="M270 62 L170 92" class="st-muted" stroke-width="1.5" marker-end="url(#mC20)"/>
    <path d="M390 62 L490 92" class="st-muted" stroke-width="1.5" marker-end="url(#mC20)"/>
    <rect x="20" y="94" width="300" height="150" rx="10" class="s-jatisoft"/>
    <text x="170" y="118" text-anchor="middle" font-size="13.5" font-weight="700" class="s-jati">助ける＝生じさせる（第20偈）</text>
    <text x="36" y="144" font-size="12" class="s-ink">生成時：結果が未完成 → 内属がない</text>
    <text x="36" y="166" font-size="12" class="s-ink">完成時：原因はすでに消えている</text>
    <text x="36" y="188" font-size="12" class="s-ink">残るとしても：共存する二つに助けはない</text>
    <line x1="36" y1="202" x2="304" y2="202" class="st-line" stroke-width="1"/>
    <text x="36" y="224" font-size="12" class="s-muted">生成を根拠にすれば陶工も関係項（過大適用）</text>
    <rect x="340" y="94" width="300" height="150" rx="10" class="s-jatisoft"/>
    <text x="490" y="118" text-anchor="middle" font-size="13.5" font-weight="700" class="s-jati">助けない（第21偈）</text>
    <text x="356" y="144" font-size="12" class="s-ink">関係項どうしは助けない</text>
    <text x="356" y="166" font-size="12" class="s-ink">関係項は常住の内属を助けない</text>
    <text x="356" y="188" font-size="12" class="s-ink">内属も他の何ものも関係項を助けない</text>
    <line x1="356" y1="202" x2="624" y2="202" class="st-line" stroke-width="1"/>
    <text x="356" y="224" font-size="12" class="s-muted">それでも関係なら、全世界が相互に内属</text>
    <path d="M170 244 L290 270" class="st-muted" stroke-width="1.5" marker-end="url(#mC20)"/>
    <path d="M490 244 L370 270" class="st-muted" stroke-width="1.5" marker-end="url(#mC20)"/>
    <rect x="170" y="272" width="320" height="50" rx="10" class="s-anssoft"/>
    <text x="330" y="294" text-anchor="middle" font-size="13" font-weight="700" class="s-ans">どちらの立場でも内属はない</text>
    <text x="330" y="313" text-anchor="middle" font-size="12" class="s-ink">他の仕方はない。結合する二つも同様（31,7–9）</text>
  </svg>
  </div>
  <figcaption><b>図20　第20–21偈の両刀論法。</b>左は Vṛtti 30,3–9、右は 31,3–7。「助ける」角は、生じさせることと内属が同時に成り立たないことで退けられ、「助けない」角は、帰結が広すぎることで退けられる。</figcaption>
</figure>'''
    s.append(fig)
    s.append(mula("SPV 31,7–9",
      "na caivam. tasmād evam upakārānupakārapakṣe na samavāyo 'sti. na cānyaḥ prakāraḥ sambhavati. anena saṃyogināv api pratyuktau.",
      "しかし、そうではない。それゆえ、このように、助けるという立場でも助けないという立場でも、内属はない。そして、他の仕方はありえない。これによって、結合する二つ〔が関係項であること〕も退けられた。",
      "<p>第20偈（助ける）と第21偈（助けない）が一組の両刀論法であることを、Vṛtti がここで明言する。助けるか助けないかのほかに第三の可能性はない（<i>na cānyaḥ prakāraḥ</i>）。同じ論法は結合する二つにもそのまま当てはまる。結合については、さらに「結合を生じさせる」という固有の主張が第22偈で取り上げられる。</p>",
      kind="vrtti",
      crit="<b>本文</b>　8 <i>'sti</i> : <i>sti</i> Ms。8 <i>sambhavati.</i>(Ms 8b)<i>anena</i>：写本の葉替わり。"))
    out.append(("s16", "16", "内属：助けるか助けないか", "k.20–21 / SPV 30,3–31,9", "生じさせても内属するものではない。助けなしの関係は全世界の内属になる", "".join(s)))

    # ================================================================ §17 k.22
    s = []
    s.append(mula("SP 7 / k.22",
      "saṃyogajanane 'pīṣṭau tataḥ saṃyoginau na tau / karmādiyogitāpatteḥ sthitiś ca prativarṇitā // 22",
      "結合を生じさせることが認められるとしても、その二つは、それ（生じさせること）によって結合するものではない。運動（<i>karman</i>）なども結合するものとなってしまうからである。また、存続（<i>sthiti</i>）はすでに論駁されている。",
      "", kind="sutra",
      crit="<b>異読</b>　22a <i>'pīṣṭau</i> : <i>pīṣṭau</i> Ms。22cd <i>karmādiyogitāpatteḥ sthitiś ca prativarṇitā</i> SP, PKM : <i>karmāder api saṃyogitā syāj jananāt tataḥ</i> SVR。引用 Ci PKM 510,29f; SVR 818,11f。"))
    s.append(mula("SPV 32,3–8",
      "api ca saṃyogasya kāryatvāt tābhyāṃ tajjananāt saṃyogitā yadi tayoḥ, tadaivaṃ saṃyogajanane 'pīṣṭau tataḥ saṃyogajananāt kāraṇān na tau saṃyoginau. kiṃ kāraṇam. karmādiyogitāpatteḥ. yadi saṃyogajananāt saṃyogī karmaṇo 'pi saṃyogitā syāt. tathā hy anyatarakarmaja ubhayakarmajaḥ saṃyoga iṣyate. ādigrahaṇena saṃyogasyāpi saṃyogitā syāt, yataḥ saṃyogajo 'pīṣyate 'sāv iti.",
      "さらに、結合は結果であるから、その二つがそれ（結合）を生じさせることによって、その二つが結合するものであるとするなら、そのときは、このように「結合を生じさせることが認められるとしても」、「それによって」、すなわち結合を生じさせるという理由によって、「その二つは結合するものではない」。なぜか。「運動なども結合するものとなってしまうからである」。もし結合を生じさせることによって結合するものであるなら、運動も結合するものとなるであろう。というのは、結合は、一方の運動から生じるもの（<i>anyatarakarmaja</i>）、両方の運動から生じるもの（<i>ubhayakarmaja</i>）と認められているからである。「など」の語によって、結合もまた結合するものとなるであろう〔ということが含まれる〕。それ（結合）は、結合から生じるもの（<i>saṃyogaja</i>）とも認められているからである。",
      "<p>第21偈 Vṛtti の結び（「結合する二つも退けられた」）を受けて、結合に固有の主張を検討する。結合は性質であり、生じるもの（<i>kārya</i>）である。そこで対論者は、二つの実体が結合を生じさせることによって「結合するもの」になる、と主張しうる。第20偈で内属について退けた「生じさせることによる関係」を、結合について立て直す試みである。</p>"
      "<p>答論は第20偈の過大適用と同じ型である。Vaiśeṣika 自身の分類では、結合は一方の運動から生じるもの、両方の運動から生じるもの、結合から生じるものの三種である（校訂者は PDhS §§169–171 を参照させる）。結合を生じさせることが結合するものであることの根拠なら、運動も、結合を生む結合も「結合するもの」になってしまう。偈の <i>karmādi</i> の <i>ādi</i> を、Vṛtti はこの第三の種類（<i>saṃyogaja</i>）によって説明している。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>°jananāt kāraṇāt</i> em.（cf. PKM 509,18）: <i>°jananakāraṇāt</i> Ms。6 <i>'pi</i> : <i>pi</i> Ms。8 <i>'pīṣyate</i> : <i>pīṣyate</i> Ms。3–11 は PKM 509,13–20 に並行（cf.）、3–5 <i>tajjananāt … saṃyoginau</i> は SVR 818,13–14、6 以下の三種の結合の記述は SVR 818,15–17 に並行し、校訂者は PDhS §§169–171 を参照させる（cf.）。"))
    s.append(mula("SPV 32,9–11",
      "na saṃyogajananāt saṃyogitā, kin tarhi, sthāpanād iti cet. tan na. sthitiś ca prativarṇitā, sthāpyasthāpakayor janyajanakabhāvān nānyā sthitir iti pramāṇavārttike pratikṣiptā.",
      "〔反論〕「結合を生じさせることによって結合するものであるのではない。では何によるか。〔結合を〕存続させること（<i>sthāpana</i>）による」と言うなら。〔答論〕そうではない。「また、存続はすでに論駁されている」。存続させられるもの・存続させるもののあいだには、生じられるもの・生じさせるものの関係があるのだから、〔それとは〕別の存続はない、と『<i>Pramāṇavārttika</i>』において退けられているのである。",
      "<p>最後の逃げ道は、二つの実体は結合を生じさせるのではなく、存続させるのだ、という主張である。Vṛtti は、偈の <i>prativarṇitā</i> を <i>pramāṇavārttike pratikṣiptā</i> と注し、Dharmakīrti の主著を名指しで参照する。校訂者は PV 1.145 と PVSV 71,11–72,10 を挙げている。</p>"
      "<p>Vṛtti が要約する論点は、存続させることは生じさせることと別ではない、ということである。存続させられるものと存続させるものとの関係は、生じられるものと生じさせるものとの関係にほかならない。そうであれば、「存続させる」は「生じさせる」に帰着し、すぐ前の過大適用がそのまま及ぶ。この帰着は、存在は刹那ごとに生じ直すので、存続とは同類の後続刹那が生じることにすぎない、という前提に立っている。</p>",
      kind="vrtti",
      crit="<b>本文</b>　9–10 <i>na saṃyogajananāt … prativarṇitā</i> は TR 70*,3 に引用（Cie）。11 <i>pramāṇavārttike</i>：cf. PV 1.145 with PVSV 71,11–72,10（校訂者による同定）。"))
    tbl = '''<div class="tbl min"><table>
<thead><tr><th>結合を生じさせるもの</th><th>Vaiśeṣika の分類</th><th>「生じさせるから結合するもの」とした場合</th></tr></thead>
<tbody>
<tr><td class="k">二つの実体</td><td>（対論者の主張）</td><td>二つは結合するもの。ただし以下も同じ資格をもつ</td></tr>
<tr><td class="k">一方の運動</td><td><i>anyatarakarmaja</i></td><td><span class="pill j">運動が結合するもの</span></td></tr>
<tr><td class="k">両方の運動</td><td><i>ubhayakarmaja</i></td><td><span class="pill j">運動が結合するもの</span></td></tr>
<tr><td class="k">先行する結合</td><td><i>saṃyogaja</i></td><td><span class="pill j">結合が結合するもの</span>（偈の <i>ādi</i>）</td></tr>
<tr><td class="k">存続させること（<i>sthāpana</i>）</td><td>（代案）</td><td>存続させることは生じさせることに帰着する（PV で論駁済み）</td></tr>
</tbody></table></div>'''
    s.insert(2, tbl)
    out.append(("s17", "17", "結合を生じさせることと存続", "k.22 / SPV 32,3–11", "運動も結合するものになる。存続（sthiti）は生成に帰着する", "".join(s)))

    # ================================================================ §18 k.23–24
    s = []
    s.append(mula("SP 7 / k.23",
      "saṃyogādyāśraye yogyam ayogyaṃ tac ca jāyate / nityayogyasvabhāvasya tadvaikalyavirodhataḥ // 23",
      "そして、〔以前は〕不適合（<i>ayogya</i>）であったそれが、結合などの基体となることに適合したもの（<i>yogya</i>）として生じる。常に適合する本性をもつものには、それ（結合など）を欠くことが矛盾するからである。",
      "", kind="sutra",
      crit="<b>異読</b>　23a <i>saṃyogādyāśraye</i> TR（SPV）: <i>śaṃyogyāśraye</i> Ms : <i>°ñcaye</i> VR。23b <i>&lt;yogyam a&gt;yogyaṃ tac ca jāyate</i> TR : <i>yogyan (ta)c (ca) jāyate</i> Ms（<i>yogyam a</i> を欠く）: <i>ayogyaś cāpi jāyate</i> VR。23c <i>nitya°</i> em. : <i>nityaṃ</i> TR, VR。23d <i>°vaikalya°</i> TR : <i>°vikalpa°</i> VR。第23–25偈は TR 70*,5–10; 71*,4f と VR 19,1–6 に引用（Cie）。"))
    s.append(mula("SPV 33,3–8",
      "yadi saṃyogādim antareṇa saṃyogādibuddhiḥ, vibhaktayor yad rūpaṃ tat samprayuktayor api. evaṃ samprayuktayor yad rūpaṃ tad vibhaktayor api sthitāsthitayoś ceti kin na saṃyogādibuddhiḥ. na caivam. tasmāt saṃyogavibhāgakarmāṇi saṃyogādibuddher nimittam iti cet. na, tulyaparyanuyogataḥ. tavāpi tulyarūpasya vibhaktādeḥ kin na saṃyogādisamavāyaḥ.",
      "〔反論〕「もし結合などなしに結合などの知があるのなら、分離している二つ（<i>vibhakta</i>）の姿は、結びついている二つ（<i>samprayukta</i>）の姿でもある〔ことになる〕。同様に、結びついている二つの姿は分離している二つの姿でもあり、止まっている二つと止まっていない二つ〔の姿〕も〔同様である〕。それなら、なぜ〔分離している二つにも〕結合などの知が〔生じ〕ないのか。しかし、そうではない。それゆえ、結合・分離・運動が、結合などの知の原因である」と言うなら。〔答論〕そうではない。問いが等しく〔そちらにも〕向けられるからである（<i>tulyaparyanuyoga</i>）。あなたにとっても、姿の等しい分離している二つなどに、なぜ結合などの内属がないのか。",
      "<p>第19–22偈で結合・内属が関係として否定されたので、対論者は認識の側から結合などの実在を論じる。結合などが別の実在でないなら、二つの事物の姿は結合の前後で変わらない。姿が変わらないのに「結びついている」「離れている」「動いている」という知が区別されて生じるのはなぜか。その知を生む原因として、結合・分離・運動という別個の実在が必要だ、という議論である。</p>"
      "<p>Devendrabuddhi は同じ問いを返す（<i>tulyaparyanuyoga</i>）。対論者の説では、結合は実体とは別の性質なので、結合が内属しても実体の姿は変わらない。そうであれば、姿の等しい分離した二つに、なぜ結合が内属しないのかが、同じように説明できない。結合を別の実在として立てても、知が区別される理由の説明にはならない。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>sam&lt;pra&gt;yuktayor</i> em. : <i>saṃyuktayor</i> Ms。4f <i>samprayuktayor &lt;yad rūpaṃ tad vibhaktayor api&gt;</i> em.（SPVt <i>ldan pa'i ṅo bo gaṅ yin pa de ñid bral ba'i ṅo bo yaṅ yin</i>; cf. T 24a5f）: <i>samprayuktayoḥ</i> Ms（目移りによる脱文）。6–8 <i>na, tulyaparyanuyogataḥ … samavāyaḥ</i> は TR 70*,16f に引用（Ci）。"))
    s.append(mula("SPV 33,9–10",
      "tajjananakarmābhāvān na saṃyogavibhāgāv iti cet. tad evaṃ sati kin na karmāpi tatkāraṇāni ceti duruttaram etat.",
      "〔反論〕「それ（結合・分離）を生じさせる運動がないので、結合・分離がないのである」と言うなら。〔答論〕そうであるなら、なぜ運動もなく、その原因もないのか〔という問いが同じように立つ〕。これは答えがたい。",
      "<p>対論者は、分離した二つに結合が内属しない理由を、結合を生む運動がないことに求める（第22偈 Vṛtti の <i>anyatarakarmaja</i> など）。しかし同じ問いは運動にも、運動の原因にも向けられ、どこまでも遡る。第4偈の無限遡及と同じ構造で、どこで止めても、そこでは「なぜここにはあり、あそこにはないのか」が説明されないまま残る（<i>duruttara</i>）。</p>",
      kind="vrtti",
      crit="<b>本文</b>　9 <i>tajjanana°</i> : <i>tarjjanana°</i> Ms。9 <i>ta</i>(Ms 9a)<i>d</i>：写本の葉替わり。"))
    s.append(mula("SPV 33,10–14",
      "tasmāt tvayaitad eva vaktavyam. tad vibhaktādirūpam ayogyaṃ prāk paścāt saṃyogādyāśraye yogyañ jāyate. kiṃ kāraṇam. yato nityasaṃyogādiyogayogyasvabhāvasya tadvaikalyavirodhataḥ, saṃyogādiyogavaikalyaṃ virudhyate. mayāpi caitad eva vaktavyam saṃyogādivarjitam.",
      "それゆえ、あなたはまさに次のことを言わなければならない。「分離しているものなどのその姿は、以前は不適合であり、後に、結合などの基体となることに適合したものとして生じる」と。なぜか。「常に」結合などとの結びつきに「適合する本性をもつものには、それを欠くことが矛盾する」から、すなわち、結合などとの結びつきを欠くことが矛盾するからである。そして私もまた、まさにこのことを、〔ただし〕結合などを除いて、言わなければならない。",
      "<p>第23偈はここで解かれる。対論者が問いの応酬から抜け出すには、事物の姿そのものが変わると認めるしかない。以前の姿は結合の基体になるのに不適合で、後に適合した姿が生じる。姿が変わらず、常に適合しているのなら、結合を欠く時があることと矛盾する（<i>tadvaikalyavirodhataḥ</i>）。</p>"
      "<p>最後の一文が要点である。対論者もこの「適合した姿の生起」を認めざるをえない。そうであれば、仏教徒の側は同じことを、結合などの別個の実在を立てずに言えばよい（<i>saṃyogādivarjitam</i>）。結合の知を説明するのは、新たに生じた事物の本性そのものであり、結合という性質は説明に何も加えない。この結論が第24偈の <i>kim anyair gamanādibhiḥ</i> と、第25偈の刹那ごとに生じるものの本性の差異へと続く。</p>",
      kind="vrtti",
      crit="<b>本文</b>　11 <i>saṃyog&lt;ād&gt;yāśraye</i> em.（SPVt <i>sbyor ba la sogs pa'i gnas</i>; T 25a2）: <i>saṃyogyāśraye</i> Ms。12 <i>nitya°</i> em. : <i>nityaṃ</i> Ms, TR, VR。10–12 <i>tasmāt … jāyate</i> は TR 70*,18–20、12–13 <i>yato … virodhataḥ</i> は TR 70*,21f に並行（cf.）。"))
    s.append(mula("SP 7 / k.24",
      "iti tadyogyatāvācyaḥ svabhāvo 'sya nirucyatām / vibhāgayogagatibhiḥ kim anyair gamanādibhiḥ // 24",
      "それゆえ、それへの適合性（<i>yogyatā</i>）と言い表される、このものの本性が、分離・結合・運動〔という語〕によって表現されればよい。別の〔実在としての〕運動などが、何の役に立とうか。",
      "", kind="sutra",
      crit="<b>異読</b>　24b <i>'sya</i> TR : <i>sya</i> Ms。24c <i>°gatibhiḥ</i> TR : <i>°jātibhiḥ</i> VR。"))
    s.append(mula("SPV 34,3–6",
      "tasmād yogyatāśabdavācyaḥ svabhāvo 'syārthasya nirucyatām vibhāgayogagatibhiḥ saṃyogavibhāgakarmaśabdaiḥ. tadā kim aphalair anyair gamanādibhiḥ kalpitaiḥ. naiva kiñcit. ādigrahaṇāntare saṃyogavibhāgaparatvāparatvādibhiḥ.",
      "それゆえ、「適合性」という語で言い表される、この事物の本性が、「分離・結合・運動によって」、すなわち結合・分離・運動という語によって、「表現されればよい」。そうであれば、想定された、効果のない「別の運動など」が「何の役に立とうか」。何の役にも立たない。「など」の語の内には、結合・分離・遠さ（<i>paratva</i>）・近さ（<i>aparatva</i>）などが〔含まれる〕。",
      "<p>校訂者の分析 2.2.2.1.1。結合・分離・運動の語は捨てられず、事物の適合性という本性を言い表す語として残される。否定されるのは、その語に対応する別個の実在（<i>anyair … kalpitaiḥ</i>）だけである。語と知は残し、その対象を分別の構成物とする点で、第5–6偈（言語の行為・行為者の語）と同じ立場である。</p>"
      "<p><i>gamanādibhiḥ</i> の <i>ādi</i> には、Vaiśeṣika が別個の性質として立てる結合・分離・遠さ・近さなどが含められる。チベット訳 SPVt は <i>paratva</i>・<i>aparatva</i> を <i>gźan daṅ gźan ma yin pa</i>（他と他でないこと）と訳している。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>yogyatāśabdavācyaḥ</i>（T <i>ruṅ ba'i tshig brjod pa na</i>）: <i>yogyatā(śa){bde . .}(bda)vācyaḥ</i> Ms。5 <i>aphalair</i> : <i>apha(l)er</i> Ms。<i>anyair</i> : <i>anyer</i> Ms。5f <i>°grahaṇāntare saṃyoga°</i> rec.（SPVt <i>naṅ du sbyor ba</i>）: <i>°graha . . . . . ga°</i> Ms。3–5 <i>tasmād … gamanādibhiḥ</i> は TR 70*,28–30 に並行（cf.）。"))
    fig = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 300" style="min-width:560px;width:100%" role="img" aria-label="第23–24偈。結合の知の説明を、別個の性質としての結合による説明と、事物の本性の変化による説明とで比べる">
    <defs><marker id="mC21" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <text x="170" y="24" text-anchor="middle" font-size="13.5" font-weight="700" class="s-jati">対論者：別個の結合（<tspan class="ia" font-style="italic">saṃyoga</tspan>）</text>
    <text x="490" y="24" text-anchor="middle" font-size="13.5" font-weight="700" class="s-ans">Vṛtti：本性の変化（<tspan class="ia" font-style="italic">yogyatā</tspan>）</text>
    <rect x="20" y="40" width="300" height="62" rx="10" class="s-jatisoft"/>
    <text x="170" y="64" text-anchor="middle" font-size="12" class="s-ink">実体 a・b（姿は結合の前後で同じ）</text>
    <text x="170" y="86" text-anchor="middle" font-size="12" class="s-ink">＋ 内属する性質としての結合</text>
    <path d="M170 102 V126" class="st-muted" stroke-width="1.5" marker-end="url(#mC21)"/>
    <rect x="20" y="128" width="300" height="40" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="170" y="153" text-anchor="middle" font-size="12" class="s-ink">「結びついている」という知</text>
    <rect x="20" y="182" width="300" height="80" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="170" y="204" text-anchor="middle" font-size="12" class="s-muted">問いが等しく返る：同じ姿の二つに</text>
    <text x="170" y="222" text-anchor="middle" font-size="12" class="s-muted">なぜ今は内属し、前は内属しないのか</text>
    <text x="170" y="244" text-anchor="middle" font-size="12" class="s-muted">運動 → その原因 → …（答えがたい）</text>
    <rect x="340" y="40" width="300" height="62" rx="10" class="s-anssoft"/>
    <text x="490" y="64" text-anchor="middle" font-size="12" class="s-ink">以前の不適合な姿 → 後に適合した姿が生じる</text>
    <text x="490" y="86" text-anchor="middle" font-size="12" class="s-ink">（対論者も認めざるをえない：33,10–12）</text>
    <path d="M490 102 V126" class="st-muted" stroke-width="1.5" marker-end="url(#mC21)"/>
    <rect x="340" y="128" width="300" height="40" rx="10" class="s-card st-line" stroke-width="1"/>
    <text x="490" y="153" text-anchor="middle" font-size="12" class="s-ink">「結びついている」という知と語</text>
    <rect x="340" y="182" width="300" height="80" rx="10" class="s-anssoft"/>
    <text x="490" y="206" text-anchor="middle" font-size="12.5" font-weight="700" class="s-ans">結合などを除いて同じことを言う</text>
    <text x="490" y="228" text-anchor="middle" font-size="12" class="s-ink">語は適合性という本性を表す（第24偈）</text>
    <text x="490" y="248" text-anchor="middle" font-size="12" class="s-ink">別の運動などは何の役にも立たない</text>
    <text x="330" y="288" text-anchor="middle" font-size="12" class="s-muted">右の説明では、事物は姿を変えて新たに生じる。第25偈「刹那ごとに生じるもの」の本性の差異へ</text>
  </svg>
  </div>
  <figcaption><b>図21　結合の知の二つの説明（第23–24偈）。</b>Vṛtti 33,3–34,6。どちらの側も「適合した姿の生起」を認めるので、別個の範疇としての結合・分離・運動は説明に何も加えない。</figcaption>
</figure>'''
    s.append(fig)
    out.append(("s18", "18", "適合性（yogyatā）", "k.23–24 / SPV 33,3–34,6", "不適合なものが適合したものとして生じる。結合などの語はその本性を表す", "".join(s)))

    # ================================================================ §19 k.25 + colophon
    s = []
    s.append(mula("SP 7 / k.25",
      "teṣu satsv api tasyeti sambandhasyāprasiddhitaḥ / yuktaḥ svabhāvabhedo 'yaṃ tat pratikṣaṇajanmanām // 25",
      "それら〔運動など〕が存在するとしても、「これの」という関係が成立しないので、それゆえ、刹那ごとに生じるもの（<i>pratikṣaṇajanman</i>）には、この本性の差異（<i>svabhāvabheda</i>）こそが妥当である。",
      "", kind="sutra",
      crit="<b>異読</b>　25a <i>satsv api</i> TR : <i>satyepi</i> VR。偈の後にカーリカー部の奥書 <i>sambandhaparīkṣākārikā samāptā // // kṛtir ācāryadharmakīrtipādānām // //</i>（SP 7）がある。"))
    s.append(mula("SPV 35,3–7",
      "kutaḥ. yatas teṣu gamanādiṣu satsv api kalpiteṣu tasyeti sambandhasyāprasiddhitaḥ. pāratantryam ityādinā sarvathā sambandhasya niṣiddhatvāt, asya karma saṃyogo vibhāgo veti sambandhāsiddheḥ, kutas tannimitto vyapadeśaḥ. yathānyagataiḥ karmādibhir anyasambandhī na bhavaty asambandhāt, tadvad abhimatair api.",
      "〔運動などが役に立たないのは〕なぜか。「それら」運動などが、想定されたものとして「存在するとしても」、「『これの』という関係が成立しない」からである。「従属とは…」云々〔の第1偈以下〕によって、関係はあらゆる仕方で否定されているので、「これの運動」「これの結合」「これの分離」という関係は成立しない。〔そうであれば〕どうして、それ（関係）にもとづく呼称（<i>vyapadeśa</i>）があろうか。別のものにある運動などによっては、〔あるものが〕その別のものに関係するものとならない。関係がないからである。それと同じく、〔そのものに属すると〕認められている〔運動など〕によっても〔関係するものとはならない〕。",
      "<p>第24偈の問い「何の役に立とうか」の理由。運動などを別個の実在として仮に認めても、それが「この事物の」運動である、という属格の関係（<i>tasya</i>）が成り立たなければ、事物を「動いている」と呼ぶ根拠にはならない。そしてその関係は、第1偈以来の論証によってすべて否定されている。校訂者の分析はこの節を「これの、という属格の関係は成立しない」とまとめる。</p>"
      "<p>最後の比較が論点をはっきりさせる。他の事物にある運動によって、この事物が「動いている」と呼ばれないのは、両者に関係がないからである。関係が否定された以上、対論者が「この事物の運動」と認めるものも、この事物に対しては他の事物の運動と同じ立場にある。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>kalpiteṣu</i>：校訂本の印字（OCR 3回とも）は <i>kalpiteṣv tasyeti</i>。ここでは <i>kalpiteṣu</i> と読んだ。3 <i>tasyeti</i> : <i>tasyaiti</i> Ms。4 <i>°āprasiddhitaḥ</i> : <i>°āpraṣiddhitaḥ</i> Ms。4 <i>pāratantryam ityādinā</i>：Ms f. 2b4（第1偈 Vṛtti の冒頭）を参照（校訂者）。4–5 <i>pāratantryam … niṣiddhatvāt</i> は TR 70*,31–71*,1 に並行（cf.）。6–7 <i>kutas … asambandhāt</i> は TR 71*,1f に引用（Cie）。"))
    s.append(mula("SPV 35,7–12",
      "yata evaṃ na karmādisambandhād gamanādayaḥ, tasmāt pratikṣaṇajanmanāṃ bhāvānāṃ nirantarotpattyādyāśrayair aparāparaiḥ pratyayaiḥ svabhāvabhedo 'yaṃ saṃyukto viyukto gacchatīty evamādir yuktaḥ, sasthiraikasvabhāvānāṃ yogādisambandhāsiddher iti na kaścid bhāvataḥ sambandhaḥ saṃyogādilakṣaṇaḥ.",
      "このように、運動などとの関係によって「行く」など〔の呼称〕があるのではないので、「それゆえ、刹那ごとに生じる」存在には、間なく生じることなどのよりどころとなる、次々と異なる条件（<i>pratyaya</i>）によって、「結びついている」「離れている」「行く」などという「この本性の差異」こそが「妥当である」。常住で単一の本性をもつものには、結合などの関係は成立しないからである。こうして、結合などを特徴とする関係は、実在としては何もない。",
      "<p>第25偈後半の説明で、第2部の結論にあたる（校訂者の分析 (2.2)、35,3–11; 35,11–12）。存在は刹那ごとに、次々と異なる条件によって生じる。「結びついている」「離れている」「行く」は、別個の結合・分離・運動が事物に関係することではなく、そのつど生じる事物の本性が違うことを言う語である。第23偈 Vṛtti で対論者にも認めさせた「適合した姿の生起」が、ここで刹那滅の存在論の語で言い直されている。</p>"
      "<p><i>nirantarotpattyādyāśraya</i> は、結合を「間なく（隣接して）生じること」として説明する語と解した（第2偈 Vṛtti の <i>nairantarya</i> を参照）。SPVt は <i>rgyun mi 'chad par skye ba'i gźi</i>（途切れずに生じることのよりどころ）と訳しており、連続の意味にも読める。<i>sasthiraika°</i> の <i>sa</i> は解しがたい。SPVt は <i>brtan pa gcig pu'i ṅo bo</i>（常住で単一の本性）とだけ訳しているので、訳はそれに従った。</p>",
      kind="vrtti",
      crit="<b>本文</b>　9 <i>aparā</i>(Ms 9b)<i>paraiḥ</i>：写本の葉替わり。10 <i>gacchatīty evamādir</i> em. (?) : <i>gacchatīty . . . . ādir</i> Ms。10 <i>yuktaḥ, sa°</i> : <i>yukto sa°</i> Ms。"))
    s.append(mula("SPV 35,12–13",
      "ity asambandhāḥ sarvabhāvasvabhāvāḥ. śāntiḥ.",
      "このように、あらゆる存在の本性は、関係をもたない。寂静（<i>śānti</i>）。",
      "<p>校訂者の分析では、この一文が第1部・第2部を通じた全体の総括（(1.)、35,11–13）にあたる。第1偈 Vṛtti の結論 <i>sarvasya bhāvasya sambandho nāsti bhāvataḥ</i> が、ここで <i>svabhāva</i> の語を用いて言い直される。各存在はそれぞれ自らの本性に立ち（第5偈 <i>sarve te svātmani sthitāḥ</i>）、関係はその本性のどこにも含まれない。</p>"
      "<p>結びの <i>śāntiḥ</i> は写本の欠損部で、チベット訳 <i>źi ba yin no</i>（寂静である）から復元された。単なる結語なのか、分別による関係の構成が鎮まることを含意するのかは、本文からは決められない。</p>",
      kind="vrtti",
      crit="<b>本文</b>　12 <i>sarvabhāvasvabhāvāḥ</i> rec.（SPVt <i>dṅos po thams cad kyi raṅ bźin ni</i>）: <i>sarva . . . . . ti . . . . .</i> Ms。13 <i>śāntiḥ</i> rec.（SPVt <i>źi ba yin no</i>）。"))
    s.append(mula("SPV 35,14–15（奥書）",
      "sambandhaparīkṣāvṛttiḥ samāptā. kṛtir ācāryadevendrabuddheḥ. krauddha anvitasya pustakam.",
      "『<i>Sambandhaparīkṣāvṛtti</i>』終わる。師 Devendrabuddhi の作。<i>krauddhānvita</i>（?）の〔所有する〕写本。",
      "<p>写本の奥書は注釈を Devendrabuddhi の作とする。一方、チベット訳 SPVt の奥書は「論者の獅子である師 Dharmakīrti の作」とする。校訂本は写本に従っており、このページもそれに従う（「テキストと注記の基礎」を参照）。</p>"
      "<p>最後の一句は写本の所有者か書写者を記したものと思われるが、<i>krauddha~anvita</i> の語義は不明で、校訂者も (?) を付している。</p>",
      kind="vrtti",
      crit="<b>本文</b>　14 <i>sambandhaparīkṣāvṛttiḥ samāptā</i> em.（OCR では Ms の読みが示されていない）: <i>sambandhaparīkṣāvṛttir vādisiṃhācāryadharmakīrtinā kṛtā samāptā</i> retr.（SPVt <i>'brel pa brtag pa źes bya ba'i 'grel pa smra ba'i seṅ ge slob dpon chos kyi grags pas mdzad pa rdzogs so</i>）。14f <i>krauddha~anvitasya</i> (?) : <i>kroddha~anvitasya</i> Ms（校訂本は <i>~</i> で連声しない形を示す。デーヴァナーガリーでは分けて表記した）。"))
    tbl = '''<div class="tbl min"><table>
<thead><tr><th>偈</th><th>検討される関係</th><th>否定の要点</th><th>Vṛtti</th></tr></thead>
<tbody>
<tr><td class="num">19</td><td class="k">結合・内属・所有物と所有者など</td><td>関係一般の否定が及ぶ。内属する二項は互いに生じさせず、依存しない</td><td class="num">29,3–16</td></tr>
<tr><td class="num">20</td><td class="k">生じさせる内属するもの</td><td>生成と内属は同時に成り立たない。生成を根拠にすれば陶工も関係項</td><td class="num">30,3–9</td></tr>
<tr><td class="num">21</td><td class="k">助けなしの内属</td><td>全世界が相互に内属することになる</td><td class="num">31,3–9</td></tr>
<tr><td class="num">22</td><td class="k">結合を生じさせる・存続させる</td><td>運動・結合も結合するものになる。存続は生成に帰着（PV）</td><td class="num">32,3–11</td></tr>
<tr><td class="num">23–24</td><td class="k">適合性（<i>yogyatā</i>）</td><td>適合した姿が生じることは双方が認める。結合などの語はその本性を表す</td><td class="num">33,3–34,6</td></tr>
<tr><td class="num">25</td><td class="k">総括</td><td>「これの」という関係は成立しない。刹那ごとに生じるものの本性の差異で足りる</td><td class="num">35,3–13</td></tr>
</tbody></table></div>'''
    s.insert(4, tbl)
    out.append(("s19", "19", "総括と奥書", "k.25 / SPV 35,3–15", "刹那ごとに生じるものの本性の差異（svabhāvabheda）。すべての存在は無関係", "".join(s)))

    return out
