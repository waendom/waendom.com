# Bilder

Zwei Fassungen von jedem Werk:

- **`images/`** — max. 1200 px, Qualität 80. Das ist, was im Raster geladen wird.
- **`images/full/`** — bis 2000 px, Qualität 82. Wird ausschließlich geladen, wenn jemand ein Bild in der Lightbox öffnet.

Dadurch bleibt das Blättern schnell, aber die Vollansicht ist scharf. Zusammen rund 20 MB.

Die Sticker-Fotos liegen in `full/` in derselben Auflösung wie im Raster — die Originaldateien standen dafür nicht mehr zur Verfügung.

## Banner
`man-left.png` · `man-right.png` — freigestellt, transparenter Hintergrund.

## Startseite — die 5 Werke
`mary-cooper` · `canvas-05` · `cap` · `analog-03` · `sticker-backstein`

Im Raster auf 4:5 beschnitten; in der Lightbox erscheinen sie im Originalformat.

## About waendom
`portrait.jpg`

## digital (11)
`antoinette` · `mary-cooper` · `coated` · `astronaut` · `die-ruderer` · `rouven` · `flat-cap` · `blue` · `greyscale` · `sunbleached` · `cap`

Coverbild des Albums: `die-ruderer`

## canvas (8)
`heisenberg` · `canvas-01` bis `canvas-05` · `canvas-07` · `canvas-08`

Coverbild: `canvas-03`

## analog (8)
`analog-01` (Helikopter) · `analog-02` (Silhouette am Fenster) · `analog-03` (Fassade) · `analog-04` (Seehund) · `analog-05` (Helikopter in Wolken) · `analog-06` (Cap & Sonnenbrille) · `analog-07` (Kornfeld) · `analog-08` (Kletterer)

Coverbild: `analog-01`

## sticker (7)
`sticker-stapel` · `sticker-alpenrod` · `sticker-bergstation` · `sticker-laptop` · `sticker-dschungel` · `sticker-backstein` · `sticker-stahl`

Coverbild: `sticker-alpenrod`

## Favicon

`favicon-32.png`, `favicon-180.png`, `favicon-512.png` — aus der sitzenden Illustration erzeugt, auf Creme-Hintergrund freigestellt.

## Hintergrundfarbe

Bei `greyscale` war der Original-Hintergrund reines Weiß und wurde durch das Cremeweiß der Seite ersetzt. Änderst du `--cream` in `style.css`, muss dieses Bild (und die Favicons) neu erzeugt werden.

## Bildbeschreibungen

Die `alt`-Texte aller Werke stehen gesammelt in `alt_text.py` (außerhalb dieses Ordners, beim Build-Skript). Dort ändern, nicht im HTML — beim nächsten Generieren würde es sonst überschrieben.

## Neue Arbeiten hinzufügen

1. Bild als JPG hier ablegen (max. 1200 px breit) und eine 2000-px-Fassung nach `full/` legen.
2. In der passenden Datei unter `gallery/` einen Block kopieren:

```html
<figure class="art-piece">
  <img src="../images/DATEINAME.jpg" alt="digital" loading="lazy">
</figure>
```

Ein Werk in ein anderes Album verschieben heißt: den Block ausschneiden und in die andere Datei einfügen.
