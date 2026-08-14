# Waendom.com

Statische Portfolio-Seite — reines HTML/CSS/JS, bereit für GitHub Pages.

## Struktur

```
waendom-site/
├── index.html              Startseite: Banner, Welcome-Text, 5 Werke, "more"
├── about.html               about waendom
├── contact.html             contact — E-Mail
├── style.css                 Design
├── script.js                   Menü, Scroll-Effekte, Lightbox
├── tools/                     Build-Skripte (nicht Teil der Website, s. tools/README.md)
├── 404.html                  eigene Fehlerseite (GitHub Pages nutzt sie automatisch)
├── gallery/
│   ├── index.html             Übersicht: digital / canvas / analog / sticker
│   ├── digital.html             11 Arbeiten
│   ├── canvas.html               8 Arbeiten
│   ├── analog.html               8 Fotografien
│   └── sticker.html              7 Fotos
└── images/                    Rasterbilder (max. 1200 px)
    └── full/                    hochauflösende Fassungen für die Lightbox
```

Gesamtgröße: rund 22 MB (davon 13 MB die hochauflösenden Lightbox-Fassungen) — deutlich unter der 1-GB-Grenze und schnell im Laden.

## Aufbau

- **Kopfzeile:** links „waendom.com" als Button zur Startseite, rechts der 3-Striche-Menübutton. Sobald man scrollt, schrumpft die linke Leiste zu einem runden Pfeil-Button. Wohin der Pfeil führt, ist pro Seite fest verdrahtet (nicht von der Browser-History abhängig): ein Album führt hoch zur Gallery-Übersicht, die Gallery-Übersicht hoch zur Startseite, About/Contact hoch zur Startseite. Auf der Startseite selbst scrollt der Pfeil stattdessen nach oben.
- **Banner:** die beiden Tuschezeichnungen füllen 2/5 der Bildschirmhöhe. Beim Scrollen gleiten sie seitlich auseinander, werden kleiner und blenden aus — durch den Drehpunkt unten mittig hebt das Schrumpfen das Driften an den Rändern auf, sie werden nie angeschnitten.
- **Menü:** vollflächiges Overlay mit home, gallery, about waendom, contact.
- **Bilder:** ohne Rahmen und ohne Beschriftung. Jedes Werk wirft einen weichen Schatten, dessen Winkel sich mit der Scroll-Position leicht verschiebt.
- **Lightbox:** Klick auf ein Werk zeigt es formatfüllend im Originalformat. Zuerst erscheint sofort die Rasterfassung, dann wird im Hintergrund die hochauflösende Datei aus `images/full/` nachgeladen und ausgetauscht — so gibt es nie einen leeren Rahmen, aber am Ende ein scharfes Bild. Blättern per Pfeiltasten, Buttons oder Wischen; schließen mit Escape, ×, oder Klick daneben. Geblättert wird nur innerhalb des geöffneten Albums.
- **Barrierefreiheit:** jedes Werk hat eine echte Bildbeschreibung im `alt`-Attribut (in `alt_text.py` gepflegt), und alle Bilder tragen ihre Maße im HTML, damit das Layout beim Laden nicht springt.
- **Nach oben:** ein runder Button unten rechts blendet sich ein, sobald das Seitenende in Reichweite kommt — genauer: wenn die verbleibende Scroll-Strecke unter etwa drei Viertel einer Bildschirmhöhe fällt. Auf Seiten, die kaum scrollen, erscheint er gar nicht.
- **Favicon & Vorschaubild:** eigenes Icon (aus der sitzenden Illustration) plus Open-Graph-Bild für Link-Vorschauen bei WhatsApp, Discord, Reddit & Co. — zeigt überall das letzte Werk aus dem Digital-Album.
- **Typografie:** Space Mono für Überschriften, Menü und Album-Beschriftungen, durchgängig klein geschrieben. Fließtext in Work Sans. Beide werden von Google Fonts geladen, es sind keine Schriftdateien im Repo nötig.

## In dein GitHub-Repository einspielen

1. ZIP entpacken.
2. Den **Inhalt** des Ordners ins Hauptverzeichnis deines Repos kopieren.
3. Committen & pushen.

## GitHub Pages aktivieren

Settings → Pages → Source: **Deploy from a branch** → Branch `main`, Ordner `/ (root)` → Save.
Nach ein bis zwei Minuten liegt die Seite unter `https://<username>.github.io/<repo>/`.

## Anpassen

- **Farben:** oben in `style.css` im Block `:root`.
- **Banner-Höhe:** `style.css`, bei `.hero` der Wert `height: 40vh`.
- **Banner-Bewegung:** `script.js`, die Konstanten `DRIFT` und `SHRINK`. `DRIFT` sollte unter `SHRINK / 2 * 100` bleiben, sonst können die Figuren den Rand berühren.
- **Wann der Nach-oben-Button erscheint:** `script.js`, Funktion `nearPageEnd` — der Faktor `0.75` bestimmt, wie früh er auftaucht (kleiner = später).
- **Neigung des About-Porträts:** `style.css` bei `.about-portrait img`, der Wert `rotate(-1.6deg)`. Auf `0deg` setzen, wenn du es gerade willst.
- **Schatten-Bewegung:** `script.js` in `onScroll`, die Werte bei `--sx`, `--sy`, `--sblur`.
- **E-Mail-Adresse:** `contact.html`, Suche nach `contact@waendom.com`.
- **Vorschaubild beim Teilen:** in `build_site.py` die Variable `og_image` in der `head()`-Funktion (Standard: `images/cap.jpg`).
- **Zurück-Hierarchie:** in `build_site.py` bei den `chrome(...)`-Aufrufen der Parameter `up=`.

## Neue Bilder hinzufügen

Bild in den passenden Ordner unter `albums/` hochladen — fertig. GitHub verkleinert es, erzeugt die Lightbox-Fassung und trägt es in die Galerie ein. Ausführlich in `albums/README.md`.

Einmalig nötig: **Settings → Actions → General → Workflow permissions → Read and write permissions**.

## Offene Punkte

- **Rechtsklick** ist deaktiviert. Das hält Gelegenheitskopien auf, ist aber kein echter Schutz: Bilder lassen sich weiterhin über die Entwicklerkonsole, den Seitenquelltext oder schlicht per Screenshot sichern. Wenn dir das wichtig ist, wäre ein sichtbares Wasserzeichen der wirksamere Weg.
- **Vorschaubild-URL:** die `og:image`-Angabe ist auf `https://waendom.com/...` fest verdrahtet. Läuft die Seite noch nicht unter der eigenen Domain, greifen Plattformen wie WhatsApp oder Reddit beim Teilen ins Leere. Sobald die netcup-Domain live ist, passt das automatisch — bis dahin in `build_site.py` bei `SITE_URL` anpassbar.
- **Zurück-Wischgeste des Handys:** Das ist Verhalten des Browsers bzw. der App, in der die Seite geöffnet wird (z. B. Reddits eingebauter Browser), nicht etwas, das der Seitencode direkt steuert. Kommt man über einen externen Link direkt auf eine Unterseite, ist dort noch keine eigene Vorgeschichte vorhanden — die Wischgeste verlässt dann die Seite, was in den meisten Browsern normales Verhalten ist. Tritt es auch nach mehreren Klicks innerhalb der Seite auf, sag mir, in welcher App/welchem Browser genau — das würde für ein browserspezifisches Verhalten sprechen, das sich eventuell umgehen lässt.

