# Contributing to SoloOS

SoloOS is open source. Contributions that make it genuinely more useful for solo founders
are welcome. Here's what moves the needle vs. what doesn't.

---

## What Actually Helps (High Impact)

### 1. Better examples
The single highest-impact contribution. Real input → output examples that show
a skill working in a real founder scenario.

**Format**: See `examples/validate-saas-idea.md` as the template.
Requirements:
- Real product idea, real competitor landscape, real output
- "What happened after" section — shows the outcome, not just the process
- "What this demonstrates" section — explains what's non-obvious about the output

### 2. Sharper role system prompts
Not more roles — sharper ones. The 10 core roles need to be senior-quality.
That means: specific frameworks (named, sourced), specific output formats,
and honest "escalate when" criteria that reflect what the role actually can't do.

**How to evaluate quality**:
Ask: "Would a real senior [role] give this advice, or would they ask for more context first?"
If the role gives confident advice without sufficient context → it's not senior quality.

**What not to contribute**:
- New extended roles (we have 44, we don't need more)
- Generic additions to existing prompts (longer ≠ better)

### 3. Real /onboard improvements
Finding questions that produce better context calibration, or output templates
that make the context files more useful across sessions.

### 4. Fixing the skills that are still shallow
`/content`, `/ops`, `/growth`, `/geo` still describe what should happen rather than
encode specific frameworks. Converting any of them to the standard set by `/research`
or `/validate` is high value.

### 5. MCP server implementations (technical)
If you build one of the planned MCP servers, it belongs here.
Requirements:
- Must use `@modelcontextprotocol/sdk`
- Typed with Zod schemas
- README with environment variables
- Must actually work (test it before submitting)
- Publish as `@soloos/mcp-[name]` or submit as PR

---

## What Doesn't Help

- Adding more roles to `agents/roles/extended/` — we have enough
- Documentation about planned features that don't exist
- Generic SEO/marketing/sales tips that aren't encoded as behavioral rules
- Typo fixes without any other change
- Advice about "what SoloOS should be" without building the thing

---

## Standards for Skill Contributions

A skill contribution must pass this test:
**"Does this skill change Claude's behavior in a way it wouldn't behave by default?"**

If the skill just describes a framework Claude already knows about → it's not a behavioral unlock.
If the skill encodes a specific sequence, specific output format, or specific anti-pattern flag
that Claude wouldn't apply without the prompt → it's a real contribution.

Template for new skills:
```markdown
# Skill Name — One-line description

**Usage**: `/skillname "[input]"`

**Examples**: [2-3 real examples]

[1-2 sentences on what behavioral problem this solves]

---

## [Framework or sequence]
[Specific steps, not generic advice]

## Output Format
[Exact format with labeled sections]
```

---

## How to Submit

1. Fork the repo
2. Create a branch: `feature/skill-[name]` or `fix/[what-you-fixed]`
3. Make your change
4. If it's a skill: test it by running the command in Claude Code and pasting the output in a `examples/` file
5. Open a PR with: what you built, why it helps, and an example output

---

## What We're Not Looking For

To be blunt: SoloOS doesn't need to be bigger. It needs to be better.

The next 10 contributions that matter most are:
1. Better examples (2-3 more real ones)
2. Sharper /content skill (currently a menu)
3. Sharper /growth skill (currently a menu)
4. Sharper /ops skill (currently a menu)
5. One working MCP server (any of the planned ones)
6. Real /onboard output quality improvement
7. Better morning brief output with real metrics
8. A second CLAUDE.md behavioral rule that changes behavior visibly
9. A stage-based routing system (different advice at different MRR stages)
10. An example of a full /swarm product-launch run with real output

If your contribution fits one of these 10: open the PR.
