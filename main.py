from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routers import anime, poster, file, category, page
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from fastapi.routing import APIRoute

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def set_default_content_type(request: Request, call_next):
    response = await call_next(request)
    if response.headers.get("content-type") == "application/json":
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response


# ['127.0.0.1:8000', 'localhost:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)


# 代码压缩开了还不如不开，效果不明显，反向提速
# app.add_middleware(GZipMiddleware, minimum_size=400000)

app.mount("/static", StaticFiles(directory="./static"), name="static")

app.include_router(page.router)
app.include_router(anime.router)
app.include_router(poster.router)
app.include_router(file.router)
app.include_router(category.router)


for route in app.routes:
    if isinstance(route, APIRoute):
        print(route.name, route.path)
