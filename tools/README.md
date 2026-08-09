# Build-Skripte

Diese Dateien erzeugen die HTML-Seiten. Sie sind **nicht Teil der veröffentlichten Website** — GitHub Pages ignoriert sie. Du kannst sie im Repo lassen (praktisch als Archiv) oder löschen.

| Datei | Zweck |
|---|---|
| `build_site.py` | erzeugt alle HTML-Seiten aus den Listen ganz oben in der Datei |
| `alt_text.py` | die Bildbeschreibungen aller Werke |
| `build_full_images.py` | erzeugt die hochauflösenden Fassungen in `images/full/` |
| `image_dims.json` | die Bildmaße, die ins HTML geschrieben werden |

## Etwas ändern

Ein Werk verschieben, hinzufügen oder umsortieren: die Listen `DIGITAL`, `CANVAS`, `ANALOG`, `STICKER`, `HOME` oben in `build_site.py` anpassen, dann `python3 build_site.py` ausführen.

Eine Bildbeschreibung ändern: in `alt_text.py`, dann ebenfalls neu generieren.

Wenn du lieber direkt im HTML arbeitest, geht das auch — dann solltest du die Skripte aber löschen, damit du sie nicht versehentlich ausführst und deine Änderungen überschreibst.
