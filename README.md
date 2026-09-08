# Ingeniería en Computación 2 — Ejercicios Resueltos

Repositorio individual con las soluciones y el andamiaje estructurado para las prácticas de **Ingeniería en Computación 2 (Bloque de Software)**.

---

## 1. Configuración del Entorno de Desarrollo

Para aislar las dependencias del proyecto y garantizar la reproducibilidad entre entornos de desarrollo, se utiliza un entorno virtual de Python (`venv`).

### 1.1. Crear el Entorno Virtual (`.venv`)

Asegúrate de estar ubicado en la raíz de este directorio (`ejercicios_resueltos/`):

**En Windows (PowerShell / Command Prompt):**
```powershell
python -m venv .venv
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
```

### 1.2. Activar el Entorno Virtual

**En Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```
*(Si la política de ejecución bloquea la activación en PowerShell, ejecutar previamente: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

**En Windows (CMD):**
```cmd
.\.venv\Scripts\activate.bat
```

**En Linux / macOS:**
```bash
source .venv/bin/activate
```

*(El prompt de tu terminal mostrará `(.venv)` indicando que el entorno está activo).*

### 1.3. Instalar Dependencias

Con el entorno virtual activado, actualiza `pip` e instala las dependencias fijadas en `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Estructura del Repositorio

El proyecto se encuentra organizado modularmente respetando los estándares de la cátedra:

```text
ejercicios_resueltos/
├── .gitignore
├── requirements.txt
├── README.md
├── clase_1/
│   ├── __init__.py
│   ├── parte_a_tipos.py            # Ejercicios A1 a A7 (Tipos, variables y operaciones)
│   ├── parte_b_listas.py           # Ejercicios B1 a B8 (Listas, slicing, ordenamiento)
│   ├── parte_c_dicts.py            # Ejercicios C1 a C8 (Diccionarios y JSON prep)
│   ├── parte_d_funciones.py        # Ejercicios D1 a D6 (Funciones y reutilización)
│   ├── parte_e_archivos.py         # Ejercicios E1 a E5 (Procesamiento de archivos CSV)
│   ├── parte_h_mini_proyecto.py    # Ejercicios H1 y H2 (Mini-proyecto integrador)
│   └── tests/
│       ├── __init__.py
│       ├── test_funciones.py       # Tests unitarios Parte D y G (pytest)
│       └── test_mini_proyecto.py   # Tests unitarios para el mini-proyecto
└── clase_2/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   ├── main.py                 # Instancia de FastAPI, configuración y endpoints raíz
    │   ├── models.py               # Modelos Pydantic v2 (Libro, Autor, Editorial)
    │   └── routers/
    │       ├── __init__.py
    │       └── libros.py           # Endpoints CRUD para gestión de libros
    ├── cliente/
    │   ├── __init__.py
    │   └── cliente_api.py          # Cliente HTTP con requests.Session, timeout y manejo de errores
    ├── docs/
    │   └── mqtt-notas.md           # Respuestas y análisis conceptual de MQTT (Parte D)
    └── tests/
        ├── __init__.py
        ├── test_api_libros.py      # Tests de integración API con TestClient y HTTPX
        └── test_cliente.py         # Tests unitarios del cliente HTTP
```

---

## 3. Ejecución de Tests con `pytest`

Todos los tests automáticos están escritos con `pytest` y no requieren levantar servidores externos.

### 3.1. Ejecutar todos los tests de la suite
```bash
pytest
```

### 3.2. Ejecutar tests de una clase específica con detalle (`-v`)
```bash
# Tests de la Clase 1
pytest clase_1/tests/ -v

# Tests de la Clase 2
pytest clase_2/tests/ -v
```

### 3.3. Ejecutar un archivo de tests puntual
```bash
pytest clase_1/tests/test_funciones.py -v
pytest clase_2/tests/test_api_libros.py -v
```

---

## 4. Ejecución de la API y el Cliente (Clase 2)

### 4.1. Levantar el servidor FastAPI
Desde la raíz del proyecto con el entorno virtual activo:

```bash
uvicorn clase_2.api.main:app --reload --port 8000
```

- Documentación interactiva Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Documentación alternativa ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 4.2. Ejecutar el Cliente HTTP de Prueba
En otra terminal (con `.venv` activado):

```bash
python -m clase_2.cliente.cliente_api
```

---

## 5. Convención de Git, Ramas y Pull Requests (Requisito de Cátedra)

De acuerdo con las consignas oficiales de la cátedra:

1. **Nombre del Repositorio Individual en GitHub:**
   - Formato: `IC-IC2-apellido-fecha_de_la_practica` con la fecha en formato `AAAA-MM-DD`.
   - Ejemplo: `IC-IC2-perez-2026-08-03`.

2. **Flujo de Trabajo obligatorio (Ramas y PRs):**
   - **Un Pull Request por cada Parte** de la guía (ej. `feature/clase1-parte-a`, `feature/clase1-parte-b`, `feature/clase2-parte-b`, etc.).
   - No se permiten PRs gigantes con todo el trabajo junto ni un PR por cada micro-ejercicio suelto.
   - Cada PR se revisa y se **mergea a `main` directamente desde la interfaz web de GitHub** (botón *Merge pull request*).
   - **IMPORTANTE:** Un commit directo a `main` sin pasar por su respectivo Pull Request **no se considera entregado**.
