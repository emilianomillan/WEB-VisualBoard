# WEB-VisualBoard
<div align="center">

# 📌 Visual Board

### Proyecto Integrador — COM-11117 Introducción al Desarrollo Web

[![ITAM](https://img.shields.io/badge/ITAM-Otoño%202025-00524E?style=for-the-badge)](https://www.itam.mx)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.8-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

---

**Aplicación web inspirada en Pinterest** para gestionar y descubrir contenido visual.  
Desarrollada como proyecto integrador del curso de Desarrollo Web.

[🚀 Ver Demo en Vivo](#) · [📡 API Health Check](#) · [📖 Documentación API](#)

</div>

---

## 📋 Tabla de Contenidos

- [Resumen del Proyecto](#-resumen-del-proyecto)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Instalación y Configuración](#-instalación-y-configuración)
  - [Requisitos Previos](#requisitos-previos)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [Variables de Entorno](#-variables-de-entorno)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Despliegue](#-despliegue)
- [Autores](#-autores)

---

## 🎯 Resumen del Proyecto

**Visual Board** es una aplicación web fullstack que replica la experiencia de Pinterest, permitiendo a los usuarios crear, explorar y gestionar colecciones de imágenes de manera intuitiva.

El proyecto integra conocimientos de:
- Desarrollo frontend con **React** y **Bootstrap**
- Desarrollo backend con **FastAPI** y **PostgreSQL**
- Consumo y transformación de APIs externas (**Unsplash**)
- Control de versiones colaborativo con **Git/GitHub**
- Despliegue de aplicaciones en la nube

---

## ✨ Características

### Frontend
- 🖼️ **Mosaico dinámico** de imágenes estilo Pinterest
- 📱 **Diseño responsivo** adaptable a móviles y escritorio
- 📝 **CRUD completo** para gestión de posts
- 🔍 **Sección Descubrimiento** con imágenes aleatorias de Unsplash
- 💾 **Caché inteligente** con localStorage y timestamps
- 📄 **Paginación** del lado del cliente
- 🔗 **OpenGraph** para compartir en redes sociales

### Backend
- ⚡ **API RESTful** con FastAPI
- 🔐 **Autenticación por headers** para identificación de usuarios
- 📊 **Paginación** en endpoints de listado
- 🔄 **Integración con Unsplash** (datos transformados)
- 🏥 **Health endpoint** con verificación de servicios externos
- 🧪 **Pruebas unitarias** con pytest
- 📚 **Documentación automática** con Swagger/OpenAPI

---

## 🛠️ Tecnologías

| Capa | Tecnología | Versión |
|------|------------|---------|
| **Frontend** | React + Vite | 18.x |
| **Estilos** | Bootstrap | 5.3.8 |
| **Backend** | FastAPI | 0.100+ |
| **Base de Datos** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | 2.x |
| **Testing** | pytest | 7.x |
| **API Externa** | Unsplash API | - |

---

## 🏗️ Arquitectura

```
visual-board/
├── frontend/                 # Aplicación React
│   ├── public/
│   ├── src/
│   │   ├── components/       # Componentes reutilizables
│   │   ├── pages/            # Vistas principales
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # Llamadas a API
│   │   └── utils/            # Funciones auxiliares
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── api/              # Endpoints
│   │   ├── models/           # Modelos SQLAlchemy
│   │   ├── schemas/          # Schemas Pydantic
│   │   ├── services/         # Lógica de negocio
│   │   └── core/             # Configuración
│   ├── tests/                # Pruebas unitarias
│   ├── requirements.txt
│   └── main.py
│
└── README.md
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Node.js** 18.x o superior
- **Python** 3.10 o superior
- **PostgreSQL** 15 o superior
- **Git**

---

### Frontend

1. **Navegar al directorio del frontend:**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con la URL de tu API
   ```

4. **Iniciar servidor de desarrollo:**
   ```bash
   npm run dev
   ```

5. **Acceder a la aplicación:**
   ```
   http://localhost:5173
   ```

#### Scripts disponibles

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Inicia servidor de desarrollo |
| `npm run build` | Genera build de producción |
| `npm run preview` | Previsualiza build de producción |
| `npm run lint` | Ejecuta linter |

---

### Backend

1. **Navegar al directorio del backend:**
   ```bash
   cd backend
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales
   ```

5. **Configurar base de datos:**
   ```bash
   # Crear base de datos en PostgreSQL
   createdb visual_board
   
   # Ejecutar migraciones (si aplica)
   alembic upgrade head
   ```

6. **Iniciar servidor:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

7. **Acceder a la documentación:**
   ```
   http://localhost:8000/docs      # Swagger UI
   http://localhost:8000/redoc     # ReDoc
   ```

#### Scripts disponibles

| Comando | Descripción |
|---------|-------------|
| `uvicorn main:app --reload` | Inicia servidor en modo desarrollo |
| `pytest` | Ejecuta pruebas unitarias |
| `pytest --cov` | Ejecuta pruebas con cobertura |

---

## 🔐 Variables de Entorno

### Frontend (`.env`)

```env
VITE_API_URL=http://localhost:8000
```

### Backend (`.env`)

```env
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/visual_board

# Unsplash API
UNSPLASH_ACCESS_KEY=tu_access_key_aqui

# Configuración
DEBUG=True
SECRET_KEY=tu_secret_key_aqui
```

---

## 📡 Endpoints de la API

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

### Headers requeridos

```http
X-User-Id: <identificador_usuario>
```

> ⚠️ Los endpoints de modificación (`PUT`, `PATCH`, `DELETE`) validan que el usuario sea el creador del post.

---

## ☁️ Despliegue

### Frontend
- **Plataforma:** GitHub Pages / Vercel / Netlify
- **URL:** [Pendiente de configurar]

### Backend
- **Plataforma:** Heroku / Railway / Azure
- **Health Check:** [Pendiente de configurar]

---

## 👨‍💻 Autores

<table>
  <tr>
    <td align="center">
      <img src="https://via.placeholder.com/150" width="150px;" alt="David Fernando Avila Díaz"/><br />
      <sub><b>David Fernando Avila Díaz</b></sub><br />
      <sub>197851</sub><br />
      <sub>Licenciatura en Ciencia de Datos</sub>
    </td>
    <!-- Agregar más integrantes aquí -->
  </tr>
</table>

---

<div align="center">

### Instituto Tecnológico Autónomo de México

**COM-11117 Introducción al Desarrollo Web**  
Otoño 2025

---

<sub>Hecho con ❤️ para el curso de Desarrollo Web</sub>

</div>