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

description = """
github地址：[kalicyh/knowledge_server](https://github.com/kalicyh/knowledge_server)
"""

app = FastAPI(
    title="智库管理系统",
    description=description,
    version="1.7.9",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

UPLOAD_DIR = Path("./file")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class TagModel(BaseModel):
    tag: str

app.mount("/dist", StaticFiles(directory="dist"), name="dist")

@app.get("/", tags=["前端页面"], description="UI界面")
def root():
    return FileResponse('dist/index.html')

@app.get("/info", tags=["信息"], description="返回前端版本，后端版本，前端软件名")
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

@app.post("/client-file-tag/", tags=["信息"], description="更新前端版本及上传软件接口")
async def client_file_tag(tag: str, file: UploadFile = File(...)):
    db = SessionLocal()
    update_version_info(db, tag, "client")
    update_version_filename(db, file.filename+"_"+tag)
    db.close()
    file_path = UPLOAD_DIR / f"{file.filename}_{tag}"
    with file_path.open("wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded successfully"}

@app.get("/client-file/{filename}", tags=["信息"], description="前端软件下载接口")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)
    return {"error": "File not found"}

app.include_router(talking_points_router, prefix="/talking_points")
app.include_router(numbers_router, prefix="/numbers")