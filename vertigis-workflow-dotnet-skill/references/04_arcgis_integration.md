# VertiGIS Studio Workflow .NET SDK: ArcGIS Integration

## 1. Overview
VertiGIS Studio Workflow integrates natively with Esri's .NET SDKs across target platforms:
- **Mobile**: Uses **ArcGIS Maps SDK for .NET** (`Esri.ArcGISRuntime`).
- **Desktop**: Uses **ArcGIS Pro SDK** (`ArcGIS.Desktop.*`).

---

## 2. Integrating ArcGIS Maps SDK for .NET (Mobile)

In VertiGIS Studio Mobile, activities can interact directly with the active map, feature layers, and spatial geometry engines.

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Esri.ArcGISRuntime.Geometry;
using Esri.ArcGISRuntime.Mapping;
using VertiGIS.Mobile.Composition;
using VertiGIS.Workflow.Runtime;

[assembly: Export(typeof(CreateBufferGraphicActivity))]

namespace MyCompany.Mobile.Workflow
{
    public class CreateBufferGraphicActivity : IActivityHandler
    {
        public static string Action { get; } = "CreateBufferGraphic";

        public Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            if (!inputs.TryGetValue("pointX", out var xObj) || !inputs.TryGetValue("pointY", out var yObj))
            {
                throw new ArgumentException("pointX and pointY are required.");
            }

            double x = Convert.ToDouble(xObj);
            double y = Convert.ToDouble(yObj);
            double distance = inputs.TryGetValue("distance", out var dObj) ? Convert.ToDouble(dObj) : 100.0;

            // 1. Create Point using ArcGIS Maps SDK for .NET
            MapPoint point = new MapPoint(x, y, SpatialReferences.Wgs84);

            // 2. Perform Geometry Calculation
            Geometry bufferGeometry = GeometryEngine.Buffer(point, distance);

            return Task.FromResult<IDictionary<string, object?>>(new Dictionary<string, object?>
            {
                ["bufferedGeometry"] = bufferGeometry,
                ["area"] = GeometryEngine.Area(bufferGeometry as Polygon)
            });
        }
    }
}
```

---

## 3. Integrating ArcGIS Pro SDK (Desktop)

Activities running in ArcGIS Pro must execute UI and spatial queries on the Pro internal worker thread using `QueuedTask.Run`:

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;
using VertiGIS.Workflow.Runtime;

[assembly: WorkflowActivities]

namespace MyCompany.Pro.Workflow
{
    public class GetActiveLayerCountActivity : IActivityHandler
    {
        public static string Action => "uuid:41a87e22-83b4-4b5c-b17d-93729e4726aa::GetActiveLayerCount";

        public async Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            // ArcGIS Pro SDK operations MUST run inside QueuedTask.Run
            int layerCount = await QueuedTask.Run(() =>
            {
                MapView activeView = MapView.Active;
                if (activeView?.Map == null)
                {
                    return 0;
                }

                return activeView.Map.GetLayersAsFlattenedList().Count;
            });

            return new Dictionary<string, object?>
            {
                ["layerCount"] = layerCount
            };
        }
    }
}
```

---

## 4. Key Rules for ArcGIS .NET Integration

1. **Threading in ArcGIS Pro**: NEVER access ArcGIS Pro objects (`MapView`, `Map`, `Layer`, `FeatureClass`) outside `QueuedTask.Run()`.
2. **Spatial References**: Always verify spatial references before performing `GeometryEngine` operations in mobile activities.
3. **Async / Cancellation**: Pass `context.CancellationToken` to long-running ArcGIS query tasks.
