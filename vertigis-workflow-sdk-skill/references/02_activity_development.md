# VertiGIS Studio Workflow SDK: Activity Development

## 1. Activity Canonical Pattern (`src/activities/<Name>/main.ts`)

```typescript
import type { IActivityHandler } from "@vertigis/workflow";

/**
 * An interface that defines the inputs of the activity.
 */
interface MyActivityInputs {
  /**
   * @displayName Required Parameter
   * @description Full description of what this input does.
   * @required
   */
  requiredInput: string;

  /**
   * @displayName Optional Parameter
   * @description Description of optional input.
   */
  optionalInput?: number;

  /**
   * @displayName Run Activity
   * @description Whether to run the activity. Defaults to true. If false, the activity is skipped.
   */
  runActivity?: boolean;

  /**
   * @displayName Show Logger
   * @description Enable console debug output. Defaults to false.
   */
  showLogger?: boolean;

  /**
   * @displayName Theme Style
   * @description Select the theme style.
   */
  theme?: "light" | "dark" | "system" | string; // MUST BE INLINE
}

/**
 * An interface that defines the outputs of the activity.
 */
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
 * @description One-sentence description shown in the Workflow Designer toolbox.
 * @helpUrl https://docs.vertigisstudio.com/workflow/latest/help/
 * @clientOnly
 * @supportedApps VSW, EXB
 */
export default class MyActivity implements IActivityHandler {
  async execute(inputs: MyActivityInputs): Promise<MyActivityOutputs> {
    const { showLogger = false } = inputs;

    // 1. Conditional Execution Check
    const runActivity = inputs.runActivity !== undefined ? inputs.runActivity : true;
    if (!runActivity) {
      if (showLogger) console.log("MyActivity skipped (runActivity = false)");
      return { result: "" };
    }

    try {
      // 2. Debug Logger
      if (showLogger) {
        console.log("MyActivity executing with inputs:", inputs);
      }

      // 3. Guard Missing Inputs
      if (!inputs.requiredInput) {
        throw new Error("requiredInput is required");
      }

      // 4. Execution (Orchestration only - delegate heavy domain logic to utils/)
      return { result: "completed" };
      
    } catch (error) {
      // 5. Defensive Error Handling
      console.error("MyActivity failed:", error);
      throw new Error(`MyActivity execution failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
}
```

---

## 2. Mandatory Activity Rules

1. **Orchestrator Only**: `main.ts` should only contain the class definition, I/O interfaces, and top-level orchestration. Complex helper logic belongs in `utils/`.
2. **Class Default Export**: The class must be exported as `export default class <Name>Activity`.
3. **Exact Return Types**: `execute` return type must be typed as `Promise<MyActivityOutputs>` or `MyActivityOutputs`, **never** `any` or `Promise<any>`.
4. **JSDoc Block Tags**: Every input property must have `@displayName` and `@description`. Mark mandatory inputs with `@required`.
5. **Debug Flag (`showLogger`)**: Standard optional debug toggle `showLogger?: boolean` on all activities.
6. **Conditional Execution (`runActivity`)**: If an activity can be skipped conditionally, implement `runActivity?: boolean` and return a safe, typed empty output:
   - `string` → `""`
   - `number` → `0`
   - `boolean` → `false`
   - `array` → `[]`
   - `File` / `Blob` → `null as unknown as File`
   - `object` → `{}`
7. **Dropdown / Dynamic Selection Inputs**: If you want an input parameter to appear as a dropdown with predefined options in the Workflow Designer, you MUST define the string literal union type *inline* on the input interface. If you extract the type to a `type` alias or interface elsewhere, the Designer will not recognize the options.
   - ✅ Correct: `inputType: 'a' | 'b' | string;`
   - ❌ Wrong: `inputType: MyOptions;`
8. **Defensive Error Handling**: Always wrap the core execution logic in a `try/catch` block. Surface meaningful errors back to the workflow runtime using `throw new Error(...)` rather than letting the activity crash silently.

---

## 3. Splitting Complex Activities (`utils/`)

When `main.ts` would exceed ~150 lines or handles multiple domains:

### `utils/types.ts`
```typescript
export interface BufferCalculationOptions {
  distance: number;
  unit: "meters" | "feet" | "kilometers";
}
```

### `utils/<domain>Helpers.ts`
```typescript
import { BufferCalculationOptions } from "./types";

/**
 * Calculates polygon buffer using geometry engine.
 */
export async function computeBuffer(
  geometry: __esri.Geometry,
  options: BufferCalculationOptions
): Promise<__esri.Polygon> {
  // Pure helper logic
  return {} as __esri.Polygon;
}
```
