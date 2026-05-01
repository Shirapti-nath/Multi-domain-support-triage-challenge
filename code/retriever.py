"""
retriever.py — Hybrid BM25 + TF-IDF cosine retrieval over the support corpus.

Design:
  - BM25Okapi      : keyword overlap, precise on exact terms (doc IDs, commands, product names)
  - TF-IDF cosine  : vector similarity, stronger on paraphrase and synonym matching
  - Final score    : 0.6 × normalised_BM25 + 0.4 × TF-IDF_cosine
  - Domain filter  : builds a smaller index for the ticket's known company first;
                     falls back to the full corpus when company is None/unknown or
                     when the best filtered score is below MIN_DOMAIN_SCORE.

Why hybrid over BM25-only?
  BM25 alone misses tickets that paraphrase the corpus
  (e.g. "block crawler" vs "stop crawling website").
  TF-IDF cosine catches those cases via shared sub-word vocabulary.
  Combining both improves recall without losing BM25 precision.
"""

import re
import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from corpus import CORPUS

# If the best domain-filtered score is below this, supplement with full-corpus retrieval
MIN_DOMAIN_SCORE = 1.5

# Raw BM25 score considered "high confidence" (used by compute_confidence)
HIGH_CONFIDENCE_THRESHOLD = 8.0


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _doc_text(doc: dict) -> str:
    return f"{doc['title']} {doc['content']} {' '.join(doc['keywords'])}"


class HybridRetriever:
    """
    Combines BM25 and TF-IDF cosine similarity for improved retrieval.

    Each result includes:
      score      – hybrid score used for ranking
      bm25_score – raw BM25 score (used for confidence calculation)
    """

    def __init__(self, docs: list[dict]):
        self._docs = docs
        texts = [_doc_text(d) for d in docs]

        # BM25 index
        self._bm25 = BM25Okapi([_tokenize(t) for t in texts])

        # TF-IDF index
        self._tfidf = TfidfVectorizer(
            tokenizer=_tokenize, token_pattern=None, sublinear_tf=True
        )
        self._tfidf_matrix = self._tfidf.fit_transform(texts)

    def retrieve(self, query: str, top_k: int = 4) -> list[dict]:
        tokens = _tokenize(query)

        # BM25 scores — normalise to [0, 1]
        bm25_raw = np.array(self._bm25.get_scores(tokens))
        bm25_norm = bm25_raw / (bm25_raw.max() + 1e-9)

        # TF-IDF cosine scores — already in [0, 1]
        q_vec = self._tfidf.transform([query])
        tfidf_scores = cosine_similarity(q_vec, self._tfidf_matrix).flatten()

        # Weighted hybrid
        hybrid = 0.6 * bm25_norm + 0.4 * tfidf_scores

        ranked = sorted(enumerate(hybrid), key=lambda x: x[1], reverse=True)[:top_k]

        return [
            {
                **self._docs[idx],
                "score":      round(float(h), 4),
                "bm25_score": round(float(bm25_raw[idx]), 4),
            }
            for idx, h in ranked
            if h > 0
        ]


def retrieve_for_issue(
    issue: str,
    subject: str,
    company: str | None,
    top_k: int = 4,
) -> list[dict]:
    """
    Main retrieval entry point used by triage.py.

    Strategy:
      1. Domain-filtered retrieval when company is known.
      2. If best filtered score < MIN_DOMAIN_SCORE, supplement with full-corpus retrieval.
      3. Deduplicate by doc ID, re-rank by hybrid score, return top-k.
    """
    query = f"{subject or ''} {issue}".strip()

    domain = None
    if company and company.strip().lower() not in ("none", ""):
        domain = company.strip()

    results: list[dict] = []

    # Step 1: domain-filtered retrieval
    if domain:
        domain_docs = [d for d in CORPUS if d["domain"].lower() == domain.lower()]
        if domain_docs:
            results = HybridRetriever(domain_docs).retrieve(query, top_k=top_k)

    # Step 2: full-corpus fallback / supplement
    if max((r["score"] for r in results), default=0.0) < MIN_DOMAIN_SCORE:
        full_results = HybridRetriever(CORPUS).retrieve(query, top_k=top_k)
        seen = {r["id"] for r in results}
        for doc in full_results:
            if doc["id"] not in seen:
                results.append(doc)
                seen.add(doc["id"])
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:top_k]

    return results


def compute_confidence(docs: list[dict]) -> float:
    """
    Confidence in [0.0, 1.0] based on the top document's raw BM25 score.

    - 0.0 → no relevant documents found → agent should auto-escalate
    - 1.0 → very strong keyword match in corpus
    """
    if not docs:
        return 0.0
    top_bm25 = docs[0].get("bm25_score", 0.0)
    return round(min(1.0, top_bm25 / HIGH_CONFIDENCE_THRESHOLD), 2)


def format_context(docs: list[dict]) -> str:
    """
    Format retrieved docs for injection into the LLM prompt.
    Each doc is prefixed with its DOC_ID so the LLM can cite it.
    """
    if not docs:
        return "No relevant support documentation found."
    parts = [
        f"[DOC_ID: {d['id']}] [{d['domain']} | {d['product_area']}] "
        f"{d['title']}\n{d['content']}"
        for d in docs
    ]
    return "\n\n---\n\n".join(parts)
