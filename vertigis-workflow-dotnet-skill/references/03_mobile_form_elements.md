# VertiGIS Studio Workflow .NET SDK: Mobile Form Elements

## 1. Overview
VertiGIS Studio Mobile supports custom form elements built in .NET (XAML + C#). A custom mobile form element consists of:
1. **XAML View (`*.xaml`)**: Extends `ContentComponent` to define the mobile UI layout.
2. **C# Code-Behind (`*.xaml.cs`)**: Handles element initialization, data binding, and event handling.
3. **Registration Activity (`RegisterCustomFormElementBase`)**: Registers the element with the workflow runtime so forms can render it.

---

## 2. Creating the XAML View (`CustomRatingElement.xaml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<core:ContentComponent xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
                       xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
                       xmlns:core="clr-namespace:VertiGIS.Mobile.Workflow.Core;assembly=VertiGIS.Mobile.Workflow"
                       x:Class="MyCompany.Mobile.Workflow.Elements.CustomRatingElement">
    <StackLayout Orientation="Vertical" Padding="10" Spacing="8">
        <Label Text="{Binding Title}" 
               FontSize="16" 
               FontAttributes="Bold" />
        
        <Slider x:Name="RatingSlider"
                Minimum="1" 
                Maximum="5" 
                Value="{Binding Value, Mode=TwoWay}"
                ValueChanged="OnRatingChanged" />
                
        <Label Text="{Binding Source={x:Reference RatingSlider}, Path=Value, StringFormat='Selected Rating: {0:F0} / 5'}" 
               FontSize="14" 
               TextColor="Gray" />
    </StackLayout>
</core:ContentComponent>
```

---

## 3. Creating the Code-Behind (`CustomRatingElement.xaml.cs`)

```csharp
using System;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Controls.Xaml;
using VertiGIS.Mobile.Workflow.Core;
using VertiGIS.Workflow.Runtime.Definition.Forms;

namespace MyCompany.Mobile.Workflow.Elements
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class CustomRatingElement : ContentComponent
    {
        public CustomRatingElement(Element element, string name)
            : base(element, name)
        {
            InitializeComponent();
        }

        private void OnRatingChanged(object sender, ValueChangedEventArgs e)
        {
            // 1. Update public workflow value
            Value = (int)Math.Round(e.NewValue);

            // 2. Raise structured custom event to Workflow runtime
            OnEventRaised("changed", Value);
        }
    }
}
```

---

## 4. Registering the Form Element (`RegisterCustomFormElements.cs`)

Form elements must be registered in the workflow runtime using an activity extending `RegisterCustomFormElementBase`:

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using VertiGIS.Mobile.Composition;
using VertiGIS.Mobile.Workflow.Core;
using VertiGIS.Workflow.Runtime;
using MyCompany.Mobile.Workflow.Elements;

[assembly: Export(typeof(RegisterRatingElementActivity))]

namespace MyCompany.Mobile.Workflow.Elements
{
    public class RegisterRatingElementActivity : RegisterCustomFormElementBase
    {
        public static string Action { get; } = "RegisterRatingElement";

        public override Task<IDictionary<string, object?>> Execute(
            IDictionary<string, object?> inputs, 
            IActivityContext context)
        {
            // Register element ID matching the Workflow Form Designer Custom Type
            Register("CustomRating", typeof(CustomRatingElement), context);

            return Task.FromResult<IDictionary<string, object?>>(new Dictionary<string, object?>());
        }
    }
}
```

---

## 5. Best Practices for Mobile Form Elements

1. **Run Registration First**: Always execute the `RegisterCustomFormElementBase` activity at the start of your workflow before displaying the Form.
2. **Designer Custom Type**: In VertiGIS Studio Workflow Designer, add a **Custom** form element and set its **Custom Type** property to the registered ID (e.g. `"CustomRating"`).
3. **Two-Way Binding**: Bind inputs to `{Binding Value, Mode=TwoWay}` on `ContentComponent` so changes automatically synchronize with the workflow engine.
4. **Raising Events**: Use `OnEventRaised("custom", eventData)` or `OnEventRaised("changed", value)` for workflow branching.
