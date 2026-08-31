# VertiGIS Studio Workflow SDK: Project Structure & Standards

## 1. Directory Structure

A VertiGIS Studio Workflow SDK project must follow this strict, modular architecture:

```text
src/
├── index.ts                          ← Barrel export: exports ALL activities + elements
├── activities/
│   └── <ActivityName>/
│       ├── main.ts                   ← ONLY class + I/O interfaces + JSDoc tags
│       └── utils/                    ← Required when main.ts > ~150 lines or domain logic is distinct
│           ├── types.ts              ← Interfaces, type aliases, constants
│           └── <domain>Helpers.ts   ← Pure/async functions per logical concern
└── elements/
    └── <ElementName>/
        ├── main.tsx                  ← Component logic + FormElementRegistration entry point
        ├── hooks/                    ← Custom hooks for state/effects (e.g. useMyLogic.ts, index.ts)
        ├── components/               ← Sub-components for UI decomposition (e.g. StatusBar.tsx, index.ts)
        ├── styles/                   ← Styling / theme files (if needed)
        └── utils/                    ← Types, default config, pure helper functions
            ├── types.ts
            ├── defaults.ts
            └── <domain>Utils.ts
```

---

## 2. Naming Conventions

- **Activity Class**: `<PascalCase>Activity` (e.g. `CalculateBufferActivity`, `PDFMapGeneratorActivity`).
- **Activity File**: `src/activities/<ActivityName>/main.ts`.
- **Form Element Registration ID**: Matches the element display name (e.g. `"FeatureInformation"`, `"StarRating"`).
- **Form Element File**: `src/elements/<ElementName>/main.tsx`.
- **Barrel Exports in `src/index.ts`**:
  - Activities end with `Activity` (e.g. `export { default as PDFMapGeneratorActivity } from "./activities/PDFMapGenerator/main";`).
  - Elements end with `Registration` (e.g. `export { default as FeatureInformationRegistration } from "./elements/FeatureInformation/main";`).

---

## 3. Top-Level Barrel Export (`src/index.ts`)

Every new activity and form element must be registered and exported in `src/index.ts`:

```typescript
// ==========================================
// Activities
// ==========================================
export { default as CalculateBufferActivity } from "./activities/CalculateBuffer/main";
export { default as PDFMapGeneratorActivity } from "./activities/PDFMapGenerator/main";

// ==========================================
// Form Elements
// ==========================================
export { default as StarRatingRegistration } from "./elements/StarRating/main";
export { default as FeatureInformationRegistration } from "./elements/FeatureInformation/main";
```
