from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from typing import List

router = APIRouter()

# Veritabanı bağlantısı için yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔍 Belirli bir soruya ait cevapları getir
@router.get("/questions/{question_id}/answers/", response_model=List[schemas.AnswerOut])
def get_answers_for_question(question_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="Bu soruya ait cevap bulunamadı.")
    return answers

# 🔍 Belirli bir kullanıcıya ait cevapları getir
@router.get("/users/{user_id}/answers/", response_model=List[schemas.AnswerOut])
def get_answers_by_user(user_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.user_id == user_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="Bu kullanıcıya ait cevap bulunamadı.")
    return answers

# 🔍 Belirli bir soruya ait cevapları getir
@router.get("/questions/{question_id}/answers/", response_model=List[schemas.AnswerOut])
def get_answers_by_question(question_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="Bu soruya ait cevap bulunamadı.")
    return answers

# ❌ DELETE /answers/{answer_id} → Belirli bir cevabı sil
@router.delete("/answers/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer is None:
        return {"error": "Answer not found."}
    db.delete(answer)
    db.commit()
    return {"message": "Answer deleted successfully."}

# 🔄 PUT /answers/{answer_id} → Belirli bir cevabı güncelle
@router.put("/answers/{answer_id}", response_model=schemas.AnswerOut)
def update_answer(answer_id: int, updated_data: schemas.AnswerCreate, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer is None:
        return {"error": "Answer not found."}

    answer.content = updated_data.content
    answer.question_id = updated_data.question_id
    answer.user_id = updated_data.user_id

    db.commit()
    db.refresh(answer)
    return answer
