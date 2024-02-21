from fastapi import FastAPI,status, HTTPException, Response, Depends
from schemas.post import CreatePost, PostResponse
from schemas.user import CreateUser, UserResponse
from database.database import engine, get_db
from models import post, user
from sqlalchemy.orm import Session
from typing import List

post.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def hello():
    return{"Welcome": "Message"}

@app.get('/posts', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(post.Post).all()
    return posts

@app.get('/posts/{id}')
def get_post(id : int, db: Session = Depends(get_db)):

    npost = db.query(post.Post).filter(post.Post.id == id).first()
    print(post)

    if not npost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return post


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(npost: CreatePost, db: Session = Depends(get_db)):
    
    new_post = post.Post(**npost.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post

@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    
    post_q = db.query(post.Post).filter(post.Post.id == id)
    npost = post_q.first()
    if npost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_q.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()
    return post_q.first()

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
   
    npost = db.query(post.Post).filter(post.Post.id == id)

    if npost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist") 
           
    npost.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(n_user : CreateUser , db: Session = Depends(get_db)):

    new_user = user.User(**n_user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user