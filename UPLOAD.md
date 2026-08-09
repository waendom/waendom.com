# Was hier hochgeladen wird

**Der Inhalt dieses Ordners kommt ins Repository-Hauptverzeichnis — nicht der Ordner selbst.**

Nach dem Upload muss `index.html` direkt in der obersten Ebene deines Repositories liegen, also unter `github.com/waendom/waendom.com/`. Wenn du dort einen Ordner namens `waendom-site` siehst, ist es eine Ebene zu tief und GitHub Pages findet nichts.

## Die vollständige Struktur

```
index.html            Startseite
about.html            about waendom
contact.html          contact
404.html              Fehlerseite
style.css             Design
script.js             Menü, Scroll-Effekte, Lightbox
CNAME                 enthält "waendom.com" — hält die Domain fest
README.md             Doku (optional)

gallery/
  index.html          Übersicht der vier Alben
  digital.html
  canvas.html
  analog.html
  sticker.html

images/               alle Bilder fürs Raster (max. 1200 px)
  full/               hochauflösende Fassungen für die Lightbox
  favicon-32.png
  favicon-180.png
  favicon-512.png
  man-left.png        Banner-Zeichnungen
  man-right.png
  portrait.jpg
  README.md

tools/                Build-Skripte (optional, gehören nicht zur Website)
```

## Kurzanleitung

1. **An einem Computer arbeiten**, nicht am Handy — Ordner lassen sich mobil nicht zuverlässig hochladen.
2. Im Repository die alten Dateien löschen. `CNAME` darf ruhig mit weg, sie ist hier enthalten.
3. `github.com/waendom/waendom.com` → **Add file → Upload files**
4. Alle Dateien und Ordner aus diesem Ordner markieren und ins Browserfenster ziehen. Nicht den umschließenden Ordner ziehen, sondern seinen Inhalt.
5. Warten, bis alle Dateien in der Liste erscheinen — bei 90 Dateien dauert das einen Moment.
6. Unten **"Commit directly to the main branch"** auswählen → **Commit changes**.

## Prüfen, ob es geklappt hat

- Im Repository liegt `index.html` ganz oben, kein Zwischenordner.
- Settings → Pages zeigt weiterhin `waendom.com` als Custom domain.
- Nach ein bis zwei Minuten: `waendom.com/gallery/digital.html` öffnen. Erscheint das Album, sitzt alles richtig.
- Der Seitentitel im Browser-Tab lautet **"waendom.com"** — steht dort noch "Vorschau", liegt die alte Datei noch drin.
