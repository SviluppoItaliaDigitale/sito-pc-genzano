/* Galleria auto: trova <p><img></p> consecutivi nel corpo articolo e li
   marca con classe .is-galleria-pair così CSS può affiancarli.
   Fallback per browser senza supporto :has() (Safari ≤15.3, FF <121,
   IE 11). Sui browser moderni :has() fa già il lavoro, questo script è
   ridondante ma innocuo (la classe viene applicata, nessun layout shift).

   Idempotente: chiamabile più volte, non duplica la classe. */
(function () {
  'use strict';

  function isParaWithLoneImg(node) {
    if (!node || node.nodeType !== 1 || node.tagName !== 'P') return false;
    var imgs = node.querySelectorAll('img');
    if (imgs.length !== 1) return false;
    // Accettiamo p contenenti solo <img> (eventualmente con <a> wrapper o <em>)
    var text = (node.textContent || '').trim();
    return text === '';
  }

  function processArticle(article) {
    if (!article) return;
    var paras = article.querySelectorAll(':scope > p');
    var pairing = false;
    for (var i = 0; i < paras.length; i++) {
      var cur = paras[i];
      var next = paras[i + 1];
      if (isParaWithLoneImg(cur) && isParaWithLoneImg(next)) {
        cur.classList.add('is-galleria-pair');
        next.classList.add('is-galleria-pair');
        pairing = true;
      } else if (pairing) {
        pairing = false;
      }
    }
  }

  function init() {
    document.querySelectorAll('article.article-body, article:not(.card)').forEach(processArticle);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
