# VertiGIS Studio Workflow SDK: MapProvider & ArcGIS Integration

## 1. Accessing the Map with the `MapProvider` Pattern

Use `MapProvider` when an activity needs direct access to the live ArcGIS `MapView` or `map` object from the host web application (e.g. VertiGIS Studio Web, Experience Builder).

### Required Pattern

```typescript
import { MapProvider } from "@vertigis/workflow/activities/arcgis/MapProvider";
import { activate } from "@vertigis/workflow/Hooks";
import type { IActivityContext } from "@vertigis/workflow/IActivityHandler";
import WebMap from "@arcgis/core/WebMap";

interface ZoomToLayerInputs {
  /**
   * @displayName Layer ID
   * @description The ID of the layer to zoom to.
   * @required
   */
  layerId: string;
}

interface ZoomToLayerOutputs {
  /**
   * @description Whether the zoom action succeeded.
   */
  success: boolean;
}

/**
 * @displayName Zoom To Layer
 * @category Map Utilities
 * @description Zooms the active web map to the extent of a specified layer.
 * @clientOnly
 * @supportedApps VSW, EXB
 */
@activate(MapProvider) // ← Injects MapProvider as 3rd argument to execute()
export default class ZoomToLayerActivity implements IActivityHandler {
  async execute(
    inputs: ZoomToLayerInputs,
    _context: IActivityContext, // ← 2nd argument (prefix with _ if unused)
    type: typeof MapProvider    // ← 3rd argument (always named `type`)
  ): Promise<ZoomToLayerOutputs> {
    // 1. Create and load the map provider
    const mapProvider = type.create();
    await mapProvider.load(); // MUST await load() before accessing map or view

    // 2. Access the map instance
    const map = mapProvider.map as WebMap;
    if (!map) {
      throw new Error("Map is not available");
    }

    // 3. Access the MapView (if needed)
    const view = mapProvider.view as __esri.MapView;

    const layer = map.findLayerById(inputs.layerId);
    if (layer && view) {
      await view.goTo(layer.fullExtent);
      return { success: true };
    }

    return { success: false };
  }
}
```

### Critical Rules for MapProvider
- **Always `await mapProvider.load()`** before accessing `mapProvider.map` or `mapProvider.view`.
- Add `@clientOnly` to JSDoc (MapProvider requires a browser environment).
- Add `@supportedApps VSW, EXB`.
- Do **not** pass `MapView` as an explicit input parameter when using `MapProvider`.

---

## 2. ArcGIS API Import Rules (`@arcgis/core`)

### Type Annotations: Use Ambient `__esri.*`
Never import `@arcgis/core` classes solely for TypeScript type checking:
```typescript
// ✅ CORRECT: Zero bundle overhead
function processGeometry(geom: __esri.Geometry, view: __esri.MapView) { ... }

// ❌ AVOID: Unnecessary import for type-only usage
import Geometry from "@arcgis/core/geometry/Geometry";
```

### Class Modules vs Function-Only Modules
Most `@arcgis/core` modules export a class as their **default export**, but utility/helper modules only export **named functions**:

| Module Type | Examples | Correct Import Syntax |
| :--- | :--- | :--- |
| **Class Modules** (Default Export) | `Graphic`, `Polygon`, `Point`, `FeatureLayer`, `WebMap` | `import Polygon from "@arcgis/core/geometry/Polygon";` |
| **Utility / Function Modules** (No Default Export) | `@arcgis/core/geometry/projection`<br>`@arcgis/core/geometry/geometryEngine`<br>`@arcgis/core/geometry/geometryEngineAsync` | `import * as projection from "@arcgis/core/geometry/projection";`<br>`import * as geometryEngine from "@arcgis/core/geometry/geometryEngine";` |

> ⚠️ **Common Bug**: Writing `import projection from "@arcgis/core/geometry/projection"` causes a build failure (`does not contain a default export`). Furthermore, using named imports like `import { load, project }` can sometimes cause `Unsupported AMD module` runtime errors in certain webpack configurations (as per Esri community guidance). **Always use the star import syntax `import * as moduleName` for geometry helper modules.**
