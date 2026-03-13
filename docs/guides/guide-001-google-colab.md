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

### Training Output

During training, you'll see a progress line like:

```
step 00042 (8.3%) | loss: 2.145678 | lrm: 1.00 | dt: 7123ms | tok/sec: 9,170 | mfu: 12.3% | epoch: 0 | remaining: 275s
```

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

The key metric is **val_bpb** (validation bits per byte) — lower is better.

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
