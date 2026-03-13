"""
Story generation from trained model.

Usage:
    python generate.py --prompt "Once upon a time" --max-tokens 100
    python generate.py --prompt "The little dog" --temperature 0.8

Note: Run training first (uv run train.py) for meaningful outputs.
This script uses the model with current weights (random if untrained).
"""

import argparse
import torch
import torch.nn.functional as F

from prepare import Tokenizer, MAX_SEQ_LEN


def sample(logits, temperature=1.0, top_k=None):
    """Sample next token from logits."""
    if temperature == 0:
        return logits.argmax(dim=-1)
    
    logits = logits / temperature
    
    if top_k is not None:
        v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
        logits[logits < v[:, [-1]]] = float('-inf')
    
    probs = F.softmax(logits, dim=-1)
    return torch.multinormal(probs, 1).squeeze(-1)


@torch.no_grad()
def generate(model, tokenizer, prompt, max_tokens=100, temperature=0.8, top_k=40, device="cuda"):
    """Generate text continuation from prompt."""
    model.eval()
    
    # Encode prompt
    tokens = tokenizer.encode(prompt, prepend=tokenizer.get_bos_token_id())
    tokens = torch.tensor([tokens], dtype=torch.long, device=device)
    
    with torch.no_grad():
        for _ in range(max_tokens):
            # Truncate if too long
            if tokens.size(1) > MAX_SEQ_LEN:
                tokens = tokens[:, -MAX_SEQ_LEN:]
            
            # Get logits for next token
            logits = model(tokens)
            next_token_logits = logits[0, -1, :]
            
            # Sample next token
            next_token = sample(next_token_logits, temperature, top_k)
            
            # Append to sequence
            tokens = torch.cat([tokens, next_token.unsqueeze(0).unsqueeze(0)], dim=1)
    
    # Decode generated text
    return tokenizer.decode(tokens[0].tolist())


def main():
    parser = argparse.ArgumentParser(description="Generate stories from trained model")
    parser.add_argument("--prompt", type=str, default="Once upon a time, there was a little",
                        help="Starting prompt for generation")
    parser.add_argument("--max-tokens", type=int, default=100,
                        help="Maximum tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.8,
                        help="Sampling temperature (0 = greedy)")
    parser.add_argument("--top-k", type=int, default=40,
                        help="Top-k sampling")
    args = parser.parse_args()

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = Tokenizer.from_directory()
    vocab_size = tokenizer.get_vocab_size()
    print(f"Vocab size: {vocab_size}")

    # Import model from train.py
    from train import GPT, GPTConfig, DTYPE, DEPTH, ASPECT_RATIO, HEAD_DIM, WINDOW_PATTERN
    
    # Build model config (same as train.py)
    model_dim = ((DEPTH * ASPECT_RATIO + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    
    config = GPTConfig(
        sequence_len=MAX_SEQ_LEN,
        vocab_size=vocab_size,
        n_layer=DEPTH,
        n_head=num_heads,
        n_kv_head=num_heads,
        n_embd=model_dim,
        window_pattern=WINDOW_PATTERN,
    )
    
    print(f"Building model ({DEPTH} layers, {model_dim} dim, {num_heads} heads)...")
    model = GPT(config)
    model.to(device)
    model.to(DTYPE)
    
    # Note: This uses the current model weights (random if untrained)
    # In production, you'd load trained weights:
    # model.load_state_dict(torch.load("best_model.pt"))
    
    print()
    print("=" * 60)
    print("STORY GENERATION")
    print("=" * 60)
    print()
    print(f"Prompt: {args.prompt}")
    print()
    
    # Generate
    story = generate(
        model, tokenizer, args.prompt,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
        device=device
    )
    
    print("Generated story:")
    print("-" * 60)
    print(story)
    print("-" * 60)
    print()
    print(f"Settings: temperature={args.temperature}, top_k={args.top_k}, max_tokens={args.max_tokens}")
    print()
    print("Note: For meaningful outputs, train the model first:")
    print("  uv run train.py")


if __name__ == "__main__":
    main()
