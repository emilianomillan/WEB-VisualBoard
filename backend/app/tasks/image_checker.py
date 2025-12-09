"""
Tarea programada para verificar la salud de las imágenes
Puede ejecutarse manualmente con: python -m app.tasks.image_checker
"""

import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.post import Post
from app.api.image_health import verify_post_images

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_all_images():
    """Verifica todas las imágenes que necesitan ser chequeadas"""
    db = SessionLocal()
    try:
        logger.info(f"Iniciando verificación de imágenes - {datetime.now()}")
        
        # Verificar posts que no se han chequeado en las últimas 24 horas
        results = await verify_post_images(db)
        
        logger.info(f"Verificación completada: {results}")
        return results
        
    except Exception as e:
        logger.error(f"Error durante verificación: {e}")
        raise
    finally:
        db.close()


async def run_periodic_check(interval_hours: int = 6):
    """Ejecuta la verificación periódicamente"""
    while True:
        try:
            await check_all_images()
        except Exception as e:
            logger.error(f"Error en verificación periódica: {e}")
        
        # Esperar el intervalo especificado
        await asyncio.sleep(interval_hours * 3600)


if __name__ == "__main__":
    # Ejecutar verificación manual una vez
    print("Ejecutando verificación manual de imágenes...")
    results = asyncio.run(check_all_images())
    print(f"Resultados: {results}")