# 🎲 MesaMaestra - Grupo 11

**MesaMaestra** es una aplicación web diseñada para gestionar campañas de juegos de rol, TTRPG y juegos de mesa. Desarrollada como proyecto final para la asignatura de **Integración de Tecnologías** (Curso 2025/2026).

Este proyecto permite a las personas que dirigen partidas (Directores de Juego) y a los jugadores centralizar toda la información de sus campañas: desde la creación de hojas de personaje hasta la planificación de sesiones y almacenamiento de recursos, integrando además un bestiario en tiempo real consumiendo una API externa.

## 🛠️ Tecnologías utilizadas
El proyecto es una aplicación web "production-ready" construida con:
- **Backend:** Django (Python)
- **Base de Datos:** PostgreSQL
- **Infraestructura y Despliegue:** Docker Compose, Gunicorn y Nginx
- **API Externa:** Consumo de la API pública de Open5e

## ✨ Funcionalidades principales
- **Gestión de Campañas:** Creación, edición y control de visibilidad (Pública/Privada) con sistema de etiquetas.
- **Personajes y Participación:** Creación de personajes vinculados a los usuarios y asociados a las campañas.
- **Sesiones y Recursos:** Planificación de sesiones de juego y subida de archivos/enlaces útiles para la aventura.
- **Bestiario (API):** Buscador de criaturas integrado para la consulta rápida de atributos.
- **Autenticación y Permisos:** Sistema robusto de roles donde solo los creadores o directores autorizados pueden modificar los datos.

## 👥 Equipo de Desarrollo
El trabajo se ha repartido de forma funcional y equilibrada:
* **Mery:** Campañas, Etiquetas, Autenticación y configuración base estable.
* **Nuria:** Personajes, Participación y modelado de base de datos (ER).
* **Carlos:** Sesiones, Recursos y manual de usuario.
* **Guillermo:** Integración de API externa (Open5e) e infraestructura Docker.

## 🚀 Cómo desplegar en local (Entorno Docker)

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/nmirgar/IT-MesaMaestra-Grupo11.git](https://github.com/nmirgar/IT-MesaMaestra-Grupo11.git)
   cd IT-MesaMaestra-Grupo11

https://drive.google.com/drive/folders/1YQon-_bKQGhhANrP_aGzbzbyTs4yJTDX?usp=sharing
