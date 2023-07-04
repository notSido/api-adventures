from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

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

def authenticata_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True
        

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependancy):
    return form_data.username