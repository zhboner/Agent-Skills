# PDF Design Guide — C3 Indigo

## Pandoc (Primary)

### HTML output with design system

Use `html.css` from this directory as the stylesheet:

```bash
pandoc input.md -o output.html --css ~/.claude/skills/frontend-design/html.css --standalone
```

### PDF output via wkhtmltopdf (HTML → PDF)

```bash
pandoc input.md -o output.pdf \
  --css ~/.claude/skills/frontend-design/html.css \
  --pdf-engine=wkhtmltopdf \
  --pdf-engine-opt="--page-size" --pdf-engine-opt="A4" \
  --standalone
```

### YAML Frontmatter (for Pandoc + XeLaTeX PDF engine)

Add this block to the top of any `.md` file:

```yaml
---
geometry: "margin=2.5cm"
fontsize: 11pt
linestretch: 1.5
mainfont: "Inter"
sansfont: "Inter"
monofont: "JetBrains Mono"
CJKmainfont: "PingFang SC"
colorlinks: true
linkcolor: "5B5EA6"
urlcolor: "5B5EA6"
---
```

Run:
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Pandoc inline CSS override

For a quick HTML output without a separate file, add to the YAML front matter:

```yaml
header-includes: |
  <style>
    body { background: #F7F6FA; color: #23243A; font-family: Inter, "PingFang SC", sans-serif; }
    a    { color: #5B5EA6; }
    code { background: #ECEAF5; color: #5B5EA6; border-radius: 4px; padding: 2px 5px; }
  </style>
```

---

## Typst (Future Reference)

### Theme block — paste at top of any `.typ` file

```typst
// ── C3 Indigo Design Tokens ──
#let bg          = rgb("#F7F6FA")
#let surface     = rgb("#ECEAF5")
#let accent      = rgb("#5B5EA6")
#let accent-soft = rgb("#ECEAF5")
#let text-color  = rgb("#23243A")
#let muted       = rgb("#8A8CA8")
#let border      = rgb("#D8D6EC")

#let font-base = ("Inter", "PingFang SC", "Hiragino Sans", "Noto Sans SC")
#let font-mono = ("JetBrains Mono", "Noto Sans Mono CJK SC")

// ── Page setup ──
#set page(fill: bg, margin: 2.5cm)
#set text(font: font-base, size: 11pt, fill: text-color)
#set par(leading: 0.8em)

// ── Headings ──
#show heading.where(level: 1): it => text(size: 24pt, weight: 700, fill: text-color, it)
#show heading.where(level: 2): it => text(size: 18pt, weight: 600, fill: text-color, it)
#show heading.where(level: 3): it => text(size: 14pt, weight: 600, fill: text-color, it)

// ── Code ──
#show raw: it => box(
  fill: surface, stroke: border + 0.5pt,
  inset: (x: 6pt, y: 3pt), radius: 4pt,
  text(font: font-mono, size: 10pt, fill: accent, it)
)
```

### Typst callout box

```typst
#block(
  fill: surface,
  stroke: (left: 3pt + accent, rest: 0.5pt + border),
  inset: 12pt, radius: 6pt,
  width: 100%
)[
  Your callout content here.
]
```
