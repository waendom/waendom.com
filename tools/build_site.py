import os, json
from alt_text import ALT

SITE = "/home/claude/waendom-site"
DIMS = json.load(open("/home/claude/image_dims.json"))

def img_tag(slug, prefix, cls="", eager=False):
    """An <img> with its real dimensions (so the layout never jumps while
    loading), a proper description, and a pointer to the full-size file
    the lightbox loads on demand."""
    w, h = DIMS.get(slug, (0, 0))
    ext = "png" if slug.startswith("man-") else "jpg"
    size = f' width="{w}" height="{h}"' if w else ""
    klass = f' class="{cls}"' if cls else ""
    loading = "eager" if eager else "lazy"
    # only pieces that open in the lightbox need a full-size counterpart
    no_full = slug.startswith("man-") or slug.startswith("favicon") or slug == "portrait"
    full = "" if no_full else f' data-full="{prefix}images/full/{slug}.jpg"'
    alt = ALT.get(slug, "")
    return (f'<img{klass} src="{prefix}images/{slug}.{ext}"{full} '
            f'alt="{alt}"{size} loading="{loading}" decoding="async">')

# ---------------------------------------------------------------- content ----

DIGITAL = ["antoinette", "mary-cooper", "coated", "astronaut", "die-ruderer",
           "rouven", "flat-cap", "blue", "greyscale", "sunbleached", "cap"]

CANVAS = ["heisenberg", "canvas-01", "canvas-02", "canvas-03",
          "canvas-04", "canvas-05", "canvas-07", "canvas-08"]

ANALOG = ["analog-01", "analog-02", "analog-03", "analog-04",
          "analog-05", "analog-06", "analog-07", "analog-08"]

STICKER = ["sticker-stapel", "sticker-alpenrod", "sticker-bergstation",
           "sticker-laptop", "sticker-dschungel", "sticker-backstein",
           "sticker-stahl"]

HOME = ["mary-cooper", "canvas-05", "cap", "analog-03", "sticker-backstein"]

# file, name, subtitle, cover, works — order as shown on the gallery page
CATEGORIES = [
    ("digital.html", "digital", "illustration", "die-ruderer",       DIGITAL),
    ("canvas.html",  "canvas",  "traditional",  "canvas-03",         CANVAS),
    ("analog.html",  "analog",  "photography",  "analog-01",         ANALOG),
    ("sticker.html", "sticker", "in the wild",  "sticker-alpenrod",  STICKER),
]

INTRO = {
    "digital": "Digitally painted portraits, illustrations and studies.",
    "canvas":  "On canvas and paper &mdash; charcoal, pastel, oil.",
    "analog":  "Shot on film. Grain, light leaks and all.",
    "sticker": "Where the work ended up. Lampposts, lifts, laptops.",
}

ABOUT_TEXT = [
    "hang around and take a moment to scroll through this visual archive — a "
    "collection of photography and creative work I&rsquo;ve been building over "
    "the past few years.",
    "It&rsquo;s all about capturing mood, texture and light: finding art in the "
    "details that usually pass us by. No rush, no hype. Just explore at your own "
    "pace and enjoy.",
]

CONTACT_TEXT = [
    "If you like my work, want some stickers, or have an inquiry &mdash; hit me up.",
    "I read everything and answer as soon as I can.",
]

ICON_MAIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.6"><rect x="3" y="5" width="18" height="14" rx="2"/>'
             '<path d="m4 7 8 6 8-6"/></svg>')
# ----------------------------------------------------------------- shared ----

SITE_URL = "https://waendom.com"
DEFAULT_DESC = "A visual archive of photography, illustration and painted work."

def head(title, prefix, description=DEFAULT_DESC, og_image="images/cap.jpg"):
    css_path = f"{prefix}style.css"
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">

<link rel="icon" type="image/png" sizes="32x32" href="{prefix}images/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}images/favicon-180.png">

<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_URL}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:image" content="{SITE_URL}/{og_image}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_path}">
</head>
<body>
"""

def chrome(prefix, current="", up=None):
    """Wordmark bar, menu button and overlay menu — identical on every page.
    `up` is the fixed, hierarchical target for the collapsed back-arrow:
    an album goes up to the gallery, the gallery goes up to home, and so on.
    It never depends on browser history, so it's the same every time."""
    items = [("index.html", "home"), ("gallery/index.html", "gallery"),
             ("about.html", "about waendom"), ("contact.html", "contact")]
    links = []
    for href, label in items:
        cur = ' aria-current="page"' if label == current else ""
        links.append(f'    <a href="{prefix}{href}"{cur}>{label}</a>')
    up_attr = f' data-up="{up}"' if up else ""
    return f"""<a class="wordmark-bar" href="{prefix}index.html"{up_attr} aria-label="Zur Startseite">
  <span class="wordmark-text">waendom.com</span>
  <svg class="wordmark-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
</a>

<button class="menu-toggle" aria-label="Menü öffnen" aria-expanded="false">
  <span></span><span></span><span></span>
</button>

<div class="menu-overlay">
  <span class="eyebrow">menu</span>
  <nav class="overlay-nav" aria-label="Hauptnavigation">
{chr(10).join(links)}
  </nav>
</div>"""

def footer(js_path):
    return f"""
<button class="to-top" aria-label="Nach oben">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<footer class="site-footer">
  <div class="wrap">
    <span class="copyright">copyright &copy; waendom 2016 &ndash; 2026</span>
  </div>
</footer>

<script src="{js_path}"></script>
</body>
</html>
"""

def piece(slug, prefix, category=""):
    return f"""        <figure class="art-piece">
          {img_tag(slug, prefix)}
        </figure>"""

# ------------------------------------------------------------------ pages ----

def build_home():
    cards = "\n".join(
        f'''        <figure class="art-piece">
          {img_tag(s, "")}
        </figure>''' for s in HOME)
    body = head("waendom.com", "") + "\n" + chrome("", "home") + f"""

<header class="hero">
  <div class="hero-media">
    {img_tag("man-left", "", cls="figure-left", eager=True)}
    {img_tag("man-right", "", cls="figure-right", eager=True)}
  </div>
</header>

<main>
  <div class="wrap">

    <section class="intro">
      <h2>welcome!</h2>
      <p>hang around and scroll through my little collection that I've been working on for the past few years, enjoy.</p>
    </section>

    <section class="highlights">
      <div class="highlights-grid">
{cards}
      </div>
      <div class="more-row">
        <a class="more-btn" href="gallery/index.html">more</a>
      </div>
    </section>

  </div>
</main>
""" + footer("script.js")
    open(f"{SITE}/index.html", "w").write(body)
    print("index.html")

def build_about():
    paras = "\n".join(f"        <p>{t}</p>" for t in ABOUT_TEXT)
    body = head("about waendom — waendom.com", "", "The person behind waendom — a short introduction.") + "\n" + chrome("", "about waendom", up="index.html") + f"""

<main>
  <div class="wrap">
    <section class="page-head">
      <h1>about waendom</h1>
    </section>

    <section class="about">
      <figure class="about-portrait">
{img_tag("portrait", "")}
      </figure>
      <div class="about-text">
{paras}
        <a class="cta-link" href="contact.html">get in touch &#8594;</a>
      </div>
    </section>
  </div>
</main>
""" + footer("script.js")
    open(f"{SITE}/about.html", "w").write(body)
    print("about.html")

def build_contact():
    paras = "\n".join(f"        <p>{t}</p>" for t in CONTACT_TEXT)
    body = head("contact — waendom.com", "", "Get in touch about commissions, stickers or anything else.") + "\n" + chrome("", "contact", up="index.html") + f"""

<main>
  <div class="wrap">
    <section class="page-head">
      <h1>contact</h1>
    </section>

    <section class="contact">
      <div class="contact-text">
{paras}
        <div class="contact-links">
          <a class="contact-btn" href="mailto:contact@waendom.com">
            {ICON_MAIL}
            <span>contact@waendom.com</span>
          </a>
        </div>
      </div>
    </section>
  </div>
</main>
""" + footer("script.js")
    open(f"{SITE}/contact.html", "w").write(body)
    print("contact.html")

# a closing line for albums that need one — the sticker album is the only
# place where a visitor might actually want something, so it gets a way to ask
OUTRO = {
    "sticker": '<p class="album-outro">want some for your own lamppost? '
               '<a href="../contact.html">hit me up</a>.</p>',
}

def build_category(fname, title, works):
    if works:
        inner = f'''      <hr class="gallery-rule">
      <div class="gallery">
{chr(10).join(piece(s, "../", title) for s in works)}
      </div>'''
    else:
        inner = '      <p class="empty-note">nothing here yet.</p>'
    outro = f"\n    {OUTRO[title]}" if title in OUTRO else ""
    body = head(f"{title} — waendom.com", "../", INTRO[title]) + "\n" + chrome("../", "gallery", up="index.html") + f"""

<main>
  <div class="wrap">
    <section class="page-head">
      <h1>{title}</h1>
      <p>{INTRO[title]}</p>
    </section>

    <section>
{inner}
    </section>{outro}
  </div>
</main>
""" + footer("../script.js")
    open(f"{SITE}/gallery/{fname}", "w").write(body)
    print(f"gallery/{fname} ({len(works)} Bilder)")

def build_gallery_landing():
    cards = []
    for fname, name, sub, cover, works in CATEGORIES:
        cards.append(f"""      <a class="category-card" href="{fname}">
        {img_tag(cover, "../")}
        <span class="label">
          <span class="name">{name}</span>
          <span class="sub">{sub}</span>
        </span>
      </a>""")
    body = head("gallery — waendom.com", "../", "Four collections. Pick one to see the individual works.") + "\n" + chrome("../", "gallery", up="../index.html") + f"""

<main>
  <div class="wrap">
    <section class="page-head">
      <h1>gallery</h1>
      <p>Four collections. Pick one to see the individual works.</p>
    </section>

    <section class="category-grid">
{chr(10).join(cards)}
    </section>
  </div>
</main>
""" + footer("../script.js")
    open(f"{SITE}/gallery/index.html", "w").write(body)
    print("gallery/index.html")

def build_404():
    """GitHub Pages serves this file for any missing path, at any depth — so it
    can't use relative links. The tiny script works out the site root itself,
    which keeps it correct both on a project page (/repo/) and on a custom
    domain (/)."""
    body = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>not found — waendom.com</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400&family=Work+Sans:wght@400&display=swap" rel="stylesheet">
<style>
  :root {{ --cream:#f8f4ea; --ink:#24221d; --ink-soft:#79746a; }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; min-height:100vh; background:var(--cream); color:var(--ink);
    font-family:"Work Sans",-apple-system,sans-serif;
    display:flex; flex-direction:column; align-items:center;
    justify-content:center; text-align:center; padding:40px 28px; gap:22px;
  }}
  h1 {{
    font-family:"Space Mono",monospace; font-weight:400; text-transform:lowercase;
    font-size:clamp(1.6rem,5vw,2.2rem); letter-spacing:.02em; margin:0;
  }}
  p {{ margin:0; color:var(--ink-soft); max-width:38ch; line-height:1.6; }}
  .links {{ display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin-top:10px; }}
  a.btn {{
    font-family:"Space Mono",monospace; text-transform:lowercase;
    font-size:.78rem; letter-spacing:.16em; text-decoration:none; color:var(--ink);
    padding:14px 30px; border:1px solid var(--ink); border-radius:999px;
    transition:background .25s cubic-bezier(.22,1,.36,1), color .25s cubic-bezier(.22,1,.36,1);
  }}
  a.btn:hover {{ background:var(--ink); color:var(--cream); }}
</style>
</head>
<body>
  <h1>nothing here</h1>
  <p>This page doesn&rsquo;t exist &mdash; or it moved. The work is all still where it was.</p>
  <div class="links">
    <a class="btn" id="home" href="/">home</a>
    <a class="btn" id="gallery" href="/gallery/index.html">gallery</a>
  </div>
<script>
  // Works out the site root: on username.github.io the first path segment is
  // the repository, on a custom domain the root is simply "/".
  (function () {{
    var base = "/";
    if (location.hostname.endsWith("github.io")) {{
      var seg = location.pathname.split("/").filter(Boolean)[0];
      if (seg) base = "/" + seg + "/";
    }}
    document.getElementById("home").href = base;
    document.getElementById("gallery").href = base + "gallery/index.html";
  }})();
</script>
</body>
</html>
"""
    open(f"{SITE}/404.html", "w").write(body)
    print("404.html")

# ------------------------------------------------------------------- run ----

build_home()
build_about()
build_contact()
for fname, name, sub, cover, works in CATEGORIES:
    build_category(fname, name, works)
build_gallery_landing()
build_404()
