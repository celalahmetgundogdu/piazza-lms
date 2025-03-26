from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from typing import List

router = APIRouter(prefix="/answers", tags=["Answers"])

# ✅ POST: Cevap oluştur
@router.post("/", response_model=schemas.AnswerOut)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    new_answer = models.Answer(
        content=answer.content,
        question_id=answer.question_id,
        user_id=answer.user_id,
        is_anonymous=answer.is_anonymous
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

# ✅ GET: Belirli bir kullanıcıya ait cevapları getir
@router.get("/users/{user_id}/", response_model=List[schemas.AnswerOut])
def get_answers_by_user(user_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.user_id == user_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="Bu kullanıcıya ait cevap bulunamadı.")
    return answers

# ✅ GET: Belirli bir soruya ait cevapları getir
@router.get("/questions/{question_id}/", response_model=List[schemas.AnswerOut])
def get_answers_by_question(question_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="Bu soruya ait cevap bulunamadı.")
    return answers

# ✅ DELETE: Cevap sil
@router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail="Cevap bulunamadı.")
    db.delete(answer)
    db.commit()
    return {"message": "Cevap başarıyla silindi."}

# ✅ PUT: Cevap güncelle
@router.put("/{answer_id}", response_model=schemas.AnswerOut)
def update_answer(answer_id: int, updated_data: schemas.AnswerCreate, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail="Cevap bulunamadı.")

    answer.content = updated_data.content
    answer.question_id = updated_data.question_id
    answer.user_id = updated_data.user_id
    answer.is_anonymous = updated_data.is_anonymous  # ✅ Eğer anonimliğini güncellemek istiyorsan bu da dahil

    db.commit()
    db.refresh(answer)
    return answer
