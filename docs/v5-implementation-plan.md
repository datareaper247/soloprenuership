# SoloOS v5 — Implementation Plan
## Week 1: Maximum Leverage, Zero Infrastructure Required

**Date**: March 23, 2026
**Approach**: Parallel agents executing independently. Each agent owns one file.
No agent touches another agent's file. Merge when all complete.

---

## PHASE 1 — WEEK 1 (Pure Markdown, No Infrastructure)

All changes below are pure markdown edits to existing files or creation of new skill files.
Zero infrastructure. Zero deployment. Ship Friday.

### TASK 1: Wire BSHR Visible Output into decide.md
**File**: `skills/claude-code/decide.md`
**Change**: Add ANALOGOUS CASES section as a mandatory output element for any
recommendation with reversibility ≤6/10.

```markdown
## ANALOGOUS CASES (mandatory for reversibility ≤6/10)

Before delivering recommendation, search FOUNDER_INTELLIGENCE.md and PATTERN_LIBRARY.md
for the closest matching founder situation. Output:

ANALOGOUS CASES:
- **[Founder/Product]** at **[stage]**: Faced [similar decision]. Chose [option].
  Outcome: [specific result with numbers if available].
  Pattern: [[P-XX]] or [[FL-XXX]]
  Match confidence: [HIGH if stage+domain+decision type all match / MEDIUM if 2/3 / LOW if 1/3]
  What differs in your case: [specific delta that might change the recommendation]

If no match found in knowledge base: state explicitly "No direct analog found.
Recommendation is based on general principles, not documented founder evidence."
This transparency is itself a trust signal.
```

**Why this change**: The BSHR loop already runs silently. This makes the pattern matching
visible at the exact moment the founder needs it most. 3x improvement in decision trust
at zero additional compute cost. The data is already there.

---

### TASK 2: Add [ADVERSARY] Block to decide.md
**File**: `skills/claude-code/decide.md`
**Change**: Add mandatory [ADVERSARY] block before final recommendation for reversibility ≤5/10.

```markdown
## ADVERSARY BLOCK (mandatory for reversibility ≤5/10)

For any recommendation where reversibility ≤5/10, generate the following BEFORE the
recommendation. This is a structural requirement, not a tone change.

[ADVERSARY]
The strongest case AGAINST this plan:
[1-2 sentence maximum. The single most damaging argument against the recommendation.]

Evidence supporting the adversary position:
[Specific data, pattern, or documented founder case that supports the contrary view.]

What would need to be true for the adversary to be wrong:
[The specific condition that, if confirmed, eliminates this risk.]

[/ADVERSARY]

RECOMMENDATION: [proceed with full recommendation]
```

**Why this change**: Georgetown Law research confirms tone-based anti-sycophancy is
partially effective at best. A named structural entity that is REQUIRED to appear in
output cannot be overridden by conversational momentum. The founder sees dissent before
they see the recommendation — this is the correct order.

---

### TASK 3: Add Gate 0 to validate.md
**File**: `skills/claude-code/validate.md`
**Change**: Insert Gate 0 (ChatGPT Substitution Test) BEFORE the existing Gate 1.

```markdown
## GATE 0: SUBSTITUTION TEST (AI products only — runs before all other gates)

Fires when: product involves AI, ML, LLM, automation, or "AI-powered [task]"

**The Test**:
Open ChatGPT (free tier). Attempt the core value proposition manually.
Use only a text prompt — no special tools, no API, no integrations.

**Decision tree**:
- Result is <40% of your product → ChatGPT CANNOT substitute → proceed to Gate 1
- Result is 40-60% → PARTIAL SUBSTITUTE → name your workflow integration layer and
  proprietary data source before proceeding. If you can't name both: STOP.
- Result is >60% → CHATGPT SUBSTITUTE → this specific product form will be commoditized.
  Required question: "What is my Layer 2?" Three viable answers:
  1. **Workflow embedding** (tool lives inside their existing workflow, not standalone chat)
  2. **Proprietary data moat** (you have training data/context no one else has)
  3. **Speed+convenience margin** (10x faster on this specific task, worth paying for)
  If you cannot name a Layer 2: recommend pivoting before proceeding.

**Why Gate 0 comes first**: 25-30% of AI products fail because ChatGPT absorbed the use case
after launch. Discovering this in Gate 0 costs 5 minutes. Discovering it at month 6 costs
everything. This gate is cheap insurance.
```

---

### TASK 4: Create bandwidth.md
**File**: `skills/claude-code/bandwidth.md` (NEW FILE)
**Purpose**: Founder state detection + capacity-aware recommendation routing.
Prevents worst failure mode: irreversible decisions made in depleted state.

Full file content: detect bandwidth from conversation signals, run capacity audit,
adjust recommendation depth based on state. See implementation spec below.

---

### TASK 5: Create legal-tax-structure.md
**File**: `skills/claude-code/legal-tax-structure.md` (NEW FILE)
**Purpose**: Tax optimization ladder + entity structure guidance.
At $50K+ ARR as sole proprietor: founder loses $12-18K/year vs S-Corp election.
That's more than all founder tool budgets combined.

Full file content: entity selection guide, tax optimization ladder,
stage-calibrated thresholds. See implementation spec below.

---

### TASK 6: Create content-founder.md
**File**: `skills/claude-code/content-founder.md` (NEW FILE)
**Purpose**: Detect content-founder archetype (>5K social followers) and route to
content-to-product flywheel instead of product-first advice.
Justin Welsh $4M+ model, Nathan Barry trajectory.

---

### TASK 7: Create exit-prep-early.md
**File**: `skills/claude-code/exit-prep-early.md` (NEW FILE)
**Purpose**: Backward-induction exit preparation from $5K MRR (not $50K+).
Clean metrics, founder dependency reduction, platform concentration monitoring.
Maximum ROI on exit prep habits formed at $5K, not $50K.

---

### TASK 8: Build /onboard wizard
**File**: `skills/claude-code/onboard.md` (NEW FILE)
**Purpose**: 20-minute interactive setup that populates context/ files and writes FL-001
(the founder's first kill signal). Makes SoloOS immediately valuable from session 1.

---

## PHASE 2 — WEEK 2

### TASK 9: Add failure-mode-detection to validate.md
**Change**: Add Competitor Failure Audit and Commodity Risk flag to validate.md.
"Why did the last 3 competitors in this space fail? What does that tell you about structural
failure modes in this category?"

### TASK 10: GitHub Action for kill signal pings
**File**: `.github/workflows/kill-signal-check.yml` (NEW FILE)
**Purpose**: Parses founder-log.md daily for overdue `Outcome due:` entries.
Sends notification. Zero Claude session required.

---

## PHASE 3 — WEEK 3 (Infrastructure)

### TASK 11: Memory OS hooks
Wire PostToolUse hook to auto-capture session decisions to founder-log.md.
Stop hook triggers session synthesis reminder.

### TASK 12: Mem0 MCP wrapper
Wrap Mem0 API as soloos-memory MCP. Auto-extracts business facts after every conversation.
Loads at session start instead of static context files.

### TASK 13: MCP auto-trigger wire-up
Connect CLAUDE.md auto-triggers to mcp__soloos-core__ tool calls.
VALIDATE fires → validate_idea_gates(). PMF fires → score_pmf(). FINANCE fires → calculate_ev().

---

## PHASE 4 — WEEK 4 (Distribution)

### TASK 14: Viral README
Anti-sycophancy as secondary hook. Memory Compound Effect as primary headline.
"The AI advisor that gets smarter about your business every week."

### TASK 15: Install script
`curl -sL .../install.sh | bash`
Copies CLAUDE.md + skills/ to project. Initializes context/ templates. Runs /onboard.

### TASK 16: Demo video
3 minutes. Three core moments:
1. /morning — kill signal check surfaces overdue experiment (30s)
2. DECIDE with [ADVERSARY] block fires on bad idea, founder pushes back, ANALOGOUS CASES shown (90s)
3. VALIDATE Gate 0 kills a ChatGPT-substitute idea before Gate 1 (60s)

---

## PARALLEL AGENT ASSIGNMENT (Week 1)

These tasks are fully independent — no shared files, no merge conflicts.
Launch all simultaneously:

| Agent | Task | File(s) | Estimated Lines |
|---|---|---|---|
| Agent A | Tasks 1+2: BSHR + ADVERSARY in decide.md | skills/claude-code/decide.md | +60 lines |
| Agent B | Task 3: Gate 0 in validate.md | skills/claude-code/validate.md | +50 lines |
| Agent C | Task 4: Create bandwidth.md | skills/claude-code/bandwidth.md (NEW) | ~300 lines |
| Agent D | Task 5: Create legal-tax-structure.md | skills/claude-code/legal-tax-structure.md (NEW) | ~400 lines |
| Agent E | Tasks 6+7: Create content-founder.md + exit-prep-early.md | two NEW files | ~200+200 lines |
| Agent F | Task 8: Create onboard.md | skills/claude-code/onboard.md (NEW) | ~250 lines |

**CLAUDE.md updates** (Tasks 1-8 all need corresponding auto-trigger entries):
Run as a final consolidation pass after all agents complete, not in parallel.

---

## QUALITY GATES

Before any skill file is considered complete:
1. Auto-trigger is defined in the file header (fires when: [specific patterns])
2. Output has a kill signal (what specific data proves this advice wrong)
3. Stage calibration is explicit (what changes at different MRR tiers)
4. At least 1 real founder reference in the content (specific name, product, outcome)
5. File follows the skill format: [Trigger conditions] → [Framework] → [Output format]

---

## SUCCESS CRITERIA FOR WEEK 1

All 8 tasks complete = Phase 1 done.
Definition of done for Phase 1:
- decide.md shows ANALOGOUS CASES and [ADVERSARY] block in output
- validate.md runs Gate 0 before Gate 1 for AI products
- bandwidth.md, legal-tax-structure.md, content-founder.md, exit-prep-early.md, onboard.md all created
- CLAUDE.md updated with auto-triggers for all new skills
- All files committed with tests (manual: run a sample question through each new trigger)

**Kill signal for Phase 1**: If after 1 week, any of the 8 files is incomplete or the
auto-trigger doesn't fire correctly → Phase 1 failed. Do not proceed to Phase 2 until
Phase 1 is fully working.

---

*Plan version 1.0 — March 23, 2026*
*Authors: Research Council synthesis (4 agents) + Claude Sonnet 4.6*
