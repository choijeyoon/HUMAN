(() => {
  'use strict';

  const config = window.HUMAN_ANALYTICS || {};
  const params = new URLSearchParams(window.location.search);
  const article = document.body.dataset.article || '';
  const debug = config.debug === true || params.get('debug_analytics') === '1';
  const seenImpressions = new Set();
  const seenScroll = new Set();
  let maxScroll = 0;
  let activeSeconds = 0;
  let ticking = false;

  const safeSessionId = () => {
    try {
      const key = 'human_experiment_session';
      let id = sessionStorage.getItem(key);
      if (!id) {
        id = (window.crypto && crypto.randomUUID)
          ? crypto.randomUUID()
          : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
        sessionStorage.setItem(key, id);
      }
      return id;
    } catch (_) {
      return 'unavailable';
    }
  };

  const referrerHost = (() => {
    if (!document.referrer) return '';
    try { return new URL(document.referrer).hostname; } catch (_) { return ''; }
  })();

  const context = {
    experiment: 'topic-demand-v1',
    experiment_session_id: safeSessionId(),
    path: window.location.pathname,
    page_title: document.title,
    article: article || undefined,
    utm_source: params.get('utm_source') || undefined,
    utm_medium: params.get('utm_medium') || undefined,
    utm_campaign: params.get('utm_campaign') || undefined,
    utm_content: params.get('utm_content') || undefined,
    utm_term: params.get('utm_term') || undefined,
    referrer_host: referrerHost || undefined,
  };

  const compact = (obj) => Object.fromEntries(
    Object.entries(obj).filter(([, value]) => value !== undefined && value !== null && value !== '')
  );

  const loadGA4 = () => {
    const id = config.measurementId;
    if (!id || window.__humanGa4Ready) return;
    window.__humanGa4Ready = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id, { send_page_view: false, anonymize_ip: true });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(id)}`;
    document.head.appendChild(script);
  };

  const loadPlausible = () => {
    const domain = config.plausibleDomain;
    if (!domain || window.__humanPlausibleReady) return;
    window.__humanPlausibleReady = true;
    window.plausible = window.plausible || function plausible(){
      (window.plausible.q = window.plausible.q || []).push(arguments);
    };
    const script = document.createElement('script');
    script.defer = true;
    script.dataset.domain = domain;
    script.src = config.plausibleScript || 'https://plausible.io/js/script.js';
    document.head.appendChild(script);
  };

  const sendEndpoint = (payload) => {
    if (!config.endpoint) return;
    const body = JSON.stringify(payload);
    try {
      if (navigator.sendBeacon) {
        const blob = new Blob([body], { type: 'application/json' });
        if (navigator.sendBeacon(config.endpoint, blob)) return;
      }
    } catch (_) {}
    fetch(config.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
      mode: config.endpointMode || 'cors',
    }).catch(() => {});
  };

  const forward = (payload) => {
    if (config.measurementId) {
      loadGA4();
      window.gtag('event', payload.event, compact({
        ...payload,
        event: undefined,
        debug_mode: debug || undefined,
      }));
    }
    if (config.plausibleDomain) {
      loadPlausible();
      window.plausible(payload.event, { props: compact({ ...payload, event: undefined }) });
    }
    sendEndpoint(payload);
  };

  const emit = (name, detail = {}) => {
    const payload = compact({ event: name, ...context, ...detail });
    window.dispatchEvent(new CustomEvent('human:track', { detail: payload }));
    forward(payload);
    if (debug) console.info('[HUMAN analytics]', JSON.stringify(payload));
  };

  const targetArticleId = (href) => {
    if (!href) return '';
    let pathname;
    try { pathname = new URL(href, window.location.href).pathname; } catch (_) { return ''; }
    if (pathname.includes('/idol-dating-betrayal/')) return 'feature-001';
    if (pathname.includes('/ai-love/')) return 'feature-002';
    if (pathname.includes('/scrolling/')) return 'feature-003';
    return '';
  };

  document.addEventListener('click', (event) => {
    const target = event.target.closest('a, [data-track]');
    if (!target) return;

    if (target.dataset && target.dataset.track) {
      emit('select_feature', {
        id: target.dataset.track,
        target_path: target.getAttribute('href') || undefined,
      });
      return;
    }

    if (article && target.matches('a[href]')) {
      const destination = targetArticleId(target.getAttribute('href'));
      if (destination && destination !== article) {
        emit('select_related_article', {
          from_id: article,
          to_id: destination,
          target_path: target.getAttribute('href'),
        });
      }
    }
  });

  const cards = Array.from(document.querySelectorAll('[data-track^="feature-"]'));
  if (cards.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const id = entry.target.dataset.track;
        if (!entry.isIntersecting || entry.intersectionRatio < 0.5 || seenImpressions.has(id)) return;
        seenImpressions.add(id);
        emit('feature_impression', { id });
        observer.unobserve(entry.target);
      });
    }, { threshold: [0.5] });
    cards.forEach((card) => observer.observe(card));
  }

  const updateScroll = () => {
    ticking = false;
    if (!article) return;
    const scrollable = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    const percent = Math.min(100, Math.round((window.scrollY / scrollable) * 100));
    maxScroll = Math.max(maxScroll, percent);
    [25, 50, 75, 90].forEach((threshold) => {
      if (percent >= threshold && !seenScroll.has(threshold)) {
        seenScroll.add(threshold);
        emit('scroll_depth', { id: article, percent: threshold });
        if (threshold === 90) emit('article_complete', { id: article });
      }
    });
  };

  if (article) {
    window.addEventListener('scroll', () => {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(updateScroll);
      }
    }, { passive: true });

    window.setInterval(() => {
      if (document.visibilityState !== 'visible') return;
      activeSeconds += 1;
      if (activeSeconds === 30 || activeSeconds === 60) {
        emit('engaged_read', { id: article, seconds: activeSeconds, max_scroll: maxScroll });
      }
    }, 1000);

    window.addEventListener('pagehide', () => {
      emit('article_exit', { id: article, active_seconds: activeSeconds, max_scroll: maxScroll });
    });
  }

  emit('view_page');
  if (article) {
    emit('view_article', { id: article });
    updateScroll();
  }
})();
