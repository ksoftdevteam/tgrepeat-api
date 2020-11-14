from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import User_Pydantic, UserIn_Pydantic, Users

router = APIRouter()


class Status(BaseModel):
    message: str


@router.get("/", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.get("/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    return await Users.get(id=user_id)


@router.post("/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post("/{user_id}", response_model=User_Pydantic)
async def edit_chat(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(Users.filter(id=user_id))


@router.delete("/{user_id}", response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete_chat(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")