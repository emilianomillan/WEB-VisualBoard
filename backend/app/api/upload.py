from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from datetime import datetime
from typing import Optional
import shutil

router = APIRouter(prefix="/upload", tags=["upload"])

# Configuración
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Crear directorio si no existe
os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_file(file: UploadFile) -> None:
    """Valida el archivo subido"""
    # Verificar extensión
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Solo se permiten: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Verificar tamaño (aproximado)
    file.file.seek(0, 2)  # Ir al final del archivo
    file_size = file.file.tell()
    file.file.seek(0)  # Volver al inicio
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo es demasiado grande. Máximo {MAX_FILE_SIZE // (1024*1024)}MB"
        )


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """
    Sube una imagen al servidor y retorna la URL
    """
    try:
        # Validar archivo
        validate_file(file)
        
        # Generar nombre único
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Retornar URL relativa
        image_url = f"/api/upload/images/{unique_filename}"
        
        return {
            "success": True,
            "image_url": f"http://localhost:8000{image_url}",
            "filename": unique_filename,
            "size": os.path.getsize(file_path)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")
    finally:
        file.file.close()


@router.get("/images/{filename}")
async def get_image(filename: str):
    """
    Sirve las imágenes subidas
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    # Verificar que es un archivo (no directorio) y está en UPLOAD_DIR
    if not os.path.isfile(file_path) or not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return FileResponse(file_path)


@router.delete("/images/{filename}")
async def delete_image(filename: str):
    """
    Elimina una imagen subida (para limpieza)
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    # Verificar que es un archivo y está en UPLOAD_DIR
    if not os.path.isfile(file_path) or not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        os.remove(file_path)
        return {"success": True, "message": "Imagen eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar imagen: {str(e)}")