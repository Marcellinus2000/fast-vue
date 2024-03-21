from fastapi import status, HTTPException, Response, Depends, APIRouter
from models import post
from database.database import engine, get_db
from sqlalchemy.orm import Session
from schemas.post import CreatePost, PostResponse
from typing import List
from services import auth

post.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix= "/posts", tags= ["POSTS"]
)


@router.get('/', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):

    print(current_user.email)
    
    posts = db.query(post.Post).all()
    return posts


@router.get('/{id}', response_model=PostResponse)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):

    print(current_user)
    
    npost = db.query(post.Post).filter(post.Post.id == id).first()
    print(npost)

    if not npost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return npost

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post( npost: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    
    print(current_user)
    new_post = post.Post(**npost.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    
    print (current_user)

    post_q = db.query(post.Post).filter(post.Post.id == id)
    npost = post_q.first()
    if npost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_q.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()
    return post_q.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):

    print(current_user)
   
    npost = db.query(post.Post).filter(post.Post.id == id)

    if npost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist") 
           
    npost.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)