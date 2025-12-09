from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import json
import math

from app.core.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostUpdate, PostResponse, PaginatedResponse

router = APIRouter(prefix="/posts", tags=["posts"])


def get_current_user(x_user_id: str = Header(...)) -> str:
    """Obtiene el usuario actual desde el header"""
    return x_user_id


def get_current_user_optional(x_user_id: Optional[str] = Header(None)) -> Optional[str]:
    """Obtiene el usuario actual desde el header (opcional)"""
    return x_user_id


@router.get("", response_model=PaginatedResponse)
def get_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=1000),
    user_id: Optional[str] = None,
    min_date: Optional[str] = Query(None, description="Filtrar posts creados después de esta fecha (ISO format)"),
    db: Session = Depends(get_db)
):
    """Lista todos los posts con paginación y filtros opcionales"""
    query = db.query(Post)
    
    # Solo mostrar posts activos (con imágenes válidas)
    query = query.filter(Post.is_active == True)
    
    # Filtro por usuario
    if user_id:
        query = query.filter(Post.user_id == user_id)
    
    # Filtro por fecha mínima (para el sistema de caché)
    if min_date:
        try:
            min_datetime = datetime.fromisoformat(min_date.replace('Z', '+00:00'))
            query = query.filter(Post.created_at > min_datetime)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SSZ)")
    
    total = query.count()
    total_pages = math.ceil(total / per_page) if per_page > 0 else 1
    
    # Ordenar por fecha de creación descendente (más recientes primero)
    posts = query.order_by(Post.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    # Convertir tags de JSON string a lista y agregar campo author
    for post in posts:
        if post.tags:
            post.tags = json.loads(post.tags)
        else:
            post.tags = []
        # Agregar campo author como alias de user_id
        post.author = post.user_id
    
    return PaginatedResponse(
        items=posts,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Obtiene un post específico por ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.tags:
        post.tags = json.loads(post.tags)
    else:
        post.tags = []
    
    # Agregar campo author
    post.author = post.user_id
    
    return post


@router.post("", response_model=PostResponse, status_code=201)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crea un nuevo post"""
    db_post = Post(
        title=post.title,
        description=post.description,
        image_url=str(post.image_url),
        user_id=current_user,
        tags=json.dumps(post.tags) if post.tags else "[]"
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    db_post.tags = json.loads(db_post.tags) if db_post.tags else []
    db_post.author = db_post.user_id  # Agregar el campo author
    
    return db_post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Reemplaza completamente un post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    
    db_post.title = post.title
    db_post.description = post.description
    db_post.image_url = str(post.image_url)
    db_post.tags = json.dumps(post.tags) if post.tags else "[]"
    
    db.commit()
    db.refresh(db_post)
    
    db_post.tags = json.loads(db_post.tags) if db_post.tags else []
    db_post.author = db_post.user_id  # Agregar el campo author
    
    return db_post


@router.patch("/{post_id}", response_model=PostResponse)
def partial_update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualiza parcialmente un post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    
    update_data = post.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "tags" and value is not None:
            setattr(db_post, field, json.dumps(value))
        elif field == "image_url" and value is not None:
            setattr(db_post, field, str(value))
        elif value is not None:
            setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    
    db_post.tags = json.loads(db_post.tags) if db_post.tags else []
    db_post.author = db_post.user_id  # Agregar el campo author
    
    return db_post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Elimina un post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(db_post)
    db.commit()
    
    return None