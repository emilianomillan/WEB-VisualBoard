# 📚 Instrucciones de Despliegue - Visual Board

## 🚀 Despliegue Frontend en GitHub Pages

### Prerequisitos
- Cuenta de GitHub
- Repositorio creado en GitHub
- Node.js y npm instalados

### Pasos para el Despliegue

#### 1. Configurar tu nombre de usuario de GitHub
Edita el archivo `frontend/package.json` y reemplaza `YOUR_GITHUB_USERNAME` con tu usuario real de GitHub:

```json
"homepage": "https://TU_USUARIO_GITHUB.github.io/Web-VisualBoard",
```

#### 2. Inicializar repositorio Git (si no existe)
```bash
git init
git add .
git commit -m "Initial commit"
```

#### 3. Agregar el repositorio remoto
```bash
git remote add origin https://github.com/TU_USUARIO/Web-VisualBoard.git
```

#### 4. Construir y desplegar a GitHub Pages
```bash
cd frontend
npm run deploy
```

Este comando:
1. Construirá el proyecto (`npm run build`)
2. Creará una rama `gh-pages`
3. Subirá los archivos construidos a esa rama
4. GitHub Pages servirá automáticamente el sitio

#### 5. Configurar GitHub Pages
1. Ve a tu repositorio en GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: gh-pages
5. Folder: / (root)
6. Click Save

#### 6. Esperar el despliegue
- GitHub Pages puede tardar hasta 10 minutos en activarse
- Tu sitio estará disponible en: `https://TU_USUARIO.github.io/Web-VisualBoard`

### 🔄 Actualizaciones Automáticas con GitHub Actions

El proyecto incluye un workflow que desplegará automáticamente cuando hagas push a la rama `main`:

```bash
git add .
git commit -m "Update site"
git push origin main
```

## 🌐 Despliegue del Backend

### Opción 1: Render.com (Gratis)

1. Crea cuenta en [render.com](https://render.com)
2. Nuevo Web Service → Connect GitHub
3. Selecciona tu repositorio
4. Configuración:
   - Name: `visual-board-backend`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3
5. Variables de entorno:
   ```
   DATABASE_URL=tu_url_postgresql
   UNSPLASH_API_KEY=tu_api_key
   ```

### Opción 2: Railway.app

1. Crea cuenta en [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Selecciona tu repositorio
4. Railway detectará automáticamente el proyecto Python
5. Agrega PostgreSQL como servicio
6. Las variables se configuran automáticamente

### Opción 3: Heroku (Pago)

1. Instala Heroku CLI
2. Crea archivo `backend/Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Comandos:
   ```bash
   cd backend
   heroku create visual-board-backend
   heroku addons:create heroku-postgresql:mini
   heroku config:set UNSPLASH_API_KEY=tu_api_key
   git push heroku main
   ```

## 🔧 Configuración Final

### Actualizar URL del Backend en Frontend

Una vez desplegado el backend, actualiza `frontend/src/config/api.js`:

```javascript
export const API_BASE_URL = isDevelopment 
  ? 'http://localhost:8000' 
  : 'https://tu-backend-url.onrender.com' // Tu URL real del backend
```

### Variables de Entorno del Backend

Asegúrate de configurar estas variables en tu servicio de hosting:

```env
DATABASE_URL=postgresql://usuario:password@host/database
UNSPLASH_API_KEY=tu_api_key_de_unsplash
SECRET_KEY=una_clave_secreta_aleatoria
DEBUG=False
```

## 🔍 Verificación

### Frontend
- Visita: `https://TU_USUARIO.github.io/Web-VisualBoard`
- Verifica que la página carga correctamente
- Las imágenes y estilos deben verse bien

### Backend
- Visita: `https://tu-backend.onrender.com/health`
- Deberías ver la respuesta del health check
- Prueba: `https://tu-backend.onrender.com/docs` para ver la documentación Swagger

## 🐛 Solución de Problemas

### Error 404 en GitHub Pages
- Verifica que la rama `gh-pages` existe
- Asegúrate de que GitHub Pages está configurado correctamente
- Espera 10 minutos para la propagación

### CORS Errors
- Actualiza los orígenes permitidos en `backend/main.py`:
  ```python
  allow_origins=[
      "https://TU_USUARIO.github.io",
      "http://localhost:5173"
  ]
  ```

### Base de Datos
- Asegúrate de que PostgreSQL está accesible
- Verifica las credenciales en DATABASE_URL
- Ejecuta las migraciones si es necesario

## 📝 Notas Importantes

1. **API Keys**: Nunca subas API keys a GitHub
2. **HTTPS**: GitHub Pages usa HTTPS, tu backend también debe usarlo
3. **Caché**: Limpia el caché del navegador si no ves cambios
4. **Dominios**: Puedes configurar un dominio personalizado en GitHub Pages

## 🎉 ¡Listo!

Tu aplicación Visual Board ahora está desplegada y accesible públicamente.

Para actualizaciones futuras:
1. Haz cambios localmente
2. Prueba en desarrollo
3. Commit y push a GitHub
4. GitHub Actions desplegará automáticamente