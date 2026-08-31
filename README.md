# VertiGIS SDK AI Skills

This repository contains expertly crafted AI instructions ("Skills") designed to teach Large Language Models (LLMs) how to generate production-ready, enterprise-grade code for the VertiGIS Studio Web SDK and VertiGIS Studio Workflow SDK.

## What are AI Skills?
AI Skills are robust, system-prompt-style markdown documents that provide an LLM with strict architectural guardrails, best practices, and canonical code patterns. By providing these documents as context to an AI agent (like GitHub Copilot, ChatGPT, or Google Gemini), you ensure the AI generates code that strictly adheres to the VertiGIS SDK standards rather than hallucinating generic React or TypeScript code.

## 🚀 How to Install

### Option 1: One-Line Global Install (For Antigravity / Agentic IDEs)
If you are using an agentic IDE that supports global skill directories (like Antigravity), you can install these skills globally on your machine with a single command:

```bash
mkdir -p ~/.gemini/config/skills && cd ~/.gemini/config/skills && git clone https://github.com/davekazemi/vertigis-sdk-skills.git
```
*The agent will automatically discover these skills for all your future projects.*

### Option 2: Project-Specific Install (Git Submodule)
If you want to share these skills with your development team, add them as a Git Submodule directly into your project's agent configuration folder:

```bash
git submodule add https://github.com/davekazemi/vertigis-sdk-skills.git .agents/skills/vertigis-sdk-skills
```
*When your team clones the repo, the AI assistant will automatically load the VertiGIS rules.*

### Option 3: Manual System Prompt (ChatGPT / Claude)
If you are using a standard web chat interface:
1. Open the `SKILL.md` file from either folder.
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

### 2. VertiGIS Workflow SDK Skill (`vertigis-workflow-sdk-skill/`)
Teaches the AI how to build custom activities and form elements for VertiGIS Studio Workflow.
**Key Enforcements:**
- Strict `IActivityHandler` typing
- Defensive `try/catch` orchestration in activities
- Form element accessibility (ARIA labels, keyboard navigation)
- ArcGIS AMD module loader rules (Star Imports vs Default Imports)

## Data Exclusions
Note that the raw HTML/Markdown scraped from the official VertiGIS Developer Center, as well as the Python scraping scripts used to generate these references, are intentionally excluded via `.gitignore` to keep the skill repository clean and focused strictly on AI instructions.
