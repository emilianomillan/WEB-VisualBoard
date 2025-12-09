from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    image_url = Column(String(500), nullable=False)
    user_id = Column(String(100), nullable=False, index=True)
    tags = Column(Text)  # JSON string array
    is_active = Column(Boolean, default=True, nullable=False)  # Para marcar posts con imágenes rotas
    last_image_check = Column(DateTime(timezone=True))  # Última vez que se verificó la imagen
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())