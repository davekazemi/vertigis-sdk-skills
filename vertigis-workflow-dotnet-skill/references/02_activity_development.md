# VertiGIS Studio Workflow .NET SDK: Activity Development

## 1. Canonical Activity Pattern

All custom .NET workflow activities implement the `IActivityHandler` interface:

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using VertiGIS.Workflow.Runtime;

namespace MyCompany.Workflow.Activities
{
    public class CalculateBufferActivity : IActivityHandler
    {
        // 1. Unique Action Name (matches Workflow Designer action ID)
        public static string Action { get; } = "uuid:e9a12345-6789-4abc-def0-123456789abc::CalculateBuffer";

        // 2. Execution Entry Point
        public async Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            // 3. Defensive Input Validation
            if (!inputs.TryGetValue("distance", out var distanceObj) || distanceObj == null)
            {
                throw new ArgumentException("The 'distance' parameter is required.");
            }

            double distance = Convert.ToDouble(distanceObj);
            string unit = inputs.TryGetValue("unit", out var unitObj) && unitObj is string u ? u : "meters";
            bool showLogger = inputs.TryGetValue("showLogger", out var logObj) && logObj is bool l && l;

            if (showLogger)
            {
                Console.WriteLine($"[CalculateBuffer] Executing with distance: {distance}, unit: {unit}");
            }

            try
            {
                // 4. Delegate Business Logic to Async / Pure Helper
                double bufferedArea = await PerformBufferCalculationAsync(distance, unit);

                // 5. Return Output Dictionary
                return new Dictionary<string, object?>
                {
                    ["result"] = bufferedArea,
                    ["status"] = "Success"
                };
            }
            catch (Exception ex)
            {
                // 6. Defensive Error Wrapping
                Console.Error.WriteLine($"[CalculateBuffer] Execution failed: {ex.Message}");
                throw new InvalidOperationException($"Buffer calculation failed: {ex.Message}", ex);
            }
        }

        private static Task<double> PerformBufferCalculationAsync(double distance, string unit)
        {
            // Pure domain calculation logic
            double area = Math.PI * Math.Pow(distance, 2);
            return Task.FromResult(area);
        }
    }
}
```

---

## 2. The `IActivityContext` Parameter

The `context: IActivityContext` parameter gives access to the runtime environment:
- `context.CancellationToken`: Token for gracefully canceling long-running background tasks.
- `context.GetWorkflowInstanceId()`: Retrieves unique workflow execution run ID.
- `context.Services`: Service provider for resolving dependency-injected services.

```csharp
public async Task<IDictionary<string, object?>> Execute(IDictionary<string, object?> inputs, IActivityContext context)
{
    // Check for user cancellation in loops
    context.CancellationToken.ThrowIfCancellationRequested();

    // Async operation with cancellation token support
    await Task.Delay(1000, context.CancellationToken);

    return new Dictionary<string, object?>();
}
```

---

## 3. Best Practices & Guardrails

1. **Async All the Way**: Always return `Task<IDictionary<string, object?>>`. Use `await` for I/O operations. Use `Task.FromResult(...)` for synchronous work. **NEVER use `.Result` or `.Wait()`**, which causes deadlocks on UI threads.
2. **Safe Input Parsing**: Use `inputs.TryGetValue(key, out var val)` rather than directly indexing `inputs[key]`, which throws `KeyNotFoundException`.
3. **Defensive Error Handling**: Always wrap domain operations in `try/catch` and throw clear exceptions so the Workflow engine handles the error gracefully.
4. **Action Identifier**: Use a descriptive action string or a UUID prefix (`uuid:<app-uuid>::<ActivityName>`) to prevent collision with core activities.
