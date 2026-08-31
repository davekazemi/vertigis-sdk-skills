# VertiGIS Studio Workflow SDK: Block Tags Reference

JSDoc block tags are parsed by the SDK compiler to generate `activitypack.json` metadata used by the Workflow Designer.

---

## 1. Basic Documentation Tags

| Tag | Placement | Purpose / Effect | Example |
| :--- | :--- | :--- | :--- |
| `@displayName` | Class / Property | Label displayed in Designer toolbox and property editor | `@displayName Buffer Distance (m)` |
| `@description` | Class / Property | Detailed tooltip / description text in Designer | `@description The buffer distance around features.` |
| `@required` | Input Property | Marks field as mandatory in Designer UI | `@required` |
| `@category` | Class | Sidebar category grouping in Designer | `@category Spatial Analysis` |
| `@helpUrl` | Class | Link to external online documentation | `@helpUrl https://example.com/help` |
| `@defaultName` | Class | Default activity name when dropped on canvas | `@defaultName bufferActivity1` |

> 💡 **Designer Dropdown Lists**: To render an input property as a predefined dropdown list in the Workflow Designer, you must use an **inline** union of string literals on the property interface (e.g. `type?: "Point" | "Polygon" | "Polyline" | string;`). You cannot extract the type to a separate alias.

## 2. Environment Compatibility Tags

Add these to the **activity class** JSDoc to specify supported execution targets:

| Tag | Effect |
| :--- | :--- |
| `@clientOnly` | Runs exclusively in client browsers / mobile apps (e.g. MapProvider, DOM access). |
| `@serverOnly` | Runs exclusively in server-side workflows. |
| `@onlineOnly` | Requires active internet connectivity. |
| `@supportedApps` | Comma-separated list of compatible applications (e.g. `VSW, EXB`). |
| `@unsupportedApps` | Comma-separated list of incompatible applications. |

### Application Codes (`@supportedApps`)

| Code | Application |
| :--- | :--- |
| **`VSW`** | VertiGIS Studio Web |
| **`EXB`** | ArcGIS Experience Builder |
| **`VSM`** | VertiGIS Studio Mobile |
| **`VSD`** | VertiGIS Studio Desktop (ArcGIS Pro) |
| **`GVH`** | Geocortex Viewer for HTML5 (Legacy) |
| **`WAB`** | ArcGIS Web AppBuilder (Legacy) |

---

## 3. Example Activity Header

```typescript
/**
 * @displayName Buffer Geometry
 * @defaultName bufferGeometry
 * @category Geometry Operations
 * @description Creates a geometric buffer polygon around an input point, line, or polygon.
 * @helpUrl https://developers.vertigisstudio.com/docs/workflow/sdk-web-overview
 * @clientOnly
 * @supportedApps VSW, EXB
 */
export default class BufferGeometryActivity implements IActivityHandler {
  // ...
}
```
