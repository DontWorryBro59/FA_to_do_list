from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import create_tables
from database import drop_tables
from routes.tasks import tasks_router
from routes.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print('[LOG]: Drop all tables')
    await create_tables()
    print('[LOG]: Create all tables')
    yield
    print('[LOG]: The app has stopped')


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(app='main:app', reload=True)
