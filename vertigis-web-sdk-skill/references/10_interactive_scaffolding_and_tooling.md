# VertiGIS Studio Web SDK: Interactive Scaffolding, Certificates & Tooling

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
   • Ask user intent:                • Ask Target Component/Service
     1. Review Code                  • Ask Name & Namespace
     2. Add New Extension            • Ask SSL Certificate Strategy
     3. Generate Tooling Scripts     • Scaffold & Create Helper Scripts
```

---

## 2. Automated Code Review Checklist (Best Practices)

When the user asks to **"Review my code"**, audit the codebase against these 9 strict criteria:

| # | Checkpoint | Rule / Requirement | Severity |
| :--- | :--- | :--- | :--- |
| 1 | **MUI Mandate** | React views must use `@mui/material` components. NO bare HTML tags (`<div>`, `<button>`, `<span>`). | 🔴 Critical |
| 2 | **No CSS Modules** | No `.css` / `.module.css` files. Styling must use MUI `sx` prop with CSS variable tokens (`var(--primaryBackground)`). | 🔴 Critical |
| 3 | **`<LayoutElement>` Wrapper** | All component views must wrap their JSX inside `<LayoutElement {...props}>`. | 🔴 Critical |
| 4 | **MobX `observer()`** | Component views reading model state must be wrapped with `observer()` from `mobx-react-lite`. | 🔴 Critical |
| 5 | **Designer Integration** | Props interface must extend `LayoutElementProperties<TModel>`. | 🔴 Critical |
| 6 | **ArcGIS Star Imports** | Utility modules (`projection`, `geometryEngine`) must use star imports: `import * as projection from "@arcgis/core/geometry/projection"`. | 🔴 Critical |
| 7 | **Error Boundaries** | Custom React views must be wrapped in an `ErrorBoundary` fallback. | 🟡 Medium |
| 8 | **Memory Cleanup** | Subscriptions and timers must be cleaned up in `_onDestroy()`. | 🟡 Medium |
| 9 | **Accessibility (a11y)** | Interactive buttons/inputs must have `aria-label` or `aria-labelledby`. | 🟡 Medium |

---

## 3. HTTPS Certificate Generation (OpenSSL)

VertiGIS Studio Web development requires running the local dev server over HTTPS (typically on port 3000 or 5000).

### Option A — Generate Self-Signed Certificate via OpenSSL
```bash
mkdir -p certs
openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```

### Option B — Custom Certificate Path
If the user provides an existing certificate, configure `package.json` or dev server environment:
```json
{
  "scripts": {
    "start": "vertigis-web-sdk start --https --key ./certs/key.pem --cert ./certs/cert.pem"
  }
}
```

---

## 4. Helper Scripts Templates

To prevent "Port already in use" errors during development, scaffold these scripts in the project root:

### `start.bat` (Windows Port Killer & Starter)
```cmd
@echo off
set PORT=3000
echo Checking if port %PORT% is in use...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%PORT%') do (
    echo Killing stale process on port %PORT% (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)
echo Starting VertiGIS Web SDK development server...
npm start
```

### `build.bat` (Windows Build Script)
```cmd
@echo off
echo Building production VertiGIS Web SDK library bundle...
npm run build
if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully in dist/ directory.
) else (
    echo Build failed with error code %ERRORLEVEL%.
)
```

### `start.sh` (Linux / macOS Port Killer & Starter)
```bash
#!/bin/bash
PORT=3000
echo "Checking if port $PORT is in use..."
PID=$(lsof -ti :$PORT)
if [ ! -z "$PID" ]; then
    echo "Killing stale process on port $PORT (PID: $PID)..."
    kill -9 $PID 2>/dev/null
fi
echo "Starting VertiGIS Web SDK development server..."
npm start
```

### `build.sh` (Linux / macOS Build Script)
```bash
#!/bin/bash
echo "Building production VertiGIS Web SDK library bundle..."
npm run build
```
