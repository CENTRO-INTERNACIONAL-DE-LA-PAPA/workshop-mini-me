# datasets

Los cuatro paquetes del workshop, uno por temática: `morfologia`, `mejoramiento`, `tizon_tardio` y
`consumidores`. Son datos reales de CIP, públicos y con visto bueno para el taller, y se distribuyen
a los participantes a través de este repositorio.

```
datasets/<tematica>/
  README.md                           brief del participante
  <tematica>_dirty.csv                punto de partida del participante
  <tematica>_dictionary.csv           diccionario del participante (los leakage aparecen como predictor)
  <tematica>_clean.csv                benchmark contra el que se mide
  originales/                         los archivos tal como los entregó quien produjo los datos
  <tematica>_dictionary_completo.csv  diccionario con todos los roles      (facilitador)
  <tematica>_changelog.csv            cada celda modificada y su original  (facilitador)
  <tematica>_defect_key.md            resumen de defectos y leakage        (facilitador)
  <tematica>_ADAPTATION.md            decisiones del adaptador y preguntas (facilitador)
```

Todo es visible para quien abra el repositorio: los README de cada temática piden no abrir el
limpio ni los archivos de facilitador antes de terminar.

Para regenerarlos desde `originales/` (los `.xls` se convierten antes a `.xlsx`, por ejemplo con
`soffice --headless --convert-to xlsx`):

```bash
python scripts/adapt_dataset.py "datasets/<slug>/originales/<archivo>.xlsx" --slug <slug> --key-prefix <PRE> --output-dir datasets/<slug>
python scripts/configurar_taller.py datasets/
python scripts/corrupt_dataset.py datasets/<slug>/<slug>_clean.csv --dictionary datasets/<slug>/<slug>_dictionary_completo.csv
```

La semilla es fija, así que el archivo sucio sale idéntico byte a byte. Para medir el archivo limpio
de un equipo:

```bash
python scripts/score_recovery.py archivo_del_equipo.csv --reference datasets/<slug>/<slug>_clean.csv --dictionary datasets/<slug>/<slug>_dictionary.csv
```

Detalles en el [README del repositorio](../README.md).

La encuesta de consumidores está anonimizada: personas y encuestadores aparecen solo con códigos. Los paquetes sintéticos de prueba se regeneran con
`python scripts/generate_datasets.py --output-dir .`.
