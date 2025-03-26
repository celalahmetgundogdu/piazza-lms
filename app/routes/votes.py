from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from app import schemas
from app.schemas import VoteCreate
from app.schemas import VoteDelete
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/answers/{answer_id}/votes/")
def vote_on_answer(answer_id: int, vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    existing_vote = db.query(models.Vote).filter_by(answer_id=answer_id, user_id=vote.user_id).first()
    if existing_vote:
        if existing_vote.is_upvote == vote.is_upvote:
            return {"message": "User has already voted on this answer"}
        else:
            existing_vote.is_upvote = vote.is_upvote
            db.commit()
            db.refresh(existing_vote)
            return {"message": "Vote updated", "vote": existing_vote}
    new_vote = models.Vote(
        user_id=vote.user_id,
        answer_id=answer_id,
        is_upvote=vote.is_upvote
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return {"message": "Vote recorded", "vote": new_vote}

@router.delete("/answers/{answer_id}/votes/")
def unvote_answer(answer_id: int, vote: VoteDelete, db: Session = Depends(get_db)):
    vote_to_delete = db.query(models.Vote).filter_by(answer_id=answer_id, user_id=vote.user_id).first()
    if not vote_to_delete:
        raise HTTPException(status_code=404, detail="Vote not found")

    db.delete(vote_to_delete)
    db.commit()
    return {"message": "Vote removed"}
