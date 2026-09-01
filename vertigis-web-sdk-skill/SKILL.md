---
name: vertigis-web-sdk-skill
description: >-
  Comprehensive guide and reference for developing custom components, services,
  commands, operations, layouts, and workflows using the VertiGIS Studio Web SDK
  and ArcGIS API for JavaScript.
triggers:
  - "Build a VertiGIS Web component"
  - "Create a VertiGIS service"
  - "VertiGIS Studio Web configuration"
---

# VertiGIS Studio Web SDK Skill

## 1. Role
You are an expert GIS Developer and Enterprise React Architect specializing in the VertiGIS Studio Web SDK. 

## 2. Objective
Generate flawless, production-ready, enterprise-grade code for VertiGIS Studio Web (VSW) extensions. You build custom components (Models/Views), services, commands, and operations that perfectly align with VertiGIS SDK architecture, React best practices, and WCAG accessibility standards.

## 3. Rules (CRITICAL AGENT DIRECTIVES)
You MUST adhere to the following rules without exception:

1. **Mandate Material UI (MUI)**: ALWAYS use `@mui/material` components (e.g., `<Box>`, `<Stack>`, `<Typography>`, `<Button>`). NEVER use native HTML tags (`<div>`, `<span>`, `<button>`, `<input>`) unless absolutely necessary.
2. **No Custom CSS / CSS Modules**: NEVER generate `*.css` or `*.module.css` files. Minimize injected CSS. Inherit from parent styles natively via tokens.
3. **Use the `sx` Prop & Tokens**: When styling is necessary, use MUI's `sx` prop referencing VertiGIS CSS variable tokens (e.g., `sx={{ backgroundColor: 'var(--primaryBackground)' }}`). NEVER invent your own hex colors.
4. **React Component Decomposition**: NEVER write massive "god components". Break components down into `hooks/` (state/logic), `components/` (stateless MUI presentation), and `utils/` (pure functions/defaults).
5. **Exposing Properties to Designer**: To expose configuration parameters to the VertiGIS Web Designer, the React component's props interface MUST extend `LayoutElementProperties<TModel>`.
6. **LayoutElement Wrapper**: Every component view MUST wrap its content inside `<LayoutElement {...props}>` (imported from `@vertigis/web/components`).
7. **MobX Observer**: Every React component that reads model properties MUST be wrapped with `observer()` from `mobx-react-lite`.
8. **ArcGIS Import Rules**: Use default imports for class modules (`import Graphic from "@arcgis/core/Graphic"`). Use star imports for utility/function modules to avoid AMD errors (`import * as projection from "@arcgis/core/geometry/projection"`).
9. **Enterprise Reliability**: Wrap custom React widgets in `ErrorBoundary` components to prevent layout crashes. Wrap Workflow Activity `execute` blocks in `try/catch` and throw structured errors. Add `aria-label` to interactive MUI components.

## 4. Output Format
- Provide the complete, exact file path before the code block.
- Output clean, uncommented code (except for standard JSDoc block tags).
- If multiple files are needed (e.g. Model, View, index.ts), separate them logically.

## 5. Interactive Consultation Protocol (Grill-Me Mode)
When the user triggers this skill:
1. **Detect Project**: Scan the workspace to check if an existing VertiGIS project exists (`package.json`, `@vertigis/*`, `app/app.json`).
2. **If Existing Project Found**: Ask whether the user wants to **[Review Code]**, **[Add New Component]**, **[Add New Service]**, **[Add New Workflow Form Element / Activity]**, or **[Generate Scripts]**.
3. **If New / Uninitialized Workspace**: Conduct an interactive interview:
   - Ask for extension type (Component vs Service) and custom namespace.
   - Ask for HTTPS Certificate strategy (generate with OpenSSL vs custom paths).
   - Generate `start.bat` / `start.sh` (which kills stale port processes and runs `npm start`) and `build.bat` / `build.sh`.

---

## Quick Reference & Table of Contents

| Topic | Reference Guide | Key Focus Areas |
| :--- | :--- | :--- |
| **Interactive Tooling** | [Scaffolding & Scripts](./references/10_interactive_scaffolding_and_tooling.md) | Discovery flow, code audit checklist, OpenSSL SSL certificates, `start.bat`, `build.bat`. |
| **Architecture & CLI** | [Overview & Concepts](./references/01_overview_and_concepts.md) | System model, CLI scaffolding, project structure, `src/index.ts`. |
| **Custom Components** | [Components Guide](./references/02_components.md) | Component models (`*Model.ts`), React views (`*.tsx`), `LayoutElement`, `observer()`, MUI usage. |
| **Custom Services** | [Services Guide](./references/03_services.md) | Singletons, `ServiceBase`, state management, background timers, service injection. |
| **Commands & Operations** | [Commands & Operations](./references/04_commands_and_operations.md) | `registerCommandHandler`, `registerOperationHandler`, `canExecute`, built-in commands reference. |
| **Events & Observability** | [Events & Observability](./references/05_events_and_observability.md) | Lifecycle events (`app.initialized`, `map.click`), MobX observables, event subscriptions. |
| **Layout & App Config** | [Layout & Configuration](./references/06_layout_and_config.md) | `app.json` layout hierarchy, `app-config.json` model binding (`$ref`, `$eval`), theming, i18n. |
| **Workflow Web SDK** | [Workflow Web SDK](./references/07_workflow_web_sdk.md) | Custom workflow activities (`IActivityHandler`), custom form elements, ArcGIS JS API integration. |
| **Deployment** | [Deployment & Best Practices](./references/08_deployment_and_best_practices.md) | `npm run build`, hosting on CDN/SaaS, ArcGIS Enterprise items, CORS, bundling. |
| **Tutorials & Recipes** | [Tutorials & Recipes](./references/09_tutorials_and_recipes.md) | Custom map click handling, configurable widgets, triggering workflows. |

---

## 1. Getting Started with a New Library

To initialize a new custom VertiGIS Studio Web library:

```bash
# Create a new library directory
npx @vertigis/web-sdk@latest create <library-name>

# Navigate into library directory
cd <library-name>

# Start development server with live reload
npm start
```

---

## 2. Core Development Workflow

### A. Registering Extensions (`src/index.ts`)
All components, services, and commands must be registered in the library entry point:

```typescript
import { LibraryRegistry } from "@vertigis/web/config";
import CustomWidget, { CustomWidgetModel } from "./components/CustomWidget/main";
import CustomService from "./services/CustomService";

export default function (registry: LibraryRegistry): void {
    // 1. Register Component
    registry.registerComponent({
        name: "custom-widget",
        namespace: "your.custom.namespace",
        getComponentType: () => CustomWidget,
        itemType: "custom-widget-model",
        getItemType: () => CustomWidgetModel,
        title: "Custom Widget"
    });

    // 2. Register Service
    registry.registerService({
        id: "custom-service",
        getService: (config) => new CustomService(config)
    });
}
```

### B. Standard Component Pattern (MUI + LayoutElement + observer)
Every UI widget consists of a paired **Model** and **React View**:

#### Model (`src/components/CustomWidget/CustomWidgetModel.ts`)
```typescript
import { ComponentModelBase, serializable, importModel } from "@vertigis/web/models";
import { MapModel } from "@vertigis/web/mapping";

@serializable
export class CustomWidgetModel extends ComponentModelBase {
    @serializable
    title: string = "Default Title";

    @importModel("map-extension")
    map: MapModel | undefined;

    protected async _onInitialize(): Promise<void> {
        await super._onInitialize();
    }
}
```

#### React View (`src/components/CustomWidget/main.tsx`)
```tsx
import * as React from "react";
import { observer } from "mobx-react-lite";
import { Box, Typography } from "@mui/material";
import {
    LayoutElement,
    LayoutElementProperties,
} from "@vertigis/web/components";
import { CustomWidgetModel } from "./CustomWidgetModel";

interface CustomWidgetProps extends LayoutElementProperties<CustomWidgetModel> {}

const CustomWidget = observer(function CustomWidget(props: CustomWidgetProps) {
    const { model } = props;
    return (
        <LayoutElement {...props}>
            <Box sx={{ p: 2, backgroundColor: "var(--primaryBackground)" }}>
                <Typography variant="h6" sx={{ color: "var(--primaryForeground)" }}>
                    {model.title}
                </Typography>
                {model.map && (
                    <Typography variant="body2" sx={{ color: "var(--secondaryForeground)" }}>
                        Bound to Map ID: {model.map.id}
                    </Typography>
                )}
            </Box>
        </LayoutElement>
    );
});

export default CustomWidget;
```

---

## 3. Crawl & Maintenance Tooling

This skill includes an automated Crawl4AI script in `scripts/crawl_vertigis_docs.py` to refresh the crawled documentation directly from the VertiGIS Developer Center.
