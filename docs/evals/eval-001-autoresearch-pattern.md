# Evaluation: Understanding Autoresearch as a Recipe/Pattern

**Source:** Karpathy's follow-up tweet (March 2026)

> "oh yeah i should have linked autoresearch probably
> https://github.com/karpathy/autoresearch
> (you don't 'use it' directly, it's just a recipe/idea - give it to your agent and apply to what you care about.)"

---

## Key Insight

**Autoresearch is NOT a tool you use directly. It's a RECIPE/IDEA.**

The value isn't in running the specific code — it's in the **pattern** that you can apply to any optimization problem.

---

## The Recipe (The Core Pattern)

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE AUTORESEARCH PATTERN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. DEFINE GOAL                                                 │
│      What metric do you want to optimize?                        │
│      (lower is better or higher is better)                       │
│                                                                  │
│   2. DEFINE SEARCH SPACE                                         │
│      What can be modified?                                       │
│      (code, config, parameters, strategy)                        │
│                                                                  │
│   3. AUTOMATE EXPERIMENTS                                        │
│      Let AI agent try variations                                 │
│      (modify, run, measure)                                      │
│                                                                  │
│   4. EVALUATE RESULTS                                            │
│      Did the metric improve?                                     │
│      (compare to baseline/best)                                  │
│                                                                  │
│   5. KEEP OR DISCARD                                             │
│      Keep improvements, revert failures                          │
│      (advance branch or reset)                                   │
│                                                                  │
│   6. REPEAT                                                      │
│      Continue indefinitely                                       │
│      (while you sleep, work, etc.)                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Analogy: Cookbook vs. Meal Delivery

| Aspect | Traditional Tool | Autoresearch (Recipe) |
|---------|-----------------|----------------------|
| **What it is** | Meal delivery service | Cookbook |
| **How you use it** | Order → Eat | Read recipe → Cook yourself |
| **Flexibility** | Fixed menu | Cook anything you want |
| **Value** | The food delivered | The *method* of cooking |
| **Applicability** | One specific use case | Infinite possibilities |

---

## The Pattern Applied

### Original (Karpathy's ML Training)

```
┌─────────────────────┐      ┌─────────────┐      ┌────────────────┐
│ train.py            │ ───▶ │ val_bpb     │ ───▶ │ Keep or Discard│
│ (model code)        │      │ (metric)    │      │ (git commit)   │
│                     │      │ lower=better│      │                │
└─────────────────────┘      └─────────────┘      └────────────────┘
```

### Generic Pattern (Apply to Anything)

```
┌─────────────────────┐      ┌─────────────┐      ┌────────────────┐
│ thing_to_modify     │ ───▶ │ metric      │ ───▶ │ Keep or Discard│
│ (code, config,      │      │ (what you   │      │ (track results)│
│  strategy, etc.)    │      │  care about)│      │                │
└─────────────────────┘      └─────────────┘      └────────────────┘
```

---

## Application Examples

### ML Training (Original)
| Element | Value |
|---------|-------|
| **What to modify** | `train.py` (model architecture, hyperparameters) |
| **Metric** | `val_bpb` (validation bits per byte) |
| **Experiment length** | 5 minutes |
| **Success criteria** | Lower val_bpb than baseline |

### Code Optimization
| Element | Value |
|---------|-------|
| **What to modify** | `algorithm.py` (implementations) |
| **Metric** | Execution time (ms) |
| **Experiment length** | Benchmark run |
| **Success criteria** | Faster than current |

### Business Optimization
| Element | Value |
|---------|-------|
| **What to modify** | `pricing.json`, `layout.yaml` |
| **Metric** | Conversion rate, revenue |
| **Experiment length** | A/B test period |
| **Success criteria** | Higher conversion |

### Game Playing
| Element | Value |
|---------|-------|
| **What to modify** | `agent.py` (strategy code) |
| **Metric** | Win rate |
| **Experiment length** | N games |
| **Success criteria** | Higher win rate |

### Learning Optimization
| Element | Value |
|---------|-------|
| **What to modify** | `study_plan.md` (methods, schedule) |
| **Metric** | Quiz scores, recall |
| **Experiment length** | Study session |
| **Success criteria** | Better retention |

---

## Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "I need to use autoresearch to train ML models" | Apply the **pattern** to optimize **anything** |
| "It's a tool I run" | It's a **methodology** you apply |
| "Only for ML researchers" | For **anyone** with an optimization problem |
| "I need an H100 GPU" | Can run on Colab free tier, or adapt to your constraints |
| "The code is the product" | The **pattern** is the product |

---

## Why This Distinction Matters

### If You Think It's a Tool:
```
❌ Limited to ML training
❌ Need specific hardware
❌ Fixed use case
❌ "Doesn't apply to me"
```

### If You Understand It's a Recipe:
```
✅ Apply to any optimization problem
✅ Adapt to your constraints
✅ Infinite use cases
✅ "How can I apply this to my problem?"
```

---

## How This Relates to Our Work

| What We Did | Pattern Application |
|-------------|---------------------|
| `feat/google-colab` branch | Applied pattern to T4 GPU constraints |
| `tinystories_colab.ipynb` | Applied pattern to different dataset |
| `guide-002-real-world-applications.md` | Documented pattern applications |
| `prd-001-ml-optimization-service.md` | Productized the pattern |
| `prd-002-tinystories-experiment.md` | Learning-focused pattern application |

---

## The Meta-Pattern

Autoresearch itself was created by applying the autoresearch pattern:

```
Karpathy's process:
1. Goal: Better ML training
2. Search space: Training code, hyperparameters
3. Automate: Let AI experiment
4. Evaluate: val_bpb
5. Keep/discard: Git commits
6. Repeat: Overnight experiments
```

**The pattern can improve itself.**

---

## Questions to Ask Yourself

When applying this pattern to your own problems:

1. **What metric do I want to improve?**
   - Must be measurable
   - Must have clear direction (lower/higher is better)

2. **What can I modify?**
   - Code, config, strategy, parameters
   - Must be something an AI agent can change

3. **How do I measure it?**
   - Automated evaluation
   - Fast enough to run many experiments

4. **What's my time budget?**
   - Per experiment
   - Total (overnight, weekend, week)

5. **How do I track results?**
   - Git commits
   - Results log (TSV, database)
   - Dashboard

---

## Implementation Checklist

To apply the autoresearch pattern to your problem:

- [ ] Define a measurable metric
- [ ] Identify what can be modified
- [ ] Create automated evaluation
- [ ] Set up experiment loop
- [ ] Define success criteria
- [ ] Create results tracking
- [ ] Point AI agent at the problem
- [ ] Let it run

---

## Key Takeaways

1. **Autoresearch is a pattern, not a product**
2. **Apply it to YOUR optimization problem**
3. **The recipe is simple: modify → measure → keep/discard → repeat**
4. **Works for anything with a measurable metric**
5. **Let AI do the tedious experimentation while you sleep**

---

## References

- [Original autoresearch repo](https://github.com/karpathy/autoresearch)
- [Karpathy's tweet with context](https://x.com/karpathy/status/2030371219518931079)
- [Follow-up clarification](https://x.com/karpathy/status/2031137476438548874)

---

## Related Documents

- `guide-002-real-world-applications.md` - Specific applications
- `prd-001-ml-optimization-service.md` - Productizing the pattern
- `program.md` - Original agent instructions
