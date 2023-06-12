from fastapi import FastAPI, Body

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

BOOKS = [
    Book(1, 'The idiot', 'Fyodor Dostoevsky', 'An exploration of the meaning of love and life', 5),
    Book(2, 'Notes from Underground', 'Fyodor Dostoevsky', 'A hyperconscious man reflecting on his life', 3),
    Book(3, 'Lolita', 'Vladimir Nabokov', 'Literature teacher rapes his 12 year old steapdaughter...', 2),
    Book(4, 'Dead Souls', 'Nikolai Gogol', 'An exploration into what people will do attain wealth', 4)
    
]

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.post('/create-book')
async def create_book(book_request=Body()):
    BOOKS.append(book_request)

#wip delete function
#@app.delete('/books/delete-book/{book_id}')
#async def delete_book(book_id: int):
#    for book in BOOKS:
#        if book.delete('id') == book_id.delete('id'):
#            BOOKS.remove(book)