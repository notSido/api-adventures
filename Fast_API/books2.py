from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
        
    def __init__ (self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=5)
    
    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'yours truly',
                'description': 'a new description that i am too lazy to write',
                'rating': 5
            }
        }
# hello world i am here today to tell you that my name is jeff

BOOKS = [
    Book(1, 'The idiot', 'Fyodor Dostoevsky', 'An exploration of love and life', 5),
    Book(2, 'Notes from Underground', 'Fyodor Dostoevsky', 'A hyperconscious man reflecting on his life', 3),
    Book(3, 'Lolita', 'Vladimir Nabokov', 'Literature teacher rapes his 12 year old stepdaughter...', 2),
    Book(4, 'Dead Souls', 'Nikolai Gogol', 'A deep look into what people are ready to do to attain wealth', 4)
    
]

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.post('/create-book')
async def create_book(book_request=Body()):
    BOOKS.append(book_request)
    
@app.post('/create-book2')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    
@app.get('/books/{book_id}')
async def fetch_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book

            
#wip delete function
#@app.delete('/books/delete-book/{book_id}')
#async def delete_book(book_id: int):
#    for book in BOOKS:
#        if book.delete('id') == book_id.delete('id'):
#            BOOKS.remove(book)

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book

