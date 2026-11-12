// Raghuvaṃśa bilingual pages: Devanagari / IAST toggle and notes toggle.
(function () {
  var root = document.documentElement;
  function load(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function save(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }

  function sync() {
    var script = root.getAttribute('data-script') === 'iast' ? 'iast' : 'dev';
    var notes = root.getAttribute('data-notes') === 'hide' ? 'hide' : 'show';
    document.querySelectorAll('[data-script-btn]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-script-btn') === script));
    });
    document.querySelectorAll('[data-notes-btn]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-notes-btn') === notes));
    });
  }

  function setScript(val) {
    if (val === 'iast') root.setAttribute('data-script', 'iast');
    else root.removeAttribute('data-script');
    save('rv-script', val);
    try {
      var url = new URL(location.href);
      if (url.searchParams.has('script')) {
        url.searchParams.set('script', val);
        history.replaceState(null, '', url);
      }
    } catch (e) {}
    sync();
  }

  function setNotes(val) {
    if (val === 'hide') root.setAttribute('data-notes', 'hide');
    else root.removeAttribute('data-notes');
    save('rv-notes', val);
    sync();
  }

  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-script-btn],[data-notes-btn]');
    if (!b) return;
    // keep the verse in view while the layout changes
    var anchor = null;
    var verses = document.querySelectorAll('.verse');
    for (var i = 0; i < verses.length; i++) {
      if (verses[i].getBoundingClientRect().bottom > 80) { anchor = verses[i]; break; }
    }
    var before = anchor ? anchor.getBoundingClientRect().top : 0;
    if (b.hasAttribute('data-script-btn')) setScript(b.getAttribute('data-script-btn'));
    else setNotes(b.getAttribute('data-notes-btn'));
    if (anchor) window.scrollBy(0, anchor.getBoundingClientRect().top - before);
  });

  sync();
})();
