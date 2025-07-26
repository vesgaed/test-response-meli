# Cómo Ejecutar el Proyecto

Esta guía explica cómo levantar la aplicación completa (backend y frontend) usando Docker.

## ✅ Prerrequisitos

* Tener instalado **Docker Desktop** (para Windows, Mac) o Docker Engine y Docker Compose (para Linux).

## 🚀 Instrucciones de Ejecución

1.  **Clonar el Repositorio**
    Abre una terminal y clona este repositorio en tu máquina local.

2.  **Navegar al Directorio Raíz**
    ```bash
    cd /ruta/a/la/carpeta/del/proyecto
    ```

3.  **Levantar los Contenedores**
    Ejecuta el siguiente comando. La primera vez puede tardar unos minutos mientras Docker descarga las imágenes base y construye los servicios.
    ```bash
    docker-compose up --build
    ```
    Este comando construirá las imágenes para el `backend` y el `frontend` y los iniciará. Verás los logs de ambos servicios en tu terminal.

## 🧪 Verificación

Una vez que los contenedores estén corriendo, puedes acceder a:

* **Frontend (Aplicación Web):** Abre tu navegador y ve a `http://localhost:8080`
* **Backend (Documentación de la API):** Para explorar la API directamente, ve a `http://localhost:8000/docs`

## 🛑 Cómo Detener la Aplicación

Para detener y eliminar los contenedores, presiona `Ctrl + C` en la terminal donde se está ejecutando `docker-compose`, y luego ejecuta:
```bash
docker-compose down
```

## ⚙️ Pruebas y Calidad del Código (Backend)

Para validar el correcto funcionamiento y la calidad del código del servicio backend, sigue estos pasos desde una nueva terminal.

### 1. Ejecutar la Suite de Pruebas

Este comando correrá todas las pruebas unitarias y de integración definidas para la API.

```bash
# 1. Navega al directorio del backend
cd backend/
```
# 2. Activa el entorno de Conda
```bash
conda activate meli_be
```
# 3. Ejecuta Pytest
```bash
pytest
```

Deberías ver una salida que indica que todas las pruebas se ejecutaron exitosamente.

### 2. Validar Cobertura de Código

Este comando no solo ejecuta las pruebas, sino que también genera un reporte que muestra qué porcentaje de tu código está cubierto por ellas.
```bash
pytest --cov=app
```

Para un análisis más detallado, puedes generar un reporte HTML interactivo:
```bash
pytest --cov=app --cov-report=html
```

Luego, abre el archivo htmlcov/index.html en tu navegador para ver el desglose completo.