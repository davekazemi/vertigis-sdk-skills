# VertiGIS Studio Workflow SDK: React Component Decomposition

## Overview & Architecture

When developing complex form elements (e.g. feature inspectors, spatial query builders, sketch editors), components can quickly grow into "god components" exceeding 300+ lines. 

Follow this strict four-pillar decomposition architecture:

```text
src/elements/<ElementName>/
├── main.tsx                  ← Orchestrator: wires hooks + renders sub-components + registration
├── hooks/                    ← State management, event listeners, SDK effects
│   ├── index.ts              ← Barrel export
│   └── useSketchState.ts     ← Custom hook
├── components/               ← Focused, stateless presentational sub-components using MUI
│   ├── index.ts              ← Barrel export
│   ├── StatusBar.tsx
│   └── ActionButtons.tsx
├── styles/                   ← MUI Theme overrides (if needed)
│   └── elementStyles.ts
└── utils/                    ← Pure helper functions, defaults, and types
    ├── types.ts
    ├── defaults.ts
    └── domainUtils.ts
```

---

## 1. Pillar 1: Custom Hooks (`hooks/`)

Extract complex stateful logic, asynchronous calls, and ArcGIS/VertiGIS subscriptions out of JSX:

```typescript
// src/elements/SketchWidget/hooks/useSketchLogic.ts
import { useState, useCallback } from "react";

export function useSketchLogic(initialValue: string | undefined, onValueChange: (val: string) => void) {
  const [activeTool, setActiveTool] = useState<string>("polygon");
  const [featureCount, setFeatureCount] = useState<number>(0);

  const handleDrawComplete = useCallback((geometry: any) => {
    setFeatureCount((prev) => prev + 1);
    onValueChange(JSON.stringify(geometry));
  }, [onValueChange]);

  return {
    activeTool,
    setActiveTool,
    featureCount,
    handleDrawComplete,
  };
}
```

---

## 2. Pillar 2: Presentation Components (`components/`)

Break large JSX templates into single-responsibility, stateless presentation components using MUI (`@mui/material`):

```tsx
// src/elements/SketchWidget/components/StatusBar.tsx
import * as React from "react";
import { Stack, Typography, LinearProgress } from "@mui/material";

interface StatusBarProps {
    statusText: string;
    isProcessing: boolean;
}

export function StatusBar({ statusText, isProcessing }: StatusBarProps) {
    return (
        <Stack spacing={1} sx={{ mt: 2, p: 1, backgroundColor: "var(--secondaryBackground)", borderRadius: "4px" }}>
            <Typography variant="caption" sx={{ color: "var(--secondaryForeground)" }}>
                {statusText}
            </Typography>
            {isProcessing && <LinearProgress color="primary" />}
        </Stack>
    );
}
```

```tsx
// src/elements/SketchWidget/components/ActionButtons.tsx
import * as React from "react";
import { Stack, Button } from "@mui/material";

interface ActionButtonsProps {
    enabled: boolean;
    readOnly: boolean;
    onClear: () => void;
    onSubmit: () => void;
}

export function ActionButtons({ enabled, readOnly, onClear, onSubmit }: ActionButtonsProps) {
    return (
        <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
            <Button
                variant="outlined"
                disabled={!enabled || readOnly}
                onClick={onClear}
                sx={{ borderColor: "var(--primaryBorder)", color: "var(--primaryForeground)" }}
            >
                Clear
            </Button>
            <Button
                variant="contained"
                disabled={!enabled || readOnly}
                onClick={onSubmit}
                sx={{ backgroundColor: "var(--primaryAccent)", color: "var(--buttonForeground)" }}
            >
                Submit
            </Button>
        </Stack>
    );
}
```

Always include a barrel `components/index.ts`:
```typescript
export * from "./StatusBar";
export * from "./ActionButtons";
```

---

## 3. Pillar 3: Pure Utilities & Defaults (`utils/`)

Extract static data configurations, constants, and pure transformations:

```typescript
// src/elements/SketchWidget/utils/defaults.ts
export const SKETCH_DEFAULTS = {
  defaultTool: "polygon",
  maxPoints: 50,
} as const;

// src/elements/SketchWidget/utils/types.ts
export interface SketchFeatureData {
  id: string;
  wkt: string;
}
```

---

## 4. Pillar 4: Orchestration in `main.tsx`

`main.tsx` coordinates hooks, MUI sub-components, and SDK registration:

```tsx
// src/elements/SketchWidget/main.tsx
import * as React from "react";
import { FormElementProps, FormElementRegistration } from "@vertigis/workflow";
import { Box } from "@mui/material";
import { useSketchLogic } from "./hooks";
import { StatusBar, ActionButtons } from "./components";
import { MyElementProps } from "./utils/types";

function SketchWidget(props: MyElementProps): React.ReactElement {
  const { value, setValue, enabled = true, visible = true } = props;
  const { activeTool, setActiveTool, featureCount } = useSketchLogic(value, setValue);

  if (!visible) return <></>;

  return (
    <Box 
      sx={{ 
        p: 1, 
        border: "1px solid var(--primaryBorder)", 
        background: "var(--primaryBackground)" 
      }}
    >
      <StatusBar tool={activeTool} count={featureCount} />
      <ActionButtons enabled={enabled} activeTool={activeTool} onSelectTool={setActiveTool} />
    </Box>
  );
}

const SketchWidgetRegistration: FormElementRegistration<MyElementProps> = {
  component: SketchWidget,
  id: "SketchWidget",
  getInitialProperties: () => ({
    value: undefined,
    enabled: true,
    visible: true,
  }),
};

export default SketchWidgetRegistration;
```
