"""BM25-based retrieval over the support corpus."""

import re
from rank_bm25 import BM25Okapi
from corpus import CORPUS


def _tokenize(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r"[a-z0-9]+", text)


class SupportRetriever:
    def __init__(self, domain_filter: str | None = None):
        docs = CORPUS
        if domain_filter:
            docs = [d for d in docs if d["domain"].lower() == domain_filter.lower()]
        if not docs:
            docs = CORPUS  # fallback to full corpus

        self._docs = docs
        # index: title + content + keywords concatenated
        tokenized = [
            _tokenize(f"{d['title']} {d['content']} {' '.join(d['keywords'])}")
            for d in docs
        ]
        self._bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        tokens = _tokenize(query)
        scores = self._bm25.get_scores(tokens)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in ranked[:top_k]:
            if score > 0:
                results.append({"score": round(score, 4), **self._docs[idx]})
        return results


def retrieve_for_issue(issue_text: str, subject: str, company: str | None, top_k: int = 4) -> list[dict]:
    """
    Retrieve top-k relevant corpus docs for a support issue.
    Uses domain-filtered index when company is known, falls back to full corpus.
    """
    query = f"{subject or ''} {issue_text}"

    domain = None
    if company and company.strip().lower() not in ("none", ""):
        domain = company.strip()

    retriever = SupportRetriever(domain_filter=domain)
    results = retriever.retrieve(query, top_k=top_k)

    # If domain-filtered results are empty or low, supplement with full-corpus search
    if not results or (domain and max((r["score"] for r in results), default=0) < 0.5):
        full_retriever = SupportRetriever(domain_filter=None)
        extra = full_retriever.retrieve(query, top_k=top_k)
        # merge, deduplicate
        seen_ids = {r["id"] for r in results}
        for doc in extra:
            if doc["id"] not in seen_ids:
                results.append(doc)
                seen_ids.add(doc["id"])
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

    return results


def format_context(docs: list[dict]) -> str:
    """Format retrieved docs into a context block for the LLM prompt."""
    if not docs:
        return "No relevant support documentation found."
    parts = []
    for doc in docs:
        parts.append(
            f"[{doc['domain']} | {doc['product_area']}] {doc['title']}\n{doc['content']}"
        )
    return "\n\n---\n\n".join(parts)
