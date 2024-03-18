from typing import List, Self, Dict, Optional
import string
import random

from sqlmodel import Field, SQLModel, Relationship


class UserListLink(SQLModel, table=True):
    list_id: Optional[int] = Field(default=None, foreign_key="datalist.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lists: List["DataList"] = Relationship(back_populates="users", link_model=UserListLink)


class DataList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="lists", link_model=UserListLink)


class Line(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_done: bool
    list_id: Optional[int] = Field(default=False, foreign_key="datalist.id")


class AccessKey(SQLModel, table=True):
    list_id: Optional[int] = Field(default=None, foreign_key="datalist.id", primary_key=True)
    allow_edit: bool = True
    allow_read: bool = True
    key: str
