from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas.user import TokenData 
from database import database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


#--------------------- JWT Functions --------------------------

def create_access_token(data: dict):
    to_enconde = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"Exp": expire})

    expire_str = expire.isoformat()
    to_enconde.update({"Exp": expire_str})

    encoded_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id = str(id))
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception) 
    n_user = db.query(user.User).filter(user.User.id == token.id).first()
    return n_user