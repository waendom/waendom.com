# Was hier hochgeladen wird

**Der Inhalt dieses Ordners kommt ins Repository-Hauptverzeichnis — nicht der Ordner selbst.**

Nach dem Upload muss `index.html` direkt in der obersten Ebene liegen, also unter `github.com/waendom/waendom.com/`. Erscheint dort ein Ordner `waendom-site`, ist alles eine Ebene zu tief.

## Struktur

```
index.html            -> waendom.com/
about/index.html      -> waendom.com/about/
contact/index.html    -> waendom.com/contact/
home/index.html       Weiterleitung der alten Google-Adresse /home
404.html              Fehlerseite
sitemap.xml           Seitenverzeichnis für Suchmaschinen
robots.txt
style.css
script.js
CNAME                 enthält "waendom.com" — hält die Domain fest

gallery/
  index.html          -> waendom.com/gallery/
  digital/index.html  -> waendom.com/gallery/digital/
  canvas/index.html   -> waendom.com/gallery/canvas/
  analog/index.html   -> waendom.com/gallery/analog/
  sticker/index.html  -> waendom.com/gallery/sticker/

images/               JPG + WebP, 1200 px fürs Raster
  full/               JPG + WebP, 2000 px für die Lightbox

albums/               HIER lädst du künftig neue Bilder hoch
  digital/ canvas/ analog/ sticker/
captions.txt          Bildbeschreibungen

.github/workflows/    Automatik, die neue Bilder einpflegt
tools/                Skripte (gehören nicht zur Website)
```

## Wichtig: alte Dateien löschen

Diese Umstellung **verschiebt** Seiten. Lädst du nur die neuen Dateien hoch, bleiben die alten daneben liegen und sind weiterhin erreichbar:

- `about.html`, `contact.html`
- `gallery/digital.html`, `gallery/canvas.html`, `gallery/analog.html`, `gallery/sticker.html`
- `UPLOAD.md`, `tools/build_preview.py`

Lösch diese acht Dateien nach dem Upload im Repository. Bleiben sie liegen, funktioniert die Seite zwar, aber jede Arbeit wäre unter zwei Adressen erreichbar — das verwirrt Suchmaschinen.

Am einfachsten: **erst alles im Repository löschen, dann alles neu hochladen.** Die Datei `CNAME` liegt in diesem Paket, die Domain kommt also mit zurück.

## Vorgehen (am Computer)

1. ZIP entpacken
2. Im Repository alle vorhandenen Dateien löschen
3. **Add file → Upload files**
4. Im entpackten Ordner alles markieren und ins Browserfenster ziehen — den Inhalt, nicht den Ordner
5. Warten, bis alle Dateien gelistet sind
6. „Commit directly to the main branch" → **Commit changes**

**Der Ordner `.github` wird leicht übersehen.** Am Mac blendest du versteckte Dateien mit **Cmd+Shift+Punkt** ein. Fehlt er, funktioniert die Bild-Automatik nicht.

## Nach dem Upload prüfen

- `waendom.com/gallery/digital/` öffnen — Album erscheint, Adresse ohne `.html`
- `waendom.com/home` öffnen — leitet zur Startseite weiter
- `waendom.com/sitemap.xml` öffnet eine Liste mit acht Adressen
- Settings → Pages zeigt weiterhin `waendom.com`
- Settings → Actions → General → Workflow permissions steht auf **Read and write**

## Danach: Google Bescheid geben

1. [search.google.com/search-console](https://search.google.com/search-console) öffnen, Property `waendom.com` anlegen (Bestätigung per DNS-Eintrag in Cloudflare)
2. Links unter **Sitemaps** die Adresse `sitemap.xml` einreichen
3. Unter **Entfernen** kannst du die veraltete Adresse `waendom.com/home` aus den Suchergebnissen nehmen — die Weiterleitung erledigt das sonst mit der Zeit von selbst
