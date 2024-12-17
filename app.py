import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import  SQLModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from routers import recipes, web

app = FastAPI(title="Recipe Finder")
app.include_router(web.router)
app.include_router(recipes.router)

origins =[
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*",]
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.middleware("http")
async def add_recipes_cookie(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="recipes_cookie", value="you_visited_the_recipe_app")
    return response

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
