---
name: infographic-poster
description: >
  Create beautiful, print-quality editorial infographic posters as inline HTML widgets.
  Use this skill whenever the user wants to turn structured information into a visual
  poster, guide, cheatsheet, reference card, or infographic — especially when they
  upload an image to recreate, say "make this into a poster", "design an infographic",
  "create a visual summary", "make a cheatsheet", or ask for any shareable visual
  document. Also trigger when the user wants to recreate or remix an existing poster
  design. Works for any language; CJK fonts are always loaded by default.
---

# Infographic Poster Skill

Produces a single self-contained HTML widget rendered inline via `show_widget`.
The output should feel like a professionally designed printed document — not a webpage.

---

## Step 1 — Analyse the request

Before writing any code, answer these questions mentally:

1. **Content type**: Is this a how-to guide, risk matrix, comparison, timeline, data summary, reference card, or something else? The layout should match.
2. **Language**: Detect the primary language. CJK content requires the font stack below.
3. **Tone**: Infer from content — technical/developer → monospace accents; editorial/brand → serif headline; playful → rounded sans.
4. **Palette**: Derive freely from the content's mood, the user's image, or brand context. Don't default to the same palette every time — variety is the point.

If the user uploads an image, study its layout, hierarchy, and color palette before designing — match the spirit, not necessarily the pixels.

---

## Step 2 — Design the palette

There are no fixed presets. Instead, ask: *what feeling should this poster evoke?*

- **Warm / human / analog** → off-white or cream backgrounds (`#F5F0E8`, `#FAF7F2`), warm grays for muted text
- **Cool / technical / precise** → light blue-gray backgrounds (`#F0F4F8`, `#EEF2F7`), near-navy text
- **Dark / dramatic / high-contrast** → near-black background (`#1A1A1A`, `#111827`), light cream text, a single vivid accent
- **Vibrant / brand / opinionated** → saturated background or surface color, pull from the user's brand palette if given
- **Minimal / editorial** → pure white surface, maximum whitespace, single ink color, one restrained accent

When deriving from an uploaded image, sample 2–3 dominant hues and build the variable set from those.

**The only hard rules:**
- Always define colors as CSS variables (never hardcode hex in component rules)
- Keep accents to 2–3 at most — one primary, one semantic (danger/safe), one optional highlight
- Ensure enough contrast between `--text` and `--bg` for readability (aim for 4.5:1+)

---

## Step 3 — Font stack (always include both)

Always load these two `@import` lines. They cover Latin + CJK in one shot:

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
```

**Usage rules:**
- **Headlines**: `font-family: 'Noto Serif SC', serif; font-weight: 700`
- **Body text**: `font-family: 'Noto Serif SC', serif; font-weight: 400`
- **Labels, tags, metadata, code**: `font-family: 'IBM Plex Mono', monospace`
- For Latin-only content where serif feels wrong, swap to a Google Sans or Fraunces — but always keep IBM Plex Mono for labels.

---

## Step 4 — Layout toolkit

Use these building blocks. Mix and match based on content type.

### Poster shell
```css
.poster {
  background: var(--bg);
  color: var(--text);
  padding: 48px 44px 56px;
  max-width: 580px;
  margin: 0 auto;
  border: 1px solid var(--border);
}
```

### Eyebrow / metadata line
Small monospace label above the hero title. Good for category, date, version.
```html
<div class="eyebrow">Claude Code 封号指南 · 用户版</div>
```
```css
.eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 12px; }
```

### Hero title
```css
.hero-title { font-size: 52px; font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; margin: 0 0 12px; }
```
Scale down for longer titles: 40px for 8–14 chars, 32px for 15+.

### Section opener (tag + title pattern)
```html
<div class="section-tag tag-safe">✓ 安全指南</div>
<h2 class="section-title">这样做，基本没事</h2>
```
```css
.section-tag { font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.12em; padding: 3px 8px; border-radius: 3px; display: inline-block; margin-bottom: 10px; }
.tag-safe { background: #D4E8CC; color: #2E6020; }
.tag-risk { background: #F5D5CC; color: #8B2A1A; }
.tag-neutral { border: 1px solid var(--border); color: var(--muted); }
```

### Checklist
Good for "do this / don't do this" guides.
```html
<ul class="check-list">
  <li>
    <div class="check-icon"><!-- SVG checkmark --></div>
    <div>
      <div class="check-main">Bold point here</div>
      <div class="check-sub">Supporting detail — keep under 2 lines</div>
    </div>
  </li>
</ul>
```
```css
.check-list { list-style: none; padding: 0; margin: 0 0 32px; }
.check-list li { display: grid; grid-template-columns: 22px 1fr; gap: 10px; margin-bottom: 16px; align-items: start; }
.check-icon { width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px; }
.check-main { font-size: 14px; font-weight: 700; line-height: 1.4; }
.check-sub { font-size: 12px; color: var(--muted); margin-top: 3px; line-height: 1.55; }
```

### Risk / feature grid (2-col cards)
Good for ranked items, feature comparisons, step breakdowns.
```css
.card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 32px; }
.card { background: var(--surface); border: 1px solid var(--border); border-bottom: 3px solid var(--accent-danger); border-radius: 4px; padding: 14px; }
.card-num { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--muted); margin-bottom: 6px; }
.card-title { font-size: 14px; font-weight: 700; line-height: 1.3; margin-bottom: 6px; }
.card-desc { font-size: 11px; color: var(--muted); line-height: 1.55; }
```
Change `border-bottom` color to signal severity: danger red, warning amber, info blue, success green.

### Inline tag cloud
Good for showing "what the system knows / tracks / exposes".
```css
.tags { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { font-size: 12px; padding: 6px 12px; border-radius: 4px; border: 1px solid var(--border); background: var(--surface); line-height: 1; }
.tag.highlight { background: var(--text); color: var(--bg); border-color: var(--text); font-weight: 700; }
```

### Divider
```html
<hr style="border: none; border-top: 1px solid var(--border); margin: 28px 0;">
```

### Footer bar
```html
<div class="bottom-bar">
  <span class="mono-small">@handle · source</span>
  <span class="mono-small">Date</span>
</div>
```
```css
.bottom-bar { display: flex; justify-content: space-between; margin-top: 32px; padding-top: 16px; border-top: 1px solid var(--border); }
.mono-small { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--muted); }
```

---

## Step 5 — CSS variable block (always start with this)

```css
:root {
  --bg: #F5F0E8;         /* poster background */
  --surface: #FDFAF5;    /* card/chip surface */
  --text: #1A1A1A;       /* primary text */
  --muted: #6A6258;      /* secondary text */
  --border: #D8D0C0;     /* borders and dividers */
  --accent-safe: #4A8C38;
  --accent-danger: #C0402A;
  --accent-info: #2563EB;
}
```
Swap values for other palettes. Never hardcode colors outside this block.

---

## Step 6 — Quality checklist before rendering

- [ ] Max-width is 560–620px (poster width, not full-viewport)
- [ ] No more than 3 font sizes (hero ~48px, body 14px, label 11–12px)
- [ ] Monospace only on metadata/labels/code, serif/sans on everything else
- [ ] Section tags use color meaningfully and consistently within this poster
- [ ] Cards use `border-bottom` accent, not `border-left` (more editorial)
- [ ] Footer credits source and date
- [ ] CJK font import is present even for mixed-language content
- [ ] All colors reference CSS variables, no hardcoded hex in component rules

---

## Common layout patterns

| Content type | Recommended layout |
|---|---|
| How-to / safety guide | Eyebrow → Hero → Checklist → Card grid → Tag cloud → Footer |
| Comparison / vs | Eyebrow → Hero → 2-col card grid (one per option) → Summary row |
| Timeline / steps | Eyebrow → Hero → Numbered vertical list with connector lines |
| Reference / cheatsheet | Eyebrow → Hero → Multiple section groups with dividers |
| Risk matrix | Eyebrow → Hero → Color-coded 2×2 or 2×3 card grid |
| Data summary | Eyebrow → Hero → Metric row → Chart area → Notes |

---

## Notes

- Always render via `show_widget`, not as a file download, unless the user explicitly asks for an HTML file.
- If the user provides an image to recreate, match the information architecture (what goes where) rather than copying exact pixel positions.
- Keep the poster self-contained — no external data fetches, no JS interactivity unless specifically requested.
- For very long content, split into logical sections with `<hr>` dividers rather than making the poster taller than ~1800px.
