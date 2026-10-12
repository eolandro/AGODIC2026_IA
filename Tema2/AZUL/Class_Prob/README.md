# Clasificador basado en Probabilidad Condicional

El proyecto clasifica mensajes como `spam` o `no_spam` mediante probabilidad condicional y consenso democrático.

## Orden de ejecución

```powershell
python entrenador.py
python detokenizador.py
python clasificador.py
python metricas.py
```

En `entrenador.py`, el supervisor etiqueta los 10 mensajes contenidos en `base_supervisada.txt` y genera `corpus_etiquetado.json`.

En `detokenizador.py`, se tokeniza el corpus, se eliminan artículos, preposiciones y conectores, y se genera `conocimiento_probabilistico.json`.

En `clasificador.py`, se leen los 10 mensajes de `bandeja_prueba.txt`. Cada token conocido vota por `spam` o `no_spam` y la mayoría determina la clasificación guardada en `predicciones_spam.json`.

En `metricas.py`, el supervisor etiqueta los 10 mensajes nuevos y se calculan la matriz de confusión, Recall, Accuracy, Precision, Prevalence, tasa de error, F1-score y bias de predicción. Los resultados se guardan en `evaluacion_clasificador.json`.

El programa utiliza únicamente módulos incluidos en Python.
