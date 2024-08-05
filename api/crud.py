from sqlalchemy.orm import Session
from .database import Record, Info
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
