# VertiGIS Studio Workflow SDK: Interactive Scaffolding, Certificates & Tooling

## Overview
When interacting with a developer, the agent follows an interactive consultation protocol ("Grill-Me" mode) to discover project requirements, verify SSL certificates, and generate convenience process management scripts.

---

## 1. Interactive Onboarding & Discovery Flow

```
                     [Skill Triggered]
                             │
                             ▼
              [Scan Workspace for Project Files]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [Existing Project Found]          [Empty / New Workspace]
            │                                 │
   • Ask user intent:                • Ask Target (Activity vs Form Element)
     1. Review Code against Best Practices
     2. Add New Activity
     3. Add New Form Element
     4. Generate Tooling Scripts (start.bat / build.bat)
```

---

## 2. Automated Code Review Checklist (Best Practices)

When the user asks to **"Review my code"**, audit the workflow codebase against these 9 strict criteria:

| # | Checkpoint | Rule / Requirement | Severity |
| :--- | :--- | :--- | :--- |
| 1 | **MUI Mandate for Form Elements** | Form Element views must use `@mui/material` components. NO bare HTML tags (`<div>`, `<button>`, `<input>`). | 🔴 Critical |
| 2 | **No CSS Modules / Inline Styles** | No `.css` files. Styling must use MUI `sx` prop with CSS variable tokens (`var(--primaryBackground)`). | 🔴 Critical |
| 3 | **Wire Standard Props** | Form Elements must destructure and wire `enabled`, `visible`, and `readOnly` (`disabled={!enabled}`, `inputProps={{ readOnly }}`). | 🔴 Critical |
| 4 | **Inline Literal Dropdowns** | Activity input union types must be written *inline* (e.g. `type: 'a' \| 'b' \| string;`) so Designer renders dropdowns. | 🔴 Critical |
| 5 | **ArcGIS Star Imports** | Utility modules (`projection`, `geometryEngine`) must use star imports: `import * as projection from "@arcgis/core/geometry/projection"`. | 🔴 Critical |
| 6 | **Defensive Error Handling** | Activity `execute()` must wrap logic in `try/catch` and throw clean `Error` instances. | 🔴 Critical |
| 7 | **Multiple Outputs Support** | Use `props.setProperty()` for secondary public outputs alongside primary `setValue()`. | 🟡 Medium |
| 8 | **Accessibility (a11y)** | Form Elements must have `aria-label`, `aria-pressed`, and keyboard handlers (`onKeyDown`). | 🟡 Medium |
| 9 | **Tab Remount Resilience** | Initialize state from `props.value` before defaults so form state survives tab changes. | 🟡 Medium |

---

## 3. HTTPS Certificate Generation (OpenSSL)

Workflow SDK local development server runs on HTTPS (`https://localhost:5000/activitypack.json`).

### Option A — Generate Self-Signed Certificate via OpenSSL
```bash
mkdir -p certs
openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```

### Option B — Custom Certificate Path
If the user provides an existing certificate, configure `package.json`:
```json
{
  "scripts": {
    "start": "vertigis-workflow-sdk start --https --key ./certs/key.pem --cert ./certs/cert.pem"
  }
}
```

---

## 4. Helper Scripts Templates

To prevent "Port 5000 already in use" errors during development, scaffold these scripts in the project root:

### `start.bat` (Windows Port Killer & Starter)
```cmd
@echo off
set PORT=5000
echo Checking if port %PORT% is in use...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%PORT%') do (
    echo Killing stale process on port %PORT% (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)
echo Starting VertiGIS Workflow SDK development server on port %PORT%...
npm start
```

### `build.bat` (Windows Build Script)
```cmd
@echo off
echo Building production VertiGIS Workflow activity pack...
npm run build
if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully in build/ directory.
) else (
    echo Build failed with error code %ERRORLEVEL%.
)
```

### `start.sh` (Linux / macOS Port Killer & Starter)
```bash
#!/bin/bash
PORT=5000
echo "Checking if port $PORT is in use..."
PID=$(lsof -ti :$PORT)
if [ ! -z "$PID" ]; then
    echo "Killing stale process on port $PORT (PID: $PID)..."
    kill -9 $PID 2>/dev/null
fi
echo "Starting VertiGIS Workflow SDK development server on port $PORT..."
npm start
```

### `build.sh` (Linux / macOS Build Script)
```bash
#!/bin/bash
echo "Building production VertiGIS Workflow activity pack..."
npm run build
```
