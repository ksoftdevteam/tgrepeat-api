import settings

import uvicorn

from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from routers import api_router

app = FastAPI(
    title="TGRepeatBotAPI",
    docs_url=f'{settings.API_V1_STR}/documentation',
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


register_tortoise(
    app,
    db_url="postgres://admin_tgr:kAikvcbX6o@188.93.210.133:5432/admin_tgr",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("application:app",
                host=settings.WEBAPP_HOST,
                port=settings.WEBAPP_PORT,
                debug=True)