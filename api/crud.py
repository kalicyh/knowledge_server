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