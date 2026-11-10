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
