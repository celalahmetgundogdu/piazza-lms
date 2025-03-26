from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/answer-votes/", response_model=schemas.AnswerVoteOut)
def create_vote(vote_data: schemas.AnswerVoteCreate, db: Session = Depends(get_db)):
    # Aynı kullanıcının aynı cevaba daha önce oy verip vermediğini kontrol et
    existing_vote = db.query(models.AnswerVote).filter_by(
        user_id=vote_data.user_id,
        answer_id=vote_data.answer_id
    ).first()

    if existing_vote:
        raise HTTPException(status_code=400, detail="This user has already voted for this answer.")

    new_vote = models.AnswerVote(
        user_id=vote_data.user_id,
        answer_id=vote_data.answer_id,
        vote=vote_data.vote
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote

from fastapi import Path

@router.get("/answers/{answer_id}/votes/")
def get_vote_count(answer_id: int = Path(...), db: Session = Depends(get_db)):
    upvotes = db.query(models.AnswerVote).filter_by(answer_id=answer_id, vote=1).count()
    downvotes = db.query(models.AnswerVote).filter_by(answer_id=answer_id, vote=-1).count()
    return {
        "answer_id": answer_id,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "total_score": upvotes - downvotes
    }
