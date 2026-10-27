const header = document.querySelector('.bf-site-header');
const button = header?.querySelector('.bf-site-menu-button');
const menu = header?.querySelector('.bf-site-menu');
const programs = header?.querySelector('.bf-site-programs');
document.addEventListener('pointerdown', event => { if (programs && !programs.contains(event.target)) programs.open = false; });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && programs?.open) { programs.open = false; programs.querySelector('summary')?.focus(); } });
programs?.addEventListener('click', event => { if (event.target.closest('a')) programs.open = false; });
if (button && menu) {
  const setOpen = (open, restoreFocus = false) => {
    menu.classList.toggle('is-open', open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    button.innerHTML = open
      ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>'
      : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>';
    if (restoreFocus) button.focus();
  };
  button.addEventListener('click', () => setOpen(!menu.classList.contains('is-open')));
  menu.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.classList.contains('is-open')) setOpen(false, true); });
  document.addEventListener('pointerdown', event => { if (menu.classList.contains('is-open') && !header.contains(event.target)) setOpen(false); });
}
