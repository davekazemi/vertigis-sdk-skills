# VertiGIS Studio Web SDK: Custom Components

## Overview
A VertiGIS Web component consists of two synchronized parts:
1. **The Model (`*Model.ts`)**: A class extending `ComponentModelBase` (or `ItemModelBase`) that handles business logic, state, and serialization.
2. **The View (`main.tsx`)**: A React functional component wrapped in `observer()` that renders inside a `<LayoutElement>` wrapper using Material UI (MUI).

---

## 1. Creating the Component Model

The model manages the component's state, participates in app configuration, and executes actions.

```typescript
// src/components/MyWidget/MyWidgetModel.ts
import { ComponentModelBase, serializable, importModel, exportModel } from "@vertigis/web/models";
import { MapModel } from "@vertigis/web/mapping";

// Mark with @exportModel if child components need to import this model
@exportModel
@serializable
export class MyWidgetModel extends ComponentModelBase {
    // 1. Serializable properties (configurable in app-config.json)
    @serializable(String)
    greetingText: string = "Hello VertiGIS!";

    @serializable(Number)
    refreshInterval: number = 30;

    @serializable(Boolean)
    autoStart: boolean = true;

    // 2. Observable runtime state (not saved in config)
    count: number = 0;

    // 3. Inject built-in models (e.g. MapModel)
    @importModel("map-extension")
    map: MapModel | undefined;

    // Lifecycle Hook: Initialization
    protected async _onInitialize(): Promise<void> {
        await super._onInitialize();
        console.log("MyWidgetModel initialized with text:", this.greetingText);
    }

    public increment(): void {
        this.count++;
    }

    // Lifecycle Hook: Destruction / Cleanup
    protected async _onDestroy(): Promise<void> {
        await super._onDestroy();
    }
}
```

### Advanced `@serializable` Options
You can provide type constructors or custom serializer/deserializer functions for complex properties:
```typescript
@serializable(Array)
selectedIds: string[] = [];

// Custom Serializer for Date objects
@serializable({
    serializer: (val: Date) => val?.toISOString(),
    deserializer: (raw: string) => raw ? new Date(raw) : undefined
})
lastInspectedDate?: Date;
```

---

## 2. Creating the React View (MUI + LayoutElement Required)

Views MUST:
- Use MUI components (`@mui/material`) — **NEVER use standard HTML tags**
- Use VertiGIS CSS variable tokens — **NEVER hardcode hex colors**
- Extend `LayoutElementProperties<TModel>` in props to expose parameters to the Designer
- Wrap all content inside `<LayoutElement {...props}>` — this is **REQUIRED** by the SDK
- Wrap the component function with `observer()` from MobX to enable reactive re-rendering when model observables change

### 💡 Exposing Configuration Parameters to VertiGIS Web Designer
If you want to expose configuration parameters that appear in the **VertiGIS Studio Web Designer**, you MUST extend `LayoutElementProperties<TModel>` in your React component's props interface.

```tsx
// src/components/MyWidget/main.tsx
import * as React from "react";
import { observer } from "mobx-react-lite";
import { Box, Typography, Button, Stack } from "@mui/material";
import {
    LayoutElement,
    LayoutElementProperties,
} from "@vertigis/web/components";
import { useUIContext, useService } from "@vertigis/web/ui";
import { I18nService } from "@vertigis/web/i18n";
import { ErrorBoundary } from "../../utils/ErrorBoundary";
import { MyWidgetModel } from "./MyWidgetModel";

interface MyWidgetProps extends LayoutElementProperties<MyWidgetModel> {
    /**
     * @displayName Custom Config Property
     * @description This property will automatically show up in the Web Designer.
     */
    customConfigParam?: string;
}

const MyWidget = observer(function MyWidget(props: MyWidgetProps): React.ReactElement {
    const { model, customConfigParam = "Default" } = props;

    // Direct access to UI Context commands & services in React views
    const { commands, operations } = useUIContext();
    const i18n = useService<I18nService>("i18n");

    const handleAction = async () => {
        await commands.ui.displayNotification.execute({
            title: i18n?.translate("widget-title") || "Action",
            message: `Count incremented to ${model.count + 1}`,
            status: "info"
        });
        model.increment();
    };

    return (
        <LayoutElement {...props}>
            <ErrorBoundary fallbackMessage="Widget failed to load.">
                <Box
                    sx={{
                        p: 2,
                        backgroundColor: "var(--primaryBackground)",
                        borderRadius: "var(--borderRadius, 4px)",
                    }}
                >
                    <Typography variant="h6" sx={{ color: "var(--primaryAccent)", mb: 1 }}>
                        {model.greetingText}
                    </Typography>

                    <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                        <Typography variant="body1" sx={{ color: "var(--primaryForeground)" }}>
                            Current Count: {model.count}
                        </Typography>
                        <Button
                            variant="contained"
                            onClick={handleAction}
                            sx={{
                                backgroundColor: "var(--primaryAccent)",
                                color: "var(--buttonForeground)",
                                "&:hover": {
                                    backgroundColor: "var(--primaryAccentHover)",
                                },
                            }}
                        >
                            Increment
                        </Button>
                    </Stack>

                    {model.map && (
                        <Typography variant="caption" sx={{ color: "var(--secondaryForeground)" }}>
                            Attached Map ID: {model.map.id}
                        </Typography>
                    )}
                </Box>
            </ErrorBoundary>
        </LayoutElement>
    );
});

export default MyWidget;
```

---

## 3. Creating and Registering Custom SVG Icons

VertiGIS Studio Web SDK supports registering custom SVG icons for use in toolbars, menus, and components.

### 1. Define Icon (`src/icons/CustomArrowIcon.tsx`)
```tsx
import React from "react";
import createSvgIcon from "@vertigis/web/ui/icons/utils/createSvgIcon";

export default createSvgIcon(
    <path d="M20 11H7.8l5.6-5.6L12 4l-8 8 8 8 1.4-1.4L7.8 13H20v-2z" />
);
```

### 2. Register Icon in `src/index.ts`
```typescript
import { LibraryRegistry } from "@vertigis/web/config";
import CustomArrowIcon from "./icons/CustomArrowIcon";

export default function (registry: LibraryRegistry): void {
    registry.registerIcon({
        id: "myorg-custom-arrow",
        getComponentType: () => CustomArrowIcon
    });
}
```

### 3. Using Custom Icons in Views or App Config
- **In React Views**:
  ```tsx
  import DynamicIcon from "@vertigis/web/ui/DynamicIcon";
  <DynamicIcon src="myorg-custom-arrow" />
  ```
- **In `app-config.json` menus / buttons**:
  ```json
  {
    "id": "my-tool-button",
    "$type": "menu-item",
    "title": "Custom Tool",
    "icon": "myorg-custom-arrow",
    "action": "custom.my-command"
  }
  ```

---

## 4. Styling and Theming Rules

- **Use the `sx` prop**: Apply styles inline using MUI's `sx` prop.
- **Use CSS Variables (Tokens)**: NEVER invent hex colors. Always map styles to standard tokens:
  - `var(--primaryBackground)`
  - `var(--secondaryBackground)`
  - `var(--primaryForeground)`
  - `var(--secondaryForeground)`
  - `var(--primaryAccent)`
  - `var(--primaryAccentHover)`
  - `var(--primaryBorder)`
  - `var(--buttonForeground)`
  - `var(--emphasizedButtonBackground)`
  - `var(--itemHoverBackground)`
  - `var(--itemSelectedBackground)`
  - `var(--alertRedBackground)`
  - `var(--defaultFont)`
- **No CSS Modules**: Do NOT create `.css` or `.module.css` files. Inherit from parent application styles natively via tokens.

---

## 5. Component Lifecycle Hooks

| Hook | Timing | Purpose |
| :--- | :--- | :--- |
| `_onInitialize()` | After constructor and property assignment | Async setup, subscribing to events/services, loading external data. |
| `_load()` | When component becomes active / visible | Lazy loading of heavy resources. |
| `_unload()` | When component is hidden / deactivated | Releasing temporary listeners or pausing timers. |
| `_onDestroy()` | When component is permanently removed | Tear down subscriptions, free memory. |

---

## 6. UI Context and Component Services Injection

Components can access application services and contexts in two ways:

### A. In Models via `@inject`
```typescript
import { inject } from "@vertigis/web/services";
import { I18nService } from "@vertigis/web/i18n";
import { NotificationService } from "@vertigis/web/ui";

export class MyWidgetModel extends ComponentModelBase {
    @inject("i18n")
    i18n: I18nService | undefined;

    @inject("notification")
    notification: NotificationService | undefined;

    public showNotification(): void {
        this.notification?.show({
            title: "Success",
            message: this.i18n?.translate("my-message-key") || "Operation completed.",
            status: "success"
        });
    }
}
```

### B. In React Functional Views via `useService` / `useUIContext`
```tsx
import { useService, useUIContext } from "@vertigis/web/ui";
import { I18nService } from "@vertigis/web/i18n";

export function HeaderView() {
    const i18n = useService<I18nService>("i18n");
    const { commands } = useUIContext();
    // ...
}
```

---

## 7. React Error Boundaries (Enterprise Pattern)

Wrap custom widget contents in an Error Boundary (`src/utils/ErrorBoundary.tsx`) to prevent a crashing component from taking down the VertiGIS Web application:

```tsx
// src/utils/ErrorBoundary.tsx
import * as React from "react";
import { Box, Typography } from "@mui/material";

interface Props {
    children: React.ReactNode;
    fallbackMessage?: string;
}

interface State {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
        console.error("Widget Error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <Box sx={{ p: 2, backgroundColor: "var(--alertRedBackground)", color: "white", borderRadius: 1 }}>
                    <Typography variant="subtitle2">
                        {this.props.fallbackMessage || "This widget encountered an error."}
                    </Typography>
                    <Typography variant="caption" sx={{ opacity: 0.8, mt: 1, display: 'block' }}>
                        {this.state.error?.message}
                    </Typography>
                </Box>
            );
        }
        return this.props.children;
    }
}
```

---

## 8. VertiGIS Web Component Hooks (`@vertigis/web/ui`)

In addition to MobX `observer()`, VertiGIS Studio Web provides dedicated React hooks for granular property watching, collection observation, and event bus subscriptions:

| Hook | Purpose | Example |
| :--- | :--- | :--- |
| `useWatchAndRerender(target, prop \| props[])` | Watches one or more observable model properties and triggers a re-render when they change. | `useWatchAndRerender(model, "hidden");`<br>`useWatchAndRerender(model, ["count", "status"]);` |
| `useWatchCollectionAndRerender(collection)` | Watches an ArcGIS `Collection` (`__esri.Collection`) for add/remove/reorder events and triggers a re-render. | `useWatchCollectionAndRerender(model.map.layers);` |
| `useWatch(target, prop, callback)` | Watches an observable property for mutations and executes a side-effect callback. | `useWatch(model, "selectedId", (newId, oldId) => { fetchDetails(newId); });` |
| `useWatchInit(target, prop, callback)` | Same as `useWatch`, but also runs immediately upon initial mount. | `useWatchInit(model, "activeFilter", (filter) => { applyFilter(filter); });` |
| `useSubscribeAndRerender(event)` | Subscribes to an application event bus event and triggers a re-render when fired. | `useSubscribeAndRerender(messages.events.map.click);` |
| `useSubscribe(event, callback)` | Subscribes to an event bus event and executes a callback function. | `useSubscribe(messages.events.auth.signedIn, (user) => { initUser(user); });` |

### Example: Using `useWatchAndRerender` in a Functional View
```tsx
import React from "react";
import { LayoutElement, LayoutElementProperties } from "@vertigis/web/components";
import { useWatchAndRerender } from "@vertigis/web/ui";
import { Box, Typography, Button } from "@mui/material";
import { MyWidgetModel } from "./MyWidgetModel";

export default function MyWidget(props: LayoutElementProperties<MyWidgetModel>) {
    const { model } = props;

    // Granularly watch specific model property for re-renders
    useWatchAndRerender(model, "hidden");

    return (
        <LayoutElement {...props}>
            {!model.hidden ? (
                <Box sx={{ p: 2, backgroundColor: "var(--primaryBackground)" }}>
                    <Typography variant="body1">Content is visible!</Typography>
                    <Button variant="contained" onClick={() => (model.hidden = true)}>
                        Hide
                    </Button>
                </Box>
            ) : (
                <Button variant="outlined" onClick={() => (model.hidden = false)}>
                    Show
                </Button>
            )}
        </LayoutElement>
    );
}
```
