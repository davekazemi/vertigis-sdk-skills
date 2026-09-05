#!/usr/bin/env python3
"""
initiate_agents_md.py - Configure AGENTS.md in target repositories with VertiGIS Studio Web SDK directives.

Supports injecting into an existing AGENTS.md (scoped between comment markers) or generating
a fresh AGENTS.md file in the target repository.
"""

import argparse
import os
import re
import sys
from pathlib import Path

START_MARKER = "<!-- vertigis-web-sdk:start -->"
END_MARKER = "<!-- vertigis-web-sdk:end -->"

DIRECTIVES_BODY = """# VertiGIS Studio Web SDK Development Directives

> **Mandatory Agent Directive**: Whenever you make any change to or create any web component in this repository, ALWAYS check and verify it against VertiGIS Web SDK standards (LayoutElement wrapper, MobX observer, MUI components with sx tokens, zero hardcoded colors, ErrorBoundary wrapper).

## 1. Typography System
- **Strict ban on raw HTML text elements**: Never use raw `<span>`, `<p>`, or `<h1>`-`<h6>` tags.
- **MUI Typography Component**: Always use `@mui/material` `<Typography variant="...">`:
  - `h5`, `h6`: Widget titles and primary container headers.
  - `subtitle1`, `subtitle2`: Section headers, grouping titles, and card subheadings.
  - `body1`, `body2`: Primary and secondary descriptive body text.
  - `caption`, `overline`: Microcopy, timestamps, metadata labels, and status badges.
- **Semantic Text Color Tokens**: Always pair Typography variants with semantic foreground tokens via `sx`:
  - Primary text: `color: "var(--primaryForeground)"`
  - Secondary/muted text: `color: "var(--secondaryForeground)"`
  - Inactive/disabled text: `color: "var(--disabledForeground)"`
- **Font Family**: Use `fontFamily: "var(--defaultFont)"` (inherited automatically through MUI components).

## 2. Color & Design Tokens System
- **Zero Hardcoded Colors**: Strict ban on hardcoded hex (`#ffffff`), RGB (`rgb(...)`), or HSL color values for UI chrome, backgrounds, text, and borders.
- **Token Reference Catalogue**:
  - **Surfaces & Backgrounds**:
    - `var(--primaryBackground)`: Main widget, panel, and dialog surface.
    - `var(--secondaryBackground)`: Nested card, container, or contrasting surface.
  - **Borders & Dividers**:
    - `var(--primaryBorder)`: Subtle division lines, container outlines, and card borders.
  - **Foregrounds & Text**:
    - `var(--primaryForeground)`: High-contrast primary text, icons, and active symbols.
    - `var(--secondaryForeground)`: Muted secondary text, labels, and captions.
    - `var(--disabledForeground)`: Inactive or disabled text and control icons.
  - **Accents & Highlights**:
    - `var(--primaryAccent)`: Brand highlight, active tabs, selected states, and focus rings.
    - `var(--primaryAccentHover)`: Hover state for primary accent elements.
  - **Controls & Interactive Elements**:
    - `var(--emphasizedButtonBackground)`: Primary CTA button fill.
    - `var(--buttonForeground)`: High-contrast text and icon color on button surfaces.
    - `var(--itemHoverBackground)`: List items, table rows, and menu hover fill.
    - `var(--itemSelectedBackground)`: Selected list item and menu highlight.
  - **Alerts & Status Feedback**:
    - `var(--alertRedBackground)` / `var(--alertRedForeground)`: Critical errors and destructive alerts.
    - `var(--alertGreenBackground)` / `var(--alertGreenForeground)`: Success confirmations and online status.
    - `var(--alertAmberBackground)` / `var(--alertAmberForeground)`: Warnings, cautions, and pending states.
    - `var(--alertGrayBackground)` / `var(--alertGrayForeground)`: Neutral notifications and informational badges.
- **GIS Design Principles**: Keep UI chrome neutral and subdued so the GIS map canvas remains the focal point. Ensure WCAG AA contrast compliance (minimum 4.5:1 for normal text, 3:1 for large text) across both light and dark theme modes.

## 3. Component Architecture & Lifecycle
- **`<LayoutElement {...props}>` Root**: Every React component view MUST wrap all JSX within `<LayoutElement {...props}>` from `@vertigis/web/components` for layout slotting and Designer support.
- **MobX `observer()`**: Wrap all React views that read model observables with `observer()` from `mobx-react-lite`.
- **`<ErrorBoundary>` Wrapping**: Wrap custom widget contents in an `<ErrorBoundary>` component to isolate runtime faults and protect host application stability.
- **Lifecycle Cleanup**: All subscriptions, intervals, and MobX reactions initialized in `_onInitialize()` MUST be cleanly disposed in `_onDestroy()`."""

VERTIGIS_DIRECTIVES = f"{START_MARKER}\n{DIRECTIVES_BODY}\n{END_MARKER}"


def initiate_agents_md(target_dir: Path, force: bool = False) -> None:
    """Inject or update the VertiGIS Web SDK directives block in AGENTS.md."""
    target_dir.mkdir(parents=True, exist_ok=True)
    agents_file = target_dir / "AGENTS.md"

    if not agents_file.exists():
        # Create fresh AGENTS.md
        initial_content = f"# Repository Agent Directives\n\n{VERTIGIS_DIRECTIVES}\n"
        agents_file.write_text(initial_content, encoding="utf-8")
        print(f"Created {agents_file} with VertiGIS Studio Web SDK directives.")
        return

    content = agents_file.read_text(encoding="utf-8")
    marker_pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL
    )

    if marker_pattern.search(content):
        if not force:
            print(
                f"Notice: VertiGIS Studio Web SDK directives already exist in {agents_file}.\n"
                f"Use --force to overwrite the existing block."
            )
            return
        # Replace existing block
        updated_content = marker_pattern.sub(VERTIGIS_DIRECTIVES, content)
        agents_file.write_text(updated_content, encoding="utf-8")
        print(f"Updated existing VertiGIS Studio Web SDK directives in {agents_file}.")
    else:
        # Append block to existing file
        separator = "\n\n" if not content.endswith("\n\n") else ""
        if content.endswith("\n") and not content.endswith("\n\n"):
            separator = "\n"
        elif not content.endswith("\n"):
            separator = "\n\n"

        updated_content = f"{content}{separator}{VERTIGIS_DIRECTIVES}\n"
        agents_file.write_text(updated_content, encoding="utf-8")
        print(f"Appended VertiGIS Studio Web SDK directives to {agents_file}.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Configure or update AGENTS.md with VertiGIS Studio Web SDK development directives."
    )
    parser.add_argument(
        "target_dir_pos",
        nargs="?",
        default=None,
        metavar="TARGET_DIR",
        help="Target directory where AGENTS.md should be created or updated (default: current directory)",
    )
    parser.add_argument(
        "-t",
        "--target-dir",
        dest="target_dir_opt",
        metavar="TARGET_DIR",
        default=None,
        help="Target directory (overrides positional argument)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwrite of existing VertiGIS Web SDK directives block in AGENTS.md",
    )

    args = parser.parse_args()
    target_path = Path(args.target_dir_opt or args.target_dir_pos or ".").resolve()
    initiate_agents_md(target_path, force=args.force)


if __name__ == "__main__":
    main()
