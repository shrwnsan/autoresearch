# Guide: Running on Google Colab (T4 GPU)

This guide explains how to run autoresearch experiments on Google Colab's free tier with a T4 GPU.

## Prerequisites

- Google account
- Access to [Google Colab](https://colab.research.google.com)

## Setup

### 1. Create a New Notebook

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. File → Upload notebook → Select `autoresearch_colab.ipynb` from this repo

### 2. Set Runtime to T4 GPU

1. Runtime → Change runtime type
2. Select "T4 GPU"
3. Save

### 3. Update Clone URL

In Cell 1, replace `YOUR_USERNAME` with your GitHub username:

```python
!git clone -b feat/google-colab https://github.com/YOUR_USERNAME/autoresearch.git
```

### 4. Run All

Click Runtime → Run all (or Ctrl+F9)

## What to Expect

| Cell | Time | What Happens |
|------|------|--------------|
| 1. Clone | ~10 sec | Downloads repo |
| 2. Install deps | ~1-2 min | Installs uv, PyTorch with CUDA, other packages |
| 3. Prepare data | ~2 min | Downloads training shards, trains tokenizer |
| 4. Train | ~5-7 min | 5 min training + startup/eval overhead |
| 5. Results | instant | Shows `results.tsv` |

**Total time: ~8-11 minutes**

## What Each Step Actually Does

### Step 1: Clone Repository

Downloads your fork with T4-optimized `train.py` containing reduced model size and batch sizes.

### Step 2: Install Dependencies

Installs:
- **uv** — Fast Python package manager
- **PyTorch 2.9.1** with CUDA 12.8 support
- **Flash Attention kernels** — Fast attention implementation
- **Other libs** — numpy, tiktoken, rustbpe, etc.

### Step 3: Prepare Data (~2 min)

- Downloads **training data shards** from HuggingFace (climbmix-400b dataset — a shuffled mix of web text)
- Trains a **BPE tokenizer** with vocab size 8192
- Caches everything to `~/.cache/autoresearch/` for reuse in future runs

### Step 4: Train Model (~5 min)

- Builds a **GPT-style transformer** (~12M parameters, 4 layers)
- Trains for exactly **5 minutes wall-clock time**
- Uses **MuonAdamW optimizer** (Muon for matrices, AdamW for embeddings)
- Processes approximately **100 million tokens**
- Evaluates on validation data and outputs **val_bpb**

### Step 5: Show Results

Displays `results.tsv` — the experiment log tracking all runs.

## Understanding the Output

### Training Output

During training, you'll see a progress line like:

```
step 00042 (8.3%) | loss: 2.145678 | lrm: 1.00 | dt: 7123ms | tok/sec: 9,170 | mfu: 12.3% | epoch: 0 | remaining: 275s
```

| Metric | Meaning |
|--------|---------|
| `step` | Optimizer update count |
| `(8.3%)` | Progress through 5-minute budget |
| `loss` | Current training loss (lower = better) |
| `lrm` | Learning rate multiplier |
| `dt` | Time per step in milliseconds |
| `tok/sec` | Tokens processed per second |
| `mfu` | Model FLOPs utilization (efficiency) |
| `epoch` | Pass through training data |
| `remaining` | Seconds left in time budget |

### Final Summary

After training completes:

```
---
val_bpb:          1.234567
training_seconds: 300.1
total_seconds:    325.9
peak_vram_mb:     8234.5
mfu_percent:      15.20
total_tokens_M:   98.2
num_steps:        1500
num_params_M:     12.5
depth:            4
```

| Metric | Meaning |
|--------|---------|
| `val_bpb` | **Validation bits per byte** — key metric, lower = better model |
| `training_seconds` | Actual training time (target: 300s) |
| `total_seconds` | Including startup and evaluation |
| `peak_vram_mb` | Max GPU memory used (T4 has 16,384 MB) |
| `mfu_percent` | Model FLOPs utilization — how efficiently you're using the GPU |
| `total_tokens_M` | Total tokens processed (millions) |
| `num_steps` | Optimizer updates performed |
| `num_params_M` | Model parameter count (millions) |
| `depth` | Number of transformer layers |

The **key metric is `val_bpb`** (validation bits per byte) — lower is better. This measures how well the model predicts held-out data, independent of vocabulary size.

## How This Benefits You

### 1. Establishes a Baseline

You get a starting `val_bpb` score — your **reference point** for future experiments.

```
Baseline: val_bpb = 1.234567
```

Any changes to `train.py` will be measured against this.

### 2. Validates Your Setup Works

Confirms:
- ✅ T4 GPU is accessible and functional
- ✅ VRAM is sufficient (no OOM errors)
- ✅ Flash Attention kernel works on T4
- ✅ Training completes within time budget

### 3. Ready for Autonomous Research

Once the baseline works, you can:
- Let an AI agent (Claude Code, etc.) modify `train.py`
- Run experiments in a loop automatically
- Track improvements in `results.tsv`

Example experiment log after several runs:

```
commit      val_bpb    memory_gb  status   description
a1b2c3d     1.234567   8.0        keep     baseline
b2c3d4e     1.198234   8.1        keep     increase learning rate to 0.05
c3d4e5f     1.245000   8.0        discard  add dropout (worse)
d4e5f6g     1.182000   8.2        keep     reduce depth to 3, widen layers
```

### 4. Understanding ML Training Dynamics

You observe real training behavior:
- Loss decreasing over time
- Throughput (tokens/second)
- GPU efficiency (MFU)
- Memory usage patterns

## What This Does NOT Do (Yet)

| Not Included | How to Enable |
|--------------|---------------|
| Multiple experiments in a loop | Point Claude Code at `program.md` for autonomous research |
| Model checkpointing | Not in baseline; agent can add this |
| Text generation/sampling | Evaluation only; inference not included |
| Comparison to others | Results are hardware-specific (T4 vs H100) |
| TensorBoard logging | Can be added by modifying `train.py` |

## Next Steps After Successful Run

### Option 1: Manual Experimentation

Edit `train.py` directly to try different:
- Learning rates
- Model sizes (depth, width)
- Batch sizes
- Optimizer settings

Then re-run and compare `val_bpb`.

### Option 2: Autonomous Research

Point an AI coding agent (Claude Code, etc.) at this repo with `program.md`. The agent will:

1. Read `program.md` for instructions
2. Propose changes to `train.py`
3. Run experiments
4. Keep improvements, discard failures
5. Repeat indefinitely

This is the core "autoresearch" concept — AI doing its own ML research while you sleep.

### Option 3: Analyze Results

Review `results.tsv` to understand what worked:

```bash
# Sort by val_bpb to find best experiment
!cat results.tsv | sort -t$'\t' -k2 -n
```

## T4-Optimized Settings

This branch includes modifications optimized for T4 GPU (16GB VRAM):

| Setting | Original (H100) | T4 |
|---------|-----------------|-----|
| `DEPTH` | 8 | 4 |
| `DEVICE_BATCH_SIZE` | 128 | 16 |
| `TOTAL_BATCH_SIZE` | 2^19 (~524K) | 2^16 (~65K) |
| `WINDOW_PATTERN` | "SSSL" | "L" |

These changes allow the model to train within VRAM constraints while still completing meaningful experiments in the 5-minute time budget.

## Google Colab Free Tier Limits

| Limit | Free Tier | Notes |
|-------|-----------|-------|
| GPU type | T4 (16GB) | Random assignment, usually T4 |
| Session length | 12 hours max | Then disconnect |
| Idle timeout | ~90 min | If no activity |
| Daily usage | ~12 hours GPU | Not explicitly stated, varies |

### Tips to Avoid Issues

1. **Don't close the tab** — Keep the notebook open
2. **Stay interactive** — Click occasionally to show activity
3. **Expect disconnects** — Save important results
4. **One experiment at a time** — 5 min each is fine

### Expected Experiments per Session

You should be able to run **6-10 experiments** in one session before hitting limits. For overnight autonomous research (100+ experiments), consider:

- Colab Pro (longer sessions, better GPUs)
- A dedicated GPU (local or cloud)

## Checking Usage Limits

Unfortunately, **Google Colab free tier has no official quota dashboard**. The limits are opaque by design. Here's what you *can* check:

### What You Can See

**In Colab UI (limited):**
Click the RAM/Disk meter (top right) — you may see current session info and sometimes a vague "compute availability" message.

**Run this in a Colab cell:**

```python
# Check GPU assignment
!nvidia-smi --query-gpu=name,memory.total --format=csv

# Check current time (session start time is not exposed)
import time
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
```

### What You Cannot See

| Info | Free Tier | Paid (Pro/Pro+) |
|------|-----------|-----------------|
| Hours used today | ❌ | ✅ (Compute Units) |
| Hours remaining | ❌ | ✅ |
| Session time left | ❌ | ✅ |
| Daily/weekly quota | ❌ | ✅ |

### Signs You're Hitting Limits

Since there's no visibility, watch for these warning signs:

1. **"GPU unavailable"** when connecting to runtime
2. **Slower GPU assignment** (waiting in queue)
3. **Session terminates early** without warning
4. **Can't reconnect** to GPU runtime

If this happens, wait a few hours or until the next day for quota reset.

### Paid Tiers for Visibility

| Tier | Price | Benefit |
|------|-------|---------|
| Colab Pro | $10/mo | ~100 compute units, visible quota |
| Colab Pro+ | $50/mo | ~500 compute units, priority access |

## Reconnecting After Disconnect

If Colab disconnects:

1. Reconnect to the runtime
2. Re-run cells 1-2 (clone and install)
3. Data is cached in `~/.cache/autoresearch/` — prep may be faster or skipped
4. Continue experiments

## Troubleshooting

### OOM (Out of Memory)

If you get CUDA OOM errors:

1. Reduce `DEVICE_BATCH_SIZE` in `train.py` (try 8 or 4)
2. Reduce `TOTAL_BATCH_SIZE` (try 2^15 or 2^14)

### Slow Download

Data shards are downloaded from HuggingFace. If slow:

1. Check your internet connection
2. Try again later (HuggingFace rate limits)

### Flash Attention Errors

The code automatically selects the correct Flash Attention kernel:

- H100 (compute 9.0): `varunneal/flash-attention-3`
- Other GPUs (compute < 9.0): `kernels-community/flash-attn3`

T4 (compute 7.5) should work with the fallback kernel.

## Resources

- [Original autoresearch repo](https://github.com/karpathy/autoresearch)
- [Colab free tier FAQ](https://research.google.com/colaboratory/faq.html)
- [T4 GPU specs](https://www.nvidia.com/en-us/data-center/tesla-t4/)
