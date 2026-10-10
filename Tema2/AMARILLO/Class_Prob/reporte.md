# Class_Prob: Clasificador basado en Probabilidad Condicional

## Arquitectura
Entrenador (R006) → Detokenizador (R007) → Clasificador (R008) → Métricas (R009)

## Método
- **Probabilidad condicional:** Bayes con suavizado de Laplace, P(spam | palabra). Sin suavizado, P(spam | felicidades) = 6/8 = 0.75 (pizarrón); con suavizado = 0.7515.
- **Consenso (democracia):** tres votantes (media, mediana y moda de las P(spam | palabra) de cada mensaje); gana la mayoría.
- **Normalización:** minúsculas, sin acentos, sin stopwords y, si `nltk` está instalado, stemming en español (`pip install nltk`; sin él funciona igual, sin stemming).
- **Comparación de métodos:** `main.py` opción 5 corre democracia, media, mediana y moda contra las etiquetas del supervisor.

## Resultados (10 mensajes nuevos)
| | Real: spam | Real: no spam | Total |
|---|---|---|---|
| Pred spam | 6 | 0 | 6 |
| Pred no spam | 0 | 4 | 4 |
| Total | 6 | 4 | 10 |

Accuracy 1.0 · Precision 1.0 · Recall 1.0 · Prevalence 0.6 · Bias 1.0 · Specificity 1.0 · F1 1.0

**Limitación:** los mensajes nuevos comparten vocabulario con el entrenamiento, por lo que el 100% no es representativo. Con mensajes de palabras desconocidas, el modelo cae a P(spam) = 0.7 y tiende a marcar spam (bias > 1, falsos positivos).

## Responsabilidad social
Un clasificador de spam toma decisiones sobre comunicaciones personales. Un falso positivo puede ocultar información importante (un aviso bancario o escolar legítimo), por lo que se prioriza revisar *recall* y *precision*, no solo *accuracy*. Los mensajes de los usuarios son datos personales y deben tratarse con consentimiento y anonimización. El conjunto de entrenamiento (10 mensajes, 8 con "felicidades") es pequeño y sesgado, así que el modelo no debe usarse en producción sin ampliar y diversificar los datos y sin supervisión humana.
