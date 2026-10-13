# Experiment Log - RAG

| Fecha | Cambio | Hipotesis | Metrica | Resultado | Decision |
|---|---|---|---|---|---|
| 2026-10-12 | chunk_size=900, overlap=120 | Baseline de fragmentación para documentos técnicos | Hit@5 | Hit@5 = 100% en backend local | Mantener configuración base |
| 2026-10-12 | top_k=5 | Un top_k=5 balancea cobertura de evidencia y latencia | Hit@5 / latencia | 10/10 hits, latencia local ~1 ms | Mantener top_k=5 |
| 2026-10-12 | Modo Keyword (Azure AI Search) | Búsqueda lexical BM25 efectiva para terminología técnica exacta | Hit@5 / latencia | Hit@5 = 10/10 (100%), latencia 1037 ms | Seleccionar como modo primario con hash embeddings |
| 2026-10-12 | Modo Vector (Azure AI Search) | Búsqueda con hash embedding (128 dims) | Hit@5 / latencia | Hit@5 = 8/10 (80%), latencia 1018 ms | Degradación esperada por falta de semántica en hash |
| 2026-10-12 | Modo Hybrid (Azure AI Search) | Fusión RRF (BM25 + vector hash) | Hit@5 / latencia | Hit@5 = 8/10 (80%), latencia 1087 ms | Mantener disponible; requiere embeddings semánticos para superar a keyword |
| 2026-10-12 | Prueba de seguridad adversaria | Inyección indirecta contenida en chunks con etiquetas no confiables | Security flags / contención | 5 flags detectadas, respuesta extractiva no manipulada | Mantener pipeline de sanitización |
