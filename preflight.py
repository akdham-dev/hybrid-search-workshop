"""
Run this BEFORE the workshop to catch problems early:
    python preflight.py

It checks your Python, installs are working, and pre-downloads the embedding
model so the session doesn't stall on wifi. Green checkmarks = you're ready.
"""

import sys


def ok(m):
    print(f"  [OK]   {m}")


def bad(m):
    print(f"  [FAIL] {m}")


print("Hybrid Search Workshop — preflight\n")

# 1. Python version
v = sys.version_info
(ok if v >= (3, 9) else bad)(f"Python {v.major}.{v.minor} (need 3.9+)")

# 2. Core imports
for mod in ["numpy", "rank_bm25", "sentence_transformers"]:
    try:
        __import__(mod)
        ok(f"import {mod}")
    except ImportError:
        bad(f"import {mod}  ->  run: pip install -r requirements.txt")

# 3. Pre-download the embedding model (the usual wifi bottleneck)
try:
    from sentence_transformers import SentenceTransformer

    print("\n  downloading all-MiniLM-L6-v2 (~80MB, one time)...")
    m = SentenceTransformer("all-MiniLM-L6-v2")
    _ = m.encode(["hello world"])
    ok("embedding model ready (cached locally)")
except Exception as e:
    bad(f"model download failed: {str(e)[:70]}")
    print("       -> the notebook will auto-fall-back to a hashing embedding,")
    print("          but dense results will be weaker. Try again on better wifi.")

# 4. Data present
import os, json

p = os.path.join(os.path.dirname(__file__), "data", "docs.json")
try:
    n = len(json.load(open(p)))
    ok(f"dataset found ({n} docs)")
except Exception:
    bad("data/docs.json missing")

print("\nIf everything says [OK], you're set for the session.")
