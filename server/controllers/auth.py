#This is where the verification of the attempted login is done

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database.database import get_db, engine
from schemas.user import UserLogin
from models import user
from services import auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

user.Base.metadata.create_all(bind=engine)

router = APIRouter(
    tags=["AUTHENTICATION"]
)

@router.post('/login')
def login(user_credentials:UserLogin, db: Session = Depends(get_db)):
    
    n_user = db.query(user.User).filter(user.User.email == user_credentials.email).first()

    if not n_user:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Invalid Credentials"))
    
    if not auth.verify(user_credentials.password, n_user.password):
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Invalid Credentials"))

    access_token = auth.create_access_token(data= {"User_id": n_user.id})
    return {"Access_Token": access_token, "Token_type": "bearer"}