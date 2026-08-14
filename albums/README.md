# Bilder hochladen

Hier legst du neue Arbeiten ab. Alles andere passiert automatisch — du musst nie HTML anfassen.

## Neues Bild hinzufügen

1. Auf GitHub in den passenden Ordner: `albums/digital`, `albums/canvas`, `albums/analog` oder `albums/sticker`
2. **Add file → Upload files**
3. Bild auswählen, unten **Commit changes**
4. Nach ein bis drei Minuten steht es auf der Website.

Das geht auch vom Handy — es sind einzelne Dateien, keine Ordner.

**Um die Nummer musst du dich nicht kümmern.** Lädst du eine Datei ohne führende Zahl hoch, bekommt sie automatisch die nächste freie und wird im Ordner entsprechend umbenannt. Sie landet damit am Ende des Albums. Aus `nebel.jpg` wird also `09-nebel.jpg`, wenn acht Bilder vorhanden waren. Lädst du mehrere auf einmal hoch, werden sie alphabetisch durchnummeriert.

## Wie das Bild am Ende heißt

Der Name kommt aus **deinem** Dateinamen — nichts wird automatisch fortnummeriert. Die führende Zahl fällt weg, Groß-/Kleinschreibung und Sonderzeichen werden vereinheitlicht:

| Du lädst hoch | Auf der Website |
|---|---|
| `09-nebel.jpg` | `images/nebel.jpg` |
| `10-analog-09.jpg` | `images/analog-09.jpg` |
| `IMG_2481.JPG` | `images/img-2481.jpg` |
| `Strand bei Nacht.jpeg` | `images/strand-bei-nacht.jpg` |

Die Nummer vergibt das Skript selbst, du brauchst sie beim Hochladen nicht mitzuliefern. Willst du eine bestimmte Position, kannst du sie aber vorgeben.

Zwei Dateien dürfen nicht denselben Endnamen ergeben. Passiert das, bricht der Durchlauf mit einer klaren Meldung ab und die Website bleibt unverändert.

## Reihenfolge

Die Zahl am Anfang des Dateinamens bestimmt die Position — sie wird beim ersten Durchlauf automatisch vergeben, du kannst sie danach jederzeit ändern:

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

**Es entsteht keine automatische Beschreibung.** Ohne Eintrag bekommt das Bild den allgemeinen Text „Work from the analog collection" — die Seite funktioniert damit, aber für Screenreader und die Bildersuche bringt das nichts.

Eine echte Beschreibung trägst du in `captions.txt` nach:

```
analog/nebel.jpg | Film photograph: fog over a field at first light
```

Links steht der Name **ohne** die führende Nummer. Dadurch bleibt die Beschreibung erhalten, wenn du später umsortierst und die Nummer sich ändert.

Das kannst du jederzeit nachholen, auch lange nach dem Upload — `captions.txt` lässt sich direkt auf GitHub bearbeiten, auch vom Handy. Nach dem Speichern läuft die Automatik erneut.

**Tipp:** Im Reiter Actions listet jeder Durchlauf am Ende alle Bilder ohne Beschreibung auf, fertig zum Kopieren.

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
