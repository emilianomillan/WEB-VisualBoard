# 🔗 Configuración de Conexión con Render

## Necesito que ejecutes estos pasos:

### 1. Obtén tu URL de PostgreSQL de Render
En tu dashboard de Render, busca tu base de datos "Clasesona" y copia:
- **Internal Database URL** o **External Database URL**

### 2. Obtén la URL de tu Web Service
En tu servicio web de Render, copia la URL pública (ejemplo: https://mi-app.onrender.com)

### 3. Proporciona estas URLs:

```bash
# URL de PostgreSQL (ejemplo):
postgresql://usuario:password@dpg-xxx.render.com/clasesona

# URL del Web Service (ejemplo):
https://mi-servicio.onrender.com
```

### 4. Una vez que tengas las URLs, ejecutaré:

1. **Migrar la base de datos:**
```bash
./migrate_to_render.sh "TU_URL_POSTGRESQL"
```

2. **Actualizar el frontend con la URL del backend**
3. **Redesplegar a GitHub Pages**

## 📝 Datos que se migrarán:
- 8 posts existentes
- 2 usuarios registrados
- Todas las imágenes y configuraciones

---

**Por favor proporciona:**
1. URL de PostgreSQL de Render (Clasesona)
2. URL del servicio web en Render