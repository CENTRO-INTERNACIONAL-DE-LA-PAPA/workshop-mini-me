# Adaptacion — consumidores

Origen: `04_Encuesta Percepcion de los consumidores sobre las papas nativas de color.xlsx`  ·  114 filas  ·  64 columnas

Este archivo deja por escrito todo lo que el adaptador dedujo. **La estructura se puede
inferir; el significado no.** Lo de abajo hay que confirmarlo con quien conoce los datos.

## Lo que se hizo

- Columnas totalmente vacias descartadas: v1NOconoce, v6RegaloDeAmistades.
- `Sexo` -> `sexo`
- `v1conoceConsume` -> `v1conoceconsume`
- `v1conoceNOconsume` -> `v1conocenoconsume`
- `v2UnaVezSemanal` -> `v2unavezsemanal`
- `v2MasDeUnaVezSemanal` -> `v2masdeunavezsemanal`
- `v2deVezEnCuando` -> `v2devezencuando`
- `v3reunionesSociales` -> `v3reunionessociales`
- `v3ReunionesCotidiano` -> `v3reunionescotidiano`
- `v3otrasOcasiones` -> `v3otrasocasiones`
- `v4unKg` -> `v4unkg`
- `v4dosKg` -> `v4doskg`
- `v4masDe2kg` -> `v4masde2kg`
- `v5platosGourmet` -> `v5platosgourmet`
- `v5platosCotidianos` -> `v5platoscotidianos`
- `v6MercadoDeAbasto` -> `v6mercadodeabasto`
- `v6Supermercados` -> `v6supermercados`
- `v6Ferias` -> `v6ferias`
- `v6Otros` -> `v6otros`
- `v7Nutricion` -> `v7nutricion`
- `v7ValorCultural` -> `v7valorcultural`
- `v7Precio` -> `v7precio`
- `v7Sabor` -> `v7sabor`
- `v7ProducidoOrganicamente` -> `v7producidoorganicamente`
- `v7BuenoParaLaSalud` -> `v7buenoparalasalud`
- `v7ContribucionDesarrolloRural` -> `v7contribuciondesarrollorural`
- `v8Nutritivo` -> `v8nutritivo`
- `v8ValorCultural` -> `v8valorcultural`
- `v8Caro` -> `v8caro`
- `v8Sabroso` -> `v8sabroso`
- `v8ComidaParaCampesinos` -> `v8comidaparacampesinos`
- `v8Sofisticado` -> `v8sofisticado`
- `v8Saludable` -> `v8saludable`
- `v9RespetoAlMedioAmbiente` -> `v9respetoalmedioambiente`
- `v9ProteccionBiodiversidad` -> `v9proteccionbiodiversidad`
- `v9DesarrolloComunidadAndina` -> `v9desarrollocomunidadandina`
- `v9PagarPrecioJustoAlAgricultor` -> `v9pagarpreciojustoalagricultor`
- `v10Television` -> `v10television`
- `v10SupermercadoTiendas` -> `v10supermercadotiendas`
- `v10Radio` -> `v10radio`
- `v10MuestrasEnEventos` -> `v10muestraseneventos`
- `v10DiariosORevistas` -> `v10diariosorevistas`
- `v10AmigosOFamiliares` -> `v10amigosofamiliares`
- `v10PanelesAfiches` -> `v10panelesafiches`
- `v10Otros` -> `v10otros`
- `v11ApoyoComprandoEnWong` -> `v11apoyocomprandoenwong`
- `v11ImagenMejoradaDePapasNativasPorWong` -> `v11imagenmejoradadepapasnativasporwong`
- `v11IncrementoConocimientoPatrimonioCZonasAndinasPorWong` -> `v11incrementoconocimientopatrimonioczonasandinasporwong`
- `v11IncrementoConocimientoVidaProductoresAndinosPorWong` -> `v11incrementoconocimientovidaproductoresandinosporwong`
- Identificador unico encontrado: `encuestado`.

## Tipos y unidades deducidos

| Columna | Original | Tipo | Unidad | Rol propuesto | Rango observado |
|---|---|---|---|---|---|
| `encuesta` | encuesta | integer | none | `context` | 0-43 |
| `distrito` | distrito | category | none | `context` | La Molina|Miraflores|San Isidro |
| `fecha` | fecha | date | none | `design` | 2015-06-22..2015-06-29 |
| `encuestador` | encuestador | category | none | `context` | Encuestador01|Encuestador02|Encuestador03 |
| `encuestado` | encuestado | string | none | `primary_key` | unique |
| `sexo` | Sexo | category | none | `context` | F|M |
| `edad` | edad | integer | none | `context` | 15-80 |
| `v1conoceconsume` | v1conoceConsume | integer | none | `context` | 0-2 |
| `v1conocenoconsume` | v1conoceNOconsume | integer | none | `context` | 0-2 |
| `v2diario` | v2diario | integer | none | `context` | 0-2 |
| `v2unavezsemanal` | v2UnaVezSemanal | integer | none | `context` | 0-2 |
| `v2masdeunavezsemanal` | v2MasDeUnaVezSemanal | integer | none | `context` | 0-2 |
| `v2quincenal` | v2quincenal | integer | none | `context` | 0-2 |
| `v2mensual` | v2mensual | integer | none | `context` | 0-2 |
| `v2devezencuando` | v2deVezEnCuando | integer | none | `context` | 0-2 |
| `v3cotidiano` | v3cotidiano | integer | none | `context` | 0-2 |
| `v3reunionessociales` | v3reunionesSociales | integer | none | `context` | 0-2 |
| `v3reunionescotidiano` | v3ReunionesCotidiano | integer | none | `context` | 0-2 |
| `v3otrasocasiones` | v3otrasOcasiones | integer | none | `context` | 0-2 |
| `v4mesos1kg` | v4mesos1kg | integer | none | `context` | 0-2 |
| `v4unkg` | v4unKg | integer | none | `context` | 0-2 |
| `v4doskg` | v4dosKg | integer | none | `context` | 0-2 |
| `v4masde2kg` | v4masDe2kg | integer | none | `context` | 0-2 |
| `v5fritos` | v5fritos | integer | none | `context` | 0-2 |
| `v5sancochados` | v5sancochados | integer | none | `context` | 0-2 |
| `v5bocaditos` | v5bocaditos | integer | none | `context` | 0-2 |
| `v5platosgourmet` | v5platosGourmet | integer | none | `context` | 0-2 |
| `v5platoscotidianos` | v5platosCotidianos | integer | none | `context` | 0-2 |
| `v5chips` | v5chips | integer | none | `context` | 0-2 |
| `v5otras` | v5otras | integer | none | `context` | 0-2 |
| `v6mercadodeabasto` | v6MercadoDeAbasto | integer | none | `context` | 0-2 |
| `v6supermercados` | v6Supermercados | integer | none | `context` | 0-2 |
| `v6ferias` | v6Ferias | integer | none | `context` | 0-2 |
| `v6otros` | v6Otros | integer | none | `context` | 0-2 |
| `v7nutricion` | v7Nutricion | integer | none | `context` | 0-4 |
| `v7valorcultural` | v7ValorCultural | integer | none | `context` | 0-4 |
| `v7precio` | v7Precio | integer | none | `context` | 0-4 |
| `v7sabor` | v7Sabor | integer | none | `context` | 0-4 |
| `v7producidoorganicamente` | v7ProducidoOrganicamente | integer | none | `context` | 0-4 |
| `v7buenoparalasalud` | v7BuenoParaLaSalud | integer | none | `context` | 0-4 |
| `v7contribuciondesarrollorural` | v7ContribucionDesarrolloRural | integer | none | `context` | 0-4 |
| `v8nutritivo` | v8Nutritivo | integer | none | `context` | 0-4 |
| `v8valorcultural` | v8ValorCultural | integer | none | `context` | 0-4 |
| `v8caro` | v8Caro | integer | none | `context` | 0-4 |
| `v8sabroso` | v8Sabroso | integer | none | `context` | 0-4 |
| `v8comidaparacampesinos` | v8ComidaParaCampesinos | integer | none | `context` | 0-4 |
| `v8sofisticado` | v8Sofisticado | integer | none | `context` | 0-4 |
| `v8saludable` | v8Saludable | integer | none | `context` | 0-4 |
| `v9respetoalmedioambiente` | v9RespetoAlMedioAmbiente | integer | none | `context` | 0-6 |
| `v9proteccionbiodiversidad` | v9ProteccionBiodiversidad | integer | none | `context` | 0-6 |
| `v9desarrollocomunidadandina` | v9DesarrolloComunidadAndina | integer | none | `context` | 0-6 |
| `v9pagarpreciojustoalagricultor` | v9PagarPrecioJustoAlAgricultor | integer | none | `context` | 0-6 |
| `v10television` | v10Television | integer | none | `context` | 0-2 |
| `v10supermercadotiendas` | v10SupermercadoTiendas | integer | none | `context` | 0-2 |
| `v10radio` | v10Radio | integer | none | `context` | 0-2 |
| `v10muestraseneventos` | v10MuestrasEnEventos | integer | none | `context` | 0-2 |
| `v10diariosorevistas` | v10DiariosORevistas | integer | none | `context` | 0-2 |
| `v10amigosofamiliares` | v10AmigosOFamiliares | integer | none | `context` | 0-2 |
| `v10panelesafiches` | v10PanelesAfiches | integer | none | `context` | 0-2 |
| `v10otros` | v10Otros | integer | none | `context` | 0-2 |
| `v11apoyocomprandoenwong` | v11ApoyoComprandoEnWong | integer | none | `context` | 0-6 |
| `v11imagenmejoradadepapasnativasporwong` | v11ImagenMejoradaDePapasNativasPorWong | integer | none | `context` | 0-6 |
| `v11incrementoconocimientopatrimonioczonasandinasporwong` | v11IncrementoConocimientoPatrimonioCZonasAndinasPorWong | integer | none | `context` | 0-6 |
| `v11incrementoconocimientovidaproductoresandinosporwong` | v11IncrementoConocimientoVidaProductoresAndinosPorWong | integer | none | `context` | 0-6 |

## Confirmar antes de usar

1. **Unidad de observacion**: ¿que representa una fila?
2. **Variable de resultado**: ¿cual es el `outcome`? Ahora todas figuran como `context`.
3. **Columnas calculadas despues del resultado**: son el `leakage` del ejercicio.
4. **Columnas de diseño**: revisar las marcadas `design` abajo, y agregar las que falten.
5. **Unidades**: las deducidas del nombre de la columna estan sin verificar.
6. **Relaciones conocidas**: ¿alguna que exista de verdad, y alguna que se sepa que no?

Los roles validos son: `primary_key`, `design`, `context`, `predictor`, `outcome`,
`outcome_secondary`, `confounded_exposure`, `leakage`, `null`.

Marcadas como `design` por el nombre: `fecha`.

## Siguiente paso

Editar `consumidores_dictionary.csv` con las respuestas de arriba y despues:

```bash
python scripts/corrupt_dataset.py datasets/consumidores/consumidores_clean.csv
```

## Configuración del taller (`configurar_taller.py`)

- 18 entradas de configuración aplicadas. Diccionario completo en `consumidores_dictionary_completo.csv`; en `consumidores_dictionary.csv` (participantes) las 0 columnas leakage aparecen como `predictor`.
- Casillas de marcar (v1, v2, v3, v4, v5, v6, v10): 0 celdas vacías pasan a 0 en `consumidores_clean.csv`. Vacío significaba 'no marcado'; sin esto, un faltante sembrado sería indistinguible de un 'no'.

Preguntas para quien produjo los datos:

1. Propuesta de resultado: `v9pagarpreciojustoalagricultor`. ¿Hay otra pregunta que interese más?
2. La escala de `v8` no está en el diccionario y los datos solo tienen 1-3: ¿qué significa cada valor?
3. En `v9` y `v11`, el 5 significa 'no sé': ¿se trata como faltante en el análisis?
