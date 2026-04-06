# Mermaid Theme — C3 Indigo

## Usage

Paste the `%%{init}%%` block at the top of **every** Mermaid diagram. No exceptions.

## Theme Block (copy-paste)

```
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background":          "#F7F6FA",
    "primaryColor":        "#ECEAF5",
    "primaryTextColor":    "#23243A",
    "primaryBorderColor":  "#D8D6EC",
    "secondaryColor":      "#F7F6FA",
    "tertiaryColor":       "#ECEAF5",
    "lineColor":           "#8A8CA8",
    "edgeLabelBackground": "#F7F6FA",
    "clusterBkg":          "#F7F6FA",
    "clusterBorder":       "#D8D6EC",
    "titleColor":          "#23243A",
    "nodeBorder":          "#D8D6EC",
    "mainBkg":             "#ECEAF5",
    "fontFamily":          "Inter, PingFang SC, Hiragino Sans, sans-serif",
    "fontSize":            "14px"
  }
}}%%
```

## Full Example — Flowchart

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#F7F6FA", "primaryColor": "#ECEAF5",
    "primaryTextColor": "#23243A", "primaryBorderColor": "#D8D6EC",
    "lineColor": "#8A8CA8", "edgeLabelBackground": "#F7F6FA",
    "mainBkg": "#ECEAF5", "nodeBorder": "#D8D6EC",
    "fontFamily": "Inter, PingFang SC, sans-serif", "fontSize": "14px"
  }
}}%%
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No|  D[Other Action]
    C --> E[End]
    D --> E
```

## Accent Node Override

To make a specific node use the accent color `#5B5EA6`, use `style`:

```
style NodeId fill:#5B5EA6,color:#F7F6FA,stroke:#5B5EA6
```