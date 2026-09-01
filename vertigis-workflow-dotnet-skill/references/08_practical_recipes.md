# VertiGIS Studio Workflow .NET SDK: Practical Recipes

## Recipe 1: Custom Math / Logarithm Activity (Cross-Platform)

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using VertiGIS.Workflow.Runtime;

namespace MyCompany.Workflow.Recipes
{
    public class CalculateLogarithmActivity : IActivityHandler
    {
        public static string Action { get; } = "uuid:11a22b33-44c5-5d6e-7f8a-9b0c1d2e3f4a::CalculateLogarithm";

        public Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            if (!inputs.TryGetValue("value", out var valObj) || valObj == null)
            {
                throw new ArgumentException("The 'value' parameter is required.");
            }

            double value = Convert.ToDouble(valObj);
            double newBase = inputs.TryGetValue("base", out var baseObj) && baseObj != null 
                ? Convert.ToDouble(baseObj) 
                : Math.E;

            double result = Math.Log(value, newBase);

            return Task.FromResult<IDictionary<string, object?>>(new Dictionary<string, object?>
            {
                ["result"] = result
            });
        }
    }
}
```

---

## Recipe 2: Mobile Custom Toggle Form Element (XAML + C#)

### XAML View (`CustomToggleElement.xaml`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<core:ContentComponent xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
                       xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
                       xmlns:core="clr-namespace:VertiGIS.Mobile.Workflow.Core;assembly=VertiGIS.Mobile.Workflow"
                       x:Class="MyCompany.Mobile.Workflow.Elements.CustomToggleElement">
    <StackLayout Orientation="Horizontal" Padding="12" Spacing="10" VerticalOptions="Center">
        <Label Text="{Binding Title}" VerticalOptions="Center" HorizontalOptions="StartAndExpand" FontSize="16" />
        <Switch IsToggled="{Binding Value, Mode=TwoWay}" Toggled="OnToggled" HorizontalOptions="End" />
    </StackLayout>
</core:ContentComponent>
```

### Code-Behind (`CustomToggleElement.xaml.cs`)
```csharp
using Microsoft.Maui.Controls;
using Microsoft.Maui.Controls.Xaml;
using VertiGIS.Mobile.Workflow.Core;
using VertiGIS.Workflow.Runtime.Definition.Forms;

namespace MyCompany.Mobile.Workflow.Elements
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class CustomToggleElement : ContentComponent
    {
        public CustomToggleElement(Element element, string name) : base(element, name)
        {
            InitializeComponent();
        }

        private void OnToggled(object sender, ToggledEventArgs e)
        {
            Value = e.Value;
            OnEventRaised("changed", e.Value);
        }
    }
}
```

---

## Recipe 3: ArcGIS Pro Active Map Layer Filter (Desktop)

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;
using VertiGIS.Workflow.Runtime;

namespace MyCompany.Pro.Workflow.Recipes
{
    public class FilterVisibleLayersActivity : IActivityHandler
    {
        public static string Action => "uuid:22b33c44-55d6-6e7f-8a9b-0c1d2e3f4a5b::FilterVisibleLayers";

        public async Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            var visibleLayerNames = await QueuedTask.Run(() =>
            {
                var layers = new List<string>();
                var map = MapView.Active?.Map;
                if (map == null) return layers;

                foreach (var layer in map.GetLayersAsFlattenedList())
                {
                    if (layer.IsVisible)
                    {
                        layers.Add(layer.Name);
                    }
                }
                return layers;
            });

            return new Dictionary<string, object?>
            {
                ["layers"] = visibleLayerNames,
                ["count"] = visibleLayerNames.Count
            };
        }
    }
}
```
