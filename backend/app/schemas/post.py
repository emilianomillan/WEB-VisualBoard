from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: HttpUrl
    tags: Optional[List[str]] = []


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    tags: Optional[List[str]] = None


class PostResponse(PostBase):
    id: int
    user_id: str
    author: str  # Alias para user_id para cumplir con el checklist
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
    
    def __init__(self, **data):
        # Asegurar que author siempre sea igual a user_id
        if 'user_id' in data and 'author' not in data:
            data['author'] = data['user_id']
        super().__init__(**data)


class PaginatedResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
    total_pages: int