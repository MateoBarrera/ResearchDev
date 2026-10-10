# Comparación de casos de estudio

Este documento resume la comparación reproducible entre Jamundí y Santa Rosalía usando las corridas completas del pipeline.

## Contexto comparable

Las dos corridas usan:

- Capacidad instalada: `1000 kW`.
- Seed completo de 26 valores, desde `1.0` hasta `0.0` en pasos de `0.04`.
- 3.276 alternativas.
- 12 indicadores.
- 29 escenarios TOPSIS.
- El mismo archivo de pesos TOPSIS.
- El mismo hash de código: `fe6bfa88c0ac653eb1c036396eaadd952b8158b0d4a628921373c8fd72921f1c`.

Por tanto, las diferencias observadas se atribuyen principalmente a los datos del sitio y a los catálogos de indicadores de cada caso, no a una configuración distinta del pipeline.

## Resultados de robustez

| Caso | Alternativa robusta | Top 5 en escenarios | Puesto medio | Desviación del puesto | Mejor puesto | Peor puesto |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Jamundí | 2921 | 20% | 871.8 | 790.31 | 3 | 2022 |
| Santa Rosalía | 3250 | 60% | 492.2 | 976.41 | 1 | 2445 |

La alternativa robusta se selecciona priorizando `top_5_rate`, después menor `rank_std` y finalmente menor `mean_rank`.

## Interpretación

### Jamundí

La alternativa `2921` alcanza posiciones muy altas en algunos escenarios, pero solo permanece entre las cinco primeras en el 20% de ellos. Su puesto medio es 871.8 y su peor puesto es 2022. Esto indica una recomendación muy dependiente de la dimensión priorizada.

Aunque su desviación estándar es menor que la de Santa Rosalía, la estabilidad no es suficiente para considerarla una alternativa consistentemente dominante. La decisión debería acompañarse de un análisis específico de pesos y de la composición tecnológica de la alternativa.

### Santa Rosalía

La alternativa `3250` permanece entre las cinco primeras en el 60% de los escenarios y alcanza el primer puesto. Su puesto medio es 492.2, mejor que el de Jamundí, aunque presenta una dispersión mayor y llega hasta el puesto 2445.

Esto sugiere una mejor robustez en términos de presencia en el grupo superior, pero no una estabilidad absoluta: ciertos énfasis de dimensión cambian sustancialmente su posición.

## Conclusión metodológica

- Santa Rosalía presenta la alternativa más robusta según permanencia en el top 5 y puesto medio.
- Jamundí presenta una alternativa que puede ser excelente bajo escenarios concretos, pero es más sensible a la ponderación de dimensiones.
- `rank_std` no debe interpretarse de forma aislada: una alternativa puede tener menor dispersión y aun así aparecer pocas veces entre las mejores.
- La robustez del ranking no sustituye la validación de unidades, fuentes, indicadores y supuestos físicos.

## Artefactos

El comparador se ejecuta con:

```bash
python compare_cases.py --output case_comparison.xlsx
```

Salidas fuente de la comparación:

- `case_studies/jamundi/results/run_manifest.json`
- `case_studies/santa_rosalia/results/run_manifest.json`
- `case_studies/jamundi/results/sensitivity_3276_alternatives.xlsx`
- `case_studies/santa_rosalia/results/sensitivity_3276_alternatives.xlsx`
