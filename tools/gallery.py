#!/usr/bin/env python3
"""
Überträgt die Bilder aus den albums/-Ordnern in die Galerieseiten.

Du führst das nie selbst aus — GitHub startet es automatisch, sobald du in
einem albums/-Ordner etwas hochlädst, umbenennst oder löschst
(siehe .github/workflows/gallery.yml).

Was passiert:

  albums/analog/03-nebel.jpg
        │
        ├── images/nebel.jpg        1200 px, fürs Raster
        ├── images/full/nebel.jpg   2000 px, für die Lightbox
        └── Eintrag in gallery/analog.html

Die Nummer vorne bestimmt nur die Reihenfolge und fällt beim Ausgabenamen
weg. Aus 03-nebel.jpg wird also images/nebel.jpg — dadurch bleiben Links
von der Startseite und der Galerie-Übersicht gültig, auch wenn du die
Reihenfolge änderst.

Geändert wird ausschließlich der Bereich zwischen

    <!-- gallery:start -->
    <!-- gallery:end -->

Alles andere in den HTML-Dateien bleibt unangetastet.
"""

import os
import re
import shutil
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow fehlt. Installieren mit:  pip install pillow")

# iPhone-Fotos kommen oft als .heic — dieser Zusatz macht sie lesbar
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUMS_DIR = os.path.join(ROOT, "albums")
IMAGES_DIR = os.path.join(ROOT, "images")
FULL_DIR = os.path.join(IMAGES_DIR, "full")
GALLERY_DIR = os.path.join(ROOT, "gallery")

ALBUMS = ["digital", "canvas", "analog", "sticker"]
SOURCE_TYPES = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".tif", ".tiff")

GRID_WIDTH, GRID_QUALITY = 1200, 80
FULL_WIDTH, FULL_QUALITY = 2000, 82

START = "<!-- gallery:start"
END = "<!-- gallery:end -->"


def output_name(filename):
    """03-nebel.jpg -> nebel   |   Nebel Bild (2).JPG -> nebel-bild-2"""
    stem = os.path.splitext(filename)[0]
    stem = re.sub(r"^\d+[-_ ]+", "", stem)          # Sortier-Präfix abschneiden
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    return stem or "bild"


def load_captions():
    caps = {}
    path = os.path.join(ROOT, "captions.txt")
    if not os.path.exists(path):
        return caps
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        key, _, text = line.partition("|")
        caps[key.strip().lower()] = text.strip()
    return caps


def scan(album):
    folder = os.path.join(ALBUMS_DIR, album)
    if not os.path.isdir(folder):
        return []
    return sorted(f for f in os.listdir(folder)
                  if f.lower().endswith(SOURCE_TYPES) and not f.startswith("."))


def derive(src_path, name):
    """Beide Fassungen schreiben, Rastermaße zurückgeben.
    Ist die Quelle schon klein genug, wird sie kopiert statt neu berechnet —
    das vermeidet unnötigen Qualitätsverlust durch mehrfaches Speichern."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(FULL_DIR, exist_ok=True)
    full_out = os.path.join(FULL_DIR, name + ".jpg")
    grid_out = os.path.join(IMAGES_DIR, name + ".jpg")

    # Unverändert seit dem letzten Lauf? Dann nur die Maße nachschlagen.
    # Das hält die Laufzeit kurz und vermeidet, dass identische Bilder bei
    # jedem Durchlauf neu geschrieben und damit erneut committet werden.
    if os.path.exists(grid_out) and os.path.exists(full_out):
        src_time = os.path.getmtime(src_path)
        if os.path.getmtime(grid_out) >= src_time and os.path.getmtime(full_out) >= src_time:
            with Image.open(grid_out) as done:
                return done.size

    with Image.open(src_path) as im:
        w, h = im.size
        is_jpeg = src_path.lower().endswith((".jpg", ".jpeg"))

        if w <= FULL_WIDTH and is_jpeg:
            shutil.copy(src_path, full_out)
        else:
            out = im.convert("RGB")
            if w > FULL_WIDTH:
                out = out.resize((FULL_WIDTH, round(h * FULL_WIDTH / w)), Image.LANCZOS)
            out.save(full_out, "JPEG", quality=FULL_QUALITY, optimize=True, progressive=True)

        grid = im.convert("RGB")
        gw = min(GRID_WIDTH, w)
        if w > gw:
            grid = grid.resize((gw, round(h * gw / w)), Image.LANCZOS)
        grid.save(grid_out, "JPEG", quality=GRID_QUALITY, optimize=True, progressive=True)
        return grid.size


def figure(name, alt, w, h):
    return ('        <figure class="art-piece">\n'
            f'          <img src="../images/{name}.jpg" '
            f'data-full="../images/full/{name}.jpg" alt="{alt}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async">\n'
            '        </figure>')


def rewrite(album, figures):
    path = os.path.join(GALLERY_DIR, album + ".html")
    if not os.path.exists(path):
        print(f"  ! gallery/{album}.html fehlt — übersprungen")
        return False
    html = open(path, encoding="utf-8").read()
    i, j = html.find(START), html.find(END)
    if i == -1 or j == -1:
        print(f"  ! Markierungen fehlen in gallery/{album}.html — übersprungen")
        return False
    head_end = html.find("\n", i) + 1
    indent = html[html.rfind("\n", 0, j) + 1:j]   # Einrückung der Endmarkierung merken
    body = ("\n".join(figures) + "\n") if figures else ""
    updated = html[:head_end] + body + indent + html[j:]
    if updated != html:
        open(path, "w", encoding="utf-8").write(updated)
        return True
    return False


def main():
    caps = load_captions()
    seen = {}
    changed = False
    keep = set()

    for album in ALBUMS:
        figures = []
        for fname in scan(album):
            name = output_name(fname)
            if name in seen:
                sys.exit(f"FEHLER: '{name}' kommt doppelt vor "
                         f"({seen[name]} und {album}/{fname}). "
                         f"Bitte eine der beiden Dateien umbenennen.")
            seen[name] = f"{album}/{fname}"

            w, h = derive(os.path.join(ALBUMS_DIR, album, fname), name)
            keep.add(name)
            alt = caps.get(f"{album}/{fname}".lower(),
                           f"Work from the {album} collection").replace('"', "&quot;")
            figures.append(figure(name, alt, w, h))
            print(f"  {album}/{fname} -> images/{name}.jpg ({w}x{h})")

        if rewrite(album, figures):
            changed = True
        print(f"{album}: {len(figures)} Bild(er)")

    # Bilder aufräumen, deren Quelldatei nicht mehr existiert. Alles, was von
    # anderen Seiten gebraucht wird (Banner, Portrait, Favicon), bleibt.
    protected = {"man-left", "man-right", "portrait"}
    for f in os.listdir(FULL_DIR):
        stem = os.path.splitext(f)[0]
        if stem not in keep and stem not in protected:
            os.remove(os.path.join(FULL_DIR, f))
            grid = os.path.join(IMAGES_DIR, f)
            if os.path.exists(grid):
                os.remove(grid)
            print(f"  - {stem} entfernt (keine Quelldatei mehr)")
            changed = True

    print("\nÄnderungen vorhanden." if changed else "\nNichts zu tun.")


if __name__ == "__main__":
    main()
