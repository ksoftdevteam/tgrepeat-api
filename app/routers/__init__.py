from fastapi import APIRouter

from routers import (
    users, tasks, questions
)


api_router = APIRouter()


api_router.include_router(users.router, prefix='/user', tags=['User'])
api_router.include_router(tasks.router, prefix='/task', tags=['Task'])
api_router.include_router(questions.router, prefix='/question', tags=['Question'])