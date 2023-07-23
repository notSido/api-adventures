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

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependancy, db: db_dependancy, todo_id: int = Path(gt=0)):
   
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')    
    
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()