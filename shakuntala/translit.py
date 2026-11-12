"""IAST（ローマ字転写）をデーヴァナーガリーに変換する。

サンスクリットとプラークリットの本文用。語末の子音にはヴィラーマ（्）をつけ、
句点「.」はダンダ「।」にする。プラークリットの母音連続を示す ï / ü は
独立母音 इ / उ として書く。
"""
import re
import unicodedata

VOWELS = {  # IAST: (独立形, 母音記号)
    'a': ('अ', ''), 'ā': ('आ', 'ा'), 'i': ('इ', 'ि'), 'ī': ('ई', 'ी'),
    'u': ('उ', 'ु'), 'ū': ('ऊ', 'ू'), 'ṛ': ('ऋ', 'ृ'), 'ṝ': ('ॠ', 'ॄ'),
    'ḷ': ('ऌ', 'ॢ'), 'e': ('ए', 'े'), 'ai': ('ऐ', 'ै'), 'o': ('ओ', 'ो'),
    'au': ('औ', 'ौ'),
    # プラークリットの母音連続（hiatus）。常に独立母音で書く
    'ï': ('इ', None), 'ü': ('उ', None), 'ë': ('ए', None),
}
CONSONANTS = {
    'kh': 'ख', 'gh': 'घ', 'ch': 'छ', 'jh': 'झ', 'ṭh': 'ठ', 'ḍh': 'ढ',
    'th': 'थ', 'dh': 'ध', 'ph': 'फ', 'bh': 'भ',
    'k': 'क', 'g': 'ग', 'ṅ': 'ङ', 'c': 'च', 'j': 'ज', 'ñ': 'ञ',
    'ṭ': 'ट', 'ḍ': 'ड', 'ṇ': 'ण', 't': 'त', 'd': 'द', 'n': 'न',
    'p': 'प', 'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र', 'l': 'ल',
    'ḻ': 'ळ', 'v': 'व', 'ś': 'श', 'ṣ': 'ष', 's': 'स', 'h': 'ह',
}
OTHERS = {'ṃ': 'ं', 'ḥ': 'ः', "'": 'ऽ', '’': 'ऽ', '.': '।'}
VIRAMA = '्'

# 2文字の単位を先に照合する
_UNITS = sorted(list(VOWELS) + list(CONSONANTS), key=len, reverse=True)


def _tokens(word):
    i = 0
    while i < len(word):
        for u in _UNITS:
            if word.startswith(u, i):
                yield ('V' if u in VOWELS else 'C'), u
                i += len(u)
                break
        else:
            yield 'X', word[i]
            i += 1


def to_deva(text):
    """IAST の文字列をデーヴァナーガリーにする。ローマ字以外の文字はそのまま残す。"""
    text = unicodedata.normalize('NFC', text).lower()
    # アヴァグラハは前の語につなげて書く（saṃnihito 'tra → संनिहितोऽत्र）
    text = re.sub(r"\s+(['’])", r'\1', text)
    out = []
    prev = None  # 直前の単位: 'C'（母音を待つ子音）, 'V', ほか
    for kind, u in _tokens(text):
        if kind == 'C':
            if prev == 'C':
                out.append(VIRAMA)
            out.append(CONSONANTS[u])
            prev = 'C'
        elif kind == 'V':
            ind, sign = VOWELS[u]
            if prev == 'C' and sign is not None:
                out.append(sign)
            else:
                if prev == 'C':
                    out.append(VIRAMA)
                out.append(ind)
            prev = 'V'
        else:
            if prev == 'C':
                out.append(VIRAMA)
            out.append(OTHERS.get(u, u))
            prev = 'X'
    if prev == 'C':
        out.append(VIRAMA)
    s = ''.join(out)
    # 「।।」や「। ।」の重複を整える
    s = re.sub(r'।\s*।', '॥', s)
    return s


if __name__ == '__main__':
    tests = [
        "yā sraṣṭuḥ sṛṣṭir ādyā pibati vidhihutaṃ yā havir yā ca hotrī",
        "tataḥ praviśati rathayātakena mṛgānusārī cāpahasto duṣyantaḥ sūtaś ca.",
        "eṣa pratisaṃhṛtaḥ. (yathoktaṃ karoti)",
        "ayaṃ saṃnihito 'tra kulapatiḥ?",
        "halā saüntale, taïtto vi kkhu tādakassavassa",
        "tad aham enām anṛṇāṃ karomi",
        "prathamo 'ṅkaḥ",
    ]
    for t in tests:
        print(t, '\n ', to_deva(t))
