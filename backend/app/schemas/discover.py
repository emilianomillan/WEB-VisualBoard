from pydantic import BaseModel, HttpUrl
from typing import Optional


class UnsplashPhoto(BaseModel):
    id: str
    description: Optional[str] = None
    alt_description: Optional[str] = None
    urls: dict
    user: dict
    likes: int
    width: int
    height: int


class DiscoverItem(BaseModel):
    id: str
    title: Optional[str] = None
    image_url: HttpUrl
    author: str
    author_url: HttpUrl
    likes: int
    source: str = "unsplash"