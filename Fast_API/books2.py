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
    published_date: int
        
    def __init__ (self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int
    
    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'yours truly',
                'description': 'a new description that i am too lazy to write',
                'rating': 5,
                'published_date': 1899
            }
        }
# hello world i am here today to tell you that my name is jeff

BOOKS = [
    Book(1, 'The idiot', 'Fyodor Dostoevsky', 'An exploration of love and life', 5, 1869),
    Book(2, 'Notes from Underground', 'Fyodor Dostoevsky', 'A hyperconscious man reflecting on his life', 3, 1864),
    Book(3, 'Lolita', 'Vladimir Nabokov', 'Literature teacher rapes his 12 year old stepdaughter...', 4, 1955),
    Book(4, 'Dead Souls', 'Nikolai Gogol', 'A deep look into what people are ready to do to attain wealth', 4, 1842)
    
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

@app.get('/books/')
async def read_book_by_rating(rating:int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book

@app.put('/book/update_book')
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete('/books/{book_id}')
async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
        
@app.get('/books/published/')
async def read_book_by_release(published_date:int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return
