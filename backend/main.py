import os
import shutil
import uuid
import json
import math
import httpx
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Header, Query, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    tags: Optional[List[str]] = []

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: str
    created_at: datetime
    is_active: bool
    author: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

app = FastAPI(title="Visual Board API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://visualboard-itam.vercel.app",
    "https://dabtcavila.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Carpeta para guardar imágenes locales
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/api/upload/images", StaticFiles(directory=UPLOAD_DIR), name="images")

async def check_image_url_helper(url: str) -> bool:
    #Si es local, se verifica el archivo
    if "/api/upload/images/" in url:
        filename = url.split("/")[-1]
        return os.path.exists(os.path.join(UPLOAD_DIR, filename))
    #Si es externa, se hace un ping
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.head(url, follow_redirects=True)
            return response.status_code == 200
    except:
        return False

async def verify_post_images_task(db: Session, user_id: str = None):
    query = db.query(models.Post).filter(models.Post.is_active == True)
    if user_id:
        query = query.filter(models.Post.user_id == user_id)
    
    #Revisa por bloques de 50
    posts = query.order_by(models.Post.last_image_check.asc().nullsfirst()).limit(50).all()
    
    for post in posts:
        is_accessible = await check_image_url_helper(post.image_url)
        post.last_image_check = datetime.utcnow()
        if not is_accessible:
            post.is_active = False
    
    db.commit()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/posts", response_model=PaginatedResponse)
def get_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1),
    user_id: Optional[str] = None,
    min_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Post).filter(models.Post.is_active == True)
    
    if user_id:
        query = query.filter(models.Post.user_id == user_id)
    if min_date:
        try:
            date_obj = datetime.fromisoformat(min_date.replace('Z', '+00:00'))
            query = query.filter(models.Post.created_at > date_obj)
        except:
            pass

    total = query.count()
    total_pages = math.ceil(total / per_page) if per_page > 0 else 1
    
    posts = query.order_by(models.Post.created_at.desc())\
                 .offset((page - 1) * per_page)\
                 .limit(per_page).all()
    
    for p in posts:
        p.tags = json.loads(p.tags) if p.tags else []
        p.author = p.user_id 

    return {
        "items": posts, "total": total, "page": page,
        "per_page": per_page, "total_pages": total_pages
    }

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.tags = json.loads(post.tags) if post.tags else []
    post.author = post.user_id
    return post

@app.post("/api/posts", response_model=PostResponse)
def create_post(
    post: PostCreate,
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    tags_str = json.dumps(post.tags) if post.tags else "[]"
    
    db_post = models.Post(
        title=post.title,
        description=post.description,
        image_url=post.image_url,
        user_id=x_user_id,
        tags=tags_str,
        is_active=True
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    db_post.tags = json.loads(db_post.tags)
    db_post.author = db_post.user_id
    return db_post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostCreate,
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post or db_post.user_id != x_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_post.title = post.title
    db_post.description = post.description
    db_post.image_url = post.image_url
    db_post.tags = json.dumps(post.tags) if post.tags else "[]"
    db_post.is_active = True # Reactivar si se edita
    
    db.commit()
    db.refresh(db_post)
    
    db_post.tags = json.loads(db_post.tags)
    db_post.author = db_post.user_id
    return db_post

@app.delete("/api/posts/{post_id}")
def delete_post(
    post_id: int,
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post or db_post.user_id != x_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db.delete(db_post)
    db.commit()
    return {"message": "Deleted"}


@app.post("/api/image-health/check")
async def check_images(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    background_tasks.add_task(verify_post_images_task, db, x_user_id)
    return {"message": "Verification started"}

@app.get("/api/image-health/status")
def get_health_status(db: Session = Depends(get_db)):
    total = db.query(models.Post).count()
    active = db.query(models.Post).filter(models.Post.is_active == True).count()
    inactive = db.query(models.Post).filter(models.Post.is_active == False).count()
    
    health = round((active / total * 100) if total > 0 else 100, 2)
    return {
        "total_posts": total, "active_posts": active,
        "inactive_posts": inactive, "health_percentage": health
    }

@app.post("/api/image-health/reactivate/{post_id}")
async def reactivate_post(
    post_id: int,
    new_image_url: Optional[str] = Query(None),
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post or post.user_id != x_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if new_image_url:
        if await check_image_url_helper(new_image_url):
            post.image_url = new_image_url
        else:
            raise HTTPException(status_code=400, detail="New URL is unreachable")
            
    post.is_active = True
    post.last_image_check = datetime.utcnow()
    db.commit()
    return {"message": "Reactivated"}

@app.get("/api/discover")
async def discover_content(count: int = 30):
    key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not key:
        return []
        
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                "https://api.unsplash.com/photos/random",
                params={"count": count},
                headers={"Authorization": f"Client-ID {key}"}
            )
            if resp.status_code != 200:
                return []
            
            data = resp.json()
            return [{
                "id": i["id"],
                "title": i.get("alt_description") or "Untitled",
                "image_url": i["urls"]["regular"],
                "author": i["user"]["name"],
                "author_url": i["user"]["links"]["html"]
            } for i in data]
        except:
            return []

@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        base = os.getenv("BASE_URL", "http://localhost:8000")
        return {"success": True, "image_url": f"{base}/api/upload/images/{unique_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
