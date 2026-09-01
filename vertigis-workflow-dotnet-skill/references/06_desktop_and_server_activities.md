# VertiGIS Studio Workflow .NET SDK: Desktop & Server Activities

## 1. VertiGIS Studio Desktop (ArcGIS Pro) Activities

Custom activities for VertiGIS Studio Desktop are deployed as part of an **ArcGIS Pro Module Add-In** (`.esriAddInX`).

### Assembly Registration (`AssemblyInfo.cs`)
To register all activities in the assembly:
```csharp
using VertiGIS.Workflow.Runtime;

[assembly: WorkflowActivities]
```

### Activity Implementation (`ProLayerExportActivity.cs`)
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;
using VertiGIS.Workflow.Runtime;

namespace MyCompany.Pro.Workflow
{
    public class ProLayerExportActivity : IActivityHandler
    {
        public static string Action => "uuid:77c12345-aaaa-bbbb-cccc-1234567890ab::ProLayerExport";

        public async Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            if (!inputs.TryGetValue("layerName", out var nameObj) || nameObj is not string layerName)
            {
                throw new ArgumentException("Parameter 'layerName' is required.");
            }

            var exportResult = await QueuedTask.Run(() =>
            {
                var map = MapView.Active?.Map;
                if (map == null) throw new InvalidOperationException("No active map view found in ArcGIS Pro.");

                var layer = map.FindLayers(layerName);
                return layer.Count > 0 ? "LayerFound" : "LayerNotFound";
            });

            return new Dictionary<string, object?>
            {
                ["status"] = exportResult
            };
        }
    }
}
```

---

## 2. VertiGIS Studio Workflow Server Activities

Workflow Server runs headless workflows on Windows Server (IIS / .NET Core) for automated scheduled tasks, batch processing, and back-office spatial analysis.

### Assembly Registration (`Properties/AssemblyInfo.cs`)
```csharp
[assembly: VertiGIS.Workflow.Runtime.WorkflowActivities]
```

### Activity Implementation (`DatabaseSyncActivity.cs`)
```csharp
using System;
using System.Collections.Generic;
using System.Data;
using System.Threading.Tasks;
using VertiGIS.Workflow.Runtime;

namespace MyCompany.Server.Workflow
{
    public class DatabaseSyncActivity : IActivityHandler
    {
        public static string Action { get; } = "uuid:88d12345-bbbb-cccc-dddd-9876543210fe::DatabaseSync";

        public async Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            if (!inputs.TryGetValue("connectionString", out var connObj) || connObj is not string connectionString)
            {
                throw new ArgumentException("connectionString is required.");
            }

            int recordsSynced = await PerformSyncAsync(connectionString, context);

            return new Dictionary<string, object?>
            {
                ["syncedCount"] = recordsSynced,
                ["timestamp"] = DateTime.UtcNow.ToString("o")
            };
        }

        private static async Task<int> PerformSyncAsync(string connectionString, IActivityContext context)
        {
            // Check cancellation token during long-running batch work
            context.CancellationToken.ThrowIfCancellationRequested();
            await Task.Delay(500, context.CancellationToken);
            return 42;
        }
    }
}
```

---

## 3. Key Differences: Desktop vs Server

| Dimension | Desktop (ArcGIS Pro) | Server (On-Premises) |
| :--- | :--- | :--- |
| **Hosting Model** | Inside ArcGIS Pro client process | Windows Service / IIS / .NET Core process |
| **GIS API** | ArcGIS Pro SDK (`ArcGIS.Desktop.*`) | ArcGIS REST APIs, Enterprise Geodatabases, direct SQL |
| **Threading** | Requires `QueuedTask.Run()` for Pro calls | Standard .NET `async/await` thread pool |
| **UI Interaction** | Can interact with active Pro maps/docks | Strictly headless / unattended execution |
