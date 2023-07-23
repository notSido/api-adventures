from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
from passlib.context import CryptContext
from .auth import getcurrentuser

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(getcurrentuser)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependancy, db: db_dependancy):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependancy, db: db_dependancy, user_verification: UserVerification):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password): # type: ignore
        raise HTTPException(status_code=401, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password) # type: ignore
    
    db.add(user_model)
    db.commit()
