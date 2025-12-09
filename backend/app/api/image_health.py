from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Dict
import httpx
import asyncio
import os

from app.core.database import get_db
from app.models.post import Post
from app.api.posts import get_current_user_optional

router = APIRouter(prefix="/image-health", tags=["image-health"])


async def check_image_url(url: str) -> bool:
    """Verifica si una URL de imagen es accesible"""
    # Si es una URL local (archivos subidos), verificar si el archivo existe
    if url.startswith("http://localhost:8000/api/upload/images/"):
        filename = url.split("/")[-1]
        file_path = os.path.join("uploads", filename)
        return os.path.exists(file_path)
    
    # Para URLs externas, hacer una petición HEAD
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.head(url, follow_redirects=True)
            # Verificar código de estado y content-type
            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                return any(img_type in content_type.lower() for img_type in ["image/", "img/"])
            return False
    except Exception:
        return False


async def verify_post_images(db: Session, post_ids: List[int] = None):
    """Verifica las imágenes de los posts y actualiza su estado"""
    query = db.query(Post).filter(Post.is_active == True)
    
    if post_ids:
        query = query.filter(Post.id.in_(post_ids))
    else:
        # Verificar posts que no se han chequeado en las últimas 24 horas
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        query = query.filter(
            (Post.last_image_check == None) | 
            (Post.last_image_check < cutoff_time)
        )
    
    posts = query.limit(50).all()  # Procesar máximo 50 posts por vez
    
    results = {"checked": 0, "deactivated": 0, "active": 0}
    
    for post in posts:
        is_accessible = await check_image_url(post.image_url)
        post.last_image_check = datetime.utcnow()
        
        if not is_accessible:
            post.is_active = False
            results["deactivated"] += 1
        else:
            results["active"] += 1
        
        results["checked"] += 1
    
    db.commit()
    return results


@router.post("/check")
async def check_images(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_optional)
):
    """
    Inicia una verificación de salud de imágenes en segundo plano.
    Si se proporciona un usuario, solo verifica sus posts.
    """
    async def run_check():
        if current_user:
            # Solo verificar posts del usuario actual
            user_posts = db.query(Post).filter(
                and_(Post.user_id == current_user, Post.is_active == True)
            ).all()
            post_ids = [p.id for p in user_posts]
            await verify_post_images(db, post_ids)
        else:
            # Verificar todos los posts
            await verify_post_images(db)
    
    background_tasks.add_task(run_check)
    
    return {
        "message": "Verificación de imágenes iniciada en segundo plano",
        "scope": "user" if current_user else "global"
    }


@router.get("/status")
async def get_health_status(db: Session = Depends(get_db)) -> Dict:
    """Obtiene estadísticas sobre el estado de salud de las imágenes"""
    total_posts = db.query(Post).count()
    active_posts = db.query(Post).filter(Post.is_active == True).count()
    inactive_posts = db.query(Post).filter(Post.is_active == False).count()
    
    # Posts no verificados recientemente
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    unchecked_posts = db.query(Post).filter(
        (Post.last_image_check == None) | 
        (Post.last_image_check < cutoff_time)
    ).count()
    
    return {
        "total_posts": total_posts,
        "active_posts": active_posts,
        "inactive_posts": inactive_posts,
        "unchecked_posts": unchecked_posts,
        "health_percentage": round((active_posts / total_posts * 100) if total_posts > 0 else 100, 2)
    }


@router.post("/check-single/{post_id}")
async def check_single_image(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Verifica la imagen de un post específico"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    is_accessible = await check_image_url(post.image_url)
    post.last_image_check = datetime.utcnow()
    
    if not is_accessible:
        post.is_active = False
    else:
        post.is_active = True
    
    db.commit()
    
    return {
        "post_id": post_id,
        "image_url": post.image_url,
        "is_accessible": is_accessible,
        "is_active": post.is_active
    }


@router.post("/reactivate/{post_id}")
async def reactivate_post(
    post_id: int,
    new_image_url: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_optional)
):
    """Reactiva un post inactivo, opcionalmente con nueva imagen"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user and post.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to reactivate this post")
    
    # Si se proporciona nueva URL, actualizarla
    if new_image_url:
        # Verificar que la nueva URL es válida
        is_accessible = await check_image_url(new_image_url)
        if not is_accessible:
            raise HTTPException(status_code=400, detail="New image URL is not accessible")
        post.image_url = new_image_url
    
    post.is_active = True
    post.last_image_check = datetime.utcnow()
    
    db.commit()
    
    return {
        "post_id": post_id,
        "is_active": True,
        "message": "Post reactivated successfully"
    }