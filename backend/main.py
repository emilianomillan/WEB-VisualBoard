import os
import shutil
import uuid
import json
import math
import hashlib
import httpx
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Header, Query, File, UploadFile, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, HttpUrl
from sqlalchemy.orm import Session
from sqlalchemy import or_, text

from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Visual Board API")

origins = [
    "http://localhost:5173", "http://localhost:5174", "http://localhost:3000",
    "https://visualboard-itam.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_FILE_SIZE = 10 * 1024 * 1024 

app.mount("/api/upload/images", StaticFiles(directory=UPLOAD_DIR), name="images")


#Esquemas base de un usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    class Config:
        from_attributes = True

#Esquemas base del post
class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    tags: Optional[List[str]] = []

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None

class PostResponse(PostBase):
    id: int
    user_id: str
    author: str
    created_at: datetime
    is_active: bool
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


#Funciones aux
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def validate_file(file: UploadFile) -> None:
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Formato no permitido")
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Archivo muy grande (>10MB)")

async def check_image_url_helper(url: str) -> bool:
    if "/api/upload/images/" in url:
        filename = url.split("/")[-1]
        return os.path.exists(os.path.join(UPLOAD_DIR, filename))
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
    
    posts = query.order_by(models.Post.last_image_check.asc().nullsfirst()).limit(50).all()
    
    for post in posts:
        is_accessible = await check_image_url_helper(post.image_url)
        post.last_image_check = datetime.utcnow()
        if not is_accessible:
            post.is_active = False
    db.commit()



@app.post("/api/users/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.username == user_data.username) | (models.User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuario o email ya registrado")
    
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/users/login", response_model=UserResponse)
def login_user(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        (models.User.username == creds.username_or_email) | 
        (models.User.email == creds.username_or_email)
    ).first()
    
    if not user or user.password_hash != hash_password(creds.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    user.last_login = datetime.utcnow()
    db.commit()
    return user

@app.get("/api/users/check/{username}")
def check_username(username: str, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.username == username).first() is not None
    return {"username": username, "available": not exists}

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
        except: pass

    total = query.count()
    total_pages = math.ceil(total / per_page) if per_page > 0 else 1
    posts = query.order_by(models.Post.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    for p in posts:
        p.tags = json.loads(p.tags) if p.tags else []
        p.author = p.user_id
        
    return {"items": posts, "total": total, "page": page, "per_page": per_page, "total_pages": total_pages}

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post: raise HTTPException(status_code=404, detail="Post not found")
    post.tags = json.loads(post.tags) if post.tags else []
    post.author = post.user_id
    return post

@app.post("/api/posts", response_model=PostResponse, status_code=201)
def create_post(
    post: PostCreate,
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = models.Post(
        title=post.title, description=post.description, image_url=post.image_url,
        user_id=x_user_id, tags=json.dumps(post.tags) if post.tags else "[]", is_active=True
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.tags = json.loads(db_post.tags)
    db_post.author = db_post.user_id
    return db_post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, post: PostCreate,
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post or db_post.user_id != x_user_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    db_post.title = post.title
    db_post.description = post.description
    db_post.image_url = post.image_url
    db_post.tags = json.dumps(post.tags) if post.tags else "[]"
    db_post.is_active = True
    db.commit()
    db.refresh(db_post)
    
    db_post.tags = json.loads(db_post.tags)
    db_post.author = db_post.user_id
    return db_post

@app.patch("/api/posts/{post_id}", response_model=PostResponse)
def partial_update(
    post_id: int, post: PostUpdate,
    x_user_id: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post or db_post.user_id != x_user_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    data = post.model_dump(exclude_unset=True)
    for k, v in data.items():
        if k == "tags": setattr(db_post, k, json.dumps(v))
        else: setattr(db_post, k, v)
    
    db.commit()
    db.refresh(db_post)
    db_post.tags = json.loads(db_post.tags) if db_post.tags else []
    db_post.author = db_post.user_id
    return db_post

@app.delete("/api/posts/{post_id}", status_code=204)
def delete_post(post_id: int, x_user_id: str = Header(..., alias="X-User-Id"), db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post or db_post.user_id != x_user_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    db.delete(db_post)
    db.commit()
    return None


@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        validate_file(file)
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4()}{file_ext}"
        path = os.path.join(UPLOAD_DIR, unique_name)
        
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        return {
            "success": True, 
            "image_url": f"{base_url}/api/upload/images/{unique_name}",
            "filename": unique_name
        }
    except HTTPException as he: raise he
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/upload/images/{filename}")
async def delete_image(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return {"success": True}
    raise HTTPException(status_code=404, detail="Imagen no encontrada")

@app.get("/api/discover")
async def discover_content(count: int = 30):
    key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not key: return []
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get("https://api.unsplash.com/photos/random", params={"count": count}, headers={"Authorization": f"Client-ID {key}"})
            if resp.status_code == 200:
                data = resp.json()
                return [{
                    "id": i["id"], "title": i.get("alt_description") or "Untitled",
                    "image_url": i["urls"]["regular"], "author": i["user"]["name"],
                    "author_url": i["user"]["links"]["html"], "likes": i["likes"]
                } for i in data]
        except: pass
    return []

@app.post("/api/image-health/check")
async def check_images_task(bg: BackgroundTasks, db: Session = Depends(get_db), x_user_id: Optional[str] = Header(None, alias="X-User-Id")):
    bg.add_task(verify_post_images_task, db, x_user_id)
    return {"message": "Started"}

@app.get("/api/image-health/status")
def health_status(db: Session = Depends(get_db)):
    total = db.query(models.Post).count()
    active = db.query(models.Post).filter(models.Post.is_active == True).count()
    inactive = db.query(models.Post).filter(models.Post.is_active == False).count()
    return {"total_posts": total, "active_posts": active, "inactive_posts": inactive}

@app.get("/health")
async def main_health(db: Session = Depends(get_db)):
    status_data = {"status": "healthy", "database": False, "unsplash": False}
    try:
        db.execute(text("SELECT 1"))
        status_data["database"] = True
    except: pass
    
    key = os.getenv("UNSPLASH_ACCESS_KEY")
    if key:
        try:
            async with httpx.AsyncClient() as c:
                r = await c.get("https://api.unsplash.com/photos/random?count=1", headers={"Authorization": f"Client-ID {key}"})
                if r.status_code == 200: status_data["unsplash"] = True
        except: pass
    return status_data
    
