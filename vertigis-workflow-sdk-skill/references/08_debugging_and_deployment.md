# VertiGIS Studio Workflow SDK: Development, Debugging & Deployment

## 1. Development Commands

```bash
# Interactively scaffold a new activity or form element
npm run generate

# Start the local development server with hot-reload (HTTPS on port 5000)
npm start

# Create production build output in build/ directory
npm run build
```

---

## 2. Debugging Workflow & Terminal Signals

### Step 1 — Check the Terminal
- If `npm start` is **already running**, changes hot-reload automatically upon file save. **Do NOT run `npm run build`**. Check the terminal output for compiler diagnostics.
- If the terminal is **idle**, start the development server with `npm start`.

### Common Error Diagnoses

| Terminal Output / Message | Root Cause | Solution |
| :--- | :--- | :--- |
| `TS2339: Property 'x' does not exist` | Interface or type mismatch | Inspect inputs/outputs interface or imported type. |
| `does not contain a default export` or `Unsupported AMD module` | Using `import x from "@arcgis/core/geometry/..."` or named imports on function-only modules | Use star imports: `import * as projection from "@arcgis/core/geometry/projection";` |
| `Module not found` | Incorrect relative path | Check relative path and barrel `index.ts` export. |
| `Cannot find module '@vertigis/...'` | Missing SDK package | Verify `package.json` dependencies. |
| `SyntaxError: Unexpected token` | JSX syntax in `.ts` file | Rename file extension from `.ts` to `.tsx`. |

---

## 3. Registering Activity Pack in Workflow Designer

To test custom activities and form elements inside the VertiGIS Studio Workflow Designer:

1. Start local dev server: `npm start` (hosted at `https://localhost:5000`).
2. Open **ArcGIS Online** or **ArcGIS Enterprise Portal**.
3. Navigate to **Content** → **Add Item** → **From URL / Web Mapping Application**.
4. Set URL to: `https://localhost:5000/activitypack.json`.
5. Add Item Tag: `geocortex-workflow-activity-pack` (REQUIRED).
6. Open **VertiGIS Studio Workflow Designer**; the custom activities and form elements will appear in the toolbox sidebar under their defined `@category`.

---

## 4. Third-Party Library Integration & Bundling

When developing activities or form elements that require external JavaScript libraries (e.g. `papaparse` for CSV parsing, `qrcode` for QR rendering, `jspdf` for PDF export):

1. **Install via npm**:
   ```bash
   npm install papaparse
   npm install --save-dev @types/papaparse
   ```
2. **Direct Import**:
   ```typescript
   import Papa from "papaparse";
   
   export function parseCsvData(csvText: string): any[] {
       const parsed = Papa.parse(csvText, { header: true });
       return parsed.data;
   }
   ```
3. **Do NOT install duplicate peer dependencies**: The Workflow host runtime already provides `@arcgis/core`, `react`, and `react-dom`. Never bundle your own duplicate versions of these host libraries.
