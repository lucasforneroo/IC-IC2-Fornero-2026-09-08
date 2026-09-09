from fastapi import FastAPI
from clase_2.api.routers.libros import router as libros_router
from clase_2.api.routers.autores import router as autores_router

app = FastAPI(
    title="API de Libros y Autores — IC2",
    description=(
        "API REST desarrollada para la práctica de la Clase 2 de Ingeniería en Computación 2. "
        "Demuestra contratos de datos, validación con Pydantic, códigos de estado HTTP y "
        "arquitectura modular."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Inclusión de routers modulares
app.include_router(libros_router)
app.include_router(autores_router)


@app.get(
    "/",
    tags=["General"],
    summary="Endpoint de bienvenida y verificación de estado (Health Check)",
)
def root():
    """Endpoint raíz que saluda al cliente (Ejercicio B1)."""
    return {"mensaje": "hola"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("clase_2.api.main:app", host="127.0.0.1", port=8000, reload=True)
