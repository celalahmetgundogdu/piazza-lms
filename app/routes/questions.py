from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /questions/ → Yeni soru ekle
@router.post("/questions/", response_model=schemas.QuestionOut)
def ask_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(
        title=question.title,
        content=question.content,
        user_id=question.user_id,
        course_id=question.course_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

from typing import List

# 🔍 GET /questions/ → Tüm soruları getir
@router.get("/questions/", response_model=List[schemas.QuestionOut])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()
