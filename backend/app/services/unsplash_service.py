import httpx
from typing import List, Optional
from app.core.config import settings
from app.schemas.discover import DiscoverItem
import random


class UnsplashService:
    BASE_URL = "https://api.unsplash.com"
    
    def __init__(self):
        self.access_key = settings.UNSPLASH_ACCESS_KEY
        self.headers = {
            "Authorization": f"Client-ID {self.access_key}"
        }
    
    async def get_random_photos(self, count: int = 30) -> List[DiscoverItem]:
        """Obtiene fotos aleatorias de Unsplash"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/photos/random",
                    headers=self.headers,
                    params={"count": count}
                )
                response.raise_for_status()
                photos = response.json()
                
                return [self._transform_photo(photo) for photo in photos]
            except Exception as e:
                print(f"Error fetching from Unsplash: {e}")
                return []
    
    def _transform_photo(self, photo: dict) -> DiscoverItem:
        """Transforma los datos de Unsplash al formato interno"""
        return DiscoverItem(
            id=photo["id"],
            title=photo.get("description") or photo.get("alt_description"),
            image_url=photo["urls"]["regular"],
            author=photo["user"]["name"],
            author_url=photo["user"]["links"]["html"],
            likes=photo["likes"]
        )
    
    async def check_health(self) -> bool:
        """Verifica si el servicio de Unsplash está disponible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/",
                    headers=self.headers
                )
                return response.status_code == 200
        except:
            return False


unsplash_service = UnsplashService()