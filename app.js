// Local-only. No fetch, XHR, storage, analytics, or third-party requests.
(function () {
  const form = document.getElementById('quote-form');
  const status = document.getElementById('form-status');
  if (!form || !status) return;
  // Keep a focused field clear of the fixed mobile call bar.
  const bar = document.querySelector('.callbar');
  form.addEventListener('focusin', function (event) {
    if (!bar || getComputedStyle(bar).display === 'none') return;
    const r = event.target.getBoundingClientRect();
    const limit = bar.getBoundingClientRect().top - 16;
    if (r.bottom > limit) window.scrollBy({ top: r.bottom - limit, behavior: 'auto' });
    else if (r.top < 80) window.scrollBy({ top: r.top - 80, behavior: 'auto' });
  });
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    form.hidden = true;
    status.hidden = false;
    status.innerHTML = '<span class="done-ico">✓</span><h2>Thanks!</h2><p>This is a design sample. Nothing was sent.</p>';
    status.focus();
  });
})();

// Scroll reveal: fade/rise sections in once. After the reveal the class is
// removed so each element's own hover transitions work normally again.
(function () {
  const els = document.querySelectorAll('.rv');
  const show = (el) => {
    el.classList.add('in');
    setTimeout(() => { el.classList.remove("rv", "in"); el.style.transitionDelay = ""; }, 1600);
  };
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach((el) => el.classList.remove('rv'));
    return;
  }
  const io = new IntersectionObserver((entries) => entries.forEach((en) => {
    if (!en.isIntersecting) return;
    const el = en.target;
    // stagger siblings in the same row
    const sibs = [...el.parentElement.children].filter((c) => c.classList.contains('rv'));
    el.style.transitionDelay = Math.min(sibs.indexOf(el), 5) * 90 + 'ms';
    show(el);
    io.unobserve(el);
  }), { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  els.forEach((el) => io.observe(el));
})();
