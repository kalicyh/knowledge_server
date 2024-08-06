from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .routes.talking_points import router as talking_points_router
from .routes.numbers import router as numbers_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

app.mount("/dist", StaticFiles(directory="dist"), name="dist")

app.include_router(talking_points_router, prefix="/talking_points")
app.include_router(numbers_router, prefix="/numbers")

@app.get("/")
def root():
    return FileResponse('dist/index.html')
