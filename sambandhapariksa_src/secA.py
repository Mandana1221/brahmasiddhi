# k.5–10 with Vṛtti (SPV 15–20). Loaded by build.py.

def sections(mula, dev, K):
    out = []

    # ---------------- §5 k.5
    s = []
    s.append(mula("SP 4 / k.5",
      "tau ca bhāvau tadanyaś ca sarve te svātmani sthitāḥ / ity amiśrāḥ svayaṃ bhāvās tān miśrayati kalpanā // 5",
      "その二つの存在も、それとは別のもの〔＝関係〕も、それらはすべて自らにおいて立っている（<i>svātmani sthita</i>）。このように、存在はそれ自体としては混じり合っていない（<i>amiśra</i>）。それらを混ぜ合わせるのは分別（<i>kalpanā</i>）である。",
      "", kind="sutra",
      crit="<b>異読</b>　5c <i>miśrayati</i> Ms, ĪPVV 1.204,6 : <i>yojayati</i> SS, ĪPVV 1.195,24; 200,16。5c <i>bhāvās</i> : <i>bhavās</i> Ms。5d <i>tān</i> : <i>tan</i> TŚV。"
           "<b>引用</b>　偈全体 TŚV 148,34; PKM 506,7f; NKC 306,18f; SVR 813,20f。後半 <i>ity amiśrāḥ … kalpanā</i> は Utpaladeva の SS 5,1（ほか 3,23f; 11,9f）、NKC 309,10、ĪPVV 1.200,16–18 に引かれ、TR 71*,20f にも引用（Cie）。Śaiva 系の引用は <i>yojayati</i> と読む。"))
    s.append(mula("SPV 15,3–6",
      "yata evam api sambandhavikalpo na jyāyān, tasmāt tau ca bhāvau sambandhitvenābhimatau tadanyaś ca sambandhākhyaḥ sarve te yathoktāḥ svātmani sthitāḥ svasmin svasmin svabhāve sthitā iti tasmād amiśrā asambaddhāḥ svayaṃ svātmanā bhāvāḥ.",
      "このように〔第4偈で提案されたように第三項を立てて〕も、関係についての分別（<i>sambandhavikalpa</i>）はよりすぐれたものではない（<i>na jyāyān</i>）。それゆえ、<b>その二つの存在</b>、すなわち関係項と認められた〔二つ〕も、<b>それとは別のもの</b>、すなわち関係と呼ばれるものも、<b>それらはすべて</b>、すでに述べたとおり、<b>自らにおいて立っている</b>。すなわち、それぞれが自らの本性にとどまっている。<b>このように</b>、それゆえ、存在は<b>それ自体としては</b>、つまり自らの本性によっては、<b>混じり合っていない</b>、すなわち関係していない（<i>asambaddha</i>）。",
      "<p>校訂者の分析 1.5「要約」。第1–4偈で、関係を二項のあいだに実在として立てる四つの定義が退けられた。第5偈はその結果を存在論の言葉でまとめ直す。偈の <i>tadanyaḥ</i> を Vṛtti は「関係と呼ばれるもの」と注する。第4偈で対論者が立てた第三項としての関係も、それが実在であるかぎり、関係項と同じく自らの本性に閉じた一つの存在にすぎない。そのため、それが二項を「混ぜる」ことはできない。</p>"
      "<p>冒頭の <i>yata evam api</i> の <i>evam</i> を、Steinkellner（2022, 試訳, n.4）は第4偈で提案された仕方（一つのものとの結合）を指すと注する。<i>api</i>（〜も）はそれを受けて、第三項を立てる案もそれ以前の三つの定義と同様に「よりすぐれてはいない」（<i>na jyāyān</i>）と言うものと解され、訳もこれに従った。<i>sambandhavikalpa</i> は関係の想定（定義の選択肢）の意。チベット訳は <i>'brel par rnam par rtog pa</i>、<i>na jyāyān</i> を <i>ruṅ ba ma yin pa</i>（妥当でない）とする。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>api</i> n.e. T。4 <i>sarve</i> : <i>sa+ve</i> Ms。5 <i>svasmin</i>（二度目）n.e. T。<i>tau ca bhāvau … bhāvāḥ</i> は PKM 506,10–12 に並行（cf.）。<i>tau ca bhāvau</i> 以下の一部について、校訂者は SVR 813,22–24 を挙げ、PVSV 147,8–9 を参照させる（Eltschinger 2010: n.30, p.199; Eltschinger–Ratié 2013: n.159, p.103）。"))
    s.append(mula("SPV 15,6–9",
      "kathaṃ tarhy āyattarūpās tais taiḥ sambandhair vyapadiśyanta iti cet, na bhāvato 'sti kaścit sambandhaḥ. kevalaṃ tān bhāvān amiśrān api miśrayati kalpanā. sāpi parāyattarūpān iva kenacin nimittenopadarśayanty utpadyate.",
      "〔反論〕では、どうして〔存在は〕依存した姿をもつものとして、あれこれの関係によって言い表されるのか。〔答論〕実在としては、いかなる関係もない。ただ<b>それら</b>の存在を、混じり合っていないにもかかわらず、<b>分別が混ぜ合わせる</b>のである。その〔分別〕もまた、何らかの契機（<i>nimitta</i>）によって、〔存在を〕他に依存した姿をもつかのように示しつつ生じる。",
      "<p>反論は言語慣用に訴える。「a は b に依存する」「a は b の結果である」と私たちは現に語っている。答えは第1偈 Vṛtti の結び（11,12）と同じで、そうした言い方の根拠は実在の側にはなく、分別の側にある。分別は、別々の存在をあたかも互いに依存した姿のものとして示す。</p>"
      "<p>最後の一文で、分別は「何らかの契機によって」生じるとされる。関係の分別にも生起の契機がある、という限定である。ただし、それが何であるかはここでは特定されない。校訂者はこの文について PVSV 34,26f、および PV 1.286 と PVSV 151,26–28 を参照させている。Ms と校訂本の <i>upadarśanty</i> は、Eltschinger の提案（Steinkellner 2022 序文）に従って <i>upadarśayanty</i>（<i>upadarśayantī</i> の連声形、「示しつつ」）と改めた。チベット訳は <i>mtshan ma 'ga' źig ston pa skye'o</i>。</p>",
      kind="vrtti",
      crit="<b>本文</b>　7 <i>'sti</i> : <i>sti</i> Ms。8 <i>tān bhāvān amiśrān</i> rec.（T <i>dṅos po de dag 'dres pa med</i>, cf. PKM 506,11f）: 欠損 Ms。<i>sāpi</i>（T 8b8 <i>de yaṅ</i>）: <i>sā . . . . .</i> Ms。9 <i>parāyattarūpān iva</i> rec.（SPVt <i>gźan la rag las pa'i ṅo bo lta bur</i>）: <i>. . . . yattarūpān iva</i> Ms。<i>upadarśayanty</i> em. E.（Steinkellner 2022 序文）: <i>upadarśanty</i> Ms, ed.。<i>kevalaṃ … utpadyate</i> について校訂者は PVSV 34,26f; PV 1.286 with PVSV 151,26–28 を挙げる（cf.）。"))
    fig3 = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 250" style="min-width:560px;width:100%" role="img" aria-label="第5偈の構図。二つの関係項と関係はそれぞれ自らの本性に立ち、混じり合っていない。それらを結びつけるのは分別である">
    <defs><marker id="mA5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <rect x="150" y="12" width="360" height="54" rx="10" class="s-goldsoft"/>
    <text x="330" y="35" text-anchor="middle" font-size="14" font-weight="700" class="s-gold">分別（kalpanā）が混ぜ合わせる</text>
    <text x="330" y="55" text-anchor="middle" font-size="12" class="s-ink">何らかの契機（nimitta）で、他に依存した姿のように示す</text>
    <path d="M220 66 L120 128" class="st-gold" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#mA5)"/>
    <path d="M440 66 L540 128" class="st-gold" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#mA5)"/>
    <path d="M330 66 V128" class="st-gold" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#mA5)"/>
    <rect x="40" y="130" width="160" height="70" rx="10" class="s-accsoft"/>
    <text x="120" y="156" text-anchor="middle" font-size="13.5" font-weight="700" class="s-acc">存在 a</text>
    <text x="120" y="176" text-anchor="middle" font-size="12" class="s-ink">関係項と認められたもの</text>
    <text x="120" y="192" text-anchor="middle" font-size="11" class="s-muted">自らの本性に立つ</text>
    <rect x="250" y="130" width="160" height="70" rx="10" class="s-jatisoft"/>
    <text x="330" y="156" text-anchor="middle" font-size="13.5" font-weight="700" class="s-jati">それとは別のもの</text>
    <text x="330" y="176" text-anchor="middle" font-size="12" class="s-ink">関係と呼ばれるもの</text>
    <text x="330" y="192" text-anchor="middle" font-size="11" class="s-muted">自らの本性に立つ</text>
    <rect x="460" y="130" width="160" height="70" rx="10" class="s-accsoft"/>
    <text x="540" y="156" text-anchor="middle" font-size="13.5" font-weight="700" class="s-acc">存在 b</text>
    <text x="540" y="176" text-anchor="middle" font-size="12" class="s-ink">関係項と認められたもの</text>
    <text x="540" y="192" text-anchor="middle" font-size="11" class="s-muted">自らの本性に立つ</text>
    <text x="330" y="232" text-anchor="middle" font-size="12.5" class="s-ink">実在の側：三者はいずれも混じり合わない（amiśra = asambaddha）</text>
  </svg>
  </div>
  <figcaption><b>図3　第5偈の構図。</b>Vṛtti 15,3–9。第4偈の第三項（関係）も、実在であるかぎり自らに立つ一つの存在にすぎない。結合は実在の層ではなく、分別の層で起こる。</figcaption>
</figure>'''
    s.append(fig3)
    out.append(("s5", "5", "要約：存在は自らに立ち、分別が混ぜる", "k.5 / SPV 15,3–9", "svātmani sthitāḥ … tān miśrayati kalpanā", "".join(s)))

    # ---------------- §6 k.6
    s = []
    s.append(mula("SP 4 / k.6",
      "tām eva cānurundhānaiḥ kriyākārakavācinaḥ / bhāvabhedapratītyarthaṃ saṃyojyante 'bhidhāyakāḥ // 6",
      "そして、まさにその〔分別〕に従う者たちによって、存在の差異（<i>bhāvabheda</i>）を知らせるために、行為と行為要素（<i>kriyākāraka</i>）を語る表示語が用いられる（<i>saṃyojyante</i>）。",
      "<p><i>saṃyojyante</i> は「結び合わされる」とも読めるが、Vṛtti はこれを <i>niveśyante</i>（あてがわれる）と言い換え、「これは行為を表示するもの、これは行為要素を表示するもの」と語に役割を割り当てることと説明する。語どうしの結合ではなく、語の使用・配置が言われているので、Steinkellner（2022, 試訳）が „are used“ と訳すのに従った。同氏は <i>kāraka</i> を „instruments“ と訳すが、ここでは行為者・対象などを含む文法上の行為要素の意に取る。</p>",
      kind="sutra",
      crit="<b>異読</b>　6a <i>°ānaiḥ</i> Ms : <i>°ānan</i> TŚV。"
           "<b>引用</b>　偈全体 TŚV 149,4f; PKM 506,18f; SVR 814,4f。6a は PKM 516,18、後半は ĪPVV 1.195,24 に引用。"))
    s.append(mula("SPV 16,3–5",
      "tām eva ca kalpanām anurundhānaiḥ puruṣaiḥ kriyākārakavācinaḥ kriyākārakābhidhāyinaś cābhidhāyakāḥ saṃyojyante, ayaṃ kriyābhidhāyy ayaṃ kārakābhidhāyīti niveśyante.",
      "<b>そして、まさにその</b>分別<b>に従う</b>人々<b>によって</b>、<b>行為と行為要素を語る</b>、すなわち行為と行為要素を表示する<b>表示語が用いられる</b>。つまり、「これは行為を表示するもの、これは行為要素を表示するもの」というように配置される（<i>niveśyante</i>）。",
      "<p>校訂者の分析 1.5.1。第5偈で関係は分別の側に移された。第6偈はその分別が言語の中でどう働くかを述べる。取り上げられるのは、行為（<i>kriyā</i>）とその行為要素（<i>kāraka</i>、行為者・対象など）との関係である。文の中で動詞と名詞が結びつくとき、そこに表されているように見える関係である。Vṛtti によれば、この語の使用は、分別に従う話者が語を「行為の語」「行為要素の語」として配置することにすぎない。</p>"
      "<p>チベット訳 SPVt の諸版本は「行為の語と行為者の語」（<i>bya ba'i tshig daṅ byed pa po'i tshig</i>）と、「これは行為の表示である」（<i>'di ni bya ba'i brjod pa'o</i>）を欠く。Frauwallner は Vinītadeva の注釈 T（8a7–8）によってこれを補っており、その補いは Ms と一致する。チベット語では <i>kāraka</i> は <i>byed pa po</i>（行為者）と訳されている。</p>",
      kind="vrtti",
      crit="<b>本文</b>　<i>tām eva … bhāvabhedapratītyartham … pratyāyanāya</i> は TŚV 149,3f; PKM 506,13–15; SVR 813,25f に並行（cf.）。"))
    s.append(mula("SPV 16,5–7",
      "bhāvabhedapratītyartham. bhāvānāṃ bhedo 'nyāpohaḥ, tasya pratyāyanāya, na punar vastubhūtaḥ kriyākārakasambandho …",
      "<b>存在の差異を知らせるために</b>。存在の差異とは、他からの排除（<i>anyāpoha</i>）である。それを知らせるために〔結び合わされるのであって〕、実在としての行為と行為要素の関係が〔あるから〕ではない。",
      "<p>語の結合の目的が「存在の差異」の伝達と規定され、その差異が <i>anyāpoha</i> と言い換えられる。語が伝えるのは、対象が他のものから区別されていることであり、実在の関係そのものではない。ここでは Dharmakīrti の言語論、すなわちアポーハ論が前提になっている。動詞と名詞の結合も、関係の実在を示すのではなく、排除の組み合わせによって差異を伝える手段にとどまる。</p>"
      "<p>文末の <i>sambandho</i> の後に、校訂本は「~ ~ ~」を印刷している。<i>-o</i> の連声形は後に語が続くことを示すが、校訂者は補っていない。チベット訳は <i>bya ba daṅ byed pa po'i 'brel pa dṅos su ni yod pa ma yin no</i>（行為と行為者の関係は実在としてはない）とする。訳はこれに従って〔　〕で補った。</p>",
      kind="vrtti",
      crit="<b>本文</b>　5 <i>°pratītyartham</i> rec.（SP 6c）: <i>°pratī . . . . m</i> Ms。7 <i>°sambandho</i> の後、校訂本「~ ~ ~」（補充なし。写本の欠損か記号かは OCR からは確定できない）。"))
    tbl6 = '''<div class="tbl min"><table>
<thead><tr><th>層</th><th>何がなされるか</th><th>Vṛtti の語</th></tr></thead>
<tbody>
<tr><td class="k">実在</td><td>各存在は自らの本性に立ち、混じり合わない。行為と行為要素の実在の関係はない</td><td><i>svātmani sthitāḥ</i>（15,5）／<i>na … vastubhūtaḥ kriyākārakasambandhaḥ</i>（16,6f）</td></tr>
<tr><td class="k">分別</td><td>別々の存在を、他に依存した姿のように示して混ぜる</td><td><i>miśrayati kalpanā</i>／<i>parāyattarūpān iva … upadarśayanty</i>（15,8f）</td></tr>
<tr><td class="k">言語</td><td>分別に従う話者が、語を行為の語・行為要素の語として配置する</td><td><i>saṃyojyante</i>／<i>niveśyante</i>（16,4f）</td></tr>
<tr><td class="k">目的</td><td>存在の差異、すなわち他からの排除を伝える</td><td><i>bhāvabhedaḥ = anyāpohaḥ</i>（16,6）</td></tr>
</tbody></table></div>'''
    s.append(tbl6)
    out.append(("s6", "6", "言語における関係：行為と行為要素", "k.6 / SPV 16,3–7", "語の結合は差異（anyāpoha）を伝えるため", "".join(s)))

    # ---------------- §7 k.7
    s = []
    s.append(mula("SP 4 / k.7",
      "kāryakāraṇabhāvo 'pi tayor asahabhāvataḥ / prasidhyati kathaṃ dviṣṭho 'dviṣṭhe sambandhatā katham // 7",
      "因果関係（<i>kāryakāraṇabhāva</i>）もまた、その二つ〔結果と原因〕が同時に存在しない（<i>asahabhāva</i>）ので、どうして二項に立つもの（<i>dviṣṭha</i>）として成立しようか。二項に立たないものに、どうして関係であることがあろうか。",
      "", kind="sutra",
      crit="<b>異読</b>　7a <i>'pi</i> : <i>pri</i> Ms。7c <i>prasidhyati</i> : <i>prasiddhyati</i> TŚV, SVR, PKM。"
           "<b>引用</b>　TŚV 149,15; PKM 509,21f; SVR 814,11f。7a は PKM 516,23 にも引用。"))
    s.append(mula("SPV 17,3–7",
      "kāryakāraṇabhāvaḥ sambandhas tarhi setsyatīti cet, tan na, yasmāt kāryakāraṇabhāvo 'pi sambandhaḥ kathaṃ prasidhyati. naiva. kimbhūtaḥ. dviṣṭhaḥ. kiṅ kāraṇam. tayoḥ kāryakāraṇayor asahabhāvataḥ. tathā hi yadā kāraṇaṃ tadā na kāryaṃ, tatkāle vā na kāraṇaṃ, tulyakālaṃ kāryakāraṇānupapatteḥ.",
      "〔反論〕「それなら、因果関係が関係として成立するだろう」と言うなら、〔答論〕そうではない。なぜなら、<b>因果関係もまた</b>関係として<b>どうして成立しようか</b>。まったく〔成立し〕ない。どのようなものとして〔成立しないのか〕。<b>二項に立つもの</b>として。なぜか。<b>その二つ</b>、すなわち結果と原因とが<b>同時に存在しないので</b>。すなわち、原因があるときには結果はなく、あるいはその〔結果の〕時には原因はない。結果と原因が同時であることは成り立たないからである。",
      "<p>校訂者の分析では、ここから第二部「個別の否定」（第7–24偈）が始まり、第7–18偈が因果関係にあてられる（2.1）。対論者は、一般的な関係が否定されても、因果関係だけは実在の関係として残ると考える。仏教徒自身が因果を認めているので、この反論は自然である。</p>"
      "<p>論証は、第2偈 Vṛtti 以来の要件「関係は二項に立つ」（<i>dviṣṭha</i>）にもとづく。二項に立つためには、二項が同時に存在しなければならない。ところが原因と結果は継起するので、どの時点にも一方しかない。「原因があるときには結果はなく…」の一文（17,6）は Bhāsarvajña, <i>Nyāyabhūṣaṇa</i> 503,11 に引かれている。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>kathaṃ prasidhyati. naiva.</i> Eltschinger の提案（Steinkellner 2022 序文）: <i>katham, naiva, prasidhyati</i> Ms, ed.（偈の語順に合わせ、挿入句を後置する）。3 <i>tan na</i> : <i>tat na</i> Ms。4 <i>kāryakāraṇabhāvo</i> rec.（SPVt <i>rgyu daṅ 'bras bu'i dṅos po'i</i>）: <i>. . . . . ṇabhāvo</i> Ms。6 <i>kāryaṃ tatkāle</i> rec.（PKM, SVR）: <i>kārya+ . . kāle</i> Ms。7 <i>°kāraṇānupapatteḥ</i> : <i>°kāraṇān+papat+eḥ</i> Ms。<i>yadā kāraṇaṃ … na kāraṇam</i> は NBhūṣ 503,11 に引用（Cie）。第7偈 Vṛtti 全体（17,3–10）は PKM 506,21–26; SVR 814,6–10 に並行（cf.）。"))
    fig4 = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 230" style="min-width:560px;width:100%" role="img" aria-label="第7偈。原因と結果は継起し、どの時点にも一方しか存在しないので、二項に立つ関係の場所がない">
    <defs><marker id="mA7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <line x1="120" y1="200" x2="620" y2="200" class="st-muted" stroke-width="1.5" marker-end="url(#mA7)"/>
    <text x="630" y="196" font-size="12" class="s-muted">時</text>
    <text x="250" y="220" text-anchor="middle" font-size="12" class="s-muted">t₁（原因の時）</text>
    <text x="490" y="220" text-anchor="middle" font-size="12" class="s-muted">t₂（結果の時）</text>
    <text x="60" y="76" text-anchor="middle" font-size="13" font-weight="700" class="s-ink">原因</text>
    <text x="60" y="146" text-anchor="middle" font-size="13" font-weight="700" class="s-ink">結果</text>
    <rect x="170" y="52" width="160" height="40" rx="9" class="s-accsoft"/><text x="250" y="77" text-anchor="middle" font-size="12.5" class="s-acc">存在する</text>
    <rect x="410" y="52" width="160" height="40" rx="9" class="s-card st-line" stroke-width="1" stroke-dasharray="4 3"/><text x="490" y="77" text-anchor="middle" font-size="12.5" class="s-muted">もうない</text>
    <rect x="170" y="122" width="160" height="40" rx="9" class="s-card st-line" stroke-width="1" stroke-dasharray="4 3"/><text x="250" y="147" text-anchor="middle" font-size="12.5" class="s-muted">まだない</text>
    <rect x="410" y="122" width="160" height="40" rx="9" class="s-accsoft"/><text x="490" y="147" text-anchor="middle" font-size="12.5" class="s-acc">存在する</text>
    <rect x="160" y="18" width="180" height="24" rx="6" class="s-jatisoft"/><text x="250" y="35" text-anchor="middle" font-size="12" class="s-jati">一項のみ → dviṣṭha でない</text>
    <rect x="400" y="18" width="180" height="24" rx="6" class="s-jatisoft"/><text x="490" y="35" text-anchor="middle" font-size="12" class="s-jati">一項のみ → dviṣṭha でない</text>
  </svg>
  </div>
  <figcaption><b>図4　第7偈：継起する二項には、二項に立つ関係の場所がない。</b>Vṛtti 17,6–7。非刹那論者が同時の因果の例を持ち出しても、同時に存在する二つの実在がそもそもないので役に立たない（17,7–10）。</figcaption>
</figure>'''
    s.append(fig4)
    s.append(mula("SPV 17,7–10",
      "akṣaṇikānām apy abhāvatvān na kāryakāraṇabhāvaḥ sahabhāvo vety akṣaṇikavādodāharaṇam apy atrāyuktam. ato na vastubhūtau sahabhāvinau vidyete yena dvayor vartamānaḥ sambandhaḥ syāt.",
      "非刹那的なものもまた非存在であるので、〔それらには〕因果関係も共存（<i>sahabhāva</i>）もない。それゆえ、非刹那論者（<i>akṣaṇikavādin</i>）の例を〔ここに〕持ち出すことも不適切である。したがって、同時に存在する二つの実在はなく、それによって関係が二つにわたって存在するということはありえない。",
      "<p>対論者は、原因と結果が同時に存在する例を、刹那滅を認めない論者の側から持ち出すことができる。Vṛtti はこれを入口で封じる。非刹那的な（持続する）ものは、そもそも実在しない（<i>abhāvatva</i>）。そのため、それらのあいだの因果も共存も問題にならない。前提にあるのは、実在するものは刹那的であるという Dharmakīrti の刹那滅論である。どのような例が想定されているかは、本文からは特定できない。</p>"
      "<p>これにより、第7偈の <i>asahabhāva</i> は経験的な観察ではなく、存在論的な主張になる。刹那的な実在のあいだでは、原因と結果は原理的に同時でありえない。同時に存在する二つの実在がないので、二項に立つ関係の場所もない。</p>"
      "<p>最後の文の接続を、校訂本は Ms に従って <i>yato</i>（なぜなら）とし、Steinkellner（2022, 試訳）もそのまま理由文として訳す。同書序文は <i>ato</i>（したがって）と読む Eltschinger の提案を記しており、ここではこれを採った。非刹那的なものは実在しないので、同時に存在する二つの実在はない、という帰結の文になり、論の流れがより自然になる。</p>",
      kind="vrtti",
      crit="<b>本文</b>　9 <i>ato na</i> Eltschinger の提案（Steinkellner 2022 序文）: <i>(y)ato na</i> Ms, ed.。7 <i>akṣaṇikānām</i> : <i>akṣaṇikā+ām</i> Ms。8 <i>°āharaṇam</i> : <i>°āhara . . m</i> Ms。8f <i>ayuktam</i> : <i>ayukta+</i> Ms。SPVt は <i>skad cig ma ma yin par smra bas brjod pa yaṅ rigs pa ma yin pa'i phyir</i>（非刹那論者が述べることも不合理なので）と訳す。"))
    s.append(mula("SPV 17,10–11",
      "adviṣṭhe ca bhāve sambandhatā katham. naiva. buddhyā vyākṛtya sambandho vikalpena nirmitaḥ syāt.",
      "<b>そして二項に立たない</b>存在に、<b>どうして関係であることがあろうか</b>。まったくない。知によって〔二項を〕区分して〔関係づけるなら〕、関係は分別によって作られたものとなろう。",
      "<p>偈の後半は、二項に立たないものは関係ではない、という要件を確認する。Vṛtti の最後の一文は第1偈・第5偈の結論を因果関係に当てはめる。原因と結果を結ぶのは知のはたらきであり、そうして立てられた関係は分別の産物である。<i>vyākṛtya</i> に対応するチベット訳は <i>blos sbrel te 'brel na ni</i>（知によって結びつけて関係づけるなら）。校訂者はここに <i>sbrel</i> を当てることに疑問符を付けている。</p>"
      "<p>Steinkellner（2022, 試訳）は <i>buddhyā vyākṛtya</i> を <i>sambandhaḥ</i> にかけ、「知によって顕わにされた関係」は分別が作ったもの（„created by conceptual construction“）だろう、と一文に訳す。ここでは、チベット訳の条件文（<i>… 'brel na ni</i>）に従い、絶対分詞を「〔二項を〕区分して〔関係づけるなら〕」と補って訳した。どちらでも、知のはたらきで立てられた関係は分別の産物だ、という趣旨は同じである。</p>",
      kind="vrtti",
      crit="<b>本文</b>　11 <i>vyākṛtya</i>：校訂者注「<i>sbrel</i>? for <i>vyākṛtya</i>」。11 校訂本の本文は <i>sambandho vikalpena nirmitaḥ</i> と印刷するが、注記は「<i>sambandho vikalpena miśritaḥ</i> rec.（cf. T <i>'brel na ni / rnam par rtog pas bskyed par 'gyur ro</i>）: <i>sambandha . . . . . miś+itaḥ</i> Ms」とする。Ms の残存字は <i>miśritaḥ</i>（第5偈 <i>miśrayati</i> と同語根）を支持し、T の <i>bskyed</i>（生じさせる）は <i>nirmita</i> に近い。OCR の三つの版はいずれも本文を <i>nirmitaḥ</i> とする。Steinkellner（2022, 試訳）は „created“ と訳し、本文 <i>nirmitaḥ</i> に従っている。同書序文の訂正表にもこの箇所はないので、印刷された本文 <i>nirmitaḥ</i> を校訂者の採る読みとみなし、注記の lemma <i>miśritaḥ</i> は不整合として残る（Ms の残存字 <i>miś+itaḥ</i> は <i>miśritaḥ</i> を示唆する）。訳は <i>nirmitaḥ</i> に従った。"))
    out.append(("s7", "7", "因果関係の否定 (1)：二項は同時にない", "k.7 / SPV 17,3–11", "asahabhāva のため dviṣṭha でない", "".join(s)))

    # ---------------- §8 k.8
    s = []
    s.append(mula("SP 4 / k.8",
      "krameṇa bhāva ekatra vartamāno 'nyaniḥspṛhaḥ / tadabhāve 'pi tadbhāvāt sambandho naikavṛttimān // 8",
      "〔関係という〕存在が継起的に（<i>krameṇa</i>）一方に存するなら、〔それは〕他方に関心をもたない（<i>anyaniḥspṛha</i>）。その〔他方〕がなくても、それは存在するからである。一方にのみ存するもの（<i>ekavṛttimat</i>）は関係ではない。",
      "", kind="sutra",
      crit="<b>異読</b>　8b <i>'nyaniḥspṛhaḥ</i> SPV : <i>'nyamispṛhaḥ</i> Ms, TŚV, SVR, PKM（OCR の読み。Vṛtti 18,5.7 で Ms が <i>nispṛhaḥ</i> と書くことからみて、<i>'nyanispṛhaḥ</i> の誤認識の可能性がある）。校訂者はすべての証拠に対して Vṛtti の読みを採る。8c <i>'pi</i> : <i>pi</i> Ms。<i>tadbhāvāt</i> SVR, PKM : <i>bhāvāt tat</i> Ms : <i>bhāvāc ca</i> TŚV。Vṛtti の引用は <i>tadabhāve 'pi bhāvāt</i>（18,8）。8d <i>sambandho</i> : <i>sambandhau</i> PKM。"
           "<b>引用</b>　TŚV 149,15f; PKM 510,1f; SVR 814,14f。"))
    s.append(mula("SPV 18,3–7",
      "kāraṇe kārye vā krameṇa sambandho vartata ity apy ayuktam. tathā hi krameṇāpi bhāva ekatraikasminn api kāraṇe kārye vā vartamānaḥ sambandhākhyo 'nyaniḥspṛhaḥ. kāraṇe vartamānaḥ kāryānapekṣaḥ kārye vartamānaḥ kāraṇanirapekṣa iti dvayoḥ krameṇa vartamāno na tatsambandhaḥ.",
      "〔反論〕「関係は原因あるいは結果に継起的に存する」〔と言うなら〕、それもまた不適切である。すなわち、<b>継起的に</b>であっても、<b>一方に</b>、つまり原因か結果かのどちらか一つに<b>存する</b>、関係と呼ばれる<b>存在</b>は、<b>他方に関心をもたない</b>。原因に存するときは結果に依存せず、結果に存するときは原因に依存しない。だから、二つに継起的に存するものは、それら〔二つ〕の関係ではない。",
      "<p>校訂者の分析 2.1.2。第7偈の難点（同時に二項がない）を避けるため、対論者は関係を時間の上に分配する。関係は、原因の時には原因に、結果の時には結果に、順に存する。こうすれば、どの時点でも関係は現にある項に支えられている。</p>"
      "<p>Vṛtti の応答は、関係の同一性の条件を問う。どの時点でも関係は一方の項にしか存しない。そのとき関係は、そこにない他方の項に依存していない（<i>anapekṣa</i>, <i>nirapekṣa</i>）。他方に依存しないものは、他方との関係ではありえない。<i>niḥspṛha</i>（欲求・関心をもたない）は第3偈の <i>nirāśaṃsa</i> と同じく、依存の欠如を擬人的に言う語である。次の第9偈では反対語 <i>saspṛha</i> が対論者の側から使われる。</p>",
      kind="vrtti",
      crit="<b>本文</b>　4 <i>bhāva</i> : <i>bhāve</i> Ms。5 <i>°niḥspṛhaḥ</i> : <i>°nispṛhaḥ</i> Ms。7 <i>tat</i>（<i>tatsambandhaḥ</i>）n.e. T。第8偈 Vṛtti（18,3–8）は PKM 506,27–507,3; SVR 814,16–17 に並行（cf.）。"))
    s.append(mula("SPV 18,7–10",
      "yo yasmin niḥspṛho na tasyāsau sambandho bhavaty ekavṛttimān, krameṇa kāryakāraṇabhāvī, tadabhāve 'pi bhāvāt, kāryakāraṇabhūtayoḥ parasparābhāve 'pi sambandhākhyasyārthasya sattākāraṇāt.",
      "あるものに関心をもたないものは、それの関係ではない。〔すなわち〕<b>一方にのみ存するもの</b>、つまり継起的に因果関係となるものは、〔関係ではない〕。<b>その〔他方〕がなくても存在するからである</b>。すなわち、原因と結果であるものが互いに他方を欠いていても、関係と呼ばれるものは存在するからである。",
      "<p>一般原則が示される。y に関心をもたない（y に依存しない）ものは、y の関係ではない。<i>ekavṛttimat</i> を Vṛtti は「継起的に因果関係となるもの」と言い換え、対論者の案そのものを指していることを明らかにする。</p>"
      "<p>理由は、関係が他方の非存在のもとでも存在するという点にある。t₁ では結果がないのに関係は原因に存し、t₂ では原因がないのに関係は結果に存する。他方の存否と無関係に存在するものは、他方との関係とは言えない。関係であるためには、両項の存在に依存していなければならないからである。第9偈は、この依存を対論者が回復しようとする試みを扱う。</p>",
      kind="vrtti",
      crit="<b>本文</b>　7 <i>niḥspṛho</i> : <i>nispṛho</i> Ms。8 <i>'pi</i> : <i>pi</i> Ms。9 <i>'pi</i> : <i>pi</i> Ms。10 <i>sattākāraṇāt</i> : <i>satākāraṇāt</i> Ms。"))
    tbl8 = '''<div class="tbl min"><table>
<thead><tr><th>時点</th><th>原因</th><th>結果</th><th>関係 R の所在</th><th>R は他方に依存するか</th></tr></thead>
<tbody>
<tr><td class="num">t₁</td><td>存在</td><td>まだない</td><td>原因にのみ存する</td><td><span class="pill j">結果に依存しない</span>（<i>kāryānapekṣa</i>）</td></tr>
<tr><td class="num">t₂</td><td>もうない</td><td>存在</td><td>結果にのみ存する</td><td><span class="pill j">原因に依存しない</span>（<i>kāraṇanirapekṣa</i>）</td></tr>
<tr><td class="k" colspan="3">帰結（18,7–10）</td><td colspan="2">他方の非存在のもとでも存在するので、一方にのみ存するものであり、関係ではない（<i>sambandho naikavṛttimān</i>）</td></tr>
</tbody></table></div>'''
    s.append(tbl8)
    out.append(("s8", "8", "因果関係の否定 (2)：継起的な関係", "k.8 / SPV 18,3–10", "一方にのみ存するもの（ekavṛttimat）は関係でない", "".join(s)))

    # ---------------- §9 k.9
    s = []
    s.append(mula("SP 4 / k.9",
      "yady apekṣya tayor ekam anyatrāsau pravartate / upakārī hy apekṣyaḥ syāt kathaṃ copakaroty asan // 9",
      "もし二つのうちの一方に依存して、それ（関係）が他方に存するとするなら、依存されるものは助けるもの（<i>upakārin</i>）でなければならない。そして、存在しないものがどうして助けようか。",
      "", kind="sutra",
      crit="<b>異読</b>　9a <i>apekṣya tayor</i> : <i>apekṣitayor</i> SVR。9c <i>apekṣyaḥ</i> : <i>apekṣaḥ</i> TŚV, SVR。"
           "<b>引用</b>　TŚV 149,16f; PKM 510,3f; SVR 814,19f。9d <i>kathaṃ copakaroty asan</i> は PKM 520,1f にも引用。"))
    s.append(mula("SPV 19,3–6",
      "mā bhūd eṣa doṣa iti. yady apekṣya tayoḥ kāryakāraṇayor ekaṃ kāryaṃ kāraṇaṃ vānyatra kārye kāraṇe vāsau sambandhaḥ krameṇa pravartata iti saspṛhatvena dviṣṭha eveṣyate, tadā tenāpekṣyamāṇenopakāriṇā bhavitavyam. kiṅ kāraṇam. yata upakārī hy apekṣyaḥ syān nānyaḥ.",
      "この過失が生じないように、と〔考えて〕、<b>もし</b><b>その二つ</b>、すなわち結果と原因の<b>一方</b>、結果あるいは原因<b>に依存して</b>、<b>他方</b>、原因あるいは結果に、<b>それ</b>、すなわち関係が継起的に<b>存する</b>とし、こうして〔他方に〕関心をもつ（<i>saspṛha</i>）ことによって、まさに二項に立つものと認めるなら、そのときは、その依存されるものは助けるものでなければならない。なぜか。<b>依存されるものは助けるものでなければならない</b>からであり、他の〔助けないもの〕は〔依存されることは〕ない。",
      "<p>校訂者の分析 2.1.3。第8偈の難点は、継起的な関係が他方の項に依存しないことであった。対論者はそこで、関係は一方に存しながら他方に依存する（<i>saspṛha</i>）と修正する。たとえば結果に依存して原因に存する、あるいは原因に依存して結果に存する。こうすれば、関係は依存を通じて二項に立つ（<i>dviṣṭha</i>）ことになる。</p>"
      "<p>Vṛtti はこれを、依存の一般条件によって退ける。依存されるもの（<i>apekṣya</i>）は、依存するものを助けるもの（<i>upakārin</i>）でなければならない。この原則は、第3偈 Vṛtti の解説で触れた PVSV の消滅無因論の論法と同じ型で、本書ではここで因果関係に適用される。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>°kāraṇayor ekam</i> rec.（PKM, SVR）: <i>°kāraṇa . . . . .</i> Ms。4 <i>kārye</i> : <i>kārya</i> Ms。<i>kāryakāraṇayor … bhavitavyam</i> は PKM 519,24–520,1 に並行（cf.）。第9偈 Vṛtti 全体（19,3–8）は PKM 507,3–8; SVR 814,21–815,1 に並行（cf.）。"))
    s.append(mula("SPV 19,7–8",
      "apekṣyamāṇam upakāry astv iti cet. kathañ copakaroty asan. kāraṇakāle kāryākhyo 'san kāryakāle kāraṇākhyo 'san naivopakaroty asāmarthyāt.",
      "〔反論〕「依存されるものは助けるものであってよい」と言うなら、〔答論〕<b>そして、存在しないものがどうして助けようか</b>。原因の時には結果と呼ばれるものは存在せず、結果の時には原因と呼ばれるものは存在しない。〔存在しないものは〕能力がない（<i>asāmarthya</i>）ので、決して助けない。",
      "<p>対論者が「依存されるものは助けるものだ」と認めても、問題は解決しない。依存されるべき他方の項は、関係が存するその時点には存在しないからである。原因に存する関係が結果に依存するなら、原因の時に結果はまだない。結果に存する関係が原因に依存するなら、結果の時に原因はもうない。存在しないものには能力がなく、助けることはできない。</p>"
      "<p>こうして、第7偈（同時性）、第8偈（継起的な所在）、第9偈（継起的な依存）の三段で、因果関係を二項に立つ実在として立てる道はすべて塞がれる。どの案も、原因と結果が同時に存在しない、という一点で行き詰まる。</p>",
      kind="vrtti",
      crit="<b>本文</b>　8 <i>kāryākhyo 'san</i>（PKM, SVR）: <i>kā . .（khyo +san）</i> Ms。"))
    fig5 = '''<figure>
  <div class="scroll">
  <svg viewBox="0 0 660 240" style="min-width:560px;width:100%" role="img" aria-label="第9偈。関係が一方に存して他方に依存するとしても、依存される他方はその時点に存在せず、助けることができない">
    <defs><marker id="mA9" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" class="s-muted"/></marker></defs>
    <text x="165" y="24" text-anchor="middle" font-size="13" font-weight="700" class="s-ink">(i) 原因に存し、結果に依存する</text>
    <text x="495" y="24" text-anchor="middle" font-size="13" font-weight="700" class="s-ink">(ii) 結果に存し、原因に依存する</text>
    <rect x="40" y="44" width="250" height="34" rx="8" class="s-band"/><text x="165" y="66" text-anchor="middle" font-size="12.5" class="s-ink">時点 t₁（原因の時）</text>
    <rect x="370" y="44" width="250" height="34" rx="8" class="s-band"/><text x="495" y="66" text-anchor="middle" font-size="12.5" class="s-ink">時点 t₂（結果の時）</text>
    <rect x="40" y="100" width="110" height="56" rx="10" class="s-accsoft"/><text x="95" y="124" text-anchor="middle" font-size="13" font-weight="700" class="s-acc">原因</text><text x="95" y="143" text-anchor="middle" font-size="11.5" class="s-ink">R が存する</text>
    <rect x="180" y="100" width="110" height="56" rx="10" class="s-card st-line" stroke-width="1" stroke-dasharray="4 3"/><text x="235" y="124" text-anchor="middle" font-size="13" class="s-muted">結果</text><text x="235" y="143" text-anchor="middle" font-size="11.5" class="s-muted">まだない（asat）</text>
    <path d="M150 128 L178 128" class="st-muted" stroke-width="1.5" marker-end="url(#mA9)"/>
    <rect x="370" y="100" width="110" height="56" rx="10" class="s-card st-line" stroke-width="1" stroke-dasharray="4 3"/><text x="425" y="124" text-anchor="middle" font-size="13" class="s-muted">原因</text><text x="425" y="143" text-anchor="middle" font-size="11.5" class="s-muted">もうない（asat）</text>
    <rect x="510" y="100" width="110" height="56" rx="10" class="s-accsoft"/><text x="565" y="124" text-anchor="middle" font-size="13" font-weight="700" class="s-acc">結果</text><text x="565" y="143" text-anchor="middle" font-size="11.5" class="s-ink">R が存する</text>
    <path d="M510 128 L482 128" class="st-muted" stroke-width="1.5" marker-end="url(#mA9)"/>
    <text x="165" y="176" text-anchor="middle" font-size="11.5" class="s-muted">依存（apekṣā）</text>
    <text x="495" y="176" text-anchor="middle" font-size="11.5" class="s-muted">依存（apekṣā）</text>
    <rect x="130" y="192" width="400" height="38" rx="10" class="s-anssoft"/>
    <text x="330" y="216" text-anchor="middle" font-size="12.5" class="s-ans">依存されるものは助けるもの。だが存在しないものは助けない（asāmarthya）</text>
  </svg>
  </div>
  <figcaption><b>図5　第9偈：依存される項は、その時点に存在しない。</b>Vṛtti 19,3–8。依存を条件として二項性を回復しようとしても、依存は助け（<i>upakāra</i>）を前提とし、助けは存在を前提とする。</figcaption>
</figure>'''
    s.append(fig5)
    out.append(("s9", "9", "因果関係の否定 (3)：依存と助け", "k.9 / SPV 19,3–8", "依存されるものは助けるもの（upakārin）", "".join(s)))

    # ---------------- §10 k.10
    s = []
    s.append(mula("SP 4 / k.10",
      "yady ekārthābhisambandhāt kāryakāraṇatā tayoḥ / prāptā dvitvādisambandhāt savyetaraviṣāṇayoḥ // 10",
      "もし一つのもの（<i>ekārtha</i>）との結合によって、その二つに因果性（<i>kāryakāraṇatā</i>）があるとするなら、二性（<i>dvitva</i>）などとの結合によって、左右の角にも〔因果性が〕あることになってしまう。",
      "", kind="sutra",
      crit="<b>異読</b>　10d <i>savyetara°</i> : <i>savyetāra°</i> Ms。"
           "<b>引用</b>　TŚV 149,17f; PKM 510,5f; SVR 815,3f。"))
    s.append(mula("SPV 20,3–5",
      "kiñ ca. yady ekārthābhisambandhāt kāraṇāt kāryakāraṇatā tayoḥ kāryakāraṇatvenābhimatayoḥ, tadā saṅkhyākhyena dvitvādinā sambandhāt prāptā kāryakāraṇatā savyetaragoviṣāṇayor api.",
      "さらに、<b>もし</b><b>一つのものとの結合</b>という原因<b>によって</b>、<b>その二つ</b>、すなわち結果と原因であると認められている〔二つ〕に<b>因果性がある</b>とするなら、そのときは、数（<i>saṅkhyā</i>）と呼ばれる<b>二性など</b>との<b>結合によって</b>、牛の<b>左右の角</b>にも<b>因果性があることになってしまう</b>。",
      "<p>校訂者の分析 2.1.4。第4偈の第三項案（<i>ekābhisambandha</i>）を因果関係に適用した場合である。二つのものが一つの第三のものと結合していることが因果性の根拠だとすると、二つのものに同時に属する性質は他にもいくらでもある。たとえば数の「二」（<i>dvitva</i>）は、どの二つのものにも属する。すると、同時に並んでいて互いに原因でも結果でもない牛の左右の角にも、因果性があることになる。</p>"
      "<p>挙げられた例はいずれも Vaiśeṣika の範疇から取られている。<i>dvitva</i> は性質（<i>guṇa</i>）のうち数（<i>saṅkhyā</i>）に属する。偈の <i>dvitvādi</i>（二性など）の「など」は、次のブロックで説明される。</p>",
      kind="vrtti",
      crit="<b>本文</b>　3 <i>kāryakāraṇatā</i> rec.（SPVt <i>rgyu daṅ 'bras bu ñid</i>, PKM）: <i>kārya . . . . .</i> Ms。4 <i>°ābhimatayoḥ</i> rec.（SPVt <i>mṅon par 'dod pa</i>, PKM）: <i>°ābhi . . . . . yos</i> Ms。<i>kiñ ca … savyetaragoviṣāṇayor</i> は PKM 507,9–11; SVR 815,7–9 に並行（cf.）。"))
    s.append(mula("SPV 20,5–7",
      "na ceṣyate, tadanyatrāpi mā bhūt. ādigrahaṇena paratvāparatvaviṣāṇatvādinā sambandhāt.",
      "〔左右の角の場合に因果性が〕認められないなら、それ以外の場合にも〔因果性は〕あってはならない。「など」という語によって、遠さ・近さ（<i>paratva</i>, <i>aparatva</i>）、角性（<i>viṣāṇatva</i>）などとの結合による〔場合が含まれる〕。",
      "<p>帰謬の形式。左右の角に因果性がないことは誰もが認める。<i>na ceṣyate</i> は、Steinkellner（2022, 試訳, n.6）に従い条件文に解した。SPVt は <i>de ltar mi 'dod na ni</i>、Vinītadeva の注釈（T 12b1）も <i>de ltar na mi 'dod na</i> と、いずれも「認めないなら」と訳す。共通の第三項と結合していることが同じなら、本来の原因と結果のあいだにも、それを根拠として因果性を認めることはできない。</p>"
      "<p>「など」には、<i>paratva</i>・<i>aparatva</i>（Vaiśeṣika の性質）と、<i>viṣāṇatva</i>（角であること。二つの角に共通する普遍）が数えられている。性質であれ普遍であれ、二つのものに共通に関わる第三項はどれも因果性の根拠にならない、という一般化である。校訂者の分析はこれを「あらゆる種類の共通の属性によって関係することになる」とまとめている。</p>",
      kind="vrtti"))
    tbl10 = '''<div class="tbl min"><table>
<thead><tr><th>「一つのもの」の候補</th><th>Vaiśeṣika での位置</th><th>左右の角にも共通か</th><th>帰結</th></tr></thead>
<tbody>
<tr><td class="k"><i>dvitva</i>（二性）</td><td>性質のうち数（<i>saṅkhyā</i>）</td><td>共通（二つで一つの「二」）</td><td rowspan="3"><span class="pill j">左右の角も因果関係になる</span>。認められないので、本来の因果にも根拠とならない（20,5f）</td></tr>
<tr><td class="k"><i>paratva / aparatva</i>（遠さ・近さ）</td><td>性質</td><td>Vṛtti が同類として挙げる</td></tr>
<tr><td class="k"><i>viṣāṇatva</i>（角性）</td><td>二つの角に共通する普遍</td><td>共通</td></tr>
</tbody></table></div>'''
    s.append(tbl10)
    out.append(("s10", "10", "因果関係の否定 (4)：一つのものとの結合", "k.10 / SPV 20,3–7", "二性などとの結合なら左右の角も因果に", "".join(s)))

    return out
