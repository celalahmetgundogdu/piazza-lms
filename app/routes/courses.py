from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter()

# Veritabanı bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔧 POST /courses/ → Yeni ders oluştur
@router.post("/courses/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(
        title=course.title,
        description=course.description,
        created_by=course.created_by
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

