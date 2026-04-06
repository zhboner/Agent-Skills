# Canvas Design Guide — C3 Indigo

## Obsidian Canvas

### Node colors

Obsidian Canvas stores node colors as hex strings in the `.canvas` JSON file.
Use these values when setting node background colors:

| Role | Hex | When to use |
|------|-----|-------------|
| Default node | `#ECEAF5` | Standard content nodes |
| Highlighted node | `#5B5EA6` | Key concepts, entry points |
| Muted node | `#F7F6FA` | Supporting / background nodes |
| Warning / note | `#F5EFD8` | Callouts, reminders |

Text color in all nodes: `#23243A`
Node border: `#D8D6EC`

### Canvas JSON snippet — node with design tokens

```json
{
  "id": "node-id",
  "type": "text",
  "x": 0, "y": 0,
  "width": 300, "height": 120,
  "color": "#ECEAF5",
  "text": "Node content here"
}
```

For an accent (highlighted) node, set `"color": "#5B5EA6"` and use white text by
adding a CSS snippet (see below).

### Obsidian CSS snippet for Canvas

Create `~/.obsidian/snippets/canvas-design.css`:

```css
/* C3 Indigo — Obsidian Canvas */
.canvas-node .canvas-node-container {
  font-family: "Inter", "PingFang SC", "Hiragino Sans", sans-serif;
  font-size: 14px;
  color: #23243A;
}

.canvas-node[style*="background-color: #5B5EA6"] .canvas-node-container {
  color: #F7F6FA;
}
```

Enable it in Obsidian → Settings → Appearance → CSS Snippets.

---

## Excalidraw

### Palette to add in Excalidraw

In Excalidraw, open the color picker → add these as custom palette colors:

```
#F7F6FA   (background)
#ECEAF5   (surface / fill)
#5B5EA6   (accent stroke + fill)
#23243A   (text / dark stroke)
#8A8CA8   (muted stroke)
#D8D6EC   (border / light stroke)
```

### Default element style

| Property | Value |
|----------|-------|
| Stroke color | `#23243A` |
| Fill color | `#ECEAF5` |
| Background | `#F7F6FA` |
| Stroke width | 1.5px |
| Stroke style | Solid |
| Fill style | Solid |
| Font | Nunito (closest to Inter in Excalidraw) |
| Font size | 16 |
| Roughness | 0 (architect / clean) |
| Roundness | Round (border-radius on) |

### Accent shape

For key nodes or highlighted boxes:
- Stroke color: `#5B5EA6`
- Fill color: `#5B5EA6`
- Text color: `#F7F6FA`

### Excalidraw JSON theme snippet

Paste into `.excalidraw` file under `"appState"`:

```json
"appState": {
  "currentStrokeColor": "#23243A",
  "currentBackgroundColor": "#ECEAF5",
  "viewBackgroundColor": "#F7F6FA",
  "currentStrokeWidth": 1.5,
  "currentRoughness": 0,
  "currentRoundness": { "type": "adaptive" }
}
```
