# Clave de defectos — consumidores

> No distribuir antes del ejercicio. Este archivo dice exactamente qué se rompió.

Semilla: `20261022`. Volver a correr `corrupt_dataset.py` con la misma semilla reproduce
estos archivos byte por byte.

**Total de cambios registrados: 496**

## Por familia

| Familia | Cambios | Columnas afectadas |
|---|---:|---|
| `category_variant` | 190 | distrito, encuestador, sexo, v10amigosofamiliares, v10diariosorevistas, v10muestraseneventos, v10otros, v10panelesafiches, v10radio, v10supermercadotiendas, v10television, v1conoceconsume, v1conocenoconsume, v2devezencuando, v2diario, v2masdeunavezsemanal, v2mensual, v2quincenal, v2unavezsemanal, v3cotidiano, v3otrasocasiones, v3reunionescotidiano, v3reunionessociales, v4doskg, v4masde2kg, v4mesos1kg, v4unkg, v5bocaditos, v5chips, v5fritos, v5otras, v5platoscotidianos, v5platosgourmet, v5sancochados, v6ferias, v6mercadodeabasto, v6otros, v6supermercados |
| `date_format` | 3 | fecha |
| `duplicate_row` | 3 | — |
| `impossible_value` | 48 | edad, encuesta, v11apoyocomprandoenwong, v11imagenmejoradadepapasnativasporwong, v11incrementoconocimientopatrimonioczonasandinasporwong, v11incrementoconocimientovidaproductoresandinosporwong, v7buenoparalasalud, v7contribuciondesarrollorural, v7nutricion, v7precio, v7producidoorganicamente, v7sabor, v7valorcultural, v8caro, v8comidaparacampesinos, v8nutritivo, v8sabroso, v8saludable, v8sofisticado, v8valorcultural, v9desarrollocomunidadandina, v9pagarpreciojustoalagricultor, v9proteccionbiodiversidad, v9respetoalmedioambiente |
| `missing_cell` | 252 | distrito, edad, encuesta, encuestador, fecha, sexo, v10amigosofamiliares, v10diariosorevistas, v10muestraseneventos, v10otros, v10panelesafiches, v10radio, v10supermercadotiendas, v10television, v11apoyocomprandoenwong, v11imagenmejoradadepapasnativasporwong, v11incrementoconocimientopatrimonioczonasandinasporwong, v11incrementoconocimientovidaproductoresandinosporwong, v1conoceconsume, v1conocenoconsume, v2devezencuando, v2diario, v2masdeunavezsemanal, v2mensual, v2quincenal, v2unavezsemanal, v3cotidiano, v3otrasocasiones, v3reunionescotidiano, v3reunionessociales, v4doskg, v4masde2kg, v4mesos1kg, v4unkg, v5bocaditos, v5chips, v5fritos, v5otras, v5platoscotidianos, v5platosgourmet, v5sancochados, v6ferias, v6mercadodeabasto, v6otros, v6supermercados, v7buenoparalasalud, v7contribuciondesarrollorural, v7nutricion, v7precio, v7producidoorganicamente, v7sabor, v7valorcultural, v8caro, v8comidaparacampesinos, v8nutritivo, v8sabroso, v8saludable, v8sofisticado, v8valorcultural, v9desarrollocomunidadandina, v9pagarpreciojustoalagricultor, v9proteccionbiodiversidad, v9respetoalmedioambiente |

## Por columna

| Columna | Cambios | Familias |
|---|---:|---|
| `distrito` | 9 | category_variant, missing_cell |
| `edad` | 6 | impossible_value, missing_cell |
| `encuesta` | 6 | impossible_value, missing_cell |
| `encuestador` | 9 | category_variant, missing_cell |
| `fecha` | 7 | date_format, missing_cell |
| `sexo` | 9 | category_variant, missing_cell |
| `v10amigosofamiliares` | 9 | category_variant, missing_cell |
| `v10diariosorevistas` | 9 | category_variant, missing_cell |
| `v10muestraseneventos` | 9 | category_variant, missing_cell |
| `v10otros` | 9 | category_variant, missing_cell |
| `v10panelesafiches` | 9 | category_variant, missing_cell |
| `v10radio` | 9 | category_variant, missing_cell |
| `v10supermercadotiendas` | 9 | category_variant, missing_cell |
| `v10television` | 9 | category_variant, missing_cell |
| `v11apoyocomprandoenwong` | 6 | impossible_value, missing_cell |
| `v11imagenmejoradadepapasnativasporwong` | 6 | impossible_value, missing_cell |
| `v11incrementoconocimientopatrimonioczonasandinasporwong` | 6 | impossible_value, missing_cell |
| `v11incrementoconocimientovidaproductoresandinosporwong` | 6 | impossible_value, missing_cell |
| `v1conoceconsume` | 9 | category_variant, missing_cell |
| `v1conocenoconsume` | 9 | category_variant, missing_cell |
| `v2devezencuando` | 9 | category_variant, missing_cell |
| `v2diario` | 9 | category_variant, missing_cell |
| `v2masdeunavezsemanal` | 9 | category_variant, missing_cell |
| `v2mensual` | 9 | category_variant, missing_cell |
| `v2quincenal` | 9 | category_variant, missing_cell |
| `v2unavezsemanal` | 9 | category_variant, missing_cell |
| `v3cotidiano` | 9 | category_variant, missing_cell |
| `v3otrasocasiones` | 9 | category_variant, missing_cell |
| `v3reunionescotidiano` | 9 | category_variant, missing_cell |
| `v3reunionessociales` | 9 | category_variant, missing_cell |
| `v4doskg` | 9 | category_variant, missing_cell |
| `v4masde2kg` | 9 | category_variant, missing_cell |
| `v4mesos1kg` | 9 | category_variant, missing_cell |
| `v4unkg` | 9 | category_variant, missing_cell |
| `v5bocaditos` | 9 | category_variant, missing_cell |
| `v5chips` | 9 | category_variant, missing_cell |
| `v5fritos` | 9 | category_variant, missing_cell |
| `v5otras` | 9 | category_variant, missing_cell |
| `v5platoscotidianos` | 9 | category_variant, missing_cell |
| `v5platosgourmet` | 9 | category_variant, missing_cell |
| `v5sancochados` | 9 | category_variant, missing_cell |
| `v6ferias` | 9 | category_variant, missing_cell |
| `v6mercadodeabasto` | 9 | category_variant, missing_cell |
| `v6otros` | 9 | category_variant, missing_cell |
| `v6supermercados` | 9 | category_variant, missing_cell |
| `v7buenoparalasalud` | 6 | impossible_value, missing_cell |
| `v7contribuciondesarrollorural` | 6 | impossible_value, missing_cell |
| `v7nutricion` | 6 | impossible_value, missing_cell |
| `v7precio` | 6 | impossible_value, missing_cell |
| `v7producidoorganicamente` | 6 | impossible_value, missing_cell |
| `v7sabor` | 6 | impossible_value, missing_cell |
| `v7valorcultural` | 6 | impossible_value, missing_cell |
| `v8caro` | 6 | impossible_value, missing_cell |
| `v8comidaparacampesinos` | 6 | impossible_value, missing_cell |
| `v8nutritivo` | 6 | impossible_value, missing_cell |
| `v8sabroso` | 6 | impossible_value, missing_cell |
| `v8saludable` | 6 | impossible_value, missing_cell |
| `v8sofisticado` | 6 | impossible_value, missing_cell |
| `v8valorcultural` | 6 | impossible_value, missing_cell |
| `v9desarrollocomunidadandina` | 6 | impossible_value, missing_cell |
| `v9pagarpreciojustoalagricultor` | 6 | impossible_value, missing_cell |
| `v9proteccionbiodiversidad` | 6 | impossible_value, missing_cell |
| `v9respetoalmedioambiente` | 6 | impossible_value, missing_cell |

## Cómo se usa

El detalle celda a celda está en `consumidores_changelog.csv`: cada fila trae `record_id`,
columna, valor original y valor sucio. Ese archivo permite medir cuántos de los defectos
sembrados reparó realmente un equipo, que es una pregunta más estricta que el score global
de `score_cleanliness.py`.
