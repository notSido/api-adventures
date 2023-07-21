from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '42ad77a0b0e723c50c8e6a1e5994e86ef15d8075d702ac3fdd298266c32e485c'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str 
    
class User(BaseModel):
    username: str
    email: str   
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

@router.post('/', status_code=status.HTTP_201_CREATED)
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
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def getcurrentuser(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub') # type: ignore
        user_id: int = payload.get('id') # type: ignore
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                db: db_dependancy):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    token = create_access_token(user.username, user.id, timedelta(minutes=20)) # type: ignore
    
    return {'access_token': token, 'token_type': 'bearer'}