import base64, os, io
from PIL import Image
import sys
sys.path.insert(0, '/home/claude/waendom-site/tools')
import build_site as S
from alt_text import ALT

site = "/home/claude/waendom-site"
css = open(f"{site}/style.css").read()
js = open(f"{site}/script.js").read()

def embed(name, max_w=740, quality=68):
    im = Image.open(f"{site}/images/{name}")
    w, h = im.size
    if w > max_w:
        im = im.resize((max_w, round(h * max_w / w)), Image.LANCZOS)
    buf = io.BytesIO()
    if name.endswith(".png"):
        im.save(buf, "PNG", optimize=True); mime = "png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True); mime = "jpeg"
    return f"data:image/{mime};base64," + base64.b64encode(buf.getvalue()).decode()

MAN_L = embed("man-left.png", 620)
MAN_R = embed("man-right.png", 520)

ALL = sorted({s for _, _, _, _, w in S.CATEGORIES for s in w} | set(S.HOME) | {"portrait"})
IMGS = {s: embed(s + ".jpg") for s in ALL}

def pieces(slugs, label=""):
    return "\n".join(f'''        <figure class="art-piece">
          <img src="{IMGS[s]}" alt="{ALT.get(s, label)}">
        </figure>''' for s in slugs)

def cat_page(pid, title, intro, works):
    return f'''
<div class="page" id="page-{pid}">
  <main><div class="wrap">
    <section class="page-head">
      <h1>{title}</h1><p>{intro}</p>
    </section>
    <section>
      <hr class="gallery-rule">
      <div class="gallery">
{pieces(works, title)}
      </div>
    </section>
  </div></main>
</div>
'''

nav_items = [("home", "home"), ("gallery", "gallery"),
             ("about", "about waendom"), ("contact", "contact")]
nav_links = "\n".join(
    f'    <a href="#" data-go="{pid}">{label}</a>' for pid, label in nav_items)

cards = "\n".join(f'''      <a class="category-card" href="#" data-go="{fname.replace(".html","")}">
        <img src="{IMGS[cover]}" alt="{ALT.get(cover, '')}">
        <span class="label"><span class="name">{name}</span><span class="sub">{sub}</span></span></a>'''
    for fname, name, sub, cover, works in S.CATEGORIES)

about_paras = "\n".join(f"        <p>{t}</p>" for t in S.ABOUT_TEXT)
contact_paras = "\n".join(f"        <p>{t}</p>" for t in S.CONTACT_TEXT)

body = f"""
<a class="wordmark-bar" href="#" aria-label="Zur Startseite">
  <span class="wordmark-text">waendom.com</span>
  <svg class="wordmark-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M15 5l-7 7 7 7"/></svg>
</a>

<button class="menu-toggle" aria-label="Men&uuml; &ouml;ffnen" aria-expanded="false">
  <span></span><span></span><span></span>
</button>

<div class="menu-overlay">
  <span class="eyebrow">menu</span>
  <nav class="overlay-nav" aria-label="Hauptnavigation">
{nav_links}
  </nav>
</div>

<div class="page active" id="page-home">
  <header class="hero">
    <div class="hero-media">
      <img class="figure-left"  src="{MAN_L}" alt="{ALT['man-left']}">
      <img class="figure-right" src="{MAN_R}" alt="{ALT['man-right']}">
    </div>
  </header>
  <main><div class="wrap">
    <section class="intro">
      <h2>welcome!</h2>
      <p>hang around and scroll through my little collection that I've been working on for the past few years, enjoy.</p>
    </section>
    <section class="highlights">
      <div class="highlights-grid">
{pieces(S.HOME)}
      </div>
      <div class="more-row"><button class="more-btn" data-go="gallery">more</button></div>
    </section>
  </div></main>
</div>

<div class="page" id="page-gallery">
  <main><div class="wrap">
    <section class="page-head">
      <h1>gallery</h1>
      <p>Four collections. Pick one to see the individual works.</p>
    </section>
    <section class="category-grid">
{cards}
    </section>
  </div></main>
</div>
{"".join(cat_page(f.replace(".html",""), n, S.INTRO[n], w) for f, n, s, c, w in S.CATEGORIES)}
<div class="page" id="page-about">
  <main><div class="wrap">
    <section class="page-head"><h1>about waendom</h1></section>
    <section class="about">
      <figure class="about-portrait"><img src="{IMGS['portrait']}" alt="{ALT['portrait']}"></figure>
      <div class="about-text">
{about_paras}
        <a class="cta-link" href="#" data-go="contact">get in touch &#8594;</a>
      </div>
    </section>
  </div></main>
</div>

<div class="page" id="page-contact">
  <main><div class="wrap">
    <section class="page-head"><h1>contact</h1></section>
    <section class="contact">
      <div class="contact-text">
{contact_paras}
        <div class="contact-links">
          <a class="contact-btn" href="mailto:contact@waendom.com">{S.ICON_MAIL}<span>contact@waendom.com</span></a>
        </div>
      </div>
    </section>
  </div></main>
</div>

<button class="to-top" aria-label="Nach oben">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<footer class="site-footer"><div class="wrap">
  <span class="copyright">copyright &copy; waendom 2016 &ndash; 2026</span>
</div></footer>
"""

preview_js = """
// mirrors the site's fixed hierarchy: an album goes up to gallery,
// gallery goes up to home — same rule as the real wordmark-bar data-up
var UP = {gallery:"home", digital:"gallery", canvas:"gallery",
          analog:"gallery", sticker:"gallery", about:"home", contact:"home"};
var current = "home";
function go(n){
  current = n;
  document.querySelectorAll(".page").forEach(function(p){p.classList.remove("active");});
  document.getElementById("page-"+n).classList.add("active");
  document.body.classList.remove("menu-open");
  window.scrollTo(0,0);
  document.querySelectorAll(".art-piece").forEach(function(p){p.classList.add("in-view");});
  window.dispatchEvent(new Event("scroll"));
}
document.addEventListener("click",function(e){
  var bar = e.target.closest(".wordmark-bar");
  if(bar){
    e.preventDefault();e.stopPropagation();
    if(document.body.classList.contains("is-scrolled")){ go(UP[current] || "home"); }
    else { go("home"); }
    return;
  }
  var el=e.target.closest("[data-go]");
  if(el){e.preventDefault();e.stopPropagation();go(el.dataset.go);}
}, true);
"""

extra_css = """
.page{display:none}
.page.active{display:block}
.more-btn{font-family:var(--font-mono);cursor:pointer;background:none}
"""

html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Waendom.com &mdash; Vorschau</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{css}
{extra_css}
</style>
</head>
<body>
{body}
<script>
{js}
</script>
<script>
{preview_js}
</script>
</body>
</html>
"""

out = "/home/claude/waendom-preview.html"
open(out, "w").write(html)
print(f"Vorschau: {os.path.getsize(out)/1024/1024:.1f} MB")
