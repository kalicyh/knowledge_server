from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd
import uuid
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from ..database import SessionLocal, Record, Info
from pydantic import BaseModel
from ..crud import clear_records, add_records, get_records, get_info, update_info, get_records_by_category, get_records_by_category_and_month, get_records_by_full_filter

router = APIRouter()

upload_progress = {}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    upload_id = str(uuid.uuid4())
    upload_progress[upload_id] = {'progress': 0}  # Initialize progress

    file_content = await file.read()
    file_buffer = BytesIO(file_content)

    background_tasks.add_task(process_file, file_buffer, upload_id)

    return {"upload_id": upload_id, "message": "Upload started"}

@router.post("/overwrite_upload")
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

@router.get("/progress/{upload_id}")
async def get_progress(upload_id: str):
    progress = upload_progress.get(upload_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Upload ID not found")
    return progress

def process_file(file_buffer: BytesIO, upload_id: str):
    df = pd.read_excel(file_buffer)
    df.columns = df.columns.str.strip()
    df['月份'] = df['月份'].fillna('未设置')
    df['分类'] = df['分类'].fillna('未分类')

    total_rows = len(df)
    records = []
    chunk_size = 50

    for index, row in df.iterrows():
        records.append(
            Record(
                name=row['名字'],
                month=row['月份'],
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

@router.get("/data")
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
                "月份": record.month,
                "分类": record.category,
                "文案": record.text
            }
            for record in records
        ]
    })

@router.get("/info")
async def get_infos():
    db = SessionLocal()
    info_record = get_info(db)
    if not info_record:
        db.close()
        return JSONResponse(content={
            "total_rows": "0",
            "last_updated": "暂无数据",
        }, status_code=200)
    
    name_categories = db.query(Record.name).distinct().all()
    db.close()
    
    name_categories = [category[0] for category in name_categories]
    
    return JSONResponse(content={
        "last_updated": info_record.last_updated,
        "total_rows": info_record.total_rows,
        "name_categories": name_categories
    })

class FilterRequest(BaseModel):
    category: Optional[str] = None
    month: Optional[str] = None
    name: Optional[str] = None

@router.post("/filter")
async def get_filter_data(filter_request: FilterRequest) -> Dict[str, Any]:
    db = SessionLocal()  # 创建数据库会话
    try:
        category = filter_request.category
        month = filter_request.month
        name = filter_request.name

        if category and not month and not name:
            # 仅通过 category 返回 month
            records = get_records_by_category(db, category)
            months = set()
            for record in records:
                if record.month:
                    # 分割逗号分隔的月份并添加到集合中
                    months.update(record.month.split(','))
            # 将集合转换为列表并返回
            return {"months": sorted(list(months))}

        if category and month and not name:
            # 通过 category 和 month 返回 name
            records = get_records_by_category_and_month(db, category, month)
            names = list(set(record.name for record in records if record.name))
            return {"names": names}

        if category and month and name:
            # 通过 category, month 和 name 返回 text
            records = get_records_by_full_filter(db, category, month, name)
            texts = [record.text for record in records if record.text]
            return {"texts": texts}

        # 如果没有匹配的条件，则返回空结果或适当的错误信息
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    finally:
        db.close()  # 确保会话关闭'

class NameRequest(BaseModel):
    name: str

@router.post("/get-details-by-name")
async def get_details_by_name(name_request: NameRequest) -> Dict[str, Any]:
    db = SessionLocal()
    try:
        # 根据 name 查询记录
        records = db.query(Record).filter(Record.name.ilike(f"%{name_request.name}%")).all()
        
        if not records:
            raise HTTPException(status_code=404, detail="No records found")

        names = list(set(record.name for record in records if record.name))
        return {"names": names}
    finally:
        db.close()
