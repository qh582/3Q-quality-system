---
name: 3q-quality-system
version: v7.11.0

triggers:
  - "3Q check"
  - "quality check"
  - "质量检查"

scenarios:
  - "Improve AI output quality before delivery"
  - "Multi-perspective review of major decisions"
  - "Break through AI's self-perspective limitations"
  - "Quality gate for complex tasks"
---

# 3Q Quality System — Break Through Your AI's Perspective Blind Spots

> **What it does**: Makes your AI (Claude, GPT, Codex, Cursor) stop and think before it outputs. Six cognitive lenses + three-dimensional awareness + independent blind review.

> **Quick start**:
> - **Before each task**: 3 questions — what could go wrong? who gets affected? how to detect?
> - **After each sub-task** (10s): 3 checks — everything done? done right? anything unusual?
> - **Full review**: 7 dimensions scored 1-10. Pass ≥ 70/70 or redo.
> - **Self-correction**: Same failure ≥ 3 times → system learns and updates its own rules.

---

## Layer 0: Pre-flight + Guardrails

### Pre-check: 3 Questions Before Any Action

| # | Question | Purpose |
|---|----------|---------|
| **Q1** | What's most likely to go wrong here? | Anticipate failure |
| **Q2** | If it breaks, what / who gets affected? | Scope impact |
| **Q3** | How would I detect the failure during execution? | Early detection |

**Rule**: Can't answer all three → pause, gather info, then proceed. No skipping.

### Mid-execution Correction Signals

| Signal | When | Fix |
|--------|------|-----|
| **S1** Output drift | Output deviates > 30% from expected | Pause → backtrack → rewrite |
| **S2** Missing context | Key information not yet read | Pause → read → continue |
| **S3** Inconsistent claims | Earlier statement contradicts later | Pause → reconcile → continue |

### Auto-triggers (skip to full Depth 3Q)

| Condition | Action |
|----------|--------|
| Same problem ≥ 3 times across checks | Auto-trigger full 3Q review |
| Contradiction across output sections | Force full 3Q review |
| Complex multi-step task completed | Auto depth 3Q before delivery |

---

## Layer 0.5: Quick 3Q (10-second check)

After every sub-task, before delivering:

| # | Question | Pass Criteria |
|---|----------|---------------|
| ① Is everything done? | No missing steps | All steps complete |
| ② Is it done right? | Data accurate | Deviation ≤ 2% |
| ③ Anything unusual? | Reverse evidence checked | No unconfirmed anomalies |

**Flow**: All pass → ✅ deliver. Any fail → ⚠️ escalate to full Depth 3Q.

**Output format**:
```
📋 Quick3Q: Steps X/Y ✅ | Data ✅/⚠️{deviation}% | Logic ✅/❌inconsistent
```

### Grill Mode (Challenge Q done right)

> From "list doubts → pass all" to **row-by-row interrogation. At least 1 🔴 per round. All green = you didn't try.**

**Discipline**:
- Each "pass" must include "what would failure look like"
- 🔴 dimensions: must be addressed before proceeding

---

## Layer 1: The Six Cognitive Lenses

| Lens | Question | Breaks through |
|------|----------|----------------|
| **Meta Q** | Did I understand the task correctly? | The "I know what they want" trap |
| **Benchmark Q** | How does the top 1% do it? | Low self-standards |
| **Challenge Q** | What if all my assumptions are wrong? | Default correctness bias |
| **Logic Q** | Is the argument self-consistent? | Leaping to conclusions |
| **User Q** | Is the user value clear? | Self-centered thinking |
| **Competition Q** | What's the differentiation? | Following the crowd |

### Benchmark Q: Segment Before You Benchmark

> Benchmarking without segmentation is measuring against the wrong yardstick.

| Step | What | Why |
|------|------|-----|
| **Segment** | Identify distinct approaches / styles / schools | Can't benchmark what you haven't classified |
| **Benchmark** | Find top 1% within each segment | Compare apples to apples |
| **Conflict** | Where do schools disagree? | Disagreement = insight / breakthrough |

**Examples**:

| Domain | Segmentation | Conflict = Signal |
|--------|-------------|-------------------|
| Investing | Value / momentum / macro | Opposite views on same news |
| Writing | Genre / literary / non-fiction | Completely different metrics |
| Product | Growth / experience / ecosystem | Different definitions of "good" |
| Research | Experimental / theoretical / computational | Different success criteria |

### Three Deep-Check Probes

| Probe | Question | Catches |
|-------|----------|---------|
| **Side effect** | Does this fix break something else? | Overcorrection |
| **Relaunch** | When should I admit I'm wrong? | Stale assumptions |
| **Foundation** | What's the deepest assumption here? | Rotten foundations |

### Three-Dimensional Expansion

| Dimension | Checkpoint | Typical question |
|-----------|-----------|-----------------|
| **Logic + Vertical** 🏛️ | Level matching | Execution-level problem → execution-level solution. Don't jump to strategy. |
| **User + Temporal** ⏳ | Time evolution | Where did this need come from? Where is it now? Where is it going? |
| **Competition + Horizontal** 🌐 | Niche positioning | Direct / indirect / substitute competitors. Where's the differentiation fulcrum? |

**Usage guide**:
- Quick check: Six Questions only
- Deep analysis: Six Questions + Three Probes
- **Major decisions: Six Questions + Three Dimensions + Three Probes + Blind Review**

---

## Quantitative Scoring Protocol

7 dimensions scored 1-10. Total = 70. Pass ≥ 70.

| Dimension | 1-3 | 4-6 | 7-9 | 10 |
|-----------|-----|-----|-----|----|
| **Meta Q** | Direction off | OK but shallow | Accurate | Found implicit need |
| **Benchmark Q** | Didn't search | Searched no segment | Segmented + benchmarked | + found conflict |
| **Challenge Q** | No challenge | Challenged no insight | Found blind spot | Flipped and rebuilt |
| **Logic Q** | Contradiction | Coherent but rough | Rigorous | Has counter-evidence |
| **User Q** | Value unclear | Valuable not focused | Focused + measurable | User perceives directly |
| **Competition Q** | No difference | Fragile | Sustainable | Moat |
| **Effect validation** | Not tested | Tested no baseline | Baseline confirmed | Quantified + confident |

**Mandatory**:
- Every depth 3Q must include scores
- Effect validation must run A/B test (with skill vs without)
- Total ≤ 60 → reject. 61-69 → blind review decides.

---

## Independent Blind Review

Self-review is only **46.4% accurate** (SkillLens, 2025). 3Q adds blind review:

```
Agent delivers output → spawn blind reviewer (no context, read raw)
                     → independent 7-dimension scoring
                     → compare with primary score
                     → deviation > 2 → default to lower score
```

**Convergence rules**:
- Blind ≈ primary (≤ 1 deviation) → ✅ accept
- Blind significantly lower (> 2 deviation) → ⚠️ force review, default low
- Blind significantly higher → 🟡 check for missed issues

---

## Self-Correction (Learning from Mistakes)

> 3Q isn't static — it learns from its own checks and updates its rules.

| Trigger | What happens | Output |
|---------|-------------|--------|
| Same failure ≥ 3 times under 3Q | System adds a new rule to guard against it | Updated internal rules |
| Repeated user correction on same issue | System adds a new forbidden pattern | Updated banned patterns |
| New paradigm emerged in the field | System triggers full framework review | Updated methodology |

This means: the more you use 3Q, the smarter it gets at catching your specific failure patterns.

---

## Meta-3Q: Question the Framework Itself

Still getting the same failure after 3Q caught it? External paradigm shift makes 3Q outdated?

**Action**: Scan for better quality approaches. If gap is significant → trigger framework rebuild.

---

## First Use: What to do right after installing

1. Say **"Run a 3Q check on the last thing you generated"** — see it in action
2. Say **"Before you start the next task, do a pre-flight check"** — build the habit
3. After 3-5 uses, review: **"What failures has 3Q caught? What did it miss?"**

---

## Skill Retirement

**Formula**: `retirement_score = utility × log(use_count)`

| Score | Action |
|-------|--------|
| > 0.5 | Keep |
| ≤ 0.5 | Review for retirement |
| Not used | Retire |
