# VertiGIS Studio Workflow SDK: Form Element Development

## 1. Form Element Canonical Pattern (MUI Required)

A single `main.tsx` file defines both the component view and its registration object. **ALWAYS use MUI components (e.g., `<TextField>`, `<Box>`).**

```tsx
// src/elements/<Name>/main.tsx
import * as React from "react";
import { FormElementProps, FormElementRegistration } from "@vertigis/workflow";
import { Box, TextField } from "@mui/material";

/**
 * Interface defining the element's public props and state.
 * T is the type of value the element produces.
 */
export interface MyElementProps extends FormElementProps<string> {
  /** Custom configurable property */
  customPlaceholder?: string;
}

/**
 * @displayName My Element Display Name
 * @description Configurable custom input element for Workflow forms.
 */
function MyElement(props: MyElementProps): React.ReactElement {
  const {
    value,
    setValue,
    customPlaceholder = "Enter value...",
    enabled = true,   // Always destructure with safe default
    visible = true,   // Always destructure with safe default
    readOnly = false, // Always destructure with safe default
  } = props;

  // 1. Respect visible prop
  if (!visible) {
    return <></>;
  }

  // 2. Render UI with standard prop wiring
  return (
    <Box sx={{ py: 1 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder={customPlaceholder}
        value={value ?? ""}
        disabled={!enabled}
        inputProps={{ readOnly }}
        onChange={(e) => setValue(e.currentTarget.value)}
        sx={{
          backgroundColor: "var(--primaryBackground)",
          "& .MuiInputBase-input": {
            color: "var(--primaryForeground)"
          },
          "& .MuiOutlinedInput-root": {
            "& fieldset": {
              borderColor: "var(--primaryBorder)",
            },
            "&:hover fieldset": {
              borderColor: "var(--primaryAccent)",
            },
            "&.Mui-focused fieldset": {
              borderColor: "var(--primaryAccent)",
            },
          },
        }}
      />
    </Box>
  );
}

const MyElementRegistration: FormElementRegistration<MyElementProps> = {
  component: MyElement,
  id: "MyElement", // MUST match Custom Type in Workflow Designer
  getInitialProperties: () => ({
    value: undefined,
    enabled: true,
    visible: true,
    readOnly: false,
    customPlaceholder: "Enter text...",
  }),
};

export default MyElementRegistration;
```

### Firing Custom Events (`raiseEvent`)

If your form element needs to trigger custom logic in the workflow (e.g. a "Scan QR Code" button that executes a sub-workflow before returning), use `raiseEvent`. You must also declare the event using the `@event` block tag so the Designer knows it exists.

```tsx
import * as React from "react";
import { FormElementProps, FormElementRegistration } from "@vertigis/workflow";
import { Button } from "@mui/material";

export interface ScannerProps extends FormElementProps<string> {}

/**
 * @displayName Barcode Scanner
 * @description A custom scanner element.
 * @event custom-scan-started Fired when the user clicks scan.
 */
function ScannerElement(props: ScannerProps) {
    const { raiseEvent, enabled } = props;

    const handleScanClick = async () => {
        // Trigger the custom event in the workflow
        await raiseEvent("custom-scan-started");
    };

    return (
        <Button variant="contained" disabled={!enabled} onClick={handleScanClick}>
            Start Scan
        </Button>
    );
}
```

---

## 2. Form Element Props API Reference

| Prop / Callback | Type | Purpose |
| :--- | :--- | :--- |
| `value` | `T` | The primary public value (retrieved via *Get Form Element Property*). |
| `setValue(v: T)` | `(v: T) => void` | Updates the public value in workflow runtime. |
| `setProperty(name, v)` | `(k: string, v: any) => void` | Updates named public property. |
| `raiseEvent(name, data)` | `(name: string, data: any) => void` | Fires a custom event to the workflow. |
| `enabled` | `boolean` | Interactivity toggle (*Set Form Element* → `enabled`). |
| `visible` | `boolean` | Visibility toggle (*Set Form Element* → `visible`). |
| `readOnly` | `boolean` | Read-only mode toggle (*Set Form Element* → `readOnly`). |

---

## 3. CRITICAL — Wiring Standard Props to MUI

The workflow runtime injects `enabled`, `visible`, and `readOnly` automatically. However, they only work if you **destructure them** and **forward them** to the UI:

| Prop | Target HTML / MUI Prop | Rule |
| :--- | :--- | :--- |
| `enabled` | `disabled={!enabled}` | Inverted boolean for standard HTML / MUI |
| `readOnly` | `inputProps={{ readOnly }}` | Forwarded to `inputProps` on MUI components |
| `visible` | `if (!visible) return <></>;` | Conditionally hides DOM element |

---

## 4. CRITICAL — Surviving Tab Changes & Remounts

When workflow forms switch tabs or reload steps, form elements may unmount and remount.

### State Persistence Rules
1. **Always persist critical state in `setValue(...)` or public props** instead of keeping it strictly in local React `useState`.
2. **Rehydrate on mount**: On initial render/mount, read from `props.value` before falling back to initial defaults.
3. **Never overwrite saved state with initial defaults** on remount.
4. If managing complex collections (e.g. drawn geometries, selected layers, table rows), serialize sufficient metadata into `value` so the UI completely restores on remount.
