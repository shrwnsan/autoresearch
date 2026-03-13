# Guide: Running on Google Colab (T4 GPU)

This guide explains how to run autoresearch experiments on Google Colab's free tier with a T4 GPU.

## Prerequisites

- Google account
- Access to [Google Colab](https://colab.research.google.com)

## Quick Start

### 1. Upload Notebook

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

### 5. Pull Updates (If Re-running)

If you need to get the latest code changes, add this cell and run it before training:

```python
%cd /content/autoresearch
!git pull
```

## What to Expect

| Cell | Time | What Happens |
|------|------|--------------|
| 1. Clone | ~10 sec | Downloads repo |
| 2. Install deps | ~1-2 min | Installs uv, PyTorch with CUDA, other packages |
| 3. Prepare data | ~2 min | Downloads training shards, trains tokenizer |
| 4. Train | ~8-9 min | 5 min training + startup/eval overhead (float32 is slower) |
| 5. Results | instant | Shows `results.tsv` |

**Total time: ~10-14 minutes**

## What Each Step Actually Does

### Step 1: Clone Repository

Downloads your fork with T4-optimized `train.py` containing:
- Reduced model size and batch sizes
- Automatic Flash Attention fallback to PyTorch SDPA
- Automatic bfloat16 → float32 fallback for numerical stability

### Step 2: Install Dependencies

Installs:
- **uv** — Fast Python package manager
- **PyTorch 2.9.1** with CUDA 12.8 support
- **Other libs** — numpy, tiktoken, rustbpe, etc.

Note: Flash Attention kernels are NOT used on T4 (requires Ampere+ GPU).

### Step 3: Prepare Data (~2 min)

- Downloads **training data shards** from HuggingFace (climbmix-400b dataset — a shuffled mix of web text)
- Trains a **BPE tokenizer** with vocab size 8192
- Caches everything to `~/.cache/autoresearch/` for reuse in future runs

### Step 4: Train Model (~8-9 min)

- Builds a **GPT-style transformer** (~12M parameters, 4 layers)
- Trains for exactly **5 minutes wall-clock time**
- Uses **MuonAdamW optimizer** (Muon for matrices, AdamW for embeddings)
- Uses **float32** precision (T4 doesn't support bfloat16, float16 is unstable)
- Uses **PyTorch scaled_dot_product_attention** (Flash Attention not supported on T4)
- Processes approximately **15 million tokens**
- Evaluates on validation data and outputs **val_bpb**

### Step 5: Show Results

Displays `results.tsv` — the experiment log tracking all runs.

## Understanding the Output

### Startup Messages

On T4, you'll see these informational messages:

```
Flash Attention not supported on this GPU (compute 7.5), using PyTorch SDPA fallback
bfloat16 not supported on this GPU (compute 7.5), using float32 (slower but stable)
```

This is expected — T4 is a Turing GPU and doesn't support these newer features.

### Training Output

During training, you'll see a progress line like:

```
step 00230 (99.6%) | loss: 5.355986 | lrm: 0.01 | dt: 1398ms | tok/sec: 46,880 | mfu: 32.8% | epoch: 1 | remaining: 0s
```

| Metric | Meaning |
|--------|---------|
| `step` | Optimizer update count |
| `(99.6%)` | Progress through 5-minute budget |
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
val_bpb:          1.903347
training_seconds: 300.2
total_seconds:    503.1
peak_vram_mb:     6952.1
mfu_percent:      33.73
total_tokens_M:   15.1
num_steps:        231
num_params_M:     11.5
depth:            4
```

| Metric | Meaning | T4 Typical Value |
|--------|---------|------------------|
| `val_bpb` | **Validation bits per byte** — key metric, lower = better | ~1.9 (baseline) |
| `training_seconds` | Actual training time (target: 300s) | ~300s |
| `total_seconds` | Including startup and evaluation | ~500s |
| `peak_vram_mb` | Max GPU memory used (T4 has 16,384 MB) | ~7,000 MB |
| `mfu_percent` | Model FLOPs utilization | ~30-35% |
| `total_tokens_M` | Total tokens processed (millions) | ~15M |
| `num_steps` | Optimizer updates performed | ~230 |
| `num_params_M` | Model parameter count (millions) | 11.5M |
| `depth` | Number of transformer layers | 4 |

The **key metric is `val_bpb`** (validation bits per byte) — lower is better. This measures how well the model predicts held-out data, independent of vocabulary size.

## How This Benefits You

### 1. Establishes a Baseline

You get a starting `val_bpb` score — your **reference point** for future experiments.

```
Baseline (T4 float32): val_bpb = 1.903347
```

Any changes to `train.py` will be measured against this.

### 2. Validates Your Setup Works

Confirms:
- ✅ T4 GPU is accessible and functional
- ✅ VRAM is sufficient (no OOM errors)
- ✅ PyTorch SDPA attention works
- ✅ Training completes within time budget

### 3. Ready for Autonomous Research

Once the baseline works, you can:
- Let an AI agent (Claude Code, etc.) modify `train.py`
- Run experiments in a loop automatically
- Track improvements in `results.tsv`

Example experiment log after several runs:

```
commit      val_bpb    memory_gb  status   description
a1b2c3d     1.903347   6.8        keep     baseline (T4 float32)
b2c3d4e     1.856234   6.9        keep     increase learning rate to 0.03
c3d4e5f     1.924000   6.8        discard  add dropout (worse)
d4e5f6g     1.812000   7.0        keep     reduce depth to 3, widen layers
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
| Flash Attention | Not supported on T4 (requires Ampere+) |
| bfloat16 precision | Not supported on T4 (requires Ampere+) |

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

### Hyperparameters

| Setting | Original (H100) | T4 |
|---------|-----------------|-----|
| `DEPTH` | 8 | 4 |
| `DEVICE_BATCH_SIZE` | 128 | 16 |
| `TOTAL_BATCH_SIZE` | 2^19 (~524K) | 2^16 (~65K) |
| `WINDOW_PATTERN` | "SSSL" | "L" |

### Automatic Fallbacks

The code automatically detects T4 limitations and applies fallbacks:

| Feature | Ampere+ (A100, H100) | T4 (Turing) |
|---------|---------------------|-------------|
| Flash Attention | ✅ FA3 kernel | ❌ → PyTorch SDPA |
| Precision | ✅ bfloat16 | ❌ → float32 |
| torch.compile | ✅ Enabled | ❌ → Disabled |

These changes allow the model to train within VRAM constraints while maintaining numerical stability.

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
4. **One experiment at a time** — ~8-9 min each on T4

### Expected Experiments per Session

With ~8-9 minutes per experiment on T4, you should be able to run **6-8 experiments** in one session before hitting limits. For overnight autonomous research (100+ experiments), consider:

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
2. Run: `%cd /content/autoresearch && !git pull`
3. Re-run cells 2 (install deps)
4. Data is cached in `~/.cache/autoresearch/` — prep may be faster or skipped
5. Continue experiments

## Troubleshooting

### NaN Loss (Loss becomes nan)

This was a major issue on T4 with float16. The fix is to use **float32** instead.

**Symptoms:**
```
step 00002 (0.0%) | loss: 8.826544 | ...
FAIL: loss=nan (NaN=True, >100=False)
```

**Solution:** The code automatically uses float32 on T4. If you modified the code and see this error, ensure `DTYPE = torch.float32` for T4.

### Flash Attention Error

**Symptoms:**
```
RuntimeError: FlashAttention only supports Ampere GPUs or newer.
```

**Solution:** The code automatically falls back to PyTorch SDPA on T4. If you see this error, ensure you have the latest code:
```python
%cd /content/autoresearch
!git pull
```

### bfloat16 Compilation Warning

**Symptoms:**
```
UserWarning: Tesla T4 does not support bfloat16 compilation natively, skipping
```

**Solution:** This is handled automatically — the code switches to float32 on T4. No action needed.

### OOM (Out of Memory)

If you get CUDA OOM errors:

1. Reduce `DEVICE_BATCH_SIZE` in `train.py` (try 8 or 4)
2. Reduce `TOTAL_BATCH_SIZE` (try 2^15 or 2^14)

### Slow Download

Data shards are downloaded from HuggingFace. If slow:

1. Check your internet connection
2. Try again later (HuggingFace rate limits)

### Slow Training on T4

T4 with float32 is significantly slower than H100 with bfloat16:

| GPU | Precision | Tokens/sec | Steps in 5 min |
|-----|-----------|------------|----------------|
| H100 | bfloat16 | ~100,000+ | ~950 |
| T4 | float32 | ~47,000 | ~230 |

This is expected. The trade-off is numerical stability vs. speed.

## Performance Comparison

### T4 vs H100 Baseline

| Metric | T4 (float32) | H100 (bfloat16) |
|--------|--------------|-----------------|
| val_bpb | ~1.90 | ~1.00 |
| tokens/sec | ~47K | ~500K+ |
| steps/5min | ~230 | ~950+ |
| peak VRAM | ~7 GB | ~45 GB |
| MFU | ~33% | ~40% |

**Note:** Results are not directly comparable due to different hardware, precision, and number of training steps. T4 results are valid for iterating on *your* hardware.

## Resources

- [Original autoresearch repo](https://github.com/karpathy/autoresearch)
- [Colab free tier FAQ](https://research.google.com/colaboratory/faq.html)
- [T4 GPU specs](https://www.nvidia.com/en-us/data-center/tesla-t4/)
- [Flash Attention requirements](https://github.com/Dao-AILab/flash-attention) (Ampere+ only)
