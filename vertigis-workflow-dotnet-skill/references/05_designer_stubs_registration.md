# VertiGIS Studio Workflow .NET SDK: Workflow Designer Stubs

## 1. Overview
When custom activities are implemented in .NET (for Mobile, Desktop, or Server), they can be executed by action name with the built-in `RunActivity` activity.

However, to provide a **first-class developer experience in VertiGIS Studio Workflow Designer** (with dedicated toolbox icons, display names, categorized sidebars, and strongly-typed input/output forms), you create a companion **TypeScript Stub Activity Pack**.

---

## 2. Platform Supported Tags (`@supportedApps`)

Use the appropriate `@supportedApps` tag in your TypeScript stub:

| Tag | Target Platform | Description |
| :--- | :--- | :--- |
| `VSM` | VertiGIS Studio Mobile | .NET MAUI / Xamarin Mobile application |
| `VSD` | VertiGIS Studio Desktop | ArcGIS Pro Add-In |
| `VSS` | VertiGIS Studio Workflow Server | On-premises Workflow Server |
| `VSW` | VertiGIS Studio Web | Web applications |

---

## 3. Creating the TypeScript Stub (`src/activities/CalculateBuffer.ts`)

In your companion TypeScript activity pack project:

```typescript
import type { IActivityHandler } from "@vertigis/workflow";

interface CalculateBufferInputs {
    /**
     * @displayName Buffer Distance
     * @description The distance to buffer around the geometry.
     * @required
     */
    distance: number;

    /**
     * @displayName Unit
     * @description Unit of measurement.
     */
    unit?: "meters" | "feet" | "kilometers" | string;

    /**
     * @displayName Show Logger
     * @description Enable debug logging in the console.
     */
    showLogger?: boolean;
}

interface CalculateBufferOutputs {
    /**
     * @description The resulting buffered area in square units.
     */
    result: number;

    /**
     * @description Execution status message.
     */
    status: string;
}

/**
 * @displayName Calculate Buffer
 * @defaultName CalculateBuffer
 * @category Geometry Utilities
 * @description Calculates a spatial buffer around an input point.
 * @action uuid:e9a12345-6789-4abc-def0-123456789abc::CalculateBuffer
 * @supportedApps VSM, VSD, VSS
 */
export default class CalculateBufferActivity implements IActivityHandler {
    async execute(inputs: CalculateBufferInputs): Promise<CalculateBufferOutputs> {
        // Stub implementation - actual execution happens on the .NET host
        throw new Error("This activity is implemented in .NET and must be executed in a .NET environment.");
    }
}
```

---

## 4. Key Rules for TypeScript Stubs

1. **`@action` Tag is Mandatory**: The `@action` tag on the TypeScript class MUST exactly match the `public static string Action` property in the C# class.
2. **`@supportedApps`**: Restrict the activity to the target .NET apps (`VSM`, `VSD`, `VSS`).
3. **Empty / Throwing Body**: The `execute()` method in the stub simply throws an error if called in a web environment, as the real logic runs in .NET.
4. **Publishing the Activity Pack**: Build the stub project with `npm run build` and register `activitypack.json` in ArcGIS Online / Enterprise with tag `geocortex-workflow-activity-pack`.
