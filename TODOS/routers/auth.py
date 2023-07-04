from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime

router = APIRouter()

SECRET_KEY = '42ad77a0b0e723c50c8e6a1e5994e86ef15d8075d702ac3fdd298266c32e485c'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

@router.post('/auth/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, CreateUserRequest: CreateUserRequest):
    create_user_model = Users(
        email = CreateUserRequest.email,
        username = CreateUserRequest.username,
        first_name = CreateUserRequest.first_name,
        last_name = CreateUserRequest.last_name,
        role = CreateUserRequest.role,
        hashed_password = bcrypt_context.hash(CreateUserRequest .password),
        is_active = True
    )
    
    db.add(create_user_model)
    db.commit()

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user
        
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                db: db_dependancy):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        return 'Failed Authentication'
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return token