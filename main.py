from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from routers import dashboard, data

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(data.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


register_tortoise(
    app,
    db_url="mysql://root:123456@localhost:3306/alibaba",
    modules={"models": ["database.model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
