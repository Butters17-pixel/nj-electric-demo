# Brightwire Electric (Demo)

Design sample for a fictional NJ electrical contractor. Nothing on the page is real: the company, phone number, reviews and photos are all samples.

## Editing
- Change text, services, towns, projects and reviews in `config.json`, then run `python3 build.py` to regenerate `index.html`. Don't edit `index.html` by hand; the next build overwrites it.
- Styles are in `styles.css`; the quote form behavior is in `app.js`.
- The quote form is a demo only: it checks the fields, then shows a thank-you message. Nothing is sent or stored.

## Images
Photos live in `assets/img/` as WebP, each in two sizes: `name.webp` (large, for desktop) and `name-sm.webp` (1200px, for phones). `build.py` lists the large widths in `IMG_W`. All photos are generated sample images, upscaled with Real-ESRGAN. See `assets/img/CREDITS.md`.
