# VertiGIS Studio Web SDK: Commands & Operations

## Overview
Commands and Operations are the core message bus and decoupled execution mechanism across VertiGIS Studio Web.

- **Command**: Performs an action / side-effect (asynchronous, returns `void` or `Promise<void>`).
- **Operation**: Calculates or retrieves data (synchronous or asynchronous, returns a value / `Promise<T>`).

---

## 1. Registering Custom Commands and Operations

Custom commands and operations are registered in `src/index.ts` via the `LibraryRegistry`.

### Custom Command Registration
```typescript
// src/index.ts
import { LibraryRegistry } from "@vertigis/web/config";

export default function (registry: LibraryRegistry): void {
    registry.registerCommandHandler({
        name: "custom.highlight-feature",
        // Optional guard: can this command execute right now?
        canExecute: (args, context) => {
            return !!args?.featureId;
        },
        // Execution logic
        execute: async (args, context) => {
            const { featureId } = args;
            console.log(`Highlighting feature ${featureId}`);
            // Perform actions...
        }
    });
}
```

### Custom Operation Registration
```typescript
// src/index.ts
import { LibraryRegistry } from "@vertigis/web/config";

export default function (registry: LibraryRegistry): void {
    registry.registerOperationHandler({
        name: "custom.calculate-buffer",
        execute: async (args, context) => {
            const { geometry, distance } = args;
            // Calculations or queries...
            const bufferedGeometry = await geometryService.buffer(geometry, distance);
            return { buffer: bufferedGeometry };
        }
    });
}
```

---

## 2. Invoking Commands & Operations from Code

In Models (`ComponentModelBase`, `ItemModelBase`) and Services (`ServiceBase`), access the message bus via `this.messages`:

### A. Executing Commands
Commands are organized by namespace under `this.messages.commands.<namespace>.<camelCaseCommandName>`:
```typescript
// UI Notification
await this.messages.commands.ui.displayNotification.execute({
    title: "Success",
    message: "Operation completed successfully.",
    status: "success" // "info" | "success" | "warning" | "error"
});

// UI Component Activation / Toggle
await this.messages.commands.ui.activate.execute({ target: "custom-panel" });
await this.messages.commands.ui.deactivate.execute({ target: "custom-panel" });
await this.messages.commands.ui.toggle.execute({ target: "custom-panel" });

// Map Navigation
await this.messages.commands.map.zoomToExtent.execute({
    target: {
        xmin: -123.4,
        ymin: 48.4,
        xmax: -123.3,
        ymax: 48.5,
        spatialReference: { wkid: 4326 }
    }
});

// Run a VertiGIS Workflow
await this.messages.commands.workflow.run.execute({
    id: "my-inspection-workflow",
    inputs: {
        FacilityID: "FAC-1002",
        Source: "Web SDK Component"
    }
});
```

### B. Executing Operations
Operations return values and are located under `this.messages.operations.<namespace>.<camelCaseOperationName>`:
```typescript
// Query ArcGIS Features
const queryResult = await this.messages.operations.arcgis.queryFeatures.execute({
    url: "https://services.arcgis.com/.../FeatureServer/0",
    where: "STATUS = 'ACTIVE'"
});

// Convert results to CSV / export
const csvData = await this.messages.operations.results.convertToCsv.execute({
    features: queryResult.features
});
```

---

## 3. Invoking from App Configuration (`app-config.json`)

Commands and operations can be bound to buttons, menus, and events in `app-config.json`:

### Simple Action Binding
```json
{
  "id": "zoom-button",
  "$type": "menu-item",
  "title": "Zoom to Initial View",
  "action": "map.zoom-to-initial-viewpoint"
}
```

### Action with Explicit Arguments
```json
{
  "id": "notify-button",
  "$type": "menu-item",
  "title": "Show Info",
  "action": {
    "name": "ui.display-notification",
    "arguments": {
      "title": "Site Information",
      "message": "Processing site data...",
      "status": "info"
    }
  }
}
```

### Command Chaining (Sequential Execution & Pipelining)
When using an array, operations pass their output to the next command/operation in the chain:
```json
{
  "id": "export-action",
  "$type": "menu-item",
  "title": "Export Results to CSV",
  "action": [
    "results.convert-to-csv",
    "system.download-file"
  ]
}
```

---

## 4. Built-in Commands & Operations Reference Guide

### UI Namespace (`ui.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `ui.activate` | Command | Activates a component, tab, or view | `{ target: "component-id" }` |
| `ui.deactivate` | Command | Deactivates a component | `{ target: "component-id" }` |
| `ui.toggle` | Command | Toggles active state of a component | `{ target: "component-id" }` |
| `ui.display-notification` | Command | Displays a toast notification | `{ title?: string, message: string, status?: "info"\|"success"\|"warning"\|"error" }` |
| `ui.display-alert` | Command | Displays a modal alert dialog | `{ title: string, message: string }` |
| `ui.close-panel` | Command | Closes an active side panel | `{ target?: string }` |

### Map Namespace (`map.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `map.zoom-to-viewpoint` | Command | Zooms map to a Viewpoint | `{ viewpoint: __esri.Viewpoint }` |
| `map.zoom-to-extent` | Command | Zooms map to an extent envelope | `{ target: __esri.Extent \| object }` |
| `map.zoom-to-features` | Command | Zooms to one or more graphics/features | `{ maps?: MapModel[], features: __esri.Graphic[] }` |
| `map.zoom-in` | Command | Zooms in one level | `{ maps?: MapModel[] }` |
| `map.zoom-out` | Command | Zooms out one level | `{ maps?: MapModel[] }` |
| `map.zoom-to-initial-viewpoint` | Command | Returns map to initial configured view | `{ maps?: MapModel[] }` |
| `map.draw-graphic` | Command | Draws temporary graphic on the map | `{ geometry: __esri.Geometry, symbol?: __esri.Symbol }` |
| `map.clear-graphics` | Command | Clears all temporary graphics | `{ maps?: MapModel[] }` |
| `map.set-layer-visibility` | Command | Sets visibility of a specific layer | `{ layerId: string, visible: boolean }` |
| `map.refresh-layer` | Command | Refreshes data for a dynamic layer | `{ layerId: string }` |

### Highlights Namespace (`highlights.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `highlights.pulse` | Command | Pulses/flashes feature highlights | `{ features: __esri.Graphic[] }` |
| `highlights.add` | Command | Adds features to persistent highlight set | `{ features: __esri.Graphic[] }` |
| `highlights.clear` | Command | Clears all active highlights | `{}` |

### Results Namespace (`results.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `results.display-details` | Command | Opens feature details pane for selected item | `{ features: __esri.Graphic[] }` |
| `results.remove` | Command | Removes a feature from the results list | `{ features: __esri.Graphic[] }` |
| `results.clear` | Command | Clears all results from the results table/list | `{}` |
| `results.convert-to-csv` | Operation | Converts feature attributes to CSV string/blob | `{ features: __esri.Graphic[] }` |

### Workflow Namespace (`workflow.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `workflow.run` | Command | Runs a VertiGIS Workflow by ID/URL with inputs | `{ id: string, url?: string, inputs?: Record<string, any> }` |

### Auth Namespace (`auth.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `auth.sign-in` | Command | Initiates ArcGIS / Portal sign-in | `{ provider?: string }` |
| `auth.sign-out` | Command | Signs out current user and clears session | `{}` |
| `auth.get-user` | Operation | Retrieves current authenticated user profile | `{}` |

### System Namespace (`system.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `system.download-file` | Command | Triggers browser download for a blob or URL | `{ data: Blob \| string, fileName: string }` |
| `system.open-url` | Command | Opens a URL in a new or current tab | `{ url: string, target?: "_blank" \| "_self" }` |

### ArcGIS Namespace (`arcgis.*`)
| Name | Type | Description | Key Arguments |
| :--- | :--- | :--- | :--- |
| `arcgis.query-features` | Operation | Queries an ArcGIS FeatureLayer or REST endpoint | `{ url: string, where?: string, geometry?: __esri.Geometry }` |
| `arcgis.get-portal-item` | Operation | Fetches portal item metadata | `{ id: string, portalUrl?: string }` |
