from PIL import Image
import numpy as np, os, json

SRC = "/mnt/user-data/uploads"
SITE = "/home/claude/waendom-site"
OUT = f"{SITE}/images"
FULL = f"{OUT}/full"
CREAM = (248, 244, 234)
os.makedirs(FULL, exist_ok=True)

def trim_white(im, thresh=244, pad=2):
    g = np.asarray(im.convert("L")).astype(np.int16)
    mask = g < thresh
    if not mask.any():
        return im
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    y0, y1 = max(0, rows[0] - pad), min(im.size[1], rows[-1] + 1 + pad)
    x0, x1 = max(0, cols[0] - pad), min(im.size[0], cols[-1] + 1 + pad)
    return im.crop((x0, y0, x1, y1))

def on_cream(im, white=250, solid=225):
    rgb = im.convert("RGB")
    lum = np.asarray(rgb).astype(np.float32).max(axis=2)
    a = np.clip((white - lum) / (white - solid), 0, 1)[..., None]
    arr = np.asarray(rgb).astype(np.float32) * a + np.array(CREAM, dtype=np.float32) * (1 - a)
    return Image.fromarray(arr.astype(np.uint8), "RGB")

# slug -> (source file, trim white border?, knock white background out?)
JOBS = {
    "antoinette":  ("antoinette__1_.png",                       False, False),
    "mary-cooper": ("marycooper__1_.webp",                      False, False),
    "coated":      ("coated__1_.webp",                          False, False),
    "astronaut":   ("Untitled_Artwork__3_.jpg",                 False, False),
    "die-ruderer": ("DieRuderer__1_.webp",                      False, False),
    "rouven":      ("Rouven_sketch.webp",                       False, False),
    "flat-cap":    ("Untitled_Artwork__2_.jpg",                 False, False),
    "blue":        ("Untitled_Artwork__4_.jpg",                 False, False),
    "greyscale":   ("Untitled_Artwork__1_.jpg",                 True,  True),
    "sunbleached": ("c28fe5c7-2ddf-4e0a-8478-3cd8fabf50a9.png", False, False),
    "cap":         ("6eb0f88a-c581-4668-8709-402cba8f9f04-1_all_37630.webp", False, False),
    "heisenberg":  ("IMG_0076.jpg",       False, False),
    "canvas-01":   ("IMG_0393-min.jpeg",  True,  False),
    "canvas-02":   ("IMG_0394-min.jpeg",  True,  False),
    "canvas-03":   ("IMG_0395-min.jpeg",  True,  False),
    "canvas-04":   ("IMG_0396-min.jpeg",  True,  False),
    "canvas-05":   ("IMG_0397-min.jpeg",  True,  False),
    "canvas-07":   ("3263.jpg",           False, False),
    "canvas-08":   ("3267.jpg",           False, False),
    "analog-01":   ("44213.jpg",  False, False),
    "analog-02":   ("44218.jpg",  False, False),
    "analog-03":   ("44606.jpg",  False, False),
    "analog-04":   ("44602.jpg",  False, False),
    "analog-05":   ("1626.jpg",   False, False),
    "analog-06":   ("1631.jpg",   False, False),
    "analog-07":   ("1628.jpg",   False, False),
    "analog-08":   ("3647.jpg",   False, False),
}

dims = {}
total = 0

for slug, (src, do_trim, do_cream) in JOBS.items():
    path = os.path.join(SRC, src)
    if not os.path.exists(path):
        print(f"  ! Quelle fehlt für {slug} — überspringe")
        continue
    im = Image.open(path)
    if do_trim:
        im = trim_white(im)
    if do_cream:
        im = on_cream(im)
    w, h = im.size
    target = min(2000, w)          # never upscale beyond the original
    if w > target:
        im = im.resize((target, round(h * target / w)), Image.LANCZOS)
    out = f"{FULL}/{slug}.jpg"
    im.convert("RGB").save(out, "JPEG", quality=82, optimize=True, progressive=True)
    kb = os.path.getsize(out) / 1024
    total += kb
    print(f"{slug:14s} {str(im.size):13s} {kb:6.0f} KB")

# sticker photos: originals are gone, so upscale is pointless — reuse the 1200px file
for f in sorted(os.listdir(OUT)):
    if f.startswith("sticker-") and f.endswith(".jpg"):
        slug = f[:-4]
        im = Image.open(f"{OUT}/{f}")
        out = f"{FULL}/{slug}.jpg"
        im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
        total += os.path.getsize(out) / 1024
        print(f"{slug:14s} {str(im.size):13s} (aus 1200px-Datei)")

# record the *grid* dimensions, which is what the HTML needs
for f in sorted(os.listdir(OUT)):
    if f.endswith(".jpg") or (f.endswith(".png") and f.startswith("man-")):
        slug = os.path.splitext(f)[0]
        with Image.open(f"{OUT}/{f}") as im:
            dims[slug] = im.size

json.dump(dims, open("/home/claude/image_dims.json", "w"), indent=1)
print(f"\nfull/: {total/1024:.1f} MB   |   Maße erfasst für {len(dims)} Bilder")
