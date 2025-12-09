from fastapi import APIRouter, Query
from typing import List

from app.services.unsplash_service import unsplash_service
from app.schemas import DiscoverItem

router = APIRouter(prefix="/discover", tags=["discover"])


@router.get("", response_model=List[DiscoverItem])
async def get_discover_content(count: int = Query(30, ge=1, le=50)):
    """
    Obtiene contenido aleatorio desde Unsplash para la sección Descubrimiento
    """
    photos = await unsplash_service.get_random_photos(count)
    return photos