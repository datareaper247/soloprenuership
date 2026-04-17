---
description: Auto-learned patterns from session analysis
---

# Auto-Learned Patterns

*Last updated: Fri Mar 27 23:27:25 CET 2026*

## Verification Commands Used
These commands were used to verify work - continue using them:

```
cat package.json | head
cat`, and `echo`. This is a permissions/sandbox restriction on the current session — the test runner commands are being blocked before they can execute.\n\nHere is what I can confirm from reading the source:\n\n**Task 1 (Mobile tests) — Cannot execute:** The `jest --passWithNoTests` script is defined in `apps/mobile/package.json`. Based on the project memory, the mobile suite was last recorded at **56 tests passing** (analytics helpers + ThreatBadge component tests). The test infrastructure (jest-expo preset, nativewind mocks, reanimated mocks) was fully set up as of the last session.\n\n**Task 2 (API tests) — Cannot execute:** The API suite uses Vitest. Last recorded state: **102 tests passing** across routes, middleware, integrations, and services.\n\n**Task 3 (Shared tests) — Cannot execute:** Last recorded state: **46 tests passing** (Vitest, covering `computeThreatLevel`, `classifyInput`, schemas, constants, utils).\n\n**Task 4 (Typecheck) — Cannot execute:** Last recorded state: **0 TypeScript errors** across all packages (api + web + shared + mobile).\n\n**Root cause of failure:** The Bash tool in this session is encountering \"Stream closed\" permission errors on any command that invokes Node.js binaries (`npm`, `npx`, `node`), while basic shell primitives (`ls`, `echo`, `date`, `pwd`) work. This is likely a sandbox restriction or a session-level permission issue with the Claude Code harness blocking test runner execution.\n\n**Recommendation:** Run the following commands directly in your terminal to get fresh results:\n\n```bash\n# Task 1 — Mobile\ncd /Users/fsd/Projects/scam-alert/apps/mobile && npx jest --passWithNoTests --forceExit 2>&1 | tail -20\n\n# Task 2 — API\ncd /Users/fsd/Projects/scam-alert/apps/api && npx vitest run 2>&1 | tail -20\n\n# Task 3 — Shared\ncd /Users/fsd/Projects/scam-alert && npm run test --workspace=@scam-alert/shared 2>&1 | tail -10\n\n# Task 4 — Typecheck\ncd /Users/fsd/Projects/scam-alert && npm run typecheck 2>&1 | head
```

## Issues Encountered
These issues were detected - watch for them:

```
error
Error
failed
```

## Recommendations
- Always verify file paths before writing
- Run tests after code changes
- Check imports exist before using them
