#   Pagina WEB: VisualBoard
<div align="center">

### Segundo Proyecto Integrador — COM-11117: Introducción al Desarrollo Web

[![ITAM](https://img.shields.io/badge/ITAM-Otoño%202025-00524E?style=for-the-badge)](https://www.itam.mx)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.8-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

---

**Visual Board** es una aplicación web inspirada en la experiencia de usuario de Pinterest. Su objetivo principal es permitir a los usuarios gestionar, compartir y descubrir imágenes en un contexto de red social.

El proyecto fue desarrollado en dos estructuras:

- **Backend (Python / FastAPI):** La API gestiona la lógica de negocio, la persistencia de datos en PostgreSQL y la integración con servicios externos.
- **Frontend (React):** Interfaz de usuario reactiva e interactiva, diseñada con Bootstrap para garantizar la adaptabilidad y responsabilidad en dispositivos móviles y de escritorio.

El sistema cuenta con tres módulos principales:
1. **Gestión de Contenido (CRUD):** Los usuarios pueden subir sus propias imágenes, editarlas y organizarlas mediante un sistema de etiquetado.
2. **Descubrimiento:** Integración con la API de Unsplash para ofrecer un feed infinito de imágenes.
3. **Optimización:** Implementación de caché local (`localStorage`) para mejorar la velocidad de carga y reducir el consumo de datos.

---

## ✨ Características

### Frontend
- **Mosaico dinámico** de imágenes estilo Pinterest
- **Diseño responsivo** adaptable a móviles y escritorio
- **CRUD completo** para gestión de posts
- **Sección Descubrimiento** con imágenes aleatorias de Unsplash
- **Caché** con localStorage y timestamps
- **OpenGraph** para compartir en redes sociales

### Backend
- **API** con FastAPI
- **Autenticación por headers** para identificación de usuarios
- **Integración con Unsplash** 

---

## Instalación y Configuración

### Requisitos Previos

- **Node.js** 18.x o superior
- **Python** 3.10 o superior
- **PostgreSQL** 15 o superior
- **Git**

---

### Frontend

1. **Navegar al directorio del frontend:**
   cd frontend

2. **Instalar dependencias:**
   npm install

3. **Configurar variables de entorno:**
   cp .env.example .env
   # Editar .env con la URL de la API

4. **Iniciar servidor de desarrollo:**
   npm run dev

5. **Acceder a la aplicación:**
   http://localhost:5173

---

### Backend

1. **Navegar al directorio del backend:**
   cd backend

2. **Crear y activar entorno virtual:**
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS
   source venv/bin/activate

3. **Instalar dependencias:**
   pip install -r requirements.txt

4. **Configurar variables de entorno:**
   cp .env.example .env
   # Editar .env con las credenciales

5. **Configurar base de datos:**
   # Crear base de datos en PostgreSQL
   createdb visual_board

6. **Iniciar servidor:**
   uvicorn main:app --reload --port 8000

7. **Acceder a la documentación:**
   http://localhost:8000/docs

---

## Endpoints de la API

### Posts

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/posts` | Listar posts (paginado) |
| `GET` | `/api/posts/{id}` | Obtener post por ID |
| `POST` | `/api/posts` | Crear nuevo post |
| `PUT` | `/api/posts/{id}` | Reemplazar post completo |
| `PATCH` | `/api/posts/{id}` | Actualizar post parcialmente |
| `DELETE` | `/api/posts/{id}` | Eliminar post |

### Descubrimiento

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/discover` | Obtener imágenes aleatorias de Unsplash |

### Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Estado del servidor y servicios externos |

---

## Enlaces del proyecto desplegado
El proyecto se encuentra desplegado y accesible públicamente en:

**https://dabtcavila.github.io/Web-VisualBoard/my-posts**

---

## Autores

<table>
  <tr>
    <td align="center">
      <img src="https://via.placeholder.com/150" width="150px;" alt="David Fernando Avila Díaz"/><br />
      <sub><b>David Fernando Avila Díaz</b></sub><br />
      <sub>197851</sub><br />
      <sub>Licenciatura en Ciencia de Datos</sub>
    </td>
    <td align="center">
      <img src="https://via.placeholder.com/150" width="150px;" alt="Emiliano Sebastián Millán Giffard"/><br />
      <sub><b>Emiliano Sebastián Millán Giffard</b></sub><br />
      <sub>214360</sub><br />
      <sub>Licenciatura en Ciencia de Datos</sub>
    </td>
  </tr>
</table>

---

<div align="center">

### Instituto Tecnológico Autónomo de México
