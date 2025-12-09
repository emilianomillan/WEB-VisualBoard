from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime

from app.core.database import get_db
from app.services.unsplash_service import unsplash_service

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Verifica el estado del servidor y servicios externos
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "api": True,
            "database": False,
            "unsplash": False
        }
    }
    
    # Verificar base de datos
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = True
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = False
    
    # Verificar Unsplash API
    unsplash_ok = await unsplash_service.check_health()
    health_status["services"]["unsplash"] = unsplash_ok
    
    if not unsplash_ok:
        health_status["status"] = "degraded"
    
    if not health_status["services"]["database"]:
        health_status["status"] = "unhealthy"
    
    return health_status