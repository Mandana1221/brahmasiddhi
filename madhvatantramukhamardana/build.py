"""parts/ を連結して madhvatantramukhamardana_taiyaku.html を作る。目次ナビは各節の data-nav から生成する。"""
import glob, os, re
D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, 'parts')
read = lambda f: open(os.path.join(P, f), encoding='utf-8').read()
secs = [open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(P, 's*.html')))]
nav = ['<nav class="toc" aria-label="目次">', '  <ol>',
       '    <li><a href="#intro">入口</a></li>', '    <li><a href="#map">全体の地図</a></li>']
for s in secs:
    m = re.search(r'<section id="s(\d+)"[^>]*data-nav="([^"]+)"', s)
    nav.append(f'    <li><a href="#s{m.group(1)}"><b>{m.group(1)}</b>{m.group(2)}</a></li>')
nav += ['    <li><a href="#terms">用語集</a></li>', '  </ol>', '</nav>', '']
out = read('00_head.html') + '\n'.join(nav) + read('01_hero.html') + ''.join(secs) + read('90_terms.html') + read('99_footer.html')
open(os.path.join(os.path.dirname(D), 'madhvatantramukhamardana_taiyaku.html'), 'w', encoding='utf-8').write(out)
print(len(secs), 'sections,', len(out), 'bytes')
