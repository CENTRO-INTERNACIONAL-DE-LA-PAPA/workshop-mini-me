# datasets

Vacío a propósito. Aquí van los cuatro paquetes del workshop, uno por temática, cuando
lleguen los datos reales:

```
datasets/<tematica>/
  <tematica>_clean.csv        benchmark del facilitador
  <tematica>_dirty.csv        punto de partida del participante
  <tematica>_dictionary.csv   tipos, unidades, roles y rangos válidos
  <tematica>_changelog.csv    cada celda que se modificó, con su valor original
  <tematica>_defect_key.md    resumen de defectos para el facilitador
  <tematica>_ADAPTATION.md    qué dedujo el adaptador y qué falta confirmar
  README.md                   brief del participante
```

Los tres primeros archivos los produce el pipeline; ver el
[README del repositorio](../README.md).

Nada de esto se versiona hasta que los datos estén anonimizados y con visto bueno escrito
(§2.4 del plan). Los paquetes sintéticos de prueba se regeneran con
`python scripts/generate_datasets.py --output-dir .`.
