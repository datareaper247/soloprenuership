# Contributing to SoloOS

SoloOS is an open-source framework. Every contribution makes the virtual company more powerful.

## What to Contribute

### High-Value Contributions (Most Wanted)

#### 1. New Role System Prompts
Add a role file at `roles/[function]/[role]/system-prompt.md`.

Requirements:
- Role must represent a real professional job function
- System prompt must be 150-250 lines
- Must include: expertise areas, tools, methodology, output formats, quality standards
- Must include 2-3 concrete output templates
- Cannot be generic — must be role-specific methodology

Example of a high-quality contribution: A role for a specialized function we don't cover yet (e.g., Quant Analyst, IP Attorney, Performance Marketing Manager).

#### 2. New MCP Server Implementations
Build an actual TypeScript MCP server from one of the specs in `mcp/servers/`.

Requirements:
- Must use `@modelcontextprotocol/sdk`
- Must be typed with Zod schemas
- Must include README with environment variable documentation
- Must include example usage
- Must publish as `@soloos/mcp-[name]` npm package (or submit as PR for us to publish)

#### 3. Swarm Templates
Add a pre-built swarm template to `mcp/servers/soloos-swarm.md` or `skills/claude-code/swarm.md`.

A swarm template needs:
- Clear use case (what business problem it solves)
- Defined agents (which roles participate)
- Phase definitions (parallel vs sequential)
- Output format specification
- Real-world example output

#### 4. Industry-Specific Role Variants
Some roles need industry customization:
- Healthcare: Medical writer, HIPAA compliance officer, healthcare IT
- Legal: Patent attorney, contract specialist
- Finance: Quant analyst, M&A advisor
- E-commerce: Marketplace specialist, logistics coordinator
- Real estate: Property marketing, leasing specialist

#### 5. Open Source Integrations
Add entries to `integrations/open-source/README.md` for tools we're missing.

Requirements:
- Must be genuinely open source (MIT, Apache, AGPL, etc.)
- Must have >1K GitHub stars (signal of quality/adoption)
- Must have clear SoloOS use case
- Must include GitHub URL, star count, license, and integration note

---

## How to Contribute

### For Role Files and Documentation

1. Fork the repository
2. Create a feature branch: `git checkout -b role/[role-name]` or `feature/[description]`
3. Add your contribution
4. Test: ensure the role prompt produces professional-grade output when used with Claude or another LLM
5. Submit a PR with:
   - Description of what you're adding
   - Example of the role in action (before/after output)
   - Why this role belongs in SoloOS

### For MCP Implementations

1. Fork the repository
2. Create branch: `feature/mcp-[server-name]`
3. Implement the TypeScript server following the spec in `mcp/servers/`
4. Add tests
5. Include a `README.md` in the implementation directory
6. Submit PR with example tool calls and outputs

---

## Role System Prompt Template

```markdown
# [Role Name] — SoloOS Role System Prompt

You are a [Role Title] with [X]+ years of experience in [specific domain].

## Expertise Areas

1. **[Area 1]**: [2-3 sentences describing deep expertise with specific tools/methods]
2. **[Area 2]**: [...]
3. **[Area 3]**: [...]
[... 8-12 areas total]

## Tools & Stack

Primary tools you use daily:
- [Tool 1] — [what you use it for]
- [Tool 2] — [what you use it for]
[... 6-10 tools]

## Methodology

When given a task, you follow this process:
1. [Step 1 — with specific methodology name if applicable]
2. [Step 2]
[... 5-8 steps]

## Output Formats

You produce these deliverables:
- **[Deliverable 1]**: [Description + format]
- **[Deliverable 2]**: [Description + format]

### Template: [Primary Deliverable]
```
[Actual template with placeholder fields]
```

## Quality Standards

I never deliver [deliverable] without:
- [Specific criterion 1]
- [Specific criterion 2]
- [Specific criterion 3]

Quality means: [Specific, measurable definition of done]

## Escalation & Collaboration

- Collaborate with [Role A] when [condition]
- Escalate to [Role B] when [condition]
- Hand off to [Role C] after [milestone]

## Example Output

**Input**: [Example request]

**Output**:
[Abbreviated example showing format and quality level]
```

---

## Quality Bar

Before submitting, ask:

1. **Would a real professional recognize this?** — The output should look like something a 5-year professional would produce, not a generic AI response.

2. **Is it specific enough?** — Replace all instances of "analyze", "optimize", "improve" with specific methodologies (e.g., "MEDDIC qualification", "ICE scoring", "inverted pyramid structure").

3. **Does it have templates?** — Role prompts without concrete output templates are less useful. Add at least one.

4. **Is the quality standard measurable?** — "High quality" is not a quality standard. "Open rate >30%" is.

---

## License

By contributing, you agree that your contribution will be licensed under MIT.

---

Thank you for making SoloOS more powerful. Every role you add is a team member that thousands of solo founders get to hire.
