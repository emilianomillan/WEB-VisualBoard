# ✅ Checklist de Verificación del Proyecto
## Segundo Proyecto Integrador — COM-11117
### David Fernando Avila Díaz | 197851

---

> **Instrucciones:** Revisa cada punto marcando con ✅ cuando esté completado y funcionando.
> Si un punto falla, márcalo con ❌ y corrígelo antes de entregar.
> 
> **Meta:** Todos los puntos deben estar en ✅ para garantizar el 10.

---

## 📋 ÍNDICE

1. [Frontend - Interfaz General](#1-frontend---interfaz-general)
2. [Frontend - Mosaico de Posts](#2-frontend---mosaico-de-posts)
3. [Frontend - Formularios CRUD](#3-frontend---formularios-crud)
4. [Frontend - Sección Descubrimiento](#4-frontend---sección-descubrimiento)
5. [Frontend - Sistema de Usuario](#5-frontend---sistema-de-usuario)
6. [Frontend - Caché y localStorage](#6-frontend---caché-y-localstorage)
7. [Frontend - Paginación](#7-frontend---paginación)
8. [Frontend - React y Hooks](#8-frontend---react-y-hooks)
9. [Frontend - OpenGraph](#9-frontend---opengraph)
10. [Backend - Endpoints CRUD](#10-backend---endpoints-crud)
11. [Backend - Paginación](#11-backend---paginación)
12. [Backend - Validación de Usuario](#12-backend---validación-de-usuario)
13. [Backend - Integración Unsplash](#13-backend---integración-unsplash)
14. [Backend - Health Endpoint](#14-backend---health-endpoint)
15. [Backend - Base de Datos](#15-backend---base-de-datos)
16. [Diseño Responsivo](#16-diseño-responsivo)
17. [Pruebas Unitarias](#17-pruebas-unitarias)
18. [Despliegue](#18-despliegue)
19. [Documentación README](#19-documentación-readme)
20. [Verificación Final](#20-verificación-final)

---

## 1. FRONTEND - INTERFAZ GENERAL

### 1.1 Diseño Visual
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 1.1.1 | La página tiene un diseño original (NO copia de Pinterest) | Visualmente diferente a Pinterest | ☐ |
| 1.1.2 | NO usa los colores de marca de Pinterest (rojo #E60023) | Revisar paleta de colores | ☐ |
| 1.1.3 | El diseño es visualmente consistente | Mismos estilos en toda la app | ☐ |
| 1.1.4 | Usa Bootstrap 5.3.8 | Verificar en package.json o CDN | ☐ |

**Cómo verificar 1.1.4:**
```bash
# En package.json debe aparecer:
"bootstrap": "^5.3.8"

# O en index.html el CDN:
# https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css
```

### 1.2 Estructura HTML Semántica
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 1.2.1 | Usa etiquetas semánticas de HTML5 | `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>`, `<article>` | ☐ |
| 1.2.2 | La estructura es correcta y tiene sentido | Header arriba, main en medio, footer abajo | ☐ |

---

## 2. FRONTEND - MOSAICO DE POSTS

### 2.1 Visualización del Mosaico
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 2.1.1 | Muestra un mosaico/grid de imágenes | Las imágenes se ven en formato grid/mosaico | ☐ |
| 2.1.2 | Cada post muestra la imagen | La imagen es visible | ☐ |
| 2.1.3 | Cada post muestra el usuario creador | Se ve quién lo creó | ☐ |
| 2.1.4 | Cada post muestra la fecha de alta | Se ve cuándo se creó | ☐ |
| 2.1.5 | Cada post muestra las etiquetas | Se ven los tags/etiquetas | ☐ |

### 2.2 Interacción con Posts
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 2.2.1 | Se puede hacer clic en un post para ver detalle | Navega o abre modal con info completa | ☐ |
| 2.2.2 | El detalle muestra toda la información del post | ID, usuario, imagen, fecha, etiquetas | ☐ |

---

## 3. FRONTEND - FORMULARIOS CRUD

### 3.1 Formulario de ALTA (Crear Post)
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 3.1.1 | Existe un formulario para crear posts | Hay botón/link que abre el formulario | ☐ |
| 3.1.2 | Campo: Usuario | Input para el nombre de usuario | ☐ |
| 3.1.3 | Campo: Link a imagen | Input para URL de la imagen | ☐ |
| 3.1.4 | Campo: Fecha de alta | Se captura automática o manualmente | ☐ |
| 3.1.5 | Campo: Etiquetas | Input para tags (puede ser múltiple) | ☐ |
| 3.1.6 | Botón de enviar | Botón que ejecuta POST a la API | ☐ |
| 3.1.7 | Validación de campos | No permite enviar si faltan campos requeridos | ☐ |
| 3.1.8 | Feedback al usuario | Muestra mensaje de éxito o error | ☐ |
| 3.1.9 | Actualiza la lista | Después de crear, el nuevo post aparece | ☐ |

**Cómo verificar 3.1.6:**
```javascript
// El formulario debe hacer algo como:
fetch('/api/posts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-User-Id': usuario  // Del sessionStorage
  },
  body: JSON.stringify({ usuario, imagen, etiquetas })
})
```

### 3.2 Formulario de EDICIÓN (Modificar Post - PATCH)
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 3.2.1 | Existe opción para editar un post | Botón/icono de editar visible | ☐ |
| 3.2.2 | Solo aparece si el usuario es el creador | Verificar con diferentes usuarios | ☐ |
| 3.2.3 | El formulario carga los datos actuales | Los campos vienen pre-llenados | ☐ |
| 3.2.4 | Permite modificar campos individuales | No requiere todos los campos | ☐ |
| 3.2.5 | Ejecuta PATCH a la API | Network tab muestra método PATCH | ☐ |
| 3.2.6 | Actualiza la vista después de editar | Los cambios se reflejan inmediatamente | ☐ |

### 3.3 Formulario de REEMPLAZO (PUT)
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 3.3.1 | Existe opción para reemplazar completamente | Puede ser el mismo form de editar o separado | ☐ |
| 3.3.2 | Requiere TODOS los campos | Validación de campos completos | ☐ |
| 3.3.3 | Ejecuta PUT a la API | Network tab muestra método PUT | ☐ |
| 3.3.4 | Solo el creador puede reemplazar | Validación de usuario | ☐ |

### 3.4 Función de ELIMINAR (DELETE)
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 3.4.1 | Existe opción para eliminar un post | Botón/icono de eliminar visible | ☐ |
| 3.4.2 | Solo aparece si el usuario es el creador | Verificar con diferentes usuarios | ☐ |
| 3.4.3 | Pide confirmación antes de eliminar | Modal o alert de confirmación | ☐ |
| 3.4.4 | Ejecuta DELETE a la API | Network tab muestra método DELETE | ☐ |
| 3.4.5 | Elimina el post de la vista | El post desaparece sin recargar | ☐ |

---

## 4. FRONTEND - SECCIÓN DESCUBRIMIENTO

### 4.1 Apartado de Descubrimiento
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 4.1.1 | Existe una sección/página de "Descubrimiento" | Link o tab visible en navegación | ☐ |
| 4.1.2 | Muestra imágenes aleatorias | Las imágenes cambian/son variadas | ☐ |
| 4.1.3 | Las imágenes vienen de Unsplash | Verificar en Network tab | ☐ |
| 4.1.4 | La llamada es a TU API, no directo a Unsplash | URL debe ser tu backend, ej: `/api/discover` | ☐ |
| 4.1.5 | Los datos están transformados | No viene toda la respuesta de Unsplash, solo lo necesario | ☐ |

**Cómo verificar 4.1.5:**
```javascript
// La respuesta de tu API debe verse algo así (simplificado):
{
  "images": [
    {
      "id": "abc123",
      "url": "https://images.unsplash.com/...",
      "description": "Una foto bonita",
      "author": "Fotógrafo"
    }
  ]
}

// NO debe incluir todos los campos que Unsplash envía (son muchísimos)
```

---

## 5. FRONTEND - SISTEMA DE USUARIO

### 5.1 Identificación de Usuario
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 5.1.1 | Existe formulario para ingresar/registrar usuario | Input visible al inicio o en header | ☐ |
| 5.1.2 | El usuario se guarda en sessionStorage | Verificar en DevTools > Application > Session Storage | ☐ |
| 5.1.3 | El usuario persiste durante la sesión | Navegar entre páginas y verificar que sigue | ☐ |
| 5.1.4 | Se puede cambiar de usuario | Hay opción de logout o cambiar | ☐ |
| 5.1.5 | El usuario se envía en header en cada petición | Network tab: header `X-User-Id` presente | ☐ |

**Cómo verificar 5.1.2:**
```javascript
// En DevTools > Console:
sessionStorage.getItem('userId')  // Debe retornar el usuario actual
```

**Cómo verificar 5.1.5:**
```
// En DevTools > Network > cualquier petición a tu API:
// Request Headers debe incluir:
X-User-Id: nombreDelUsuario
```

### 5.2 Permisos basados en Usuario
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 5.2.1 | Usuario A no puede editar posts de Usuario B | Probar con 2 usuarios diferentes | ☐ |
| 5.2.2 | Usuario A no puede eliminar posts de Usuario B | Probar con 2 usuarios diferentes | ☐ |
| 5.2.3 | Los botones editar/eliminar solo aparecen en posts propios | Verificar visualmente | ☐ |

---

## 6. FRONTEND - CACHÉ Y LOCALSTORAGE

### 6.1 Sistema de Caché
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 6.1.1 | Primera carga: datos se guardan en localStorage | DevTools > Application > Local Storage | ☐ |
| 6.1.2 | Se guarda el timestamp del consumo | Hay una key con la fecha/hora | ☐ |
| 6.1.3 | Segunda carga: verifica si hay datos en localStorage | Console.log o breakpoint | ☐ |
| 6.1.4 | Si hay datos, pasa parámetro de fecha mínima a la API | Network tab: query param con fecha | ☐ |
| 6.1.5 | Solo trae posts nuevos (después del timestamp) | La respuesta es menor o vacía si no hay nuevos | ☐ |

**Cómo verificar 6.1.1 y 6.1.2:**
```javascript
// En DevTools > Console después de cargar la página:
localStorage.getItem('posts')      // Debe tener los posts
localStorage.getItem('timestamp')  // Debe tener fecha/hora
```

**Cómo verificar 6.1.4:**
```
// En Network tab, la segunda llamada debe verse algo como:
GET /api/posts?since=2025-01-15T10:30:00Z
// o
GET /api/posts?min_date=2025-01-15T10:30:00Z
```

### 6.2 Lógica de Actualización
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 6.2.1 | Los posts nuevos se agregan a los existentes | No se pierden los anteriores | ☐ |
| 6.2.2 | El timestamp se actualiza después de cada fetch | Verificar que cambia la fecha | ☐ |

---

## 7. FRONTEND - PAGINACIÓN

### 7.1 Paginación del Cliente
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 7.1.1 | Los posts se muestran paginados | No aparecen todos de golpe | ☐ |
| 7.1.2 | Hay controles de paginación | Botones "Anterior", "Siguiente" o números | ☐ |
| 7.1.3 | Se puede navegar entre páginas | Los botones funcionan | ☐ |
| 7.1.4 | Se indica la página actual | Número de página visible o resaltado | ☐ |
| 7.1.5 | La paginación es del lado del cliente | Los datos ya están cargados, solo cambia la vista | ☐ |

---

## 8. FRONTEND - REACT Y HOOKS

### 8.1 Uso de React
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 8.1.1 | El proyecto usa React | Verificar package.json | ☐ |
| 8.1.2 | El proyecto fue creado con Vite | Verificar vite.config.js existe | ☐ |
| 8.1.3 | Hay componentes reutilizables | Archivos .jsx en carpeta components | ☐ |

### 8.2 Uso de Hooks
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 8.2.1 | Usa useState para manejo de estado | Buscar `useState` en el código | ☐ |
| 8.2.2 | Usa useEffect para efectos secundarios | Buscar `useEffect` en el código | ☐ |
| 8.2.3 | Los hooks se usan correctamente | No están dentro de condicionales o loops | ☐ |

**Cómo verificar 8.2.1 y 8.2.2:**
```bash
# En terminal, dentro de la carpeta frontend/src:
grep -r "useState" .
grep -r "useEffect" .
```

### 8.3 Funciones
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 8.3.1 | Hay funciones para las operaciones CRUD | fetchPosts, createPost, updatePost, deletePost | ☐ |
| 8.3.2 | Las funciones usan fetch o axios | Verificar llamadas HTTP | ☐ |

---

## 9. FRONTEND - OPENGRAPH

### 9.1 Meta Tags OpenGraph
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 9.1.1 | Existe `og:title` | En index.html dentro de `<head>` | ☐ |
| 9.1.2 | Existe `og:description` | En index.html dentro de `<head>` | ☐ |
| 9.1.3 | Existe `og:image` | URL de imagen principal | ☐ |
| 9.1.4 | Existe `og:url` | URL de tu página desplegada | ☐ |
| 9.1.5 | Existe `og:type` | Generalmente "website" | ☐ |

**Cómo verificar - El archivo index.html debe contener:**
```html
<head>
  <!-- ... otros meta tags ... -->
  <meta property="og:title" content="Visual Board - Tu título" />
  <meta property="og:description" content="Descripción de tu proyecto" />
  <meta property="og:image" content="https://tu-dominio.com/imagen-preview.png" />
  <meta property="og:url" content="https://tu-dominio.com" />
  <meta property="og:type" content="website" />
</head>
```

### 9.2 Verificación de OpenGraph
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 9.2.1 | Se ve correctamente al compartir en WhatsApp | Enviar link por WhatsApp y ver preview | ☐ |
| 9.2.2 | Se ve correctamente en Facebook/Twitter | Usar debugger de cada red social | ☐ |

**Herramientas para verificar:**
- Facebook: https://developers.facebook.com/tools/debug/
- Twitter: https://cards-dev.twitter.com/validator
- LinkedIn: https://www.linkedin.com/post-inspector/

---

## 10. BACKEND - ENDPOINTS CRUD

### 10.1 GET - Listar Posts (con paginación)
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 10.1.1 | Endpoint `GET /api/posts` existe | Probar en Postman o navegador | ☐ |
| 10.1.2 | Retorna lista de posts | JSON con array de posts | ☐ |
| 10.1.3 | Soporta paginación | Parámetros `page` y `limit` o `skip` | ☐ |
| 10.1.4 | Retorna metadatos de paginación | Total de registros, página actual, etc. | ☐ |
| 10.1.5 | Soporta filtro por fecha mínima | Parámetro `since` o `min_date` | ☐ |

**Ejemplo de respuesta correcta:**
```json
{
  "data": [
    {
      "id": 1,
      "usuario": "david",
      "imagen": "https://...",
      "fecha_alta": "2025-01-15T10:30:00Z",
      "etiquetas": ["naturaleza", "paisaje"]
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 10,
  "pages": 5
}
```

### 10.2 GET - Obtener Post por ID
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 10.2.1 | Endpoint `GET /api/posts/{id}` existe | Probar con un ID válido | ☐ |
| 10.2.2 | Retorna el post completo | Todos los campos del post | ☐ |
| 10.2.3 | Retorna 404 si no existe | Probar con ID inexistente | ☐ |

### 10.3 POST - Crear Post
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 10.3.1 | Endpoint `POST /api/posts` existe | Probar en Postman | ☐ |
| 10.3.2 | Acepta JSON con los campos requeridos | usuario, imagen, etiquetas | ☐ |
| 10.3.3 | Valida campos requeridos | Retorna error si faltan campos | ☐ |
| 10.3.4 | Guarda en base de datos | Verificar en BD | ☐ |
| 10.3.5 | Retorna el post creado con ID | JSON con el nuevo post | ☐ |
| 10.3.6 | Asigna fecha_alta automáticamente | No requiere enviarla | ☐ |

### 10.4 PATCH - Modificar Post
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 10.4.1 | Endpoint `PATCH /api/posts/{id}` existe | Probar en Postman | ☐ |
| 10.4.2 | Permite actualización parcial | Solo enviar campos a modificar | ☐ |
| 10.4.3 | Valida que el usuario sea el creador | Header X-User-Id vs usuario del post | ☐ |
| 10.4.4 | Retorna 403 si no es el creador | Probar con otro usuario | ☐ |
| 10.4.5 | Retorna el post actualizado | JSON con cambios aplicados | ☐ |

### 10.5 PUT - Reemplazar Post
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 10.5.1 | Endpoint `PUT /api/posts/{id}` existe | Probar en Postman | ☐ |
| 10.5.2 | Requiere TODOS los campos | Error si falta alguno | ☐ |
| 10.5.3 | Valida que el usuario sea el creador | Header X-User-Id vs usuario del post | ☐ |
| 10.5.4 | Retorna 403 si no es el creador | Probar con otro usuario | ☐ |
| 10.5.5 | Retorna el post reemplazado | JSON completo | ☐ |

### 10.6 DELETE - Eliminar Post
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 10.6.1 | Endpoint `DELETE /api/posts/{id}` existe | Probar en Postman | ☐ |
| 10.6.2 | Valida que el usuario sea el creador | Header X-User-Id vs usuario del post | ☐ |
| 10.6.3 | Retorna 403 si no es el creador | Probar con otro usuario | ☐ |
| 10.6.4 | Elimina de la base de datos | Verificar que ya no existe | ☐ |
| 10.6.5 | Retorna confirmación o 204 | Mensaje de éxito o No Content | ☐ |

---

## 11. BACKEND - PAGINACIÓN

### 11.1 Implementación de Paginación
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 11.1.1 | Acepta parámetro de página | `?page=1` o `?skip=0` | ☐ |
| 11.1.2 | Acepta parámetro de límite | `?limit=10` o `?take=10` | ☐ |
| 11.1.3 | Tiene valores por defecto | Si no se envían, usa defaults | ☐ |
| 11.1.4 | Retorna solo los registros de esa página | No todos los registros | ☐ |

**Ejemplos de llamadas:**
```
GET /api/posts?page=1&limit=10  → Primeros 10
GET /api/posts?page=2&limit=10  → Del 11 al 20
GET /api/posts?page=1&limit=10&since=2025-01-15T00:00:00Z → Con filtro de fecha
```

---

## 12. BACKEND - VALIDACIÓN DE USUARIO

### 12.1 Header de Usuario
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 12.1.1 | Lee header `X-User-Id` en cada petición | Verificar en código del backend | ☐ |
| 12.1.2 | Usa el header para filtrar/validar | En POST guarda como creador, en PUT/PATCH/DELETE valida | ☐ |

### 12.2 Validación en Modificaciones
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 12.2.1 | PATCH verifica X-User-Id == post.usuario | Código del endpoint | ☐ |
| 12.2.2 | PUT verifica X-User-Id == post.usuario | Código del endpoint | ☐ |
| 12.2.3 | DELETE verifica X-User-Id == post.usuario | Código del endpoint | ☐ |
| 12.2.4 | Retorna 403 Forbidden si no coincide | Status code correcto | ☐ |

**Ejemplo de validación en FastAPI:**
```python
@app.patch("/api/posts/{post_id}")
async def update_post(post_id: int, data: PostUpdate, x_user_id: str = Header(...)):
    post = get_post(post_id)
    if post.usuario != x_user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este post")
    # ... continuar con la actualización
```

---

## 13. BACKEND - INTEGRACIÓN UNSPLASH

### 13.1 Endpoint de Descubrimiento
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 13.1.1 | Endpoint `GET /api/discover` existe | Probar en Postman | ☐ |
| 13.1.2 | Hace llamada a Unsplash desde el backend | NO desde el frontend | ☐ |
| 13.1.3 | Usa la API de Unsplash list-photos | https://unsplash.com/documentation#list-photos | ☐ |
| 13.1.4 | Transforma la respuesta | No devuelve TODO lo de Unsplash | ☐ |
| 13.1.5 | Solo retorna campos necesarios para render | id, url, description, author (mínimo) | ☐ |

**Ejemplo de transformación correcta:**
```python
# Respuesta de Unsplash (simplificada, en realidad tiene ~50 campos por imagen):
unsplash_response = {
    "id": "abc123",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z",
    "width": 4000,
    "height": 3000,
    "color": "#ffffff",
    "blur_hash": "...",
    "downloads": 1000,
    "likes": 500,
    "urls": {
        "raw": "...",
        "full": "...",
        "regular": "...",
        "small": "...",
        "thumb": "..."
    },
    "user": {
        "id": "user123",
        "username": "photographer",
        "name": "John Doe",
        # ... muchos más campos
    }
    # ... muchos más campos
}

# Tu respuesta transformada (solo lo necesario):
tu_respuesta = {
    "id": "abc123",
    "url": "https://images.unsplash.com/.../regular",
    "description": "Beautiful landscape",
    "author": "John Doe"
}
```

---

## 14. BACKEND - HEALTH ENDPOINT

### 14.1 Health Check Principal
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 14.1.1 | Endpoint `GET /health` existe | Probar en navegador | ☐ |
| 14.1.2 | Retorna status del servidor | "status": "ok" o similar | ☐ |
| 14.1.3 | Verifica conexión a base de datos | "database": "connected" | ☐ |
| 14.1.4 | Verifica que Unsplash API está activa | "unsplash": "active" | ☐ |
| 14.1.5 | Retorna status general | Si todo ok = healthy, si algo falla = unhealthy | ☐ |

**Ejemplo de respuesta del health endpoint:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "services": {
    "database": {
      "status": "connected",
      "latency_ms": 5
    },
    "unsplash_api": {
      "status": "active",
      "latency_ms": 150
    }
  }
}
```

---

## 15. BACKEND - BASE DE DATOS

### 15.1 Modelo de Post
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 15.1.1 | Existe tabla/modelo para Posts | Verificar en modelos | ☐ |
| 15.1.2 | Campo: id (primary key) | Auto-generado | ☐ |
| 15.1.3 | Campo: usuario | String, quien creó el post | ☐ |
| 15.1.4 | Campo: imagen | String/URL del link a la imagen | ☐ |
| 15.1.5 | Campo: fecha_alta | DateTime, cuándo se creó | ☐ |
| 15.1.6 | Campo: etiquetas | Array de strings o relación | ☐ |

### 15.2 Conexión a PostgreSQL
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 15.2.1 | Usa PostgreSQL (no SQLite) | Verificar DATABASE_URL | ☐ |
| 15.2.2 | La conexión funciona | El servidor inicia sin errores | ☐ |
| 15.2.3 | Las migraciones están aplicadas | Tablas existen en la BD | ☐ |

---

## 16. DISEÑO RESPONSIVO

### 16.1 Adaptabilidad
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 16.1.1 | Se ve bien en desktop (>1200px) | Probar en pantalla grande | ☐ |
| 16.1.2 | Se ve bien en tablet (768px-1200px) | Usar DevTools responsive | ☐ |
| 16.1.3 | Se ve bien en móvil (<768px) | Usar DevTools responsive | ☐ |
| 16.1.4 | El mosaico se adapta | Cambia de columnas según tamaño | ☐ |
| 16.1.5 | La navegación se adapta | Menú hamburguesa en móvil | ☐ |
| 16.1.6 | Los formularios se adaptan | Inputs ocupan ancho apropiado | ☐ |
| 16.1.7 | Usa clases de Bootstrap responsive | col-sm, col-md, col-lg, etc. | ☐ |

**Cómo verificar:**
1. Abrir DevTools (F12)
2. Clic en icono de dispositivos móviles
3. Probar con diferentes tamaños

---

## 17. PRUEBAS UNITARIAS

### 17.1 Tests del Backend
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 17.1.1 | Existen archivos de pruebas | Carpeta `tests/` con archivos | ☐ |
| 17.1.2 | Usa pytest | En requirements.txt | ☐ |
| 17.1.3 | Tests para endpoint GET posts | test_get_posts | ☐ |
| 17.1.4 | Tests para endpoint POST posts | test_create_post | ☐ |
| 17.1.5 | Tests para validación de usuario | test_unauthorized_update | ☐ |
| 17.1.6 | Los tests pasan | `pytest` ejecuta sin errores | ☐ |

**Cómo verificar:**
```bash
cd backend
pytest -v
# Todos los tests deben pasar (verde)
```

---

## 18. DESPLIEGUE

### 18.1 Frontend Desplegado
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 18.1.1 | La página está en línea | URL accesible públicamente | ☐ |
| 18.1.2 | Se puede usar todas las funciones | CRUD funciona en producción | ☐ |
| 18.1.3 | Conecta al backend desplegado | No a localhost | ☐ |

### 18.2 Backend Desplegado
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 18.2.1 | La API está en línea | URL accesible públicamente | ☐ |
| 18.2.2 | Health endpoint funciona | `/health` responde correctamente | ☐ |
| 18.2.3 | Todos los endpoints funcionan | Probar CRUD en producción | ☐ |
| 18.2.4 | Base de datos en producción | PostgreSQL en la nube | ☐ |

---

## 19. DOCUMENTACIÓN README

### 19.1 Contenido Requerido
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 19.1.1 | Resumen del producto | Descripción clara del proyecto | ☐ |
| 19.1.2 | Instrucciones para levantar frontend | Paso a paso funcional | ☐ |
| 19.1.3 | Instrucciones para levantar backend | Paso a paso funcional | ☐ |
| 19.1.4 | requirements.txt mencionado/incluido | Archivo existe y está documentado | ☐ |
| 19.1.5 | Comando para levantar servidor | `uvicorn main:app --reload` o similar | ☐ |
| 19.1.6 | Enlace a página web desplegada | URL funcional | ☐ |
| 19.1.7 | Enlace a health endpoint | URL funcional | ☐ |
| 19.1.8 | Sección de autores | Con foto y nombre | ☐ |

### 19.2 Autores
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 19.2.1 | Foto de cada integrante | Imagen visible | ☐ |
| 19.2.2 | Nombre de pila de cada integrante | Texto con el nombre | ☐ |

---

## 20. VERIFICACIÓN FINAL

### 20.1 Flujo Completo de Usuario
| # | Requisito | Verificación | Estado |
|---|-----------|--------------|--------|
| 20.1.1 | Puedo ingresar mi nombre de usuario | Formulario funciona | ☐ |
| 20.1.2 | Puedo ver el mosaico de posts | Posts se cargan | ☐ |
| 20.1.3 | Puedo crear un nuevo post | Formulario y API funcionan | ☐ |
| 20.1.4 | El post aparece en el mosaico | Sin recargar la página | ☐ |
| 20.1.5 | Puedo ver el detalle de un post | Click funciona | ☐ |
| 20.1.6 | Puedo editar MI post | PATCH funciona | ☐ |
| 20.1.7 | NO puedo editar post de OTRO usuario | 403 o botón oculto | ☐ |
| 20.1.8 | Puedo eliminar MI post | DELETE funciona | ☐ |
| 20.1.9 | NO puedo eliminar post de OTRO usuario | 403 o botón oculto | ☐ |
| 20.1.10 | Puedo ver la sección Descubrimiento | Imágenes de Unsplash cargan | ☐ |
| 20.1.11 | Puedo navegar entre páginas | Paginación funciona | ☐ |
| 20.1.12 | Al recargar, los datos vienen del caché | localStorage se usa | ☐ |

### 20.2 Lista Final de URLs a Entregar
| # | Elemento | URL | Estado |
|---|----------|-----|--------|
| 20.2.1 | Repositorio GitHub | https://github.com/... | ☐ |
| 20.2.2 | Página web (frontend) | https://... | ☐ |
| 20.2.3 | Health endpoint (backend) | https://.../health | ☐ |

---

## 📊 RESUMEN DE PUNTOS

| Sección | Total Puntos | Completados |
|---------|--------------|-------------|
| 1. Frontend - Interfaz General | 6 | ☐/6 |
| 2. Frontend - Mosaico de Posts | 7 | ☐/7 |
| 3. Frontend - Formularios CRUD | 22 | ☐/22 |
| 4. Frontend - Sección Descubrimiento | 5 | ☐/5 |
| 5. Frontend - Sistema de Usuario | 8 | ☐/8 |
| 6. Frontend - Caché y localStorage | 7 | ☐/7 |
| 7. Frontend - Paginación | 5 | ☐/5 |
| 8. Frontend - React y Hooks | 8 | ☐/8 |
| 9. Frontend - OpenGraph | 7 | ☐/7 |
| 10. Backend - Endpoints CRUD | 24 | ☐/24 |
| 11. Backend - Paginación | 4 | ☐/4 |
| 12. Backend - Validación Usuario | 6 | ☐/6 |
| 13. Backend - Integración Unsplash | 5 | ☐/5 |
| 14. Backend - Health Endpoint | 5 | ☐/5 |
| 15. Backend - Base de Datos | 9 | ☐/9 |
| 16. Diseño Responsivo | 7 | ☐/7 |
| 17. Pruebas Unitarias | 6 | ☐/6 |
| 18. Despliegue | 7 | ☐/7 |
| 19. Documentación README | 10 | ☐/10 |
| 20. Verificación Final | 15 | ☐/15 |
| **TOTAL** | **163** | **☐/163** |

---

> **NOTA IMPORTANTE:** Este checklist cubre TODOS los requisitos mencionados en el documento
> "COM 11117 - Segundo proyecto integrador". Si todos los puntos están marcados con ✅,
> tu proyecto cumple al 100% con lo solicitado.
>
> **Última actualización:** Diciembre 2025
> **Basado en:** Documento oficial del proyecto - Otoño 2025

---

<div align="center">

### ¡Mucho éxito con tu proyecto, David! 🚀

</div>