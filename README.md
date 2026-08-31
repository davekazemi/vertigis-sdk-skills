# VertiGIS SDK AI Skills

This repository contains expertly crafted AI instructions ("Skills") designed to teach Large Language Models (LLMs) how to generate production-ready, enterprise-grade code for the VertiGIS Studio Web SDK and VertiGIS Studio Workflow SDK.

## What are AI Skills?
AI Skills are robust, system-prompt-style markdown documents that provide an LLM with strict architectural guardrails, best practices, and canonical code patterns. By providing these documents as context to an AI agent (like GitHub Copilot, ChatGPT, or Google Gemini), you ensure the AI generates code that strictly adheres to the VertiGIS SDK standards rather than hallucinating generic React or TypeScript code.

## 🚀 How to Install

### Option 1: Using the Vercel `skills` CLI (Recommended)
If you are using an agentic IDE like Antigravity, Cursor, or Cline, you can use the Open Agent Skills ecosystem (`npx skills`) to install these directly.

To install the **Web SDK Skill**:
```bash
npx skills@latest add davekazemi/vertigis-sdk-skills --skill=vertigis-web-sdk-skill
```

To install the **Workflow SDK Skill**:
```bash
npx skills@latest add davekazemi/vertigis-sdk-skills --skill=vertigis-workflow-sdk-skill
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
