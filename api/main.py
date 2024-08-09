from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from .routes.talking_points import router as talking_points_router
from .routes.numbers import router as numbers_router
from pydantic import BaseModel
from pathlib import Path
from .crud import update_version_info, update_version_filename, get_info
from .database import SessionLocal

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

@app.get("/info")
async def get_infos():
    db = SessionLocal()
    info = get_info(db)
    db.close()
    print()
    return JSONResponse(content={
        "client_versions": info.client_versions,
        "backend_versions": info.backend_versions,
        "client_filename": info.client_filename
    })

# 文件存储路径
UPLOAD_DIR = Path("./file")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class TagModel(BaseModel):
    tag: str

@app.post("/store-tag/")
async def store_tag(tag: TagModel):
    tag = tag.tag
    db = SessionLocal()
    update_version_info(db, tag, "client")
    db.close()
    return {"message": "Tag stored successfully"}

@app.post("/upload-file/")
async def upload_file(tag: str, file: UploadFile = File(...)):
    db = SessionLocal()
    update_version_info(db, tag, "backend")
    update_version_filename(db, file.filename+"_"+tag)
    db.close()
    file_path = UPLOAD_DIR / f"{file.filename}_{tag}"
    with file_path.open("wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded successfully"}

@app.get("/download-file/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)
    return {"error": "File not found"}
