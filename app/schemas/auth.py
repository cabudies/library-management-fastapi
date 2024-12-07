from pydantic import BaseModel, EmailStr

from app.models.user import UserRole, Honorific

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    role: UserRole
    password: str
    honorific: Honorific

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True 