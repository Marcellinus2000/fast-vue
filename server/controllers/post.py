from fastapi import status, HTTPException, Response, Depends, APIRouter
from models import post,vote
from database.database import engine, get_db
from sqlalchemy.orm import Session
from schemas.post import CreatePost, PostResponse, JoinPost
from typing import List,Optional
from services import auth
from sqlalchemy import func

post.Base.metadata.create_all(bind=engine)
vote.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix= "/posts", tags= ["POSTS"]
)

@router.get('/', response_model=List[JoinPost])
def get_posts(db: Session = Depends(get_db), limit : int = 10, skip:int = 0, search:Optional[str]= ""):
    
    # posts = db.query(post.Post).filter(post.Post.owner_id == current_user.id).all()

    # posts = db.query(post.Post).filter(post.Post.title.contains(search)).limit(limit).offset(skip).all()

    query_post = db.query(post.Post, func.count(vote.Vote.post_id).label("Votes")).outerjoin(vote.Vote, post.Post.id == vote.Vote.post_id).group_by(post.Post.id).all()
    
    posts = [
        {"post": post, "votes": vote_count}
        for post, vote_count in query_post 
    ]

    return posts


@router.get('/{id}', response_model=List[JoinPost])
def get_post(id : int, db: Session = Depends(get_db)):

    query_post = db.query(post.Post, func.count(vote.Vote.post_id).label("Votes")).outerjoin(vote.Vote, post.Post.id == vote.Vote.post_id).group_by(post.Post.id).filter(post.Post.id == id)
    
    posts = [
        {"post": post, "votes": vote_count}
        for post, vote_count in query_post 
    ]

    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post( npost: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    
    new_post = post.Post(owner_id=current_user.id, **npost.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    
    post_q = db.query(post.Post).filter(post.Post.id == id)
    npost = post_q.first()
    if npost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if npost.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_q.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()
    return post_q.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):

    print(current_user.id)
   
    npost_query = db.query(post.Post).filter(post.Post.id == id)

    npost = npost_query.first()

    if npost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    if npost.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
           
    npost_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)