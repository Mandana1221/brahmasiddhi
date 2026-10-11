# アートマタットヴァ・ヴィヴェーカ 対訳と解説

`atmatattvaviveka_zenyaku.html` は、このフォルダの原稿から生成する。HTML を直接編集しない。

- `outline.txt`：科段（Chowkhamba 版の目次にもとづく）
- `text/*.txt`：対訳とノート（`@node 番号` ごと。書き方は `tools/build_atv.py` の冒頭を参照）
- `intro.html`, `template_*.html`：見出し・読み方・スタイル（『クスマーンジャリ全訳』と同じ）

生成：`python3 tools/build_atv.py`

本文の底本は Chowkhamba Sanskrit Series 版（1940）の OCR（`texts/ATV_p249-254補完版.txt`）。読みは Asiatic Society 版（Bibliotheca Indica 170）と照合する。
