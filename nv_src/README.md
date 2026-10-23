# NV 対訳の省略の補完

ヴァールッティカ対訳（`nv/`）の原文・和訳には「……」で略した箇所があった。
Thakur 版の OCR（`NVdevAll.txt`）から欠けた原文を補い、和訳を加えて完訳にする。

- `orig/` … 補完前の対訳ページ（vidhiviveka リポジトリの claude/confident-hopper-7ii23g より）
- `NVdevAll.txt` … Thakur 版『Nyāyabhāṣyavārttika』の OCR（同ブランチの sources/ より）
- `clean.py` … OCR から柱・脚注・行番号を除き、刊本の頁 `[p. N]` を付けた `NV_clean.txt` を作る
  （p.224 は OCR が空白で、欠けている）
- `gaps.py` … 対訳ページの「……」を OCR 本文の中で特定する（`--stat` で一覧）
- `mkfill.py NN` … ページ NN の補完ファイル `fill/NN.txt`（OCR の原文 S）の下書きを作る
- `fill/NN.j.txt` … 訳者が書く分。`@ 欄 番号` のあとに
  `F 誤り<TAB>正`（原文の訂正、R はすべての箇所）、`A`/`B`（後ろ・前に補う）、`J 和訳`
- `apply.py` … `orig/` に補完を当てて `pages/` に書く
- その後 `python3 xref/nv_inject.py nv_src/pages` で `nv/` を作り直す

S が「=」の項目は、刊本そのものがスートラなどを冒頭と末尾だけで示している箇所なので補わない。
