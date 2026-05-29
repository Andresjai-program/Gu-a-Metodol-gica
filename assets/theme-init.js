/**
 * Anti-FOUC: aplica tema antes del primer paint
 */
(function () {
  var k = 'guia-theme';
  var t;
  try {
    t = localStorage.getItem(k);
  } catch (e) {
    t = null;
  }
  var dark =
    t === 'dark' ||
    (t !== 'light' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
})();
