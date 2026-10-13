# Checklist de entrega

- [x] `.env` no esta versionado.
- [x] Azure AI Search Free creado (`tsi-rag-lab-alan`, canadacentral).
- [x] Indice creado con campo vectorial (`content_vector`, dim=128).
- [x] Corpus versionado (10 documentos en data/docs/).
- [x] Golden set existe antes de optimizar (tests/golden_set.json).
- [x] Keyword, vector e hybrid ejecutados.
- [x] Hit@K medido (local: 100%, Azure keyword: 100%, Azure hybrid: 80%).
- [x] Caso sin evidencia probado (G11/G12 con respuesta "No encuentro...").
- [x] Documento malicioso probado (5 flags de seguridad detectadas).
- [x] API `/health`, `/search`, `/ask` funcional.
- [x] Tests pytest verdes (11 passed, 1 skipped).
- [x] Prueba E2E ejecutada (API E2E verde; Playwright bloqueado por CDN documentado).
- [x] Logs de latencia generados (logs/queries.jsonl).
- [x] ADR RAG actualizado (docs/adr_rag_template.md y docs/INFORME_LABORATORIO_RAG.md).
- [x] Experiment Log actualizado (docs/experiment_log_template.md).

