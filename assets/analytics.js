(() => {
  const emit = (name, detail = {}) => {
    window.dispatchEvent(new CustomEvent('human:track', {
      detail: {
        event: name,
        path: window.location.pathname,
        ...detail,
      },
    }));
  };

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-track]');
    if (!target) return;
    emit('select_feature', { id: target.dataset.track });
  });

  const article = document.body.dataset.article;
  if (article) emit('view_article', { id: article });

  // Intentionally no network request here. A future analytics provider can
  // subscribe to `human:track` without changing page markup or event names.
})();
