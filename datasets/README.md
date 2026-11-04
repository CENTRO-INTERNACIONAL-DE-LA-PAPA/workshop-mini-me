# datasets

Aquí van los cuatro paquetes del workshop (`morfologia`, `mejoramiento`, `tizon_tardio` y
`consumidores`), uno por temática, más los archivos originales en `_crudos/`. **Git ignora todo
salvo este README**: son datos reales de CIP.

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

Para regenerarlos desde los originales (los `.xls` se convierten antes a `.xlsx`):

```bash
python scripts/adapt_dataset.py "datasets/_crudos/<archivo>.xlsx" --slug <slug> --key-prefix <PRE> --output-dir datasets/<slug>
python scripts/configurar_taller.py datasets/
python scripts/corrupt_dataset.py datasets/<slug>/<slug>_clean.csv
```

Detalles en el [README del repositorio](../README.md).

Aunque los datos estén anonimizados y con visto bueno escrito (§2.4 del plan), no se
versionan: se comparten con los participantes por fuera del repositorio. Los paquetes sintéticos de prueba se regeneran con
`python scripts/generate_datasets.py --output-dir .`.
