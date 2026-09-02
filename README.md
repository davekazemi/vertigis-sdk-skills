# VertiGIS SDK AI Skills

This repository contains expertly crafted AI instructions ("Skills") designed to teach Large Language Models (LLMs) how to generate production-ready, enterprise-grade code for the VertiGIS Studio Web SDK and VertiGIS Studio Workflow SDK.

## What are AI Skills?
AI Skills are robust, system-prompt-style markdown documents that provide an LLM with strict architectural guardrails, best practices, and canonical code patterns. By providing these documents as context to an AI agent (like GitHub Copilot, ChatGPT, or Google Gemini), you ensure the AI generates code that strictly adheres to the VertiGIS SDK standards rather than hallucinating generic React or TypeScript code.

---

## 💡 Usage & Interactive Consultation ("Grill-Me" Protocol)

When an AI assistant is equipped with these skills, it doesn't just guess or output arbitrary boilerplate. It actively follows an interactive consultation flow:

```mermaid
flowchart TD
    A[Skill Triggered] --> B[Scan Workspace for Project Files]

    B --> C{Workspace State}

    C -->|Existing Project| D
    C -->|Empty / New| E

    subgraph D [Existing Workspace]
        D1[Review Code]
        D2[Add Component / Service]
        D3[Add Activity / Element]
        D4[Generate Tooling Scripts]
    end

    subgraph E [Grill-Me Discovery]
        E1[Target Extension Type]
        E2[Name & Custom Namespace]
        E3[HTTPS SSL Strategy]
        E4[Scaffold Project & Scripts]
    end
```

### 1. Existing Workspace Mode
If the agent detects an existing VertiGIS project, it prompts you before modifying files:
- **Categorized Code Review Audit**: Audits your codebase with distinct severity levels (🔴 **Critical Errors**, 🟡 **Architectural Warnings**, 🔵 **Cleanliness Recommendations**) tailored to the extension type (Web Components, Services, Workflow Activities, or Form Elements).
- **Extension Scaffolding**: Scaffolds new Components and Services (Web SDK) or new Activities and Form Elements (Workflow SDK) adhering to canonical directory structures.
- **Tooling Generation**: Generates automated port-killing start scripts and build scripts.

### 2. New Workspace Mode ("Grill-Me" Interview)
If the workspace is uninitialized, the agent conducts a focused questionnaire to align on requirements before generating code:
- **Extension Type**: Clarifies whether you are targeting Web Components, Web Services, Workflow Activities, or Custom Form Elements.
- **Naming & Namespace**: Establishes unique namespaces (e.g. `myorg.custom`), category groupings, and display names for VertiGIS Designer.
- **HTTPS SSL Setup**: Offers to generate local self-signed SSL certificates via OpenSSL (`openssl req -x509 -newkey rsa:2048 ...`) or configure paths to your organization's certificates.
- **Port Management Scripts**: Automatically creates `start.bat` / `start.sh` (which kills any lingering processes occupying dev ports 3000 or 5000 using `netstat`/`taskkill` before running `npm start`) and `build.bat` / `build.sh`.

---

## 🚀 How to Install

### Option 1: Using the `skills` CLI (Recommended)
If you are using an agentic IDE like Antigravity, Cursor, Claude Code, or Cline, you can install interactively or in bulk:

#### 🎯 Interactive Install (prompts to choose specific skills or select all)
```bash
npx skills add davekazemi/vertigis-sdk-skills
```

#### ⚡ One-Line Install for All Skills
```bash
npx skills add davekazemi/vertigis-sdk-skills --all
```

#### 🌐 Global Install (User-level across all projects and agents)
```bash
npx skills add davekazemi/vertigis-sdk-skills -g --all
```

#### 📦 Install a Specific Skill
```bash
# Web SDK only
npx skills add davekazemi/vertigis-sdk-skills --skill vertigis-web-sdk-skill

# Workflow SDK (TypeScript) only
npx skills add davekazemi/vertigis-sdk-skills --skill vertigis-workflow-sdk-skill

# Workflow .NET SDK (C#) only
npx skills add davekazemi/vertigis-sdk-skills --skill vertigis-workflow-dotnet-skill
```

### Option 2: One-Line Global Install (For Antigravity)
If you want to install them globally on your machine so the AI knows VertiGIS for all your projects:
```bash
mkdir -p ~/.gemini/config/skills && cd ~/.gemini/config/skills && git clone https://github.com/davekazemi/vertigis-sdk-skills.git
```

### Option 3: Project-Specific Git Submodule
Share these skills with your dev team by adding them directly into your project's agent configuration folder:
```bash
git submodule add https://github.com/davekazemi/vertigis-sdk-skills.git .agents/skills/vertigis-sdk-skills
```

### Option 4: Manual System Prompt (ChatGPT / Claude)
If you are using a standard web chat interface:
1. Open the `SKILL.md` file from any of the three skill folders.
2. Copy the entire contents.
3. Paste it into your LLM's "Custom Instructions", "System Prompt", or simply as your first message in the chat.

---

## Included Skills

### 1. VertiGIS Web SDK Skill (`vertigis-web-sdk-skill/`)
Teaches the AI how to build custom components, services, and commands for VertiGIS Studio Web.
**Key Enforcements:**
- Material UI (MUI) and CSS Variable Tokens (no custom CSS)
- React Component Decomposition (Hooks, View, Utils)
- MobX `observer()` wrappers for reactive state
- `<LayoutElement>` wrappers for Designer integration
- React Error Boundaries for enterprise reliability
- Custom SVG Icon registration (`createSvgIcon`, `registerIcon`)
- Comprehensive Command and Operation invocation (`useUIContext`, `useService`, `$ref`, `$eval`)
- ArcGIS AMD module loader rules (Star Imports for utilities vs Default Imports for classes)

### 2. VertiGIS Workflow SDK Skill (`vertigis-workflow-sdk-skill/`)
Teaches the AI how to build custom activities and form elements for VertiGIS Studio Workflow in TypeScript.
**Key Enforcements:**
- Strict `IActivityHandler` typing and `IActivityContext` parameter handling
- Defensive `try/catch` orchestration in activities
- Form element multi-output properties (`props.setProperty()`) and structured custom events (`props.raiseEvent()`)
- Form element accessibility (ARIA labels, keyboard navigation)
- React Component Decomposition (`hooks/`, `components/`, `utils/`) for complex form elements
- ArcGIS AMD module loader rules (Star Imports vs Default Imports)

### 3. VertiGIS Workflow .NET SDK Skill (`vertigis-workflow-dotnet-skill/`)
Teaches the AI how to build custom activities and form elements in C# for VertiGIS Studio Mobile, Desktop (ArcGIS Pro), and Workflow Server.
**Key Enforcements:**
- Strict `IActivityHandler` implementation with `Task<IDictionary<string, object?>> Execute(...)`
- Mobile Form Elements with XAML + `ContentComponent` and `RegisterCustomFormElementBase`
- Desktop (ArcGIS Pro) activities executing on worker threads via `QueuedTask.Run()`
- Headless on-premises Workflow Server activities with `[assembly: WorkflowActivities]`
- Companion TypeScript activity stubs (`@supportedApps VSM, VSD, VSS`) for Designer toolbox integration


---

## Data Exclusions
Note that the raw HTML/Markdown scraped from the official VertiGIS Developer Center, as well as the Python scraping scripts used to generate these references, are intentionally excluded via `.gitignore` to keep the skill repository clean and focused strictly on AI instructions.
