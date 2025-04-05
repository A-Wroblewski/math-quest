from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, description="")
    email: Optional[str] = Field(None, description="")
    password: Optional[str] = Field(None, description="")
    confirm_password: Optional[str] = Field(None, description="")
