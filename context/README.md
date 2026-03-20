# Context Templates — SoloOS Memory System

Copy these files into your project root to give Claude persistent business context.
Every session that runs in a directory with these files gets a fully context-aware Claude.

---

## The Four Files

| File | What It Contains | Update Frequency |
|------|-----------------|------------------|
| `business-context.md` | Current state: MRR, customers, competition, focus, blockers | Weekly |
| `customer-voice.md` | Exact quotes from customers — pain, praise, objections | After every call |
| `experiment-log.md` | Growth experiments: hypothesis, results, learnings | After every test |
| `decision-log.md` | Strategic decisions: context, rationale, kill signals, outcomes | After every major decision |

---

## Setup (60 seconds)

```bash
# Copy context templates to your project
cp -r ~/soloos/context/* ./context/

# Or if you cloned SoloOS to ~/soloos
cp ~/soloos/context/*.md ./

# Now fill in business-context.md first — takes 10 minutes
# That's all Claude needs to stop giving generic advice
```

---

## Why This Works

Most AI sessions start from scratch. Every conversation, you re-explain your business, your customers, your constraints. This wastes time and produces generic advice.

These files create **persistent business DNA**. Claude reads them automatically at session start and every response is calibrated to YOUR specific:
- Stage (different advice for $0 vs $10K MRR)
- Customers (their actual words, not your assumptions about them)
- Competition (positioned against what you actually compete with)
- Decisions (advice consistent with past strategic choices)

The compounding effect: the longer you maintain these files, the more valuable Claude becomes for your specific business.

---

## The Compound Memory Effect

Week 1: "Here's my business context..."
Month 1: "Based on the 3 experiments you logged last month, [pattern emerges]"
Month 3: "Given your customer voice file, this copy resonates more than that"
Month 6: "Your decision log shows you consistently underestimate build time — here's the adjusted estimate"
Year 1: Claude knows your business better than any employee who joined last quarter

---

## Integration With SoloOS Skills

All SoloOS skills that produce output will improve with context files present:

| Skill | How It Uses Context |
|-------|-------------------|
| `/morning` | Reads business-context.md for pulse, references open decisions |
| `/decide` | References past decisions in decision-log.md for consistency |
| `/prospect` | Uses customer-voice.md for personalization language |
| `/sales outreach` | Uses customer pain language from customer-voice.md |
| `/research customer-profile` | Cross-references against your actual ICP |
| `/swarm product-launch` | Uses business context for all role outputs |
| `/role ceo` | Strategy advice calibrated to your actual stage and metrics |
| `/role cmo` | Marketing advice uses your real customer voice |

---

## Maintenance Habit

**5-minute Friday ritual**:
1. Update `business-context.md` numbers (5 min)
2. Paste any customer quotes from the week into `customer-voice.md` (2 min)
3. Log any experiments started or completed (3 min)

This 10-minute weekly habit builds a knowledge asset that compounds.
