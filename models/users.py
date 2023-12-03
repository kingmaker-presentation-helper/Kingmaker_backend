from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

class EventBase(SQLModel):
	title: str
	description: Optional[str] = None
	date: datetime
	location: Optional[str] = None

class Event(EventBase, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	user_email: EmailStr = Field(foreign_key='user.email')
	user: Optional["User"] = Relationship(back_populates="events")

class User(SQLModel, table=True):
	email: EmailStr = Field(primary_key=True)
	username: str
	events: List["Event"] = Relationship(back_populates="user")

class Signup(BaseModel):
	email: EmailStr
	username: str
	exp: int

class TokenResponse(BaseModel):
	access_token: str
	token_type: str
