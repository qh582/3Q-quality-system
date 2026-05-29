# 3Q Quality System

> **Break through your AI's self-perspective limitations.** Six cognitive lenses + three spatial dimensions — makes AI see what it would naturally miss.

**中文**: 3Q 质量系统 — 给 AI 装上质量护栏。支持 Claude Code / Cursor / Codex / OpenClaw.

[![Quality Score](https://img.shields.io/badge/quality-15/15-brightgreen)]()
[![Version](https://img.shields.io/badge/version-v7.11.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Awesome](https://awesome.re/badge.svg)]()

> **Topics**: `AI-quality` · `agent-skills` · `quality-guardrails` · `claude-code` · `cursor-rules`

## The Problem: AI (and humans) are trapped in their own perspective

An AI can answer correctly yet still produce outputs with logical leaps, assumed premises, and self-centered framing. Not because it's wrong — because it never looked from another angle.

## The Solution: Six Cognitive Lenses

| Lens | Question | Breaks through |
|------|----------|----------------|
| **Meta Q** | Did I understand the task correctly? | Assuming you're right |
| **Benchmark Q** | How does the top 1% do it? | Low standards |
| **Challenge Q** | What if all my assumptions are wrong? | Default correctness |
| **Logic Q** | Is the argument self-consistent? | Leaping arguments |
| **User Q** | Is the user value clear? | Self-centered framing |
| **Competition Q** | Where's the differentiation? | Blindly following trends |

These aren't checklist items — they are **perspective switches**. Each run forces the AI to see through a lens it wouldn't naturally choose.

### Three-Dimensional Expansion

If the Six Questions break through perspective, the Three Dimensions break through **scope**:

| Dimension | Checkpoint | Breaks through |
|-----------|-----------|----------------|
| **Vertical** 🏛️ Level matching | Execution problem → execution solution | Solving tactical issues with strategic responses |
| **Temporal** ⏳ Time evolution | Where from? Where now? Where to? | Only seeing the present moment |
| **Horizontal** 🌐 Niche positioning | Direct/indirect/substitute competitors | Only seeing yourself |

**Usage guide**:
- Quick check: Six Questions
- Deep analysis: Six Questions + Three Probes
- **Major decisions: Six Questions + Three Dimensions + Three Probes + Blind Review**

---

## How It Works

### Layer 0: Pre-flight Guardrails

**3 questions before every action:**

```
Q1: What's most likely to go wrong?
Q2: Who / what gets affected if it breaks?
Q3: How would I detect failure mid-execution?
```

Can't answer all three → pause and gather info. No skipping.

**Mid-execution correction signals:**
- Output deviates > 30% → pause → backtrack → rewrite
- Missing dependency found → pause → re-read → continue
- Version conflict → pause → confirm → continue

**Auto-triggers (skip to full Depth 3Q):**
- Same issue ≥ 3 times across audits
- Version mismatch in declarations
- Bottom changes not propagated to top

### Layer 0.5: Quick 3Q (10-second check)

After every sub-task:

```
① Everything done?    → Steps complete
② Done right?         → Deviation ≤ 2%
③ Anything unusual?   → No unconfirmed anomalies
```

All pass → deliver. Any fail → escalate to Depth 3Q.

### Layer 1: Depth 3Q + Blind Review

7 dimensions scored 1-10. Pass ≥ 70/70.

| Dimension | 1-3 | 4-6 | 7-9 | 10 |
|-----------|-----|-----|-----|----|
| Meta Q | Direction off | OK but shallow | Accurate | Found implicit need |
| Benchmark Q | Didn't search | Searched no segment | Segmented + benchmarked | + conflict found |
| Challenge Q | No challenge | Challenged no insight | Found blind spot | Flipped and rebuilt |
| Logic Q | Contradiction | Coherent but rough | Rigorous | Has counter-evidence |
| User Q | Value unclear | Valuable not focused | Focused + measurable | User perceives directly |
| Competition Q | No difference | Fragile | Sustainable | Differentiation is moat |
| Effect validation | Not tested | Tested no baseline | Baseline confirmed | Quantified + confident |

### Independent Blind Review

Self-review accuracy is only **46.4%** (SkillLens, 2025) — the "I know why it was written this way" bias.

3Q's fix: spawn an independent blind reviewer agent (no context, raw read) → score separately → compare → when deviation > 2, default to lower score.

---

## Self-Evolution

3Q also audits itself:

**Skill retirement**: `retirement_score = utility × log(use_count)`
- > 0.5 → keep
- ≤ 0.5 → retirement candidate
- Long dormant → retire

**Meta-3Q**: Same failure 3 times under 3Q? External paradigm emerged? → Trigger framework upgrade.

---

## Install

**Claude Code / Codex:**
```bash
npx skills add https://github.com/qh582/3Q-quality-system --skill "3Q-system"
```

**Cursor:** Copy `skills/3Q-system/SKILL.md` to `.cursor/rules/3Q.mdc`

**Manual:** Paste SKILL.md into project knowledge or system prompt.

---

## FAQ

**Q: How is this different from "review your output"?**
A: That's asking the model to self-criticize, which has 46.4% accuracy. 3Q is a structured cognitive framework with independent blind review.

**Q: What does it need to run?**
A: Zero dependencies. One SKILL.md file, any agent can read it.

**Q: Use cases?**
A: Code review, analysis reports, content creation, product design, decision evaluation. Not for real-time chat or trivial queries.

---

## File Structure

```
3Q-quality-system/
├── skills/
│   └── 3Q-system/
│       ├── SKILL.md
│       └── references/
│           ├── three-dimensions.md
│           ├── daily-check-template.md
│           └── decision-checklist.md
├── README.md                    # Chinese (primary)
├── README.en.md                 # English (this file)
├── package.json
├── LICENSE
```

## License

MIT
