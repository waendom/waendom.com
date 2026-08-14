# Bilder hochladen

Hier legst du neue Arbeiten ab. Alles andere passiert automatisch — du musst nie HTML anfassen.

## Neues Bild hinzufügen

1. Auf GitHub in den passenden Ordner: `albums/digital`, `albums/canvas`, `albums/analog` oder `albums/sticker`
2. **Add file → Upload files**
3. Bild auswählen, unten **Commit changes**
4. Nach ein bis drei Minuten steht es auf der Website.

Das geht auch vom Handy — es sind einzelne Dateien, keine Ordner.

## Reihenfolge

Die Zahl am Anfang des Dateinamens bestimmt die Position:

```
01-antoinette.jpg
02-mary-cooper.jpg
03-coated.jpg
```

Willst du etwas nach vorne holen, benenne die Datei um (auf GitHub: Datei anklicken → Stift → Namen ändern → Commit). Die Zahl fällt beim Veröffentlichen weg, aus `03-coated.jpg` wird also weiterhin `images/coated.jpg`.

Tipp: Lass beim Nummerieren Lücken (10, 20, 30 …), dann kannst du später dazwischenschieben, ohne alles umzubenennen.

## Bild austauschen

Lade eine Datei mit **demselben Namen** hoch — GitHub fragt, ob du ersetzen willst. Das neue Bild erscheint dann an derselben Stelle.

## Bild entfernen

Datei im `albums/`-Ordner löschen. Die daraus erzeugten Bilddateien werden beim nächsten Durchlauf mit aufgeräumt.

**Vorsicht bei diesen sieben Bildern** — sie sind zusätzlich auf der Startseite oder als Album-Titelbild verlinkt:

| Bild | Wird verwendet als |
|---|---|
| `mary-cooper` | Startseite |
| `canvas-05` | Startseite |
| `cap` | Startseite + Vorschaubild beim Teilen |
| `analog-03` | Startseite |
| `sticker-backstein` | Startseite |
| `die-ruderer` | Titelbild digital |
| `canvas-03` | Titelbild canvas |
| `analog-01` | Titelbild analog |
| `sticker-alpenrod` | Titelbild sticker |

Löschst du eines davon, bleibt dort eine Lücke. Dann muss der Verweis in `index.html` bzw. `gallery/index.html` von Hand geändert werden — sag mir Bescheid, oder such nach dem Dateinamen und ersetze ihn.

## Bildbeschreibung ergänzen

Optional, aber gut für Screenreader und die Bildersuche. In `captions.txt` eine Zeile ergänzen:

```
analog/09-nebel.jpg | Film photograph: fog over a field at first light
```

Links steht der **Dateiname im albums-Ordner**, inklusive Nummer. Ohne Eintrag bekommt das Bild eine allgemeine Beschreibung — es geht also nichts kaputt, wenn du es vergisst.

## Dateiformate

JPG, PNG, WebP, HEIC (iPhone), TIFF. Lade ruhig die Originale hoch — die Verkleinerung auf 1200 px fürs Raster und 2000 px für die Lightbox passiert automatisch.

## Wenn etwas nicht erscheint

Im Reiter **Actions** siehst du jeden Durchlauf.

- **Grüner Haken:** fertig. Erscheint das Bild trotzdem nicht, ist es der Zwischenspeicher deines Browsers — einmal hart neu laden.
- **Rotes Kreuz:** draufklicken, dort steht im Klartext, woran es lag. Häufigster Fall: zwei Dateien ergeben denselben Namen, etwa `01-nebel.jpg` und `07-nebel.jpg`. Dann eine umbenennen.

Solange etwas schiefgeht, bleibt die Website unverändert online — zurückgeschrieben wird nur ein vollständig durchgelaufener Durchgang.

## Einmalige Einrichtung

Damit der Ablauf ins Repository zurückschreiben darf:

**Settings → Actions → General → Workflow permissions → „Read and write permissions" → Save**

Ohne diesen Schritt läuft alles durch, aber nichts wird gespeichert.
