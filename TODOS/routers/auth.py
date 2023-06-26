from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.post('/auth/')
async def create_user(CreateUserRequest: CreateUserRequest):
    create_user_model = Users(
        email = CreateUserRequest.email,
        username = CreateUserRequest.username,
        first_name = CreateUserRequest.first_name,
        last_name = CreateUserRequest.last_name,
        role = CreateUserRequest.role,
        hashed_password = CreateUserRequest.password,
        is_active = True
    )
    
    return create_user_model