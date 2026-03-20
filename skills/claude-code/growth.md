# /growth — Growth Hacking Skill

> Usage: `/growth [command] [arguments]`
>
> Activate: "use growth skill" or `/growth help`

---

## Overview

The growth skill turns Claude into a data-driven growth partner. Every command produces a structured, actionable artifact — no vague advice. Commands apply ICE scoring, statistical rigor, and proven growth frameworks so you can run experiments and move metrics with confidence.

---

## ICE Scoring (Used Across All Commands)

Every growth recommendation is scored on three axes:

| Axis | Scale | Definition |
|------|-------|-----------|
| **Impact** | 1–10 | How much will this move the north star metric if it works? |
| **Confidence** | 1–10 | How sure are we it will work, based on evidence? |
| **Ease** | 1–10 | How fast can we ship it? (10 = days, 1 = months) |

**ICE Score** = (Impact × Confidence × Ease) / 3

Prioritize items with ICE > 5. Cut items with ICE < 3 unless strategically important.

---

## Commands

### `/growth experiment [hypothesis]`

**Purpose**: Design a statistically rigorous A/B experiment.

**Hypothesis format**: "If we [change], then [metric] will [direction] because [mechanism]."

**Methodology**:
1. Parse hypothesis into independent variable, dependent variable, and causal mechanism
2. Calculate required sample size using two-proportion z-test
3. Estimate time to significance based on daily traffic
4. Define guardrail metrics (what must not degrade)
5. Specify segmentation, randomization unit, and exclusion criteria

**Sample size formula**:
```
n = 2 × ((z_α + z_β)² × p̄(1-p̄)) / (p1 - p0)²
where p̄ = (p0 + p1) / 2
For 95% confidence, 80% power: use (1.96 + 0.84)² ≈ 7.85
```

**Output format**:
```
## Experiment Brief: [Short Name]

### Hypothesis
If we [change X], then [metric Y] will [improve by Z%] because [mechanism].

### Setup
- Primary metric: [metric + measurement method]
- Guardrail metrics: [list — must not degrade >5%]
- Randomization unit: [user / session / account]
- Variants: Control (current) vs Treatment ([description])
- Traffic split: 50/50

### Sample Size Calculation
- Baseline rate: X%
- Minimum detectable effect: Y% relative improvement
- Required sample per variant: N users
- Daily traffic eligible: D users
- Estimated runtime: ~W weeks

### Launch Checklist
[ ] Instrumentation verified in staging
[ ] AA test passed (no pre-experiment divergence)
[ ] Exclusion list set (new accounts only / existing excluded)
[ ] Monitoring dashboard created
[ ] Rollback plan defined

### Decision Rules
- Ship if: p < 0.05 AND primary metric ↑ AND no guardrail regressions
- Iterate if: directionally positive but underpowered
- Stop if: guardrail metric degrades > 5% OR no movement after 2× required sample
```

**Quality standards**: Never recommend running an experiment with < 100 conversions per variant. Flag novelty effects for UI changes running < 2 weeks.

---

### `/growth funnel-analyze [description]`

**Purpose**: Analyze a conversion funnel, identify drop-off points, and prioritize fixes.

**Methodology**:
1. Calculate step-by-step conversion rates and cumulative conversion
2. Identify biggest absolute drop-off (users lost) and relative drop-off (% lost)
3. Pareto analysis: which 2–3 steps explain 80% of total leakage?
4. Benchmark each step against SaaS/product medians
5. Generate root-cause hypotheses for top drops

**SaaS funnel benchmarks**:
| Stage | Weak | Median | Strong |
|-------|------|--------|--------|
| Landing → Signup | < 2% | 3–5% | > 8% |
| Signup → Activation | < 20% | 35–50% | > 60% |
| Trial → Paid | < 5% | 10–20% | > 25% |
| Monthly retention (M1) | < 60% | 70–80% | > 85% |

**Output format**:
```
## Funnel Analysis: [Funnel Name]
**Period**: [date range]  |  **Segment**: [segment if specified]

### Step-by-Step Conversion
| Step | Users | Step CVR | Cumulative CVR | vs Benchmark | Lost Users |
|------|-------|----------|----------------|-------------|------------|

### Leakage Analysis (Pareto)
Top 3 drop-offs account for X% of total leakage:
1. [Step A → B]: X,XXX users lost (XX% of total leakage)
   Root cause hypotheses: [list 3 hypotheses]
   Recommended experiment: [specific test]
   ICE score: X

2. [Step B → C]: ...

### Quick Wins (ICE > 6)
| Action | Step improved | Estimated CVR lift | ICE | Effort |

### Investigation Priorities
- Quantitative: [what analytics queries to run]
- Qualitative: [which user research to do — session recordings, surveys, etc.]
```

---

### `/growth viral-loop [product]`

**Purpose**: Design a referral or viral growth mechanism.

**Viral loop types**:
| Type | K-factor potential | Best for |
|------|-------------------|---------|
| Word-of-mouth | 0.1–0.3 | B2B tools with visible outputs |
| Product-led viral | 0.2–0.5 | Collaboration/sharing features |
| Incentivized referral | 0.3–0.8 | B2C, high-frequency products |
| Inherent virality | 0.5–2.0 | Communication/network products |

**K-factor formula**: K = invitations sent per user × invitation conversion rate

**Methodology**:
1. Identify natural sharing moments in the user journey
2. Match viral loop type to product category and user behavior
3. Design the complete loop: trigger → share mechanism → landing → conversion
4. Calculate projected K-factor under conservative and optimistic assumptions
5. Define the minimum viable viral feature to test first

**Output format**:
```
## Viral Loop Design: [Product]

### Current Acquisition Baseline
- Organic/referral share of new signups: X%
- Target K-factor: Y (current estimated: Z)

### Recommended Viral Mechanisms (by ICE)

#### 1. [Mechanism Name] — ICE: X
**Loop**: [User does X] → [System enables Y] → [Third party sees Z] → [Action taken]
**Trigger point**: [Where in the UX this fires]
**Incentive structure**: [Giver incentive] + [Receiver incentive]
**Friction to remove**: [1-2 specific friction points]
**Estimated K-factor contribution**: +X
**Implementation effort**: [S/M/L]
**Example**: [Company that does this well]

#### 2. [Mechanism Name] — ICE: Y
...

### K-Factor Model
| Assumption | Conservative | Base | Optimistic |
|-----------|-------------|------|------------|
| Shares per active user / month | | | |
| Share → Visit CVR | | | |
| Visit → Signup CVR | | | |
| K-factor | | | |
| Effect on growth rate (monthly) | | | |

### MVP Test (Ship in < 2 weeks)
[Simplest version to validate core loop — no incentives, just raw sharing test]
```

---

### `/growth retention [problem]`

**Purpose**: Design a retention strategy and win-back campaign.

**Retention framework — four levers**:
1. **Activation**: Get users to first value quickly (reduces early churn)
2. **Habit formation**: Drive repeat usage through triggers and streaks
3. **Value expansion**: Deepen product usage via feature discovery
4. **Recovery**: Re-engage disengaged users before they cancel

**Methodology**:
1. Diagnose which lever is the primary problem (map `problem` to lever)
2. Identify the behavioral trigger or absence causing retention failure
3. Design a multi-touch intervention campaign
4. Define success metrics and measurement windows

**Output format**:
```
## Retention Strategy: [Problem Statement]

### Diagnosis
Retention lever: [Activation / Habit / Expansion / Recovery]
Root cause hypothesis: [Why users are leaving]
Evidence needed to confirm: [Data to pull]

### Campaign Design: [Campaign Name]

**Target segment**: [Who qualifies for this campaign]
**Entry trigger**: [Behavioral event that adds user to campaign]
**Exit trigger**: [Event that removes user from campaign — "graduated" or churned]

| Touch | Day | Channel | Subject/Trigger | Message hook | CTA |
|-------|-----|---------|-----------------|-------------|-----|
| 1 | D0 | In-app | [event] | [hook] | [action] |
| 2 | D3 | Email | [subject line] | [hook] | [action] |
| 3 | D7 | Email | [subject line] | [hook] | [action] |
| 4 | D14 | Email | [subject line — last chance] | [hook] | [action] |

**Win-back sequence** (for churned users):
Wave 1 (D30): [soft re-engagement — no offer]
Wave 2 (D45): [feature update — new value proof]
Wave 3 (D60): [discount offer — 20% off first month back]

### Success Metrics
- Primary: [retention rate at M1/M3]
- Secondary: [engagement metric — e.g. weekly active]
- Anti-metric: [what must not happen — e.g. spam complaints]
- Measurement window: [X days after campaign entry]
```

---

### `/growth ab-test [variant-description]`

**Purpose**: Analyze A/B test results with statistical significance.

**Bayesian vs Frequentist note**: This skill uses frequentist z-test for standard binary metrics. For revenue per user or continuous metrics, a t-test is appropriate. For early-stage tests with < 1,000 samples, Bayesian probability of being best serves as a supplementary measure.

**Output format**:
```
## A/B Test Results: [Test Name]

### Raw Data
| Variant | Visitors | Conversions | CVR |
|---------|----------|-------------|-----|
| Control | N | C | X% |
| Treatment | N | C | Y% |

### Statistical Analysis
- Absolute lift: +X percentage points
- Relative lift: +Y%
- Z-score: Z
- P-value: P
- Statistical significance: [Yes (p < 0.05) / No / Borderline]
- 95% Confidence interval for lift: [A%, B%]

### Business Impact (if shipped)
- Current monthly conversions: X
- Incremental conversions / month: +Y
- Revenue impact / month: +$Z (at $ACV avg)
- Annual impact: +$W

### Decision
[SHIP / ITERATE / STOP]

Rationale: [2-3 sentences explaining the recommendation]

### Caveats
- [Any segment imbalances detected?]
- [Did the test run long enough to capture a full weekly cycle?]
- [Were there external events during the test period?]
- [Is the effect size practically meaningful even if statistically significant?]
```

---

### `/growth pirate-metrics [data]`

**Purpose**: AARRR funnel analysis (Acquisition → Activation → Retention → Referral → Revenue).

**Framework**:
| Stage | What it measures | Key metric |
|-------|-----------------|-----------|
| Acquisition | How do users find you? | CAC by channel |
| Activation | Do users experience first value? | Activation rate |
| Retention | Do activated users return? | M1 / M3 retention |
| Referral | Do users tell others? | NPS, K-factor |
| Revenue | Do you make money? | MRR, ARPU, LTV |

**Output format**:
```
## AARRR Analysis: [Product/Period]

### Stage Scores
| Stage | Current metric | Benchmark | Score (1–5) | Priority |
|-------|---------------|-----------|-------------|---------|
| Acquisition | | | | |
| Activation | | | | |
| Retention | | | | |
| Referral | | | | |
| Revenue | | | | |

### Weakest Link
Stage [X] is the primary constraint: [evidence + root cause hypotheses]

### Improvement Roadmap
Fix stages in this order (fix leaks before adding more water):
1. [Worst stage]: [top 2 experiments] — ICE scores: X, Y
2. [Second worst]: [top 2 experiments]
...
```

---

### `/growth north-star [company]`

**Purpose**: Define the north star metric and full driver tree.

**Methodology**:
1. Evaluate 3 NSM candidates against three criteria: reflects user value, predicts long-term revenue, measurable weekly
2. Recommend one NSM with trade-off explanation
3. Build a 3-level driver tree (NSM → L2 drivers → L3 levers)
4. Assign team ownership to each lever

**Output format**:
```
## North Star Metric: [Company]

### NSM Candidates
| Candidate | Pros | Cons | Verdict |
|-----------|------|------|---------|

### Recommended NSM
**[Metric name]** — [Definition: who, what action, what time window]

Why this over alternatives: [2-3 sentences]
Current value: X  |  12-month target: Y

### Driver Tree
NSM: [Metric]
├── L2: [Driver 1] (owned by: [team])
│   ├── L3: [Lever 1a] → [Experiment ideas]
│   └── L3: [Lever 1b] → [Experiment ideas]
├── L2: [Driver 2] (owned by: [team])
│   ├── L3: [Lever 2a] → [Experiment ideas]
│   └── L3: [Lever 2b] → [Experiment ideas]
└── L2: [Driver 3] (owned by: [team])
    ├── L3: [Lever 3a] → [Experiment ideas]
    └── L3: [Lever 3b] → [Experiment ideas]

### Dashboard Spec
Metrics to track weekly: [list the L2 + NSM metrics with target values]
```

---

### `/growth channel-score [channels]`

**Purpose**: Score acquisition channels by CAC, conversion quality, scalability, and strategic fit.

**Scoring dimensions**:
| Dimension | Weight | Definition |
|-----------|--------|-----------|
| CAC efficiency | 30% | LTV:CAC ratio for this channel |
| Conversion quality | 20% | Retention of customers from this channel vs average |
| Scalability | 25% | Can spend 10× and maintain efficiency? |
| Payback speed | 15% | Months to recover CAC |
| Brand fit | 10% | Does this channel reach the ICP? |

**Output format**:
```
## Channel Scorecard: [Company]

### Per-Channel Metrics
| Channel | Spend/mo | Signups/mo | Customers/mo | CAC | LTV:CAC | Payback |
|---------|----------|------------|--------------|-----|---------|---------|

### Weighted Scores
| Channel | CAC eff. | Quality | Scalability | Payback | Brand fit | Total |
|---------|----------|---------|-------------|---------|-----------|-------|

### Portfolio Recommendation
**Double down**: [Channel A] — [rationale]
**Test and scale**: [Channel B] — [what to test next]
**Hold / optimize**: [Channel C] — [optimization suggestion]
**Cut**: [Channel D] — [why to stop]

### Next 90-Day Experiments
| Experiment | Channel | Hypothesis | Budget | Success criteria |
|-----------|---------|-----------|--------|-----------------|
```

---

## Quality Standards (All Commands)

- All statistical claims must include confidence levels and sample size context
- ICE scores must be calculated, not estimated qualitatively
- Every output must include a "Next Step" — one concrete action to take this week
- Flag when data is insufficient for a reliable recommendation
- Never recommend shipping based on statistical significance alone — require practical significance (lift > MDE)
