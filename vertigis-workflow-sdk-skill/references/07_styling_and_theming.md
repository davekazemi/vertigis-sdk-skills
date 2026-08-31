# VertiGIS Studio Workflow SDK: Styling & CSS Variables

## 1. VertiGIS Runtime CSS Variable Tokens

**NEVER hardcode hex colors or fonts.** Always reference VertiGIS runtime CSS variables to guarantee seamless integration across light, dark, and custom branded themes.

| Token | Recommended Purpose |
| :--- | :--- |
| `var(--primaryBackground)` | Main container, form, and page backgrounds |
| `var(--secondaryBackground)` | Card, panel, dialog, and dropdown backgrounds |
| `var(--primaryForeground)` | Primary text, titles, headings |
| `var(--secondaryForeground)` | Secondary / helper / muted labels |
| `var(--primaryAccent)` | Brand color, active highlights, toggle switches |
| `var(--primaryBorder)` | Borders, input field outlines, dividers |
| `var(--emphasizedButtonBackground)` | Primary action / submit button background |
| `var(--buttonForeground)` | Button text on colored backgrounds |
| `var(--itemHoverBackground)` | Hover state background on list items |
| `var(--itemSelectedBackground)` | Selected item / chip background |
| `var(--alertRedBackground)` | Error and alert backgrounds |
| `var(--defaultFont)` | Base font family |

---

## 2. Integrating with Material UI (MUI)

When using `@mui/material` components inside custom form elements, map MUI's theme palette directly to VertiGIS CSS variables:

```typescript
// src/elements/MyElement/styles/theme.ts
import { experimental_extendTheme as extendTheme } from "@mui/material/styles";

export const vertigisMuiTheme = extendTheme({
  cssVarPrefix: "vertigis-element",
  colorSchemes: {
    light: {
      palette: {
        background: {
          default: "var(--primaryBackground)",
          paper: "var(--secondaryBackground)",
        },
        text: {
          primary: "var(--primaryForeground)",
          secondary: "var(--secondaryForeground)",
        },
        primary: {
          main: "var(--primaryAccent)",
          contrastText: "var(--buttonForeground)",
        },
        divider: "var(--primaryBorder)",
      },
    },
  },
  typography: {
    fontFamily: "var(--defaultFont, sans-serif)",
    fontSize: 13,
  },
});
```

---

## 3. STRICT RULE: Use `sx` Prop over `style` or CSS Modules

**NEVER** create `.css` or `.module.css` files. 
**NEVER** use standard React `style={{...}}` objects.
**ALWAYS** use MUI's `sx` prop combined with VertiGIS CSS variable tokens.

```tsx
import { Box, Typography } from "@mui/material";

// ✅ CORRECT: Using MUI Box and sx prop with tokens
<Box
  sx={{
    backgroundColor: "var(--secondaryBackground)",
    color: "var(--primaryForeground)",
    border: "1px solid var(--primaryBorder)",
    borderRadius: 1,
    p: 1.5,
  }}
>
  <Typography 
    variant="body2" 
    sx={{ color: "var(--secondaryForeground)" }}
  >
    Feature ID
  </Typography>
</Box>

// ❌ WRONG: Do not use standard HTML div or style prop
<div
  style={{
    backgroundColor: "var(--secondaryBackground)",
    color: "var(--primaryForeground)",
    border: "1px solid var(--primaryBorder)",
    borderRadius: "4px",
    padding: "12px",
  }}
>
  ...
</div>
```
