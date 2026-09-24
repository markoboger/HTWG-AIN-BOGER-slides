# Diagrams — Einführung AIN Erstsemester

Editable Draw.io sources (`.drawio`) and exported SVGs (`.svg`) live in `diagrams/`.
Marp deck: `Einführung-AIN-Erstsemester.md` (relative embeds: `diagrams/<name>.svg`).

Source Google Slides: [Einführung AIN Erstsemester](https://docs.google.com/presentation/d/12VpE4i2CEMk00CgfC-Uah1sGcPEaVNzKVlb2AiUhWjg) (24 slides).

## Files created (19 diagrams × `.drawio` + `.svg`)

| File stem | Depicts |
|-----------|---------|
| `studieninhalte-temple` | Temple/pillars diagram: teal roof „Angewandte Informatik“ over five colored pillars (Theorie, Netze, Programmierung, Datenbanken, Anwendungen). |
| `curriculum-sem1-4` | Color-bordered curriculum grid Semesters 1–4 with Vorlesung/Übung callouts; Praxissemester row. |
| `studienverlauf-gesamt` | Full 7-semester overview (Grundstudium / Hauptstudium) with ECTS blocks. |
| `vorlesungen-1sem` | 2×2 professor cards (ECTS + module + name; photo placeholder). |
| `language-history` | Programming-language logos/years grid (ASM…Rust). |
| `paradigms` | Three columns: Procedural / Object-Oriented / Functional with language badges. |
| `sprachen-ain` | Curriculum grid annotated with language tags (Java, C, SQL, Python, ASM…). |
| `vertiefungsrichtungen` | Staggered Embedded / AI / SE description cards. |
| `vertiefung-katalog` | Three-column Vertiefung catalog (24 ECTS) with example modules + language logos. |
| `studienverlaufsplan-detail` | Color-coded detailed Studienverlaufsplan schematic (professors/modules). |
| `ai-intelligence-distorted` | WaitButWhy „Our Distorted View of Intelligence“ chart recreation. |
| `ai-intelligence-reality` | WaitButWhy „Reality“ exponential AI curve recreation. |
| `traits-software-dev` | Cross layout: Architecture / Engineering / Programming / Science around Software Development. |
| `semestertermine` | HTWG SS 2026 key dates table (schematic of screenshot). |
| `pruefungstermine` | Prüfungstermine SoSe 2026 table (schematic of screenshot). |
| `uebungsgruppen` | Moodle AINORGA Übungsgruppen mockup (Gruppe blau/grün schedules). |
| `indigit` | INdigit dashboard UI mockup (sidebar + Projekte Übersicht). |
| `modulhandbuch` | INdigit Modulhandbuch page schematic (Software Engineering module). |
| `stundenplan` | LSF Stundenplan AIN1 weekly grid schematic. |

## Slides skipped (no substantive diagram recreation)

| Slide (0-based) | Reason |
|-----------------|--------|
| 0 Title | Theme title background (`htwgin-titel.png`) used instead of recreating logos. |
| 1 Prof. Boger | Portrait photo only — not recreated (decorative/personal). |
| 16 Tools | Pure text/links already in Marp table; no image. |
| 23 Closing | Text-only closing slide. |

Repeated decorative HTWG logos on every slide were not duplicated into each diagram; Marp footer/theme handles branding.

## Notes

- Screenshots (Moodle, LSF, INdigit, HTWG dates pages) are **annotated schematics**, not pixel-perfect UI clones.
- Open any `.drawio` in [diagrams.net](https://app.diagrams.net/) to edit; re-export SVG if you change the source.
- Theme paths from this lecture folder: `../../themes/htwg.css`, `../../themes/htwgin40.png`, `../../themes/htwgin-titel.png`.

- `language-history` — Programmiersprachen-Zeitlinie (aus Programmiertechnik I, Logos unter `assets/logos/`)

## Editable `.drawio.svg` sources (used by the deck)

- The deck now embeds `diagrams/<name>.drawio.svg`. Each file is a normal SVG whose root `<svg>` carries the uncompressed Draw.io model in its `content` attribute, so it renders in Marp and opens directly in the Draw.io editor (hediet.vscode-drawio) in Cursor/VS Code. **These `.drawio.svg` files are the editable sources used by the deck; edit them rather than the plain `.svg`/`.drawio` files.**
- For diagrams whose `.svg` had been hand-edited after the `.drawio` (curriculum-sem1-4, paradigms, sprachen-ain, studieninhalte-temple, studienverlauf-gesamt, traits-software-dev, uebungsgruppen, vertiefung-katalog, vertiefungsrichtungen, vorlesungen-1sem), the Draw.io model was regenerated from the SVG and the `.drawio` files were updated to match.
- Note: when you save in Draw.io, the SVG body is re-exported by Draw.io; each generated model contains an invisible, locked frame cell that keeps the original canvas size.
