# VertiGIS Studio Workflow .NET SDK: Overview & Concepts

## 1. Overview
VertiGIS Studio Workflow provides a native **.NET runtime** for executing workflows in desktop, mobile, and on-premises server environments:

```
                          ┌───────────────────────────┐
                          │ VertiGIS Workflow Designer│
                          │   (Web-based Authoring)   │
                          └─────────────┬─────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│ VertiGIS Studio Mobile│  │VertiGIS Studio Desktop│  │   Workflow Server     │
│ (.NET MAUI / Xamarin) │  │  (ArcGIS Pro Add-In)  │  │ (.NET Core / On-Prem) │
├───────────────────────┤  ├───────────────────────┤  ├───────────────────────┤
│ • .NET Activities     │  │ • .NET Activities     │  │ • .NET Activities     │
│ • Custom Form Elements│  │   (No Form Elements)  │  │   (No Form Elements)  │
│ • ArcGIS Runtime SDK  │  │ • ArcGIS Pro SDK      │  │ • Server I/O & DBs    │
└───────────────────────┘  └───────────────────────┘  └───────────────────────┘
```

---

## 2. Platform Comparison Matrix

| Platform | Target Runtime | Supported Extensions | UI Technology | GIS Integration |
| :--- | :--- | :--- | :--- | :--- |
| **VertiGIS Studio Mobile** | .NET 8 / MAUI / .NET Standard | Activities & Custom Form Elements | XAML (`ContentComponent`) | ArcGIS Maps SDK for .NET (Runtime) |
| **VertiGIS Studio Desktop** | .NET 8 / .NET Framework | Activities only | N/A (Headless activity) | ArcGIS Pro SDK |
| **Workflow Server** | .NET Core / .NET Framework | Activities only | N/A (Server-side execution) | Enterprise databases, APIs, file systems |

---

## 3. Core NuGet Packages

Extend .NET workflows using official NuGet references:

| Package | Purpose | Target Platform |
| :--- | :--- | :--- |
| `VertiGIS.Workflow.Runtime` | Core `IActivityHandler`, `IActivityContext`, `WorkflowActivities` attribute | All .NET platforms |
| `VertiGIS.Mobile.Workflow` | `ContentComponent`, `RegisterCustomFormElementBase` | Mobile only |
| `Esri.ArcGISRuntime` | ArcGIS Maps SDK for .NET | Mobile |
| `ArcGIS.Desktop.Framework` | ArcGIS Pro SDK | Desktop |

---

## 4. Workflow Designer Integration

Workflows are authored in the web-based **VertiGIS Studio Workflow Designer**. To execute custom .NET activities in your workflow:

1. **Direct Execution via `RunActivity`**: Call the activity directly using its action string (e.g. `Action = "uuid:<app-uuid>::<ActivityName>"` or `"MyCustomActivity"`).
2. **First-Class Designer Toolbox (Recommended)**: Create a TypeScript stub activity pack that declares input/output interfaces and metadata with `@action "uuid:<app-uuid>::<ActivityName>"` and `@supportedApps VSM, VSD, VSS`. This makes the activity appear in the designer toolbox with dedicated configuration panels.
