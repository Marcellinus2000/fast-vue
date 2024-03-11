from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

#----------------- JWT Functions --------------------------

def create_access_token(data: dict):
    to_enconde = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"Exp": expire})

    expire_str = expire.isoformat()
    to_enconde.update({"Exp": expire_str})

    encoded_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt