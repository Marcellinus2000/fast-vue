from fastapi import APIRouter,status, HTTPException, Response, Depends
from models import user
from services import auth
from database.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from schemas.user import CreateUser, UserResponse

user.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(n_user : CreateUser , db: Session = Depends(get_db)):

    hashed_password = auth.hash(n_user.password)
    n_user.password = hashed_password
    
    new_user = user.User(**n_user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.get('/users/{id}', response_model=UserResponse)
def get_user(id:int , db: Session = Depends(get_db)):
    n_user = db.query(user.User).filter(user.User.id == id).first()

    if not n_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return n_user