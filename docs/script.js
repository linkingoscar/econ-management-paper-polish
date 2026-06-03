(function () {
  'use strict';

  var STORAGE_KEY = 'emp-lang';
  var currentLang = localStorage.getItem(STORAGE_KEY) || 'zh';

  function applyLang(lang) {
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);

    // Update HTML lang attribute
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';

    // Toggle button text
    var btn = document.getElementById('lang-toggle');
    if (btn) {
      btn.textContent = lang === 'zh' ? 'EN' : '中文';
    }

    // Update all elements with data-en / data-zh attributes
    var elements = document.querySelectorAll('[data-en][data-zh]');
    for (var i = 0; i < elements.length; i++) {
      var el = elements[i];
      var text = el.getAttribute('data-' + lang);
      if (text !== null) {
        el.textContent = text;
      }
    }

    // Usage cards: in zh mode show both (en italic), in en mode show en only
    var zhEls = document.querySelectorAll('.usage-zh');
    var enEls = document.querySelectorAll('.usage-en');

    for (var j = 0; j < zhEls.length; j++) {
      zhEls[j].style.display = lang === 'zh' ? 'block' : 'none';
    }
    for (var k = 0; k < enEls.length; k++) {
      if (lang === 'zh') {
        enEls[k].style.display = 'block';
        enEls[k].style.fontStyle = 'italic';
        enEls[k].style.color = '#888';
      } else {
        enEls[k].style.display = 'block';
        enEls[k].style.fontStyle = 'normal';
        enEls[k].style.color = '#555';
      }
    }
  }

  window.toggleLang = function () {
    var next = currentLang === 'zh' ? 'en' : 'zh';
    applyLang(next);
  };

  // Apply on load
  applyLang(currentLang);
})();
