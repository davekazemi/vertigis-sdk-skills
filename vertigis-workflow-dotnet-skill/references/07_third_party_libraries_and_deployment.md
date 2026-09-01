# VertiGIS Studio Workflow .NET SDK: Third-Party Libraries & Deployment

## 1. Third-Party Dependencies (NuGet)

When your activities or mobile form elements require external libraries (e.g. `Newtonsoft.Json`, `Dapper`, `CsvHelper`, `RestSharp`):

1. **Install via NuGet**:
   ```bash
   dotnet add package CsvHelper
   dotnet add package Newtonsoft.Json
   ```
2. **Include in Assembly Output**:
   Ensure dependencies are copied to the build output by checking your `.csproj`:
   ```xml
   <PropertyGroup>
       <CopyLocalLockFileAssemblies>true</CopyLocalLockFileAssemblies>
   </PropertyGroup>
   ```

---

## 2. Deployment Procedures per Platform

### A. VertiGIS Studio Mobile
1. Build the platform-specific project (Android / iOS / Windows):
   ```bash
   dotnet publish -c Release -f net8.0-android
   ```
2. The custom activities and form elements are compiled directly into the custom Mobile App binary.

---

### B. VertiGIS Studio Desktop (ArcGIS Pro)
1. Build the ArcGIS Pro Module Add-In project in Visual Studio.
2. The output is packaged into a `.esriAddInX` file in `bin/Release/`.
3. Double-click the `.esriAddInX` to install it into ArcGIS Pro on client machines, or deploy via enterprise network shares.

---

### C. VertiGIS Studio Workflow Server (On-Premises)
1. Build the class library in `Release` configuration:
   ```bash
   dotnet build -c Release
   ```
2. Copy your custom assembly DLL (and any third-party dependency DLLs) into the Workflow Server extensions directory:
   - Typical path: `C:\Program Files\Latitude Geographics\Geocortex Core\Custom\` or `C:\Program Files\VertiGIS\Workflow\Server\bin\`.
3. Restart the VertiGIS Studio Workflow Server service to load the new assemblies.

---

## 3. Best Practices & Pitfalls

- **Avoid Assembly Version Conflicts**: Use compatible versions of `Newtonsoft.Json` or `System.Text.Json` matching the host runtime.
- **Copy Local**: For Workflow Server, all non-system third-party DLLs MUST be placed alongside the custom activity DLL in the extension folder.
- **Avoid Heavy Initialization in Constructors**: Defer heavy database connections or network handshakes to the `Execute()` method.
