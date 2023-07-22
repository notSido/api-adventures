from fastapi import FastAPI, Depends, HTTPException, status, Path, APIRouter
from models import ToDos
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import getcurrentuser

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(getcurrentuser)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=101)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get('/')
async def read_all(user: user_dependancy, db: Annotated[Session, Depends(get_db)]):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')    
    
    return db.query(ToDos).filter(ToDos.owner_id == user.get('id')).all()

@router.get('/todo/{todo_id}')
async def read_by_id(user: user_dependancy, db: db_dependancy, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='not found')

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependancy, db: db_dependancy, todo_request: TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = ToDos(**todo_request.dict(), owner_id=user.get('id'))
    
    db.add(todo_model)
    db.commit()
    
@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependancy, todo_request: TodoRequest,  todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_model.title = todo_request.title # type: ignore
    todo_model.description = todo_request.description # type: ignore
    todo_model.priority = todo_request.priority # type: ignore
    todo_model.complete = todo_request.complete # type: ignore
    
    db.add(todo_model)
    db.commit()
    
@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()