# Hybrid Search Workshop — Keyword + Vector + RRF

A 1-hour, hands-on session for **data analysts / beginners**. Attendees build keyword search (BM25), vector search (dense embeddings), and fuse them with Reciprocal Rank Fusion — and *see* why production search needs both.

No prior ML needed. Runs locally in Python. Free Groq tier optional for the last step.

## What attendees walk away understanding

- **BM25 (keyword)** wins on exact terms, codes, IDs, names
- **Dense (vector)** wins on synonyms, paraphrases, meaning
- **RRF** fuses the two — the safe default for real systems

One-line takeaway: *keyword finds exact, vector finds meaning, RRF gets you both.*

## Setup (do this BEFORE the session)

```bash
git clone <this-repo>
cd hybrid-rag-workshop
pip install -r requirements.txt
python preflight.py        # verifies setup + pre-downloads the model
```

`preflight.py` is important — it pulls the ~80MB embedding model ahead of time so 30 people aren't all downloading it on conference wifi mid-session.

Then launch:

```bash
jupyter notebook notebooks/workshop.ipynb
```

## ⚠️ One thing to know about the dense step

The dense retrieval step uses the real `all-MiniLM-L6-v2` embedding model. **The "vector search rescues the synonym query" moment only lands with the real model.**

If the model can't download (no internet), the notebook auto-falls-back to a tiny hashing embedding so nothing crashes — but that fallback is *not* semantic, so dense results will look weak. **Run `preflight.py` on good wifi beforehand** so everyone has the real model cached. This is the one dependency that decides whether the key teaching moment works.