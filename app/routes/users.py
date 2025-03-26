# Gerekli olanları en üste ekleyelim (zaten varsa tekrar yazmana gerek yok)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from typing import List
router = APIRouter()

# Veritabanı bağlantısı için helper fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Yeni kullanıcı oluşturma endpoint'i (zaten vardı)
@router.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 🔍 GET /users/ → Tüm kullanıcıları getir
@router.get("/users/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
