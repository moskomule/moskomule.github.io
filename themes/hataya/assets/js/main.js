(function () {
  'use strict';

  // ---- Publication filter tabs ----
  document.querySelectorAll('.pubs').forEach(function (root) {
    var buttons = root.querySelectorAll('.pubs__tabs button');
    if (!buttons.length) return;
    root.classList.add('js-ready');

    function apply(filter) {
      buttons.forEach(function (b) {
        b.setAttribute('aria-pressed', String(b.dataset.filter === filter));
      });
      var visibleYears = {};
      root.querySelectorAll('.pub').forEach(function (li) {
        var show = filter === 'all' ||
          (filter === 'selected' ? li.dataset.selected === 'true' : li.dataset.category === filter);
        li.classList.toggle('is-hidden', !show);
        if (show) visibleYears[li.dataset.year] = true;
      });
      root.querySelectorAll('.pubs__year').forEach(function (y) {
        y.classList.toggle('is-hidden', !visibleYears[y.textContent.trim()]);
      });
    }

    buttons.forEach(function (b) {
      b.addEventListener('click', function () { apply(b.dataset.filter); });
    });
    apply(root.dataset.filter || 'all');
  });

  // ---- Copy BibTeX ----
  document.querySelectorAll('.pub__bibbox .copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.parentElement.querySelector('code');
      if (!code || !navigator.clipboard) return;
      var label = btn.textContent;
      navigator.clipboard.writeText(code.textContent).then(function () {
        btn.textContent = btn.dataset.copied || 'Copied';
        setTimeout(function () { btn.textContent = label; }, 1500);
      });
    });
  });

  // ---- Highlight the current section in the home tabs ----
  var tabs = document.querySelectorAll('.tabs a[href^="#"]');
  if (tabs.length && 'IntersectionObserver' in window) {
    var byId = {};
    tabs.forEach(function (a) { byId[decodeURIComponent(a.getAttribute('href').slice(1))] = a; });
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && byId[e.target.id]) {
          if (current) current.classList.remove('is-active');
          current = byId[e.target.id];
          current.classList.add('is-active');
          if (current.scrollIntoView && current.parentElement.scrollWidth > current.parentElement.clientWidth) {
            current.parentElement.scrollTo({ left: current.offsetLeft - 24, behavior: 'smooth' });
          }
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }
})();
