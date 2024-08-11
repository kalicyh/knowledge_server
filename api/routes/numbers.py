from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd
import uuid
from sqlalchemy.orm import Session
from ..database import SessionLocal, Number,NumberInfo
from ..crud import clear_numbers, add_numbers, get_numbers, get_numbers_info, update_numbers_info

router = APIRouter()

upload_progress = {}

@router.post("/upload", tags=["号码接口"], description="号码新增接口")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}

    file_content = await file.read()
    file_buffer = BytesIO(file_content)

    background_tasks.add_task(process_file, file_buffer, upload_id)

    return {"upload_id": upload_id, "message": "Upload started"}

@router.post("/overwrite_upload", tags=["号码接口"], description="号码覆盖接口")
async def overwrite_upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}

    db = SessionLocal()
    try:
        clear_numbers(db)
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

@router.get("/progress/{upload_id}", tags=["号码接口"], description="号码上传进度接口")
async def get_progress(upload_id: str):
    progress = upload_progress.get(upload_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Upload ID not found")
    return progress

def process_file(file_buffer: BytesIO, upload_id: str):
    df = pd.read_excel(file_buffer)
    df.columns = df.columns.str.strip()

    total_rows = len(df)
    numbers = []
    chunk_size = 50

    for index, row in df.iterrows():
        numbers.append(
            Number(
                category=row['工作站'],
                text=row['好友ID']
            )
        )

        if (index + 1) % chunk_size == 0 or (index + 1) == total_rows:
            db = SessionLocal()
            try:
                add_numbers(db, numbers)
                progress = round((index + 1) / total_rows * 100, 2)
                upload_progress[upload_id] = {
                    'progress': progress,
                    'current_row': index + 1,
                    'total_rows': total_rows
                }
                numbers = []
            except Exception as e:
                db.rollback()
                upload_progress[upload_id]['message'] = f"上传错误: {str(e)}"
                raise e
            finally:
                db.close()

    if numbers:
        db = SessionLocal()
        try:
            add_numbers(db, numbers)
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
        update_numbers_info(db, total_rows)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@router.get("/data", tags=["号码接口"], description="获取号码接口")
async def get_data():
    db = SessionLocal()
    numbers = get_numbers(db)
    db.close()

    return JSONResponse(content={
        "total_numbers": len(numbers),
        "numbers": [
            {
                "序号": number.id,
                "分类": number.category,
                "联系方式": number.text
            }
            for number in numbers
        ]
    })

@router.get("/info", tags=["号码接口"], description="获取号码信息接口")
async def get_numbers_infos():
    db = SessionLocal()
    info_number = get_numbers_info(db)
    if not info_number:
        db.close()
        return JSONResponse(content={
            "total_rows": "0",
            "last_updated": "暂无数据",
        }, status_code=200)
    
    db.close()
    
    return JSONResponse(content={
        "last_updated": info_number.last_updated,
        "total_rows": info_number.total_rows
    })
