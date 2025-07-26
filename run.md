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