# PowerPoint Design Guide — C3 Indigo

## Color Settings

Set these as **custom theme colors** in PowerPoint (Design → Variants → Colors → Customize Colors):

| Role | Hex | PowerPoint Slot |
|------|-----|-----------------|
| Background 1 | `#F7F6FA` | Background 1 |
| Background 2 | `#ECEAF5` | Background 2 |
| Text/Dark 1  | `#23243A` | Dark 1 |
| Text/Dark 2  | `#8A8CA8` | Dark 2 |
| Accent 1     | `#5B5EA6` | Accent 1 |
| Accent 2     | `#ECEAF5` | Accent 2 |
| Hyperlink    | `#5B5EA6` | Hyperlink |

Border / divider lines: `#D8D6EC`

## Fonts

| Role | Font | Fallback |
|------|------|----------|
| Heading (Latin) | Inter SemiBold | Calibri |
| Body (Latin)    | Inter Regular  | Calibri |
| CJK Heading     | PingFang SC Semibold | Microsoft YaHei |
| CJK Body        | PingFang SC Regular  | Microsoft YaHei |
| Code            | JetBrains Mono | Courier New |

Set in Design → Fonts → Customize Fonts:
- Heading font: **Inter**
- Body font: **Inter**

## Type Scale

| Element | Size | Weight |
|---------|------|--------|
| Slide title | 36–40pt | Bold (700) |
| Section heading | 24–28pt | SemiBold (600) |
| Body text | 18–20pt | Regular (400) |
| Caption / label | 12–14pt | Regular (400) |
| Code snippet | 14pt | Mono Regular |

## Slide Layouts

### Title Slide
- Background: `#F7F6FA`
- Title: 40pt, `#23243A`, centered or left-aligned
- Subtitle / lead: 20pt, `#8A8CA8`
- Accent bar: 4px horizontal rule in `#5B5EA6` below title
- Footer: date + name, 12pt, `#8A8CA8`

### Content Slide
- Background: `#F7F6FA`
- Title: 24pt, `#23243A`, top-left
- Body area: 18pt, `#23243A`
- Highlighted box / callout: fill `#ECEAF5`, border `#D8D6EC`, radius 8pt

### Section Divider Slide
- Background: `#5B5EA6`
- Title: 36pt, `#F7F6FA`, centered
- Subtitle: 18pt, `#F7F6FA` at 75% opacity, centered

### Two-Column Slide
- Left column: text or bullet list
- Right column: image, diagram, or code block
- Divider: 1pt line in `#D8D6EC`

## Component Conventions

**Tags / labels:** Rounded rectangle, fill `#ECEAF5`, text `#5B5EA6`, font 11pt SemiBold
**Code blocks:** Fill `#ECEAF5`, border `#D8D6EC`, font JetBrains Mono 13pt
**Callout box:** Left border 3pt `#5B5EA6`, fill `#ECEAF5`, text 14pt
**Charts:** Primary series `#5B5EA6`, secondary `#8A8CA8`, background `#F7F6FA`, gridlines `#D8D6EC`