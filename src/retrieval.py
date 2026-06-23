"""
Hybrid retrieval building blocks for the workshop.
BM25 (keyword) + dense (vector) + RRF (fusion), with zero heavy deps.

Dense vectors use a small hashing-based embedding so the notebook runs
instantly on any laptop with no model download. In the real world you'd
swap embed() for sentence-transformers or an API — the fusion logic is
identical.
"""
import json
import math
import re
from collections import Counter, defaultdict

WORD = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return WORD.findall(text.lower())


# ---------- BM25 ----------
class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs = docs
        self.k1, self.b = k1, b
        self.corpus = [tokenize(d["title"] + " " + d["text"]) for d in docs]
        self.doc_len = [len(c) for c in self.corpus]
        self.avgdl = sum(self.doc_len) / len(self.corpus)
        self.df = defaultdict(int)
        for c in self.corpus:
            for term in set(c):
                self.df[term] += 1
        self.N = len(self.corpus)
        self.tf = [Counter(c) for c in self.corpus]

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def search(self, query, top_k=5):
        q = tokenize(query)
        scores = []
        for i in range(self.N):
            s = 0.0
            for term in q:
                if term not in self.tf[i]:
                    continue
                freq = self.tf[i][term]
                num = freq * (self.k1 + 1)
                den = freq + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl)
                s += self.idf(term) * num / den
            scores.append((self.docs[i]["id"], s))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(d, sc) for d, sc in scores if sc > 0][:top_k]


# ---------- Dense (lightweight hashing embedding) ----------
DIM = 256


def embed(text, dim=DIM):
    """Toy semantic embedding: hashed unigrams + bigrams, L2-normalized.
    Stands in for a real embedding model so the workshop needs no downloads."""
    import numpy as np
    vec = np.zeros(dim)
    toks = tokenize(text)
    grams = toks + [a + "_" + b for a, b in zip(toks, toks[1:])]
    for g in grams:
        vec[hash(g) % dim] += 1.0
    n = np.linalg.norm(vec)
    return vec / n if n else vec


class Dense:
    def __init__(self, docs):
        import numpy as np
        self.docs = docs
        self.mat = np.vstack([embed(d["title"] + " " + d["text"]) for d in docs])

    def search(self, query, top_k=5):
        import numpy as np
        q = embed(query)
        sims = self.mat @ q
        order = np.argsort(-sims)[:top_k]
        return [(self.docs[i]["id"], float(sims[i])) for i in order if sims[i] > 0]


# ---------- RRF fusion ----------
def rrf(result_lists, k=60, top_k=5):
    """Reciprocal Rank Fusion. Each list is [(doc_id, score), ...] ranked best-first.
    Fuses on RANK, not score, so the two retrievers' incompatible score scales
    don't matter."""
    fused = defaultdict(float)
    for results in result_lists:
        for rank, (doc_id, _) in enumerate(results):
            fused[doc_id] += 1.0 / (k + rank + 1)
    out = sorted(fused.items(), key=lambda x: x[1], reverse=True)
    return out[:top_k]


def load_docs(path="../data/docs.json"):
    with open(path) as f:
        return json.load(f)
