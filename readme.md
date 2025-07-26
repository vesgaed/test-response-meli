# Desafío Técnico - Prototipo de Página de Producto

Este repositorio contiene la solución al desafío técnico, que consiste en un prototipo funcional de una página de detalle de producto inspirada en Mercado Libre, junto con su API de soporte y un frontend interactivo.

## ✨ Características Principales

* **API Backend Robusta:** Construida con FastAPI, sirviendo datos de productos desde archivos JSON locales.
* **Frontend Renderizado en Servidor:** Un frontend ligero construido también con FastAPI y plantillas Jinja2, demostrando la capacidad de crear interfaces de usuario funcionales enteramente en Python.
* **Listado y Filtrado de Productos:** La página principal permite visualizar todos los productos y filtrarlos dinámicamente por categoría y marca.
* **Recomendaciones con IA:** La página de detalle de un producto incluye una sección de "productos relacionados" generada por un modelo de similitud de contenido (TF-IDF y Similitud de Coseno).
* **Arquitectura de Microservicios:** La solución está completamente containerizada con Docker y orquestada con Docker Compose, separando el backend y el frontend en servicios independientes.
* **Enfoque en Calidad:** El código del backend cuenta con una suite de pruebas unitarias y de integración con una cobertura superior al 90%.

## 🛠️ Stack Tecnológico

* **Backend:** Python, FastAPI, Pandas, Scikit-learn.
* **Frontend:** Python, FastAPI, Jinja2, HTML5, CSS3.
* **Infraestructura:** Docker, Docker Compose.
* **Pruebas:** Pytest, pytest-cov.

## 🚀 Cómo Empezar

Para instrucciones detalladas sobre cómo ejecutar el proyecto, por favor consulta el archivo **[run.md](run.md)**.

## 📄 Documentación Técnica

Para una explicación detallada de la arquitectura, las decisiones de diseño y los desafíos técnicos abordados, consulta el **[design_document.md](design_document.md)**.