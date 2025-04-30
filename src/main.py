from fastapi import FastAPI

from routers import math, user

app = FastAPI()

app.include_router(user.router)
app.include_router(math.router)
