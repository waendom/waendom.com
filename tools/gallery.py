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
WEBP_QUALITY = 78     # entspricht etwa JPEG 82, bei rund 30 % weniger Gewicht

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


NUM_PREFIX = re.compile(r"^(\d+)[-_ ]+")


def scan(album):
    """Bilder eines Albums in Anzeigereihenfolge.

    Dateien mit führender Nummer behalten ihren Platz. Alles ohne Nummer
    ist frisch hochgeladen: es bekommt die nächste freie Nummer, wird auf
    der Festplatte entsprechend umbenannt und landet damit am Ende des
    Albums. Beim nächsten Lauf ist es dann eine gewöhnliche nummerierte
    Datei — die Reihenfolge steht also dauerhaft fest und bleibt im
    Dateinamen sichtbar."""
    folder = os.path.join(ALBUMS_DIR, album)
    if not os.path.isdir(folder):
        return []

    files = [f for f in os.listdir(folder)
             if f.lower().endswith(SOURCE_TYPES) and not f.startswith(".")]

    numbered, fresh = [], []
    for f in files:
        m = NUM_PREFIX.match(f)
        if m:
            numbered.append((int(m.group(1)), f))
        else:
            fresh.append(f)

    numbered.sort(key=lambda t: (t[0], t[1]))
    next_num = (max((n for n, _ in numbered), default=0)) + 1

    for f in sorted(fresh):
        new_name = f"{next_num:02d}-{f}"
        while os.path.exists(os.path.join(folder, new_name)):
            next_num += 1
            new_name = f"{next_num:02d}-{f}"
        os.rename(os.path.join(folder, f), os.path.join(folder, new_name))
        print(f"  ~ {album}/{f} -> {new_name} (ans Ende gestellt)")
        numbered.append((next_num, new_name))
        next_num += 1

    return [f for _, f in numbered]


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
    grid_webp = os.path.splitext(grid_out)[0] + ".webp"
    full_webp = os.path.splitext(full_out)[0] + ".webp"
    if all(os.path.exists(x) for x in (grid_out, full_out, grid_webp, full_webp)):
        src_time = os.path.getmtime(src_path)
        if min(os.path.getmtime(x) for x in (grid_out, full_out, grid_webp, full_webp)) >= src_time:
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

        # WebP-Fassungen daneben legen
        grid.save(os.path.splitext(grid_out)[0] + ".webp", "WEBP",
                  quality=WEBP_QUALITY, method=6)
        with Image.open(full_out) as f:
            f.convert("RGB").save(os.path.splitext(full_out)[0] + ".webp", "WEBP",
                                  quality=WEBP_QUALITY, method=6)
        return grid.size


def figure(name, alt, w, h):
    """Absolute Pfade, damit sie aus jeder Verzeichnistiefe stimmen, und ein
    <picture> mit WebP — der Browser nimmt das kleinere Format, wenn er kann."""
    return ('        <figure class="art-piece">\n'
            '          <picture>\n'
            f'            <source srcset="/images/{name}.webp" type="image/webp">\n'
            f'            <img src="/images/{name}.jpg" '
            f'data-full="/images/full/{name}.jpg" alt="{alt}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async">\n'
            '          </picture>\n'
            '        </figure>')


def rewrite(album, figures):
    path = os.path.join(GALLERY_DIR, album, "index.html")
    if not os.path.exists(path):
        print(f"  ! gallery/{album}/index.html fehlt — übersprungen")
        return False
    html = open(path, encoding="utf-8").read()
    i, j = html.find(START), html.find(END)
    if i == -1 or j == -1:
        print(f"  ! Markierungen fehlen in gallery/{album}/index.html — übersprungen")
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
    missing = []

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
            alt = (caps.get(f"{album}/{name}.jpg")          # stabil beim Umsortieren
                   or caps.get(f"{album}/{fname}".lower())  # alte Schreibweise mit Nummer
                   or caps.get(name)
                   or "")
            if not alt:
                missing.append(f"{album}/{fname}")
                alt = f"Work from the {album} collection"
            alt = alt.replace('"', "&quot;")
            figures.append(figure(name, alt, w, h))
            print(f"  {album}/{fname} -> images/{name}.jpg ({w}x{h})")

        if rewrite(album, figures):
            changed = True
        print(f"{album}: {len(figures)} Bild(er)")

    # Bilder aufräumen, deren Quelldatei nicht mehr existiert. Alles, was von
    # anderen Seiten gebraucht wird (Banner, Portrait, Favicon), bleibt.
    protected = {"man-left", "man-right", "portrait"}
    for stem in sorted({os.path.splitext(f)[0] for f in os.listdir(FULL_DIR)}):
        if stem in keep or stem in protected:
            continue
        for folder in (FULL_DIR, IMAGES_DIR):
            for ext in (".jpg", ".webp"):
                victim = os.path.join(folder, stem + ext)
                if os.path.exists(victim):
                    os.remove(victim)
        print(f"  - {stem} entfernt (keine Quelldatei mehr)")
        changed = True

    if missing:
        print("\nOhne Bildbeschreibung (allgemeiner Text wird verwendet).")
        print("Trage sie in captions.txt nach, wenn du magst:")
        for m in missing:
            album, fname = m.split("/", 1)
            print(f"  {album}/{output_name(fname)}.jpg | ")

    print("\nÄnderungen vorhanden." if changed else "\nNichts zu tun.")


if __name__ == "__main__":
    main()
