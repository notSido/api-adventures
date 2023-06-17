from fastapi import FastAPI, Depends, HTTPException
import models
from models import ToDos
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

@app.get('/')
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(ToDos).all()

@app.get('/todo/{todo_id}')
async def read_by_id(db: db_dependancy, todo_id: int):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='not found')