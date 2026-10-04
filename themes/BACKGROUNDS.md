# Folienhintergründe im Theme `htwg`

Dieses Dokument legt fest, welcher Hintergrund für welchen Folientyp verwendet wird.
Alle Hintergründe folgen dem HTWG-Corporate-Design (Punktraster, Kreise, Farben
Teal `#009B91`, Schiefer `#334152`, Hellblau-Grau `#D9E5EC`, Schwarz, Weiß) und
enthalten Logo und Fakultätszeile oben – deshalb blenden die Klassen den Footer
mit dem kleinen Logo automatisch aus.

## Regeln

| Folientyp | Hintergrund | Einbindung |
|---|---|---|
| Titelfolie (Vorlesungs-/Kapiteltitel mit Dozierenden) | `htwgin-titel.png` | `![bg](../../themes/htwgin-titel.png)` + `_footer: ""` (wie bisher) |
| Inhalt, Agenda, Lernziele, Zusammenfassung | `htwgin-inhalt.png` | `<!-- _class: inhalt -->` |
| Kapitel-/Abschnittsbeginn (Standard) | `htwgin-kapitel.png` | `<!-- _class: kapitel -->` |
| Beginn eines großen Teils (z. B. Teil I/II, neue Sprache) | `htwgin-kapitel-dunkel.png` | `<!-- _class: kapitel-dunkel -->` |
| Tools-Abschnitt (neue Werkzeuge, z. B. Worksheets, Mill, Git) | Beginn: `htwgin-kapitel.png` + Werkzeug-Icon (Hammer + Schraubenschlüssel, Teal); Inhaltsfolien: weiß mit Teal-Linie oben + kleinem Werkzeug-Icon | `<!-- _class: tools -->` bzw. `<!-- _class: tools-page -->` |
| Aufgabe, Übung, Task | `htwgin-aufgabe.png` | `<!-- _class: aufgabe -->` |
| Zitat, Merksatz, Definition/Kernaussage | `htwgin-zitat.png` | `<!-- _class: zitat -->` |
| Letzte Folie: Questions, Thank you, Kontakt (immer Englisch) | `htwgin-abschluss.png` | `<!-- _class: abschluss -->` |
| Normale Inhaltsfolie | – (weiß, Footer mit Logo) | keine Klasse |

- **Titelfolie:** Die erste Folie einer Vorlesung (und ein Vorlesungstitel innerhalb eines Decks) nutzt weiterhin das Bild `htwgin-titel.png` per `![bg]` – daran ändert sich nichts.
- **Inhalt:** Übersichten, Agenda, Lernziele und Zusammenfassungen bekommen die Klasse `inhalt`; die Punktlinie rechts symbolisiert den roten Faden, der Text beginnt unter dem Logo und lässt rechts ca. 200 px frei.
- **Kapitel (hell):** Jeder neue Abschnitt innerhalb einer Vorlesung beginnt mit einer kurzen Trennfolie der Klasse `kapitel` (optionale Nummer als `##`, Titel als `#`, eine Zeile Untertitel).
- **Kapitel (dunkel):** Nur für große Einschnitte (z. B. „Teil II“, Wechsel von Scratch zu Scala) – sparsam verwenden, damit der Kontrast etwas bedeutet; Text wird automatisch weiß, `**fett**` in der Überschrift erscheint in Teal.
- **Tools:** Fast jede Vorlesung führt ein neues Werkzeug ein. Der Abschnitt beginnt mit einer Folie der Klasse `tools` (Hintergrund wie `kapitel`, zusätzlich ein Teal-Werkzeug-Icon (gekreuzter Hammer und Schraubenschlüssel); `##` Oberzeile, `#` Titel, eine Zeile Untertitel). Alle Inhaltsfolien des Abschnitts bekommen `tools-page`: normale weiße Folie mit Footer und Seitenzahl, dazu eine 6 px Teal-Linie oben und ein kleines Werkzeug-Icon oben rechts – so erkennt man Werkzeug-Folien auch beim Durchblättern. Aufgaben zum Werkzeug bleiben `aufgabe`.
- **Aufgabe:** Jede Aufgabe/Übung/jeder Task steht auf einer Folie der Klasse `aufgabe`; der Text sitzt (etwas kompakter gesetzt, 21 px) im weißen Feld. Passt eine lange Aufgabe nicht hinein, wird sie mit `<div class="columns">` zweispaltig gesetzt (z. B. Anforderungen links, Deliverables rechts) statt Text zu kürzen.
- **Zitat:** Ein einzelnes Zitat (`>`), ein Merksatz oder eine zentrale Definition bekommt die Klasse `zitat`; nur wenige Zeilen, der Text steht in der weißen Kapsel links.
- **Abschluss:** Jede Vorlesung endet mit einer Folie der Klasse `abschluss` – wie alle Folien auf **Englisch**: `# Questions?`, `## Thank you!` und die Kontakt-E-Mail.
- **Normale Folien** bleiben ohne Klasse und damit weiß mit Footer und Seitenzahl.

## Beispiele

```markdown
---

<!-- _class: kapitel -->

## Kapitel 3
# Kontrollstrukturen

Schleifen, Verzweigungen und Ereignisse

---

<!-- _class: kapitel-dunkel -->

## Teil II
# **Objekt**orientierung

---

<!-- _class: inhalt -->

# Inhalt heute

1. Rückblick
2. Klone und Listen

---

<!-- _class: aufgabe -->

# Aufgabe 2.1

- Erstellen Sie ein Scratch-Projekt mit Klonen und einer Liste.

---

<!-- _class: zitat -->

> Programs must be written for people to read, and only incidentally for machines to execute.

— Harold Abelson

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
```

Alle Folien – auch Abschlussfolien – sind auf Englisch. Die Klasse gilt mit `_class` (Unterstrich) nur für die aktuelle Folie. Eigene
`<style scoped>`-Blöcke können wie bisher zusätzlich verwendet werden; bestehende Klassen
lassen sich kombinieren, z. B. `<!-- _class: compact aufgabe -->`.

## Technik

- Die PNGs liegen in `themes/` (`htwgin-<klasse>.png`, 1980×1114 wie `htwgin-titel.png`).
- Marp bettet das Theme-CSS in jedes HTML/PDF ein; relative `url()` im CSS würden
  daher nicht aufgelöst. Die Bilder sind deshalb als data-URI in `themes/htwg.css`
  eingebettet (generierter Block am Ende der Datei).
- `tools` hat kein eigenes PNG: `embed_backgrounds.py` ordnet per `ALIASES` den Hintergrund von `kapitel` auch `section.tools` zu. Icon und Linie sind reines CSS (Block „Tools“ in `themes/htwg.css`, Icon als Data-URI). Icon: Material Symbols Rounded „construction“ von Google, Apache License 2.0 (https://github.com/google/material-design-icons), auf #009b91 umgefärbt; Quellkopie in `themes/icons/tools.svg`.
- Neu erzeugen: `python3 themes/tools/make_bgs.py` (benötigt Pillow + numpy),
  danach `python3 themes/tools/embed_backgrounds.py` (nur Standardbibliothek).
