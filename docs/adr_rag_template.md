# ADR-001: Uso de RAG en el proyecto

## Estado
Aceptado

## Contexto
El sistema requiere responder consultas sobre un corpus de conocimiento técnico interno (gestión de secretos, seguridad, despliegue, observabilidad, chunking y evaluación). Este conocimiento no forma parte de los datos de entrenamiento de modelos públicos y debe poder actualizarse de forma continua e independiente sin reentrenar un modelo. Además, el negocio requiere trazabilidad auditada con citación explícita de fuentes.

## Alternativas
1. **Sin LLM**: Búsqueda por palabras clave sin generación de respuestas sintéticas en lenguaje natural. No cumple el objetivo de experiencia conversacional.
2. **LLM sin RAG**: El modelo respondería con conocimiento desactualizado o propenso a alucinaciones, sin posibilidad de verificar fuentes.
3. **RAG (Retrieval-Augmented Generation)**: Combina una etapa de recuperación (lexical, vectorial o híbrida) con inyección de contexto acotado y generación condicionada.
4. **Agente con herramientas (Tool Calling)**: Mayor latencia y complejidad operativa no justificada para una base de conocimiento documental estática/semiestática.

## Evidencia
- **Golden set**: 12 casos de validación (10 con fuente esperada + 2 casos sin evidencia para verificar abstención).
- **Hit@K**: 
  - Local (hash, top-5): 10/10 = 100%.
  - Azure AI Search (keyword, top-5): 10/10 = 100%.
  - Azure AI Search (vector hash, top-5): 8/10 = 80%.
  - Azure AI Search (híbrido RRF, top-5): 8/10 = 80%.
- **Latencia**:
  - Local: ~1.0 ms promedio.
  - Azure AI Search Free: ~1050 ms promedio.
- **Riesgos**: 
  - Indirect prompt injection desde documentos maliciosos (mitigado con delimitadores `DOCUMENTO NO CONFIABLE` y escaneo de patrones).
  - Alucinaciones ante preguntas fuera de corpus (mitigado con umbral de relevancia y respuesta formal de abstención).
- **Costo**:
  - Azure AI Search en SKU Free (0 USD en Azure for Students).
  - Generación extractiva local o con Ollama (0 USD de costo cloud).

## Decisión
Se adopta **RAG con Azure AI Search e integración híbrida**, manteniendo compatibilidad con almacenamiento local en memoria para pruebas y desarrollo.

## Consecuencias
- Requiere pipeline de indexación y sincronización de chunks ante cambios en el corpus.
- Introduce latencia adicional por el paso de retrieval (~1 s en Azure).
- Exige aislar documentos recuperados como datos no confiables para prevenir vulnerabilidades de seguridad.

## Condición para revertir la decisión
Si el corpus se vuelve extremadamente voluminoso superando la cuota Free sin presupuesto para SKU pagado, o si la latencia promedio supera los 3000 ms degradando la experiencia de usuario.
