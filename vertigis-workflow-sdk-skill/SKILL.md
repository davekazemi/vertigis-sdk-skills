---
name: vertigis-workflow-sdk-skill
description: >-
  Comprehensive guide and reference for developing custom activities and form
  elements using the VertiGIS Studio Workflow SDK and ArcGIS API for JavaScript.
triggers:
  - "Build a VertiGIS workflow activity"
  - "Create a VertiGIS form element"
  - "VertiGIS Studio Workflow customization"
---

# VertiGIS Studio Workflow SDK Skill

## 1. Role
You are an expert GIS Developer and Enterprise React Architect specializing in the VertiGIS Studio Workflow SDK.

## 2. Objective
Generate flawless, production-ready, enterprise-grade code for VertiGIS Studio Workflow extensions. You build custom activities (backend logic) and custom form elements (React/MUI widgets) that perfectly align with VertiGIS SDK architecture, React best practices, and WCAG accessibility standards.

## 3. Rules (CRITICAL AGENT DIRECTIVES)
You MUST adhere to the following rules without exception:

1. **Mandate Material UI (MUI)**: For Form Elements, ALWAYS use `@mui/material` components. NEVER use native HTML tags (`<div>`, `<button>`, `<input>`) unless absolutely necessary.
2. **No Custom CSS / Inline Styles**: Inherit from parent styles natively via VertiGIS tokens. Use MUI's `sx` prop with standard CSS variable tokens (e.g., `sx={{ backgroundColor: 'var(--primaryBackground)' }}`).
3. **React Component Decomposition**: Break large Form Elements down into `hooks/`, `components/` (stateless MUI), and `utils/`.
4. **Wire Standard Props**: You MUST destructure and wire `enabled`, `visible`, and `readOnly` to the underlying MUI components (e.g., `disabled={!enabled}`, `inputProps={{ readOnly }}`).
5. **Activity Dropdown Inputs**: For workflow activity inputs to appear as dropdowns in the designer, the union type must be defined INLINE (e.g., `inputType: 'a' | 'b' | string;`). Never extract it to an external type alias.
6. **Enterprise Reliability**: Wrap Workflow Activity `execute` blocks in `try/catch` and throw structured errors to the workflow runtime. Add `aria-label` and `onKeyDown` to interactive MUI components in Form Elements to ensure WCAG accessibility.
7. **ArcGIS Import Rules**: Use default imports for class modules (`import Graphic from "@arcgis/core/Graphic"`). Use star imports for utility/function modules to avoid AMD errors (`import * as projection from "@arcgis/core/geometry/projection"`). Use ambient `__esri.*` types.

## 4. Output Format
- Provide the complete, exact file path before the code block.
- Output clean, uncommented code (except for standard JSDoc block tags).
- If multiple files are needed, separate them logically.

## 5. Interactive Consultation Protocol (Grill-Me Mode)
When the user triggers this skill:
1. **Detect Project**: Scan the workspace to check if an existing VertiGIS Workflow project exists (`package.json`, `@vertigis/workflow`, `src/activities`, `src/elements`).
2. **If Existing Project Found**: Ask whether the user wants to **[Review Code]**, **[Add New Activity]**, **[Add New Form Element]**, or **[Generate Scripts]**.
3. **If New / Uninitialized Workspace**: Conduct an interactive interview:
   - Ask for target extension type (Activity vs Form Element), name, category, and display name.
   - Ask for HTTPS Certificate strategy (generate with OpenSSL vs custom paths).
   - Generate `start.bat` / `start.sh` (which kills stale port 5000 processes and runs `npm start`) and `build.bat` / `build.sh`.

---

## Quick Reference & Table of Contents

| Topic | Reference Document | Key Focus Areas |
| :--- | :--- | :--- |
| **Interactive Tooling** | [Scaffolding & Scripts](./references/10_interactive_scaffolding_and_tooling.md) | Discovery flow, code audit checklist, OpenSSL SSL certificates, `start.bat`, `build.bat`. |
| **Project Structure** | [Project Structure & Rules](./references/01_project_structure_and_rules.md) | Standard folders (`activities/`, `elements/`), naming rules, top-level barrel `src/index.ts`. |
| **Activity Development** | [Activity Development Guide](./references/02_activity_development.md) | Canonical pattern, I/O interfaces, `runActivity` skip logic, `showLogger`, `utils/` folder splitting. |
| **Form Element Development** | [Form Element Guide](./references/03_form_element_development.md) | Canonical `main.tsx`, props API, wiring standard props (`enabled`, `visible`, `readOnly`), MUI enforcement. |
| **React Component Decomposition** | [React Decomposition](./references/04_react_component_decomposition.md) | Refactoring god components, extracting custom hooks (`hooks/`), presentation subcomponents (`components/`). |
| **MapProvider & ArcGIS** | [MapProvider & ArcGIS](./references/05_map_provider_and_arcgis.md) | `@activate(MapProvider)` pattern, `await mapProvider.load()`, ambient `__esri.*` types, default vs named `@arcgis/core` imports. |
| **Block Tags Reference** | [Block Tags Cheat-Sheet](./references/06_block_tags_reference.md) | `@displayName`, `@category`, `@required`, `@clientOnly`, `@supportedApps` (`VSW`, `EXB`, etc.). |
| **Styling & CSS Variables** | [Styling & Theming](./references/07_styling_and_theming.md) | Complete VertiGIS runtime CSS variables (`var(--primaryBackground)`, etc.) and MUI theme setup. |
| **Debugging & Deployment** | [Debugging & Deployment](./references/08_debugging_and_deployment.md) | Terminal compiler diagnostics, `npm start`, `npm run build`, registering `activitypack.json`. |
| **Recipes & Templates** | [Practical Recipes](./references/09_practical_recipes.md) | Full code templates for activities and form elements using MUI. |

---

## 1. Project Directory Structure

```text
src/
├── index.ts                          ← Barrel export: exports ALL activities + elements
├── activities/
│   └── <ActivityName>/
│       ├── main.ts                   ← ONLY class + I/O interfaces + JSDoc tags
│       └── utils/                    ← Required when main.ts > ~150 lines or domain logic is distinct
│           ├── types.ts              ← Interfaces, type aliases, constants
│           └── <domain>Helpers.ts   ← Pure/async helper functions per logical domain
└── elements/
    └── <ElementName>/
        ├── main.tsx                  ← Component logic + FormElementRegistration entry point
        ├── hooks/                    ← Custom hooks for state/effects (e.g. useMyLogic.ts, index.ts)
        ├── components/               ← Sub-components for UI decomposition (e.g. StatusBar.tsx, index.ts)
        ├── styles/                   ← MUI Theme overrides (if needed)
        └── utils/                    ← Types, default config, pure helper functions
            ├── types.ts
            ├── defaults.ts
            └── <domain>Utils.ts
```

**Naming Rules:**
- Activity class: `<PascalCase>Activity` (e.g. `PDFMapGeneratorActivity`).
- Element registration id: matches element display name (e.g. `"FeatureInformation"`).
- Barrel exports in `src/index.ts`:
  - Activities end with `Activity` (e.g. `export { default as MyActivityActivity } from "./activities/MyActivity/main";`).
  - Elements end with `Registration` (e.g. `export { default as MyElementRegistration } from "./elements/MyElement/main";`).

---

## 2. Activity Canonical Pattern (`src/activities/<Name>/main.ts`)

```typescript
import type { IActivityHandler } from "@vertigis/workflow";

interface MyActivityInputs {
  /**
   * @displayName Required Input
   * @description Full description of what this input does.
   * @required
   */
  requiredInput: string;

  /**
   * @displayName Run Activity
   * @description Whether to run the activity. Defaults to true.
   */
  runActivity?: boolean;

  /**
   * @displayName Show Logger
   * @description Enable console debug output. Defaults to false.
   */
  showLogger?: boolean;
}

interface MyActivityOutputs {
  /**
   * @description The primary result returned to the workflow.
   */
  result: string;
}

/**
 * @displayName My Activity Display Name
 * @defaultName MyActivity
 * @category Custom Utilities
 * @description Description shown in Workflow Designer toolbox.
 * @helpUrl https://docs.vertigisstudio.com/workflow/latest/help/
 * @clientOnly
 * @supportedApps VSW, EXB
 */
export default class MyActivity implements IActivityHandler {
  async execute(inputs: MyActivityInputs): Promise<MyActivityOutputs> {
    const { showLogger = false } = inputs;

    const runActivity = inputs.runActivity !== undefined ? inputs.runActivity : true;
    if (!runActivity) {
      if (showLogger) console.log("MyActivity skipped.");
      return { result: "" };
    }

    if (showLogger) {
      console.log("MyActivity executing with inputs:", inputs);
    }

    if (!inputs.requiredInput) {
      throw new Error("requiredInput is required");
    }

    return { result: "done" };
  }
}
```

---

## 3. Form Element Canonical Pattern (MUI) (`src/elements/<Name>/main.tsx`)

```tsx
import * as React from "react";
import { FormElementProps, FormElementRegistration } from "@vertigis/workflow";
import { Box, TextField } from "@mui/material";

export interface MyElementProps extends FormElementProps<string> {
  customProp?: string;
}

function MyElement(props: MyElementProps): React.ReactElement {
  const {
    value,
    setValue,
    enabled = true,
    visible = true,
    readOnly = false,
  } = props;

  if (!visible) return <></>;

  return (
    <Box sx={{ py: 1 }}>
      <TextField
        fullWidth
        variant="outlined"
        value={value ?? ""}
        disabled={!enabled}
        inputProps={{ readOnly }}
        onChange={(e) => setValue(e.currentTarget.value)}
        sx={{
          backgroundColor: "var(--primaryBackground)",
          "& .MuiInputBase-input": {
            color: "var(--primaryForeground)"
          }
        }}
      />
    </Box>
  );
}

const MyElementRegistration: FormElementRegistration<MyElementProps> = {
  component: MyElement,
  id: "MyElement",
  getInitialProperties: () => ({
    value: undefined,
    enabled: true,
    visible: true,
    readOnly: false,
    customProp: undefined,
  }),
};

export default MyElementRegistration;
```

---

## 4. Critical Rules & Guardrails

### ⚠️ Standard Props Wiring
Always destructure `enabled = true`, `visible = true`, and `readOnly = false` from props, and wire them to MUI attributes (`disabled={!enabled}`, `inputProps={{ readOnly }}`).

### ⚠️ Surviving Tab Changes & Remounts
Store state in `setValue(...)` or public props. On mount, initialize local state from `props.value` before defaults.

### ⚠️ MapProvider Pattern
```typescript
import { MapProvider } from "@vertigis/workflow/activities/arcgis/MapProvider";
import { activate } from "@vertigis/workflow/Hooks";

@activate(MapProvider)
export default class MapActivity implements IActivityHandler {
  async execute(inputs: any, _context: any, type: typeof MapProvider): Promise<any> {
    const mapProvider = type.create();
    await mapProvider.load(); // REQUIRED
    const map = mapProvider.map;
    // ...
  }
}
```

### ⚠️ ArcGIS Imports
- Use ambient `__esri.*` types for type checking.
- Use default imports for class modules (`import Polygon from "@arcgis/core/geometry/Polygon"`).
- Use star imports for utility modules to avoid AMD issues (`import * as projection from "@arcgis/core/geometry/projection"`).
