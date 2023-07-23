from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import ToDos
from database import SessionLocal
from .auth import getcurrentuser

router = APIRouter(    
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(getcurrentuser)]




@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependancy, db: db_dependancy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(ToDos).all()