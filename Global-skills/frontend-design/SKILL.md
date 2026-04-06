---
name: frontend-design
description: Use when generating any HTML page, Mermaid diagram, PowerPoint slide, PDF via Pandoc or Typst, Obsidian Canvas, or Excalidraw diagram — applies the Indigo personal design system consistently
---

# Frontend Design System

## Overview

Personal design system for all visual output. Indigo & Warm White palette, Inter + CJK font stack, 8px spacing grid, light mode only.

**ALWAYS apply these tokens. Never invent new colors or fonts.**

## Design Tokens

| Token       | Hex       | Use                          |
| ----------- | --------- | ---------------------------- |
| bg          | `#F7F6FA` | Page / slide background      |
| surface     | `#ECEAF5` | Cards, code blocks, callouts |
| accent      | `#5B5EA6` | Buttons, links, highlights   |
| accent-soft | `#ECEAF5` | Tags, badges                 |
| text        | `#23243A` | Primary body text            |
| muted       | `#8A8CA8` | Captions, secondary text     |
| border      | `#D8D6EC` | Dividers, card borders       |

## Font Stack

```
Latin + CJK: "Inter", "PingFang SC", "Hiragino Sans", "Microsoft YaHei", "Noto Sans SC", sans-serif
Mono:        "JetBrains Mono", "Noto Sans Mono CJK SC", monospace
```

Always use the full font stack for bilingual (English + Chinese/Japanese) content.

## Format Routing

| Format                       | Load                           |
| ---------------------------- | ------------------------------ |
| HTML / CSS                   | `html.css` in this directory   |
| Mermaid diagram              | `mermaid.md` in this directory |
| PowerPoint / .pptx           | `slides.md` in this directory  |
| Pandoc / Typst / PDF         | `pdf.md` in this directory     |
| Obsidian Canvas / Excalidraw | `canvas.md` in this directory  |

When format is ambiguous, use HTML/CSS tokens.

## Rules

1. Apply tokens from the table above — never invent new colors
2. For any CJK content, always use the full bilingual font stack
3. Do not add dark mode unless explicitly asked
4. Load the format-specific file before generating output
