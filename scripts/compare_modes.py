"""Compara keyword, vector e hybrid en el golden set contra el backend configurado."""
from __future__ import annotations

import json
from pathlib import Path

from tsi_rag.config import Settings
from tsi_rag.service import RAGService

settings = Settings()
service = RAGService(settings)
cases = json.loads(Path("tests/golden_set.json").read_text(encoding="utf-8"))

print(f"=== Backend: {settings.retriever_backend} | Embedding: {settings.embedding_provider} ===\n")

summary = {}
for mode in ["keyword", "vector", "hybrid"]:
    rows = []
    for case in cases:
        query = case["question"]
        expected_source = case.get("expected_source")
        expected_no_answer = case.get("expected_no_answer", False)
        hits = service.search(query, mode, settings.top_k)
        sources = [h.source for h in hits]
        hit = (expected_source in sources) if expected_source else None
        response = service.ask(query, mode, settings.top_k)
        no_answer_ok = response.answer.startswith("No encuentro") if expected_no_answer else None
        rows.append(
            {
                "id": case["id"],
                "hit": hit,
                "no_answer_ok": no_answer_ok,
                "latency_ms": response.total_ms,
                "sources": sources[:2],
            }
        )

    retrieval_cases = [r for r in rows if r["hit"] is not None]
    hits_count = sum(1 for r in retrieval_cases if r["hit"] is True)
    no_ans_cases = [r for r in rows if r["no_answer_ok"] is not None]
    no_ans_ok = sum(1 for r in no_ans_cases if r["no_answer_ok"] is True)
    avg_lat = sum(r["latency_ms"] for r in rows) / len(rows)

    summary[mode] = {
        "hits": hits_count,
        "total": len(retrieval_cases),
        "pct": hits_count / max(1, len(retrieval_cases)),
        "no_ans_ok": no_ans_ok,
        "avg_lat_ms": avg_lat,
    }

    print(f"--- Modo: {mode.upper()} ---")
    print(f"Hit@5: {hits_count}/{len(retrieval_cases)} = {hits_count / max(1, len(retrieval_cases)):.0%}")
    print(f"Sin evidencia OK: {no_ans_ok}/{len(no_ans_cases)}")
    print(f"Latencia promedio: {avg_lat:.2f} ms")
    for r in rows:
        icon = "OK" if (r["hit"] is True or r["no_answer_ok"] is True) else "MISS"
        print(f"  [{icon}] {r['id']} | lat={r['latency_ms']:.0f}ms | src={r['sources']}")
    print()

print("=== RESUMEN COMPARATIVO ===")
print(f"{'Modo':<10} {'Hit@5':>8} {'%':>7} {'SinEvid':>9} {'Lat avg (ms)':>14}")
for mode, s in summary.items():
    print(f"{mode:<10} {s['hits']}/{s['total']:>5} {s['pct']:>7.0%} {s['no_ans_ok']}/2{' ':>7} {s['avg_lat_ms']:>12.2f}")
