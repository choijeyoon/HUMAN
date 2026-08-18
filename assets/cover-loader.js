(() => {
  const media = document.querySelector('[data-cover-media]');
  if (!media) return;

  const load = async () => {
    try {
      const parts = [];
      for (let i = 1; i <= 7; i += 1) {
        const name = String(i).padStart(2, '0');
        const response = await fetch(`assets/cover/chunk-${name}.txt?v=5`, { cache: 'no-store' });
        if (!response.ok) throw new Error(`Cover chunk ${name} returned ${response.status}`);
        parts.push((await response.text()).trim());
      }

      const base64 = parts.join('');
      if (base64.length !== 13976 || !base64.startsWith('/9j/') || !base64.endsWith('/9k=')) {
        throw new Error('Cover payload failed integrity check');
      }

      const image = new Image(360, 240);
      image.alt = 'Editorial composite of a central human portrait, a distant performance crowd and an abstract artificial profile.';
      image.decoding = 'async';
      image.onload = () => media.classList.add('cover-ready');
      image.onerror = () => media.classList.add('cover-error');
      image.src = `data:image/jpeg;base64,${base64}`;
      media.appendChild(image);
    } catch (error) {
      media.classList.add('cover-error');
      console.error('HUMAN cover failed to load:', error);
    }
  };

  load();
})();
