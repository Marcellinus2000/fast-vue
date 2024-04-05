from fastapi import status, HTTPException, Response, Depends, APIRouter
from models import vote
from database.database import engine, get_db
from sqlalchemy.orm import Session
from schemas.vote import Voting
from services import auth


vote.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix= "/votes", tags= ["VOTES"]
)

@router.get('/')
def get_votes(db: Session = Depends(get_db)):
    votes = db.query(vote.Vote).all()
    return votes

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(nvote:Voting, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):

    vote_query = db.query(vote.Vote).filter(vote.Vote.post_id == nvote.post_id, vote.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if(nvote.dir == 1):
        if found_vote:
            print(current_user.id)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {nvote.post_id}")
        
        new_vote = vote.Vote(post_id = nvote.post_id, user_id = current_user.id)

        db.add(new_vote)
        db.commit()
        print(current_user.id)
        return {"Message": "Successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Successfully deleted vote"}