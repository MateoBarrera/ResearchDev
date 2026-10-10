# Referencia técnica de instalación y ejecución

Esta guía describe cómo preparar el entorno y ejecutar los análisis de los casos de estudio incluidos en ResearchDev. El flujo recomendado es el motor de investigación de `main_2.py`, que usa los modelos del paquete `synergy`.

## 1. Requisitos del sistema

- Python 3.10 o superior.
- `pip` y `venv` disponibles.
- Git, si se parte de un clon del repositorio.
- Aproximadamente 1 GB de espacio libre para el entorno y los resultados Excel.
- Sistema operativo Linux, macOS o Windows.

El proyecto usa pandas, NumPy, SciPy, Pydantic, PyYAML, numexpr, openpyxl y las dependencias de Django declaradas en `requirements.txt`.

El notebook agrega requisitos opcionales: JupyterLab y `pywaffle`.

## 2. Obtener el proyecto

Si el repositorio todavía no existe localmente:

```bash
git clone <URL_DEL_REPOSITORIO>
cd ResearchDev
```

La ejecución debe hacerse desde la raíz del repositorio. Las rutas de los YAML y de los scripts son relativas a esa ubicación.

## 3. Crear y activar el entorno virtual

### Linux y macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows CMD

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si el sistema no reconoce `python` o `python3`, instalar Python y habilitar la opción de agregarlo al `PATH`. En VS Code, seleccionar después el intérprete `.venv` mediante **Python: Select Interpreter**.

## 4. Validar la instalación

Ejecutar desde la raíz:

```bash
python --version
python -m pip --version
python -m pytest -q
```

La prueba de importación mínima es:

```bash
python -c "from synergy.resources import Solar, Wind, Hydro, Biomass; from synergy.alternative import Alternatives; print('Entorno ResearchDev listo')"
```

Si `pytest` no está disponible, confirmar que el entorno virtual está activo y reinstalar con `python -m pip install -r requirements.txt`.

## 5. Verificar los datos de los casos

Los dos casos completos tienen los siguientes insumos:

| Caso          | Configuración                                | Solar                                    | Viento                                     | Hidro                                        | Biomasa                                        | Indicadores                                  |
| ------------- | -------------------------------------------- | ---------------------------------------- | ------------------------------------------ | -------------------------------------------- | ---------------------------------------------- | -------------------------------------------- |
| Jamundí       | `case_studies/jamundi/definition.yaml`       | `case_studies/jamundi/data/pv.csv`       | `case_studies/jamundi/data/wind.csv`       | `case_studies/jamundi/data/hydro.csv`        | `case_studies/jamundi/data/biomass.xlsx`       | `synergy/indicators_data.json`               |
| Santa Rosalía | `case_studies/santa_rosalia/definition.yaml` | `case_studies/santa_rosalia/data/pv.csv` | `case_studies/santa_rosalia/data/wind.csv` | `case_studies/santa_rosalia/data/hydro.data` | `case_studies/santa_rosalia/data/biomass.xlsx` | `case_studies/santa_rosalia/indicators.json` |

También debe existir `synergy/evaluation/mcda/weight_criteria.xlsx`, utilizado por la evaluación automática de TOPSIS.

Las rutas declaradas en los YAML son relativas a la raíz del repositorio. No ejecutar el script desde `case_studies/` ni desde `resource_synergy/`.

## 6. Ejecutar Santa Rosalía

El runner recomendado permite seleccionar el caso sin editar código:

```bash
python run_analysis.py --case santa_rosalia
```

El proceso realiza estas etapas:

1. Lee `case_studies/santa_rosalia/definition.yaml`.
2. Evalúa solar, viento, hidro y biomasa para `INSTALLED_CAPACITY: 1000`.
3. Genera combinaciones de capacidad usando los valores `seed` definidos en `main_2.py`.
4. Calcula la generación de cada alternativa.
5. Evalúa los indicadores de `case_studies/santa_rosalia/indicators.json`.
6. Ejecuta TOPSIS con `test_criteria = -1`.
7. Guarda los resultados en `case_studies/santa_rosalia/results/`.

Los archivos principales de salida son:

```text
case_studies/santa_rosalia/results/alternatives_<n>.xlsx
case_studies/santa_rosalia/results/ranking_of_<n>_alternatives.xlsx
```

El valor `<n>` depende del número de combinaciones válidas generadas.

## 7. Ejecutar Jamundí

Jamundí se ejecuta con el mismo runner:

```bash
python run_analysis.py --case jamundi
```

También se puede ejecutar una definición explícita:

```bash
python run_analysis.py --config case_studies/jamundi/definition.yaml
```

Las salidas se escribirán en:

```text
case_studies/jamundi/results/alternatives_<n>.xlsx
case_studies/jamundi/results/ranking_of_<n>_alternatives.xlsx
```

Para pruebas rápidas, limitar el conjunto de participaciones:

```bash
python run_analysis.py --case santa_rosalia --seed 1 0.5 0
```

El runner está implementado en `synergy/runner.py`; `main_2.py` se conserva como entrada histórica.

## 8. Interpretar la configuración

Cada definición YAML contiene:

- `CASE_STUDY`: nombre usado para construir la carpeta de resultados.
- `INSTALLED_CAPACITY`: capacidad total objetivo, en kW según el flujo actual.
- `BIOMASS_REQUIREMENTS`: cantidades de cultivos y ganado consideradas para biomasa.
- `RESOURCES`: tecnologías habilitadas y sus archivos de entrada.
- `INDICATORS`: ruta opcional a un catálogo de indicadores específico.

El catálogo de indicadores JSON define, para cada indicador, su dimensión, unidad, fuente, tipo (`cost` o `benefit`) y fórmula. Las variables de las fórmulas deben existir en las alternativas, por ejemplo `solar_generation`, `wind_generation`, `hydro_generation` y `biomass_generation`.

## 9. Ejecutar la API opcional

La API no es necesaria para ejecutar los casos por consola. Si se necesita levantarla:

```bash
cd resource_synergy
python manage.py migrate
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/api/v1/
http://127.0.0.1:8000/api/v1/docs
```

La API usa SQLite local y administra sitios, variables de recursos, fuentes y análisis. Actualmente no ejecuta automáticamente el pipeline de `main_2.py` ni persiste un ranking completo; debe considerarse una capa de prototipo.

## 10. Notebook de análisis

Para las visualizaciones y el análisis posterior:

```bash
python -m pip install jupyterlab pywaffle
jupyter lab analysis_result/data_exploration_01.ipynb
```

El notebook espera archivos Excel generados previamente y puede usar rutas relativas a la raíz. Conviene abrir Jupyter desde la raíz del proyecto.

## 11. Problemas frecuentes

### `python: command not found`

Instalar Python 3.10 o superior, abrir una nueva terminal y crear el entorno virtual. En Linux/macOS puede ser necesario usar `python3`; una vez activado `.venv`, el comando recomendado es `python`.

### `ModuleNotFoundError`

Activar `.venv` y reinstalar las dependencias:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows usar `.venv\Scripts\Activate.ps1` o `.venv\Scripts\activate.bat`.

### No encuentra un CSV, `.data` o Excel

Comprobar que el comando se ejecuta desde la raíz y que la ruta del YAML coincide con los archivos presentes. No renombrar las extensiones de los datos: los lectores distinguen CSV, `.data` y `biomass.xlsx`.

### Fallo al leer biomasa

El libro debe llamarse `biomass.xlsx` y contener las hojas `Historico Cultivos` y `Historico Pecuario`, con las columnas esperadas por `synergy/resources/utils/csv_readers.py`.

### El notebook no encuentra `case_studies` o `synergy`

Cerrar el kernel, iniciar Jupyter desde la raíz del proyecto y volver a abrir el notebook. También se puede revisar el directorio de trabajo configurado por VS Code/Jupyter.

### Resultados diferentes entre ejecuciones

Revisar el YAML, el catálogo de indicadores, los valores `seed` de `main_2.py` y los parámetros del modelo de cada recurso. Los archivos Excel existentes en `results/` corresponden a ejecuciones históricas y pueden tener diferente número de alternativas.

## 12. Checklist de una ejecución reproducible

- [ ] Python 3.10+ disponible.
- [ ] Entorno `.venv` creado y activado.
- [ ] `requirements.txt` instalado.
- [ ] `python -m pytest -q` ejecutado sin errores de entorno.
- [ ] Comando iniciado desde la raíz del repositorio.
- [ ] YAML seleccionado y archivos de recursos existentes.
- [ ] Indicadores y pesos disponibles.
- [ ] Carpeta `case_studies/<caso>/results/` disponible.
- [ ] Archivos `alternatives_<n>.xlsx` y `ranking_of_<n>_alternatives.xlsx` revisados.
