from typing import Union
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import mysql.connector
from io import BytesIO
import datetime
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# Database configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define your SQLAlchemy models
class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    category = Column(String(255), nullable=True)
    text = Column(String(5000))

Base.metadata.create_all(bind=engine)

# Serve static files
app.mount("/dist", StaticFiles(directory="dist"), name="dist")

@app.get("/")
def root():
    return FileResponse('dist/index.html')
# Global variable to store progress
upload_progress = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}  # Initialize progress

    # Read file content into memory
    file_content = await file.read()
    file_buffer = BytesIO(file_content)

    # Add background task
    background_tasks.add_task(process_file, file_buffer, upload_id)

    return {"upload_id": upload_id, "message": "Upload started"}

@app.post("/overwrite_upload")
async def overwrite_upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}  # Initialize progress

    # 清空数据表
    db = SessionLocal()
    try:
        db.query(Record).delete()  # 清空数据表
        db.commit()
    except Exception as e:
        db.rollback()
        upload_progress[upload_id]['message'] = f"清空数据表错误: {str(e)}"
        db.close()
        return {"upload_id": upload_id, "message": "清空数据表错误"}
    finally:
        db.close()

    # 读取文件内容到内存中
    file_content = await file.read()
    file_buffer = BytesIO(file_content)

    # 添加后台任务
    background_tasks.add_task(process_file, file_buffer, upload_id)

    return {"upload_id": upload_id, "message": "Overwrite upload started"}

@app.get("/progress/{upload_id}")
async def get_progress(upload_id: str):
    progress = upload_progress.get(upload_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Upload ID not found")
    return progress

def process_file(file_buffer: BytesIO, upload_id: str):
    # 读取 Excel 文件
    df = pd.read_excel(file_buffer)
    df.columns = df.columns.str.strip()
    df['分类'] = df['分类'].fillna('未分类')

    total_rows = len(df)
    records = []
    chunk_size = 50
    
    # 处理每一行数据
    for index, row in df.iterrows():
        records.append(
            Record(
                name=row['名字'],
                category=row['分类'],
                text=row['文案']
            )
        )
        
        # 每 chunk_size 行提交一次
        if (index + 1) % chunk_size == 0 or (index + 1) == total_rows:
            # 将记录保存到数据库
            db = SessionLocal()
            try:
                db.add_all(records)
                db.commit()
                # 更新进度
                progress = round((index + 1) / total_rows * 100, 2)
                upload_progress[upload_id] = {
                    'progress': progress,
                    'current_row': index + 1,
                    'total_rows': total_rows
                }
                print(upload_progress[upload_id])
                print(upload_progress[upload_id]['progress'])
                # 清空记录列表以准备下一批
                records = []
            except Exception as e:
                db.rollback()
                upload_progress[upload_id]['message'] = f"上传错误: {str(e)}"
                raise e
            finally:
                db.close()

    # 确保最后一批记录也被提交
    if records:
        db = SessionLocal()
        try:
            db.add_all(records)
            db.commit()
            upload_progress[upload_id]['progress'] = 100
            upload_progress[upload_id]['message'] = "文件已上传，数据已添加到数据库"
        except Exception as e:
            db.rollback()
            upload_progress[upload_id]['message'] = f"上传错误: {str(e)}"
            raise e
        finally:
            db.close()

    print(upload_progress[upload_id])

@app.get("/data")
async def get_data():
    db = SessionLocal()
    records = db.query(Record).all()
    db.close()
    
    last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return JSONResponse(content={
        "last_updated": last_updated,
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

