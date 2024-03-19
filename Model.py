from typing import List, Self, Dict, Optional
import string
import random

from sqlmodel import Field, SQLModel, Relationship


class UserListLink(SQLModel, table=True):
    """
    Many to many link.
    custom name used for users with name collisions on existing lists
    """
    list_id: Optional[int] = Field(default=None, foreign_key="datalist.id", primary_key=True)
    custom_name: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


class User(SQLModel, table=True):
    """
    Base user model
    ToDo: Add a way to map telegram user to database user
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    lists: List["DataList"] = Relationship(back_populates="users", link_model=UserListLink)


class DataList(SQLModel, table=True):
    """
    Base list model
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="lists", link_model=UserListLink)


class Line(SQLModel, table=True):
    """
    Base list line from the list
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_done: bool
    list_id: Optional[int] = Field(default=False, foreign_key="datalist.id")


class AccessKey(SQLModel, table=True):
    """
    A key for accessing the already created lists
    ToDo: find a good way to ensure that the key cannot be repeated (make it primary?)
    """
    list_id: Optional[int] = Field(default=None, foreign_key="datalist.id", primary_key=True)
    allow_edit: bool = True
    allow_read: bool = True
    key: str
