from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
import hashlib
from datetime import datetime

from app.core.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


def hash_password(password: str) -> str:
    """Hash simple para contraseñas (en producción usar bcrypt)"""
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Registrar un nuevo usuario"""
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
    
    # Crear nuevo usuario
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password)
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )
    
    return db_user


@router.post("/login", response_model=UserResponse)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Iniciar sesión"""
    # Buscar usuario por username o email
    user = db.query(User).filter(
        (User.username == credentials.username_or_email) | 
        (User.email == credentials.username_or_email)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if user.password_hash != hash_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Actualizar último login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user


@router.get("/profile/{username}", response_model=UserResponse)
def get_user_profile(
    username: str,
    db: Session = Depends(get_db)
):
    """Obtener perfil de usuario"""
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user


@router.get("/check/{username}")
def check_username_availability(
    username: str,
    db: Session = Depends(get_db)
):
    """Verificar si un nombre de usuario está disponible"""
    exists = db.query(User).filter(User.username == username).first() is not None
    
    return {
        "username": username,
        "available": not exists
    }