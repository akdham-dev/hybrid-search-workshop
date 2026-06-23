# Hybrid Search Workshop — Slides + Speaker Script

A presenter's guide. Each slide has **what's on screen** and **what you say** (the script is a guide, not a teleprompter — say it in your own words). Timings are cumulative.

---

## Slide 1 — Title (0:00–0:02)

**On screen:** "Why Search Needs Both Keywords *and* Vectors" — your name, the repo URL.

**Say:**
> Quick show of hands — how many of you have searched something at work, gotten garbage results, and just... given up? Right. By the end of this hour you'll know exactly *why* that happens, and you'll have built the fix yourself. We're going to build search the way real systems do it. No heavy math, we write it ourselves, and you'll see every piece work.

**Do:** Make sure everyone ran `preflight.py`. Ask: "Did anyone's preflight NOT show all green?" Fix stragglers now, not at slide 5.

---

## Slide 2 — The problem (0:02–0:05)

**On screen:** Two screenshots side by side — a keyword search missing an obvious answer, and a search returning the wrong thing confidently.

**Say:**
> Search fails in two opposite ways. Either it's too literal — you didn't type the exact word, so it finds nothing — or it's too loose and grabs something that sounds related but isn't. These are two different problems, and here's the key insight for today: the fix for one *makes the other worse*. Unless you combine them. That's the whole session.

---

## Slide 3 — The hook, live (0:05–0:10)

**On screen:** Switch to the notebook. Section 1.

**Say:**
> Let's see it. I've got 20 tiny help-desk docs — VPN, passwords, expenses, that kind of thing. I'll search the naive way: just count shared words.

**Do:** Run the `naive_keyword` cell with `"how do I connect to work systems from home"`.

> Look — it finds the VPN doc because we share the word 'connect'. But there's another doc that's *literally the same answer* — it says 'remote access gateway', 'secure tunnel'. Same meaning, zero shared words, so it's invisible. That's failure number one: the synonym problem. Hold that thought.

---

## Slide 4 — BM25 concept (0:10–0:15)

**On screen:** Two bullets only:
- Rare words matter more (IDF)
- The 10th repeat matters less than the 2nd (saturation)

**Say:**
> Real keyword search isn't word-counting, it's BM25 — it's what powers Elasticsearch, Lucene, most search bars you've used. Two ideas. One: rare words count more. If you search "E-4042", that code is way more informative than "the". Two: saturation — once a word appears a few times, more repeats barely help. That's it. That's BM25. Let's build it.

**Do:** Have them fill the TODO in the BM25 cell. Give them ~3 min. Walk the room. Then run it.

---

## Slide 5 — BM25 wins and loses (0:15–0:22)

**On screen:** Notebook, the two BM25 demo cells.

**Say:**
> Search "E-4042" — boom, exact hit, top result. BM25 is *unbeatable* on exact tokens: error codes, product IDs, people's names, SKUs. This is its superpower.
>
> Now the same engine, different query: "I'm locked out and can't sign in." Watch... it struggles. The right doc says 'password reset' and 'account recovery' — not 'locked out'. We never said those words, so BM25 is stuck. Same synonym problem from the hook. So how do we search by *meaning* instead of words?

---

## Slide 6 — Embeddings concept (0:22–0:28)

**On screen:** A simple 2D scatter — "locked out", "account recovery", "password reset" clustered together; "parking permit" far away. (Hand-drawn is fine.)

**Say:**
> This is the one genuinely new idea today. An embedding turns text into a list of numbers — a point in space — where things that *mean* the same land near each other. 'Locked out' and 'account recovery' end up as neighbors even though they share no words, because a model learned they're related. We don't train anything — we download a small free model that already knows this. Then "search" just becomes: find the nearest points.

---

## Slide 7 — Dense retrieval, live (0:28–0:38)

**On screen:** Notebook Section 3.

**Say:**
> Let's load the model and re-run the exact query that beat BM25.

**Do:** Run the embedder cell (model already cached from preflight), then the Dense `"locked out"` cell.

> There it is — account recovery, password reset, right at the top. It understood us without a single shared word. *This* is why vector search feels like magic.
>
> But — run the E-4042 query on dense now. See how it gets *fuzzy*? It muddles the exact code, might mix up E-4042 and E-1001. Vector search is bad at exact tokens — the opposite weakness of BM25. So look where we are: BM25 nails exact and fails meaning. Dense nails meaning and fumbles exact. They're mirror images.

**If a download failed live:** "Some of you hit the fallback embedding — your dense results will look rough, that's expected, watch mine on screen for the real behavior and grab the model on better wifi after."

---

## Slide 8 — The fusion idea (0:38–0:42)

**On screen:** "Can't we just add the scores?" with a red X. BM25 ~0–8, cosine ~0–1.

**Say:**
> Obvious move: run both, add the scores. Problem — different scales. BM25 gives like 6.2, cosine gives 0.8. Add those and BM25 just bulldozes everything. So instead of trusting the *scores*, we trust the *ranking*. Whatever each method puts at #1 gets the most points, #2 a bit less, and so on. Add up those rank-points. That's Reciprocal Rank Fusion — RRF. It's beautifully dumb and it works.

---

## Slide 9 — RRF live, the payoff (0:42–0:52)

**On screen:** Notebook Section 4.

**Say:**
> Fill in the one line of RRF — reciprocal of the rank. Now the `compare` cell runs all three side by side.

**Do:** Run `compare` over all four queries.

> Watch the hybrid column. Locked-out query — dense carries it, hybrid keeps it. E-1001 — BM25 carries it, hybrid keeps it. The mixed ones — hybrid beats *both*. That's the moment: you no longer have to choose between exact and meaning. Hybrid is never meaningfully worse and often better. This is why basically every serious RAG system in production runs hybrid retrieval.

---

## Slide 10 — Recap (0:52–0:58)

**On screen:** The recap table from the notebook.

**Say:**
> Three things to remember. Keyword — BM25 — finds *exact*. Vector finds *meaning*. RRF gets you *both*, and it's a safe default — reach for it first. If you take one sentence home: keyword finds exact, vector finds meaning, RRF gets you both.

---

## Slide 11 — Optional LLM + close (0:58–1:00)

**On screen:** The RAG answer cell.

**Say:**
> If you want the chatbot-style answer on top, that's just one more step — feed the top hybrid docs to an LLM. The retrieval we built *is* the hard part and the part that decides quality. There's a Groq cell in the notebook with a free key if you want to play after. The three challenges at the bottom are for you to take further. Thanks — what questions do you have?"

---

## Facilitator cheat-sheet

- **Biggest risk:** the model download. `preflight.py` is your insurance — enforce it.
- **If you're behind on time:** cut the optional LLM (Slide 11) and the second BM25 demo query. Never cut the locked-out vs E-4042 contrast — that's the whole lesson.
- **If someone asks "which embedding model in real life?":** all-MiniLM is the fast free starter; production often uses OpenAI/Cohere/BGE embeddings, same code shape.
- **If someone asks about scale:** "20 docs in memory here; real systems use a vector DB — pgvector, FAISS, Pinecone — but the BM25 + dense + RRF recipe is identical."
- **Common confusion:** people think dense is "always better." Hammer the E-4042 failure — that's what makes hybrid click.
