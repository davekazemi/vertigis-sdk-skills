# VertiGIS Studio Web SDK: Deployment & Best Practices

## Overview
Once custom components, services, or workflow activities have been developed and tested locally, they must be bundled and deployed to VertiGIS Studio Web.

---

## 1. Building the Library Package

Compile the production bundle using npm:

```bash
# In the custom library root
npm run build
```

This generates the production output in the `dist/` directory, typically including:
- `main.js`: The bundled JavaScript / AMD library.
- `main.css`: Combined CSS styles.
- `package.json`: Library metadata and version info.

---

## 2. Deployment Options

### Option A: Hosting on a Public or Internal Web Server / CDN
1. Upload the `dist/` folder contents to a web server accessible by your users (e.g., `https://cdn.example.com/vertigis/my-custom-lib/`).
2. Ensure CORS headers (`Access-Control-Allow-Origin: *` or allowed origins) are enabled on the server.
3. In VertiGIS Studio Web Designer or `app-config.json`, add the library URL under `libraries`:
```json
{
  "libraries": [
    "https://cdn.example.com/vertigis/my-custom-lib/main.js"
  ]
}
```

### Option B: Hosting in ArcGIS Online / ArcGIS Enterprise Portal
1. Zip the `dist/` folder.
2. Add the `.zip` file as an Item in ArcGIS Online / Enterprise with type **Web Experience Extension** or **Code Attachment**.
3. Reference the item ID in your VertiGIS Web application configuration.

---

## 3. Best Practices

### A. Performance & Lazy Loading
- Avoid heavy computation in constructors or synchronous rendering loops.
- Use `_load()` and `_unload()` lifecycle hooks to defer heavy resource initialization until components become active.

### B. Decoupled Communication
- Prefer using **Commands and Operations** over tightly coupling components with direct model references where possible.
- Use custom namespaces for your commands/operations (e.g. `myorg.inspection.start`) to avoid collision with core VertiGIS APIs.

### C. State Management
- Use `@serializable` only for properties that should be persisted in `app-config.json`.
- Keep runtime transient state as regular MobX `@observable` fields.
- Clean up event subscriptions and intervals in `_onDestroy()`.

### D. Third-Party Dependencies & Webpack Externals
- **Externals provided by VertiGIS runtime**: The host application already provides core libraries. NEVER bundle duplicate copies of:
  - `@vertigis/web`
  - `@arcgis/core`
  - `react` / `react-dom`
  - `@mui/material`
- **Bundling Utility Libraries**: For pure JavaScript utilities (e.g. `papaparse`, `canvas-confetti`, `qrcode`, `jspdf`), install them via `npm install <package>` and import them directly. They will be bundled into your `dist/main.js` output.
- **Dynamic / Lazy Imports**: For heavy libraries (e.g. Chart.js, PDF generators), use dynamic `import()` to load them on demand only when the user opens the relevant widget or executes the action:
  ```typescript
  async function generateQRCode(text: string): Promise<string> {
      const QRCode = await import("qrcode");
      return QRCode.toDataURL(text);
  }
  ```
