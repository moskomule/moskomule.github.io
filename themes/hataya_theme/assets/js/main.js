// Publication filter buttons (see _shortcodes/publications.html).
for (const root of document.querySelectorAll('.pubs')) {
  const buttons = root.querySelectorAll('.pubs__filters button');

  const show = (filter) => {
    for (const b of buttons) b.setAttribute('aria-pressed', b.value === filter);
    for (const li of root.querySelectorAll('.pub')) {
      li.hidden = !(filter === 'all' ||
        (filter === 'selected' ? li.hasAttribute('data-selected') : li.dataset.category === filter));
    }
    // hide a year heading when none of its papers is visible
    for (const year of root.querySelectorAll('.pubs__year')) {
      let next = year.nextElementSibling, visible = false;
      while (next && next.classList.contains('pub')) { visible ||= !next.hidden; next = next.nextElementSibling; }
      year.hidden = !visible;
    }
  };

  for (const b of buttons) b.addEventListener('click', () => show(b.value));
  if (buttons.length) show(root.dataset.filter);
}
