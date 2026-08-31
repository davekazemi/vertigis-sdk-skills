# VertiGIS Studio Web SDK: Layout & Application Configuration

## Overview
VertiGIS Studio Web applications are declarative:
- **`app.json` (Layout)**: Defines the DOM layout hierarchy, split panes, panels, toolbars, and slots where components sit.
- **`app-config.json` (Configuration)**: Defines component configuration, data sources, initial state, service configurations, and commands/actions.

---

## 1. Layout Structure (`app.json`)

Layouts are composed of container elements and component placeholders:

```json
{
  "schemaVersion": "1.0",
  "items": [
    {
      "id": "root-layout",
      "itemType": "layout",
      "children": [
        {
          "id": "header-bar",
          "itemType": "header",
          "slot": "header",
          "children": ["app-title", "user-menu"]
        },
        {
          "id": "main-split",
          "itemType": "split",
          "direction": "row",
          "children": [
            {
              "id": "side-panel",
              "itemType": "panel",
              "width": "350px",
              "children": ["my-custom-widget"]
            },
            {
              "id": "map-container",
              "itemType": "panel",
              "children": ["main-map"]
            }
          ]
        }
      ]
    }
  ]
}
```

### Common Layout Item Types
- `layout`: Root layout wrapper.
- `split`: Horizontal or vertical split container (`direction: "row" | "column"`).
- `panel`: Collapsible or fixed content panel.
- `tab-container`: Tabbed navigation container.
- `toolbar`: Action bar holding buttons and tool menus.
- `dialog`: Modal or non-modal popup dialog.

---

## 2. Application Configuration (`app-config.json`)

Components and models referenced by ID in the layout are configured here:

```json
{
  "schemaVersion": "1.0",
  "items": [
    {
      "id": "my-custom-widget",
      "itemType": "custom-widget-model",
      "greetingText": "Welcome to Custom GIS App",
      "themeColor": "#0078d4"
    },
    {
      "id": "main-map",
      "itemType": "map-extension",
      "webMap": "https://www.arcgis.com/sharing/rest/content/items/1234567890abcdef"
    }
  ]
}
```

---

## 3. Model Binding and Dynamic Expressions

### A. Reference Binding (`$ref`)
Inject an existing item model instance by ID:

```json
{
  "id": "my-custom-widget",
  "itemType": "custom-widget-model",
  "map": {
    "$ref": "main-map"
  }
}
```

### B. Evaluated Expressions (`$eval`)
Dynamically resolve values from application state:

```json
{
  "title": {
    "$eval": "app.title + ' - ' + user.username"
  }
}
```

---

## 4. Internationalization (i18n)

Define translation bundles in `src/locales/{lang}.json`:

```json
// src/locales/en.json
{
  "custom-widget-title": "Analytics Dashboard",
  "custom-widget-refresh": "Refresh Data"
}
```

Use in models or React views:
```tsx
import { useI18n } from "@vertigis/web/ui";
import { Typography } from "@mui/material";

export function CustomWidget() {
    const { translate } = useI18n();
    return <Typography variant="h4" sx={{ color: "var(--primaryForeground)" }}>{translate("custom-widget-title")}</Typography>;
}
```
