from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None


class UserResponse(UserBase):
    id: str = Field(..., alias="_id")
