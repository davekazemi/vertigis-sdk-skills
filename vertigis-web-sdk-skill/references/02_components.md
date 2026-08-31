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
import { ComponentModelBase, serializable, importModel } from "@vertigis/web/models";
import { MapModel } from "@vertigis/web/mapping";

@serializable
export class MyWidgetModel extends ComponentModelBase {
    // 1. Reactive and serializable property (configurable in app-config.json)
    @serializable
    greetingText: string = "Hello VertiGIS!";

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

    return (
        <LayoutElement {...props}>
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
                        onClick={() => model.increment()}
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
        </LayoutElement>
    );
});

export default MyWidget;
```

> [!IMPORTANT]
> **`<LayoutElement {...props}>`**: Every component view MUST wrap its content inside `<LayoutElement>`, passing through all props. This enables the SDK's layout system (sizing, visibility, drag-drop in Designer).
>
> **`observer()`**: Wrapping the component with `observer()` from `mobx-react-lite` ensures the view automatically re-renders whenever any MobX `@observable` or `@serializable` property on the model changes. Without this, model changes will NOT update the UI.

---

## 3. Styling and Theming Rules

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

## 4. Component Lifecycle Hooks

| Hook | Timing | Purpose |
| :--- | :--- | :--- |
| `_onInitialize()` | After constructor and property assignment | Async setup, subscribing to events/services, loading external data. |
| `_load()` | When component becomes active / visible | Lazy loading of heavy resources. |
| `_unload()` | When component is hidden / deactivated | Releasing temporary listeners or pausing timers. |
| `_onDestroy()` | When component is permanently removed | Tear down subscriptions, free memory. |

---

## 5. UI Context and Component Services Injection

Components can access application services and contexts directly:

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

---

## 6. React Error Boundaries (Enterprise Pattern)

To prevent a single crashing widget from taking down the entire VertiGIS Web application, you should wrap custom widget contents in an Error Boundary. This is an enterprise standard for all custom components.

Since React doesn't yet support functional Error Boundaries, you must create a standard class component in `src/utils/ErrorBoundary.tsx`:

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

Then wrap your component view's content (inside the `LayoutElement`):

```tsx
import { ErrorBoundary } from "../../utils/ErrorBoundary";

const MyWidget = observer(function MyWidget(props: MyWidgetProps) {
    return (
        <LayoutElement {...props}>
            <ErrorBoundary fallbackMessage="Custom Widget failed to load.">
                {/* Your actual widget content */}
            </ErrorBoundary>
        </LayoutElement>
    );
});
```
