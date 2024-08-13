from sqlalchemy.orm import Session
from .database import Record, Info, Number, NumberInfo
import datetime

def get_records(db: Session):
    return db.query(Record).all()

def get_info(db: Session):
    return db.query(Info).first()

def clear_records(db: Session):
    db.query(Record).delete()
    db.commit()

def add_records(db: Session, records):
    db.add_all(records)
    db.commit()

def update_info(db: Session, total_rows: int):
    info_record = db.query(Info).first()
    if info_record:
        info_record.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_record.total_rows = total_rows
    else:
        new_info = Info(
            last_updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_rows=total_rows
        )
        db.add(new_info)
    db.commit()


def get_numbers(db: Session):
    return db.query(Number).all()

def get_numbers_info(db: Session):
    return db.query(NumberInfo).first()

def clear_numbers(db: Session):
    db.query(Number).delete()
    db.commit()

def add_numbers(db: Session, numbers):
    db.add_all(numbers)
    db.commit()

def update_numbers_info(db: Session, total_rows: int):
    numbers_info = db.query(NumberInfo).first()
    if numbers_info:
        numbers_info.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        numbers_info.total_rows = total_rows
    else:
        new_info = NumberInfo(
            last_updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_rows=total_rows
        )
        db.add(new_info)
    db.commit()

def get_records_by_category(db: Session, category: str):
    # 模糊匹配 category 字段
    return db.query(Record).filter(Record.category.like(f'%{category}%')).all()

def get_records_by_category_and_month(db: Session, category: str, month: str):
    # 模糊匹配 category 和 month 字段
    return db.query(Record).filter(
        Record.category.like(f'%{category}%'),
        Record.month.like(f'%{month}%')
    ).all()

def get_records_by_full_filter(db: Session, category: str, month: str, name: str):
    # 模糊匹配 category, month 和 name 字段
    return db.query(Record).filter(
        Record.category.like(f'%{category}%'),
        Record.month.like(f'%{month}%'),
        Record.name.like(f'%{name}%')
    ).all()

def update_version_filename(db: Session, filename: str):
    version_info = db.query(Info).first()
    if version_info:
        version_info.client_filename = filename
    else:
        new_info = Info(
            client_filename=filename
        )
        db.add(new_info)
    db.commit()

def update_version_info(db: Session, version: str):
    version_info = db.query(Info).first()
    if version_info:
        version_info.client_versions = version
    else:
        new_info = Info(
            client_versions=version
        )
        db.add(new_info)
    db.commit()
