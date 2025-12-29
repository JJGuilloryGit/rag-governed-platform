"""Embeddings module.

For local mode we use a deterministic, lightweight hash embedding (fast + no cost).
For AWS mode you can swap in Bedrock embeddings or Titan embeddings.

This is intentional: interviewers care more about *architecture* than embedding math.
"""

import numpy as np
import hashlib

DIM = 384

def hash_embed(text: str) -> np.ndarray:
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # Expand digest deterministically to DIM floats
    rng = np.frombuffer(h, dtype=np.uint8).astype(np.float32)
    vec = np.tile(rng, int(np.ceil(DIM / rng.shape[0])))[:DIM]
    vec = vec / (np.linalg.norm(vec) + 1e-9)
    return vec.astype(np.float32)
