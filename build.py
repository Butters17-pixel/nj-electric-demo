#!/usr/bin/env python3
"""Build index.html from config.json. Local only: no CDN, no analytics, no form endpoint.
Icons: Lucide (ISC), inner SVG markup inlined below."""
import json, html, re
from pathlib import Path

ROOT = Path(__file__).parent
C = json.loads((ROOT / "config.json").read_text())
e = html.escape
LUCIDE = Path("/tmp/luc2/node_modules/lucide-static/icons")
ICON_CACHE = ROOT / "assets" / "lucide-icons.json"

NEEDED = ["server","plug-zap","lightbulb","zap","battery-charging","plug","map-pin","file-text","message-circle",
          "camera","siren","calendar","shield-check","phone","arrow-right","check","arrow-down"]
if LUCIDE.exists():
    icons = {}
    for n in NEEDED:
        svg = (LUCIDE / f"{n}.svg").read_text()
        icons[n] = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1).strip()
    ICON_CACHE.write_text(json.dumps(icons, indent=1))
ICONS = json.loads(ICON_CACHE.read_text())

def line_icon(n, cls="lico"):
    """Lucide outline variant: no fill, 1.5 stroke."""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>')

def pic(name, alt, cls="", pos=None, eager=False):
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="eager"'
    return (f'<picture><source srcset="assets/img/{name}.webp" type="image/webp">'
            f'<img class="{cls}" src="assets/img/{name}.jpg" alt="{e(alt)}" {load} decoding="async"{style}></picture>')

def bulb():
    return '''<div class="bulb" aria-hidden="true"><div class="bulb-sway"><svg viewBox="0 0 240 560">
  <defs><radialGradient id="gl" cx="50%" cy="62%" r="50%"><stop offset="0" stop-color="#FFB36B" stop-opacity=".55"/><stop offset=".45" stop-color="#F26A1B" stop-opacity=".18"/><stop offset="1" stop-color="#F26A1B" stop-opacity="0"/></radialGradient>
  <linearGradient id="sk" x1="0" x2="1"><stop offset="0" stop-color="#0c0f11"/><stop offset=".45" stop-color="#2a2f33"/><stop offset="1" stop-color="#0b0d0f"/></linearGradient></defs>
  <line x1="120" y1="0" x2="120" y2="196" class="cord"/>
  <rect x="94" y="196" width="52" height="64" rx="7" fill="url(#sk)" class="socket"/>
  <rect x="99" y="260" width="42" height="7" rx="2" class="ring"/><rect x="101" y="269" width="38" height="7" rx="2" class="ring"/>
  <ellipse cx="120" cy="402" rx="74" ry="96" fill="url(#gl)" class="inner"/>
  <path class="glass" d="M102 280 C102 318 54 336 54 404 a66 66 0 0 0 132 0 C186 336 138 318 138 280 Z"/>
  <path class="glass-core" d="M102 280 C102 318 54 336 54 404 a66 66 0 0 0 132 0 C186 336 138 318 138 280 Z"/>
  <path class="filament" d="M110 282 V350 M130 282 V350 M110 350 c0 14 6 18 10 18 s10-4 10-18"/>
  </svg></div></div>'''

name, phone, tel = C["name"], C["phone"], C["tel"]
H, EM = C["hero"], C["emergency"]
SAMPLE = f'<span class="sample">{e(C["sample_label"])}</span>'
def call(cls, label=None):
    return f'<a class="btn {cls}" href="tel:{tel}">{line_icon("phone")}<span>{e(label or "Call " + phone)}</span></a>'

h1 = "<br>".join(e(l).replace(e(H["h1_highlight"]), f'<em class="hl">{e(H["h1_highlight"])}</em>') for l in H["h1"])
trust = "".join(f'<li>{line_icon(t["icon"])}<span>{e(t["label"])}</span></li>' for t in C["trust"])
svc = "".join(f'<li class="svc"><span class="svc-ico">{line_icon(s["icon"])}</span><span class="svc-name">{e(s["name"])}</span></li>' for s in C["services"])
chips = "".join(f'<li>{line_icon("check")}{e(c)}</li>' for c in EM["chips"])
projects = "".join(f'<figure class="proj">{pic(p["img"], p["caption"] + " (sample image)", pos=p["pos"])}<figcaption><span>{e(p["caption"])}</span><b>Sample</b></figcaption></figure>' for p in C["projects"])
steps = "".join(f'<li class="step"><div class="step-top"><span class="num">0{i+1}</span>{line_icon(s["icon"])}</div><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></li>' for i, s in enumerate(C["steps"]))
reviews = "".join(f'<figure class="review"><span class="tag">Sample</span><span class="qmark" aria-hidden="true">“</span><blockquote>{e(r["quote"])}</blockquote><figcaption>{e(r["name"])} · {e(r["town"])}</figcaption></figure>' for r in C["reviews"])
towns = "".join(f'<li{" class=\"home\"" if t == C["home_town"] else ""}>{line_icon("check")}{e(t)}</li>' for t in C["towns"])
opts_town = "".join(f"<option>{e(t)}</option>" for t in C["towns"]) + "<option>Other town</option>"
opts_svc = "".join(f"<option>{e(s['name'])}</option>" for s in C["services"]) + "<option>Something else</option>"
logo = f'<a class="logo" href="#top" aria-label="{e(name)} demo home"><span class="logo-mark">{line_icon("zap")}</span><span class="logo-txt"><b>Brightwire</b><small>{e(C["tagline"])}</small></span></a>'

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(name)} (Demo) · Jersey Shore electrician design sample</title>
<meta name="description" content="Design sample for a fictional NJ electrical contractor. Not a real business.">
<meta name="robots" content="noindex">
<link rel="preload" href="assets/fonts/newsreader-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<aside class="pre-header" aria-label="Demo notice and phone"><div class="demo-ribbon">Design sample · fictional company · nothing on this page is real</div>
<div class="topbar"><div class="wrap"><span class="tb-left">{line_icon("map-pin")}{e(C["county_line"])}</span><a href="tel:{tel}">{line_icon("phone")}Call {e(phone)}</a></div></div></aside>
<header class="site-header"><div class="wrap">
  {logo}
  <nav class="nav" aria-label="Main"><a href="#services">Services</a><a href="#work">Work</a><a href="#towns">Towns</a><a href="#quote">Quote</a></nav>
  {call("btn-outline hdr-call")}
</div></header>

<main id="top">
<section class="hero">
  <div class="hero-bg">{pic(H["image"], "Dark room lit by a warm lamp (generated sample image)", "hero-img", eager=True)}</div>
  <div class="hero-shade"></div>
  <div class="bg-word" aria-hidden="true">{e(H["bg_word"])}</div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{e(H["eyebrow"])}</p>
      <h1>{h1}</h1>
      <p class="lede">{e(H["lede"])}</p>
      <div class="hero-ctas">{call("btn-primary btn-lg")}<a class="btn btn-ghost btn-lg" href="#quote">{e(H["cta"])}{line_icon("arrow-down")}</a></div>
      <ul class="trust">{trust}</ul>
    </div>
    {bulb()}
  </div>
  <p class="side-word" aria-hidden="true">Brightwire · Demo</p>
</section>

<section class="quote-sec"><div class="wrap">
  <form class="quote" id="quote-form">
    <div class="quote-head" id="quote"><h2>Quick quote</h2><span class="sample">Demo form</span></div>
    <div class="fields">
      <label>Name<input name="name" autocomplete="off" placeholder="Your name" required></label>
      <label>Phone<input name="phone" type="tel" autocomplete="off" placeholder="(732) 555-0100" required></label>
      <label>Town<select name="town">{opts_town}</select></label>
      <label>Need<select name="need">{opts_svc}</select></label>
      <button class="btn btn-primary" type="submit"><span>Request a quote</span>{line_icon("arrow-right")}</button>
    </div>
    <p class="micro">Demo form. Nothing is sent.</p>
  </form>
  <div class="quote done" id="form-status" hidden tabindex="-1"></div>
</div></section>

<section class="services" id="services"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">What we do</p><h2>Every outlet to the panel</h2></div></div>
  <ul class="svc-row">{svc}</ul>
</div></section>

<section class="em-sec"><div class="wrap"><div class="emergency">
  <span class="siren">{line_icon("siren")}</span>
  <div class="em-copy"><p class="eyebrow hot">{e(EM["eyebrow"])}</p><h2>{e(EM["h2"])}</h2><p>{e(EM["note"])}</p></div>
  <div class="em-act">{call("btn-primary btn-lg")}<ul class="chips">{chips}</ul></div>
</div></div></section>

<section class="work" id="work"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Recent work</p><h2>Lit, wired, finished</h2></div><div class="sec-note">{SAMPLE}<span>Sample images. Real job photos go here.</span></div></div>
  <div class="proj-row">{projects}</div>
</div></section>

<section class="how"><div class="how-bg">{pic("warm-outlet", "Electrician wiring an outlet (generated sample image)")}</div><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">How it works</p><h2>Four easy steps</h2></div></div>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="reviews"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Reviews</p><h2>Neighbors, lit up</h2></div><div class="sec-note">{SAMPLE}<span>Sample reviews. Real reviews go here.</span></div></div>
  <div class="review-row">{reviews}</div>
</div></section>

<section class="towns" id="towns"><div class="wrap towns-grid">
  <div><p class="eyebrow">Towns served</p><h2>Down the Shore</h2><p class="muted">Not on the list? Call and ask.</p>{call("btn-outline", "Call to check your town")}</div>
  <ul class="town-list">{towns}</ul>
</div></section>
</main>

<footer class="footer"><div class="wrap foot">
  <div>{logo}</div>
  <nav class="foot-links" aria-label="Footer"><a href="#services">Services</a><a href="#work">Work</a><a href="#towns">Towns</a><a href="#quote">Quote</a></nav>
  <div class="foot-contact"><a href="tel:{tel}">{e(phone)}</a><span>{e(C["county_line"])}</span></div>
  <p class="foot-note">{e(C["footer_note"])}</p>
</div></footer>

<nav class="callbar" aria-label="Quick contact">{call("cb-call")}<a class="cb-quote" href="#quote">Quote</a></nav>
<script src="app.js"></script>
</body>
</html>
'''
(ROOT / "index.html").write_text(page)
print("built index.html", len(page), "bytes")
