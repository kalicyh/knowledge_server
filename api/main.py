from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from io import BytesIO
import pandas as pd
import uuid
from sqlalchemy.orm import Session
from .database import SessionLocal, Record, Info
from .crud import clear_records, add_records, get_records, get_info, update_info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

app.mount("/dist", StaticFiles(directory="dist"), name="dist")

@app.get("/")
def root():
    return FileResponse('dist/index.html')

upload_progress = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}  # Initialize progress

    file_content = await file.read()
    file_buffer = BytesIO(file_content)

    background_tasks.add_task(process_file, file_buffer, upload_id)

    return {"upload_id": upload_id, "message": "Upload started"}

@app.post("/overwrite_upload")
async def overwrite_upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}  # Initialize progress

    db = SessionLocal()
    try:
        clear_records(db)
    except Exception as e:
        db.rollback()
        upload_progress[upload_id]['message'] = f"清空数据表错误: {str(e)}"
        db.close()
        return {"upload_id": upload_id, "message": "清空数据表错误"}
    finally:
        db.close()

    file_content = await file.read()
    file_buffer = BytesIO(file_content)

    background_tasks.add_task(process_file, file_buffer, upload_id)

    return {"upload_id": upload_id, "message": "Overwrite upload started"}

@app.get("/progress/{upload_id}")
async def get_progress(upload_id: str):
    progress = upload_progress.get(upload_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Upload ID not found")
    return progress

def process_file(file_buffer: BytesIO, upload_id: str):
    df = pd.read_excel(file_buffer)
    df.columns = df.columns.str.strip()
    df['分类'] = df['分类'].fillna('未分类')

    total_rows = len(df)
    records = []
    chunk_size = 50

    for index, row in df.iterrows():
        records.append(
            Record(
                name=row['名字'],
                category=row['分类'],
                text=row['文案']
            )
        )

        if (index + 1) % chunk_size == 0 or (index + 1) == total_rows:
            db = SessionLocal()
            try:
                add_records(db, records)
                progress = round((index + 1) / total_rows * 100, 2)
                upload_progress[upload_id] = {
                    'progress': progress,
                    'current_row': index + 1,
                    'total_rows': total_rows
                }
                records = []
            except Exception as e:
                db.rollback()
                upload_progress[upload_id]['message'] = f"上传错误: {str(e)}"
                raise e
            finally:
                db.close()

    if records:
        db = SessionLocal()
        try:
            add_records(db, records)
            upload_progress[upload_id]['progress'] = 100
            upload_progress[upload_id]['message'] = "文件已上传，数据已添加到数据库"
        except Exception as e:
            db.rollback()
            upload_progress[upload_id]['message'] = f"上传错误: {str(e)}"
            raise e
        finally:
            db.close()

    db = SessionLocal()
    try:
        update_info(db, total_rows)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.get("/data")
async def get_data():
    db = SessionLocal()
    records = get_records(db)
    db.close()

    return JSONResponse(content={
        "total_records": len(records),
        "records": [
            {
                "序号": record.id,
                "名字": record.name,
                "分类": record.category,
                "文案": record.text
            }
            for record in records
        ]
    })

@app.get("/info")
async def get_infos():
    db = SessionLocal()
    info_record = get_info(db)
    if not info_record:
        db.close()
        raise HTTPException(status_code=404, detail="No info record found")
    
    name_categories = db.query(Record.name).distinct().all()
    db.close()
    
    name_categories = [category[0] for category in name_categories]
    
    return JSONResponse(content={
        "last_updated": info_record.last_updated,
        "total_rows": info_record.total_rows,
        "name_categories": name_categories
    })
