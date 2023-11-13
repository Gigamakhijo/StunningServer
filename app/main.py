from fastapi import FastAPI

from .routers import auth, mate, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(mate.router)
