# VertiGIS Studio Web SDK: Commands & Operations

## Overview
Commands and Operations are the primary mechanism for decoupled communication across VertiGIS Studio Web.

- **Command**: Performs an action / side-effect (asynchronous, returns `void` or `Promise<void>`).
- **Operation**: Calculates or retrieves data (synchronous or asynchronous, returns a value / `Promise<T>`).

---

## 1. Registering Custom Commands and Operations

### Custom Command Registration
```typescript
// src/index.ts
registry.registerCommandHandler({
    name: "custom.highlight-feature",
    // Can this command run right now? (Optional guard)
    canExecute: (args, context) => {
        return !!args?.featureId;
    },
    // Execution logic
    execute: async (args, context) => {
        const { featureId } = args;
        console.log(`Highlighting feature ${featureId}`);
        // Side-effect actions...
    }
});
```

### Custom Operation Registration
```typescript
// src/index.ts
registry.registerOperationHandler({
    name: "custom.calculate-buffer",
    execute: async (args, context) => {
        const { geometry, distance } = args;
        // Calculation or query...
        const bufferedGeometry = await geometryService.buffer(geometry, distance);
        return { buffer: bufferedGeometry };
    }
});
```

---

## 2. Invoking Commands & Operations

### A. From TypeScript Code (Models / Services)
Using the messaging bus:
```typescript
// Executing a command
await this.messages.commands.ui.activate.execute({ target: "my-panel" });

// Executing an operation and getting result
const result = await this.messages.operations.arcgis.queryFeatures.execute({
    url: "https://services.arcgis.com/.../FeatureServer/0",
    where: "STATUS = 'ACTIVE'"
});
```

### B. From App Configuration (`app-config.json`)
You can bind button clicks, menu items, or events to command chains:

```json
{
  "id": "my-action-button",
  "itemType": "button",
  "title": "Zoom to Site",
  "action": {
    "name": "map.zoom-to-extent",
    "arguments": {
      "target": {
        "xmin": -123.4,
        "ymin": 48.4,
        "xmax": -123.3,
        "ymax": 48.5,
        "spatialReference": { "wkid": 4326 }
      }
    }
  }
}
```

### C. Command Chaining
Execute multiple commands sequentially or pass operation results into the next command:

```json
{
  "action": [
    {
      "name": "ui.display-notification",
      "arguments": {
        "message": "Starting processing..."
      }
    },
    {
      "name": "custom.highlight-feature",
      "arguments": {
        "featureId": 101
      }
    }
  ]
}
```

### D. From VertiGIS Studio Workflow
Workflows execute commands using the `Run Command` and `Run Operation` activities with the command name (e.g. `ui.activate`, `map.zoom-to-scale`).

---

## 3. Common Core Built-in Commands Reference

| Command Name | Description | Common Arguments |
| :--- | :--- | :--- |
| `ui.activate` | Activates a component or view | `{ "target": "component-id" }` |
| `ui.deactivate` | Deactivates a component | `{ "target": "component-id" }` |
| `ui.toggle` | Toggles component active state | `{ "target": "component-id" }` |
| `ui.display-notification` | Shows a toast notification | `{ "message": "...", "status": "success\|warning\|error" }` |
| `map.zoom-to-viewpoint` | Zooms map to a viewpoint | `{ "viewpoint": { ... } }` |
| `map.zoom-to-extent` | Zooms map to an envelope extent | `{ "target": { "xmin": ..., "ymin": ... } }` |
| `map.draw-graphic` | Draws graphic on temporary map layer | `{ "geometry": { ... }, "symbol": { ... } }` |
| `map.clear-graphics` | Clears temporary graphics from map | `{ "maps": [...] }` |
| `auth.sign-in` | Initiates authentication flow | `{ "provider": "arcgis" }` |
| `auth.sign-out` | Signs out the current user | `{}` |
| `workflow.run` | Runs a VertiGIS Workflow | `{ "id": "workflow-id", "inputs": { ... } }` |
