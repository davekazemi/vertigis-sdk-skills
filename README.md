# VertiGIS SDK AI Skills

This repository contains expertly crafted AI instructions ("Skills") designed to teach Large Language Models (LLMs) how to generate production-ready, enterprise-grade code for the VertiGIS Studio Web SDK and VertiGIS Studio Workflow SDK.

## What are AI Skills?
AI Skills are robust, system-prompt-style markdown documents that provide an LLM with strict architectural guardrails, best practices, and canonical code patterns. By providing these documents as context to an AI agent (like GitHub Copilot, ChatGPT, or Google Gemini), you ensure the AI generates code that strictly adheres to the VertiGIS SDK standards rather than hallucinating generic React or TypeScript code.

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

## How to Use
These skills are written in raw Markdown with standard YAML frontmatter. You can:
1. **Direct System Prompts**: Copy and paste the contents of the `SKILL.md` and relevant reference files directly into your LLM's system prompt or custom instructions.
2. **AI Agent Tooling**: Mount these directories into an agentic coding assistant's workspace (e.g., Antigravity, AutoGPT) so the agent can read them dynamically when asked to perform a VertiGIS task.

## Data Exclusions
Note that the raw HTML/Markdown scraped from the official VertiGIS Developer Center, as well as the Python scraping scripts used to generate these references, are intentionally excluded via `.gitignore` to keep the skill repository clean and focused strictly on AI instructions.
