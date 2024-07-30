from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import mysql.connector
from io import BytesIO
import datetime
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
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Set as auto-increment
    name = Column(String(255), index=True)  # Specify a length for VARCHAR
    category = Column(String(255), nullable=True)
    text = Column(String(5000))  # Adjust length based on your needs

Base.metadata.create_all(bind=engine)

# Serve static files
app.mount("/dist", StaticFiles(directory="dist"), name="dist")

@app.get("/")
def root():
    return FileResponse('dist/index.html')

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    df = pd.read_excel(BytesIO(await file.read()))
    df.columns = df.columns.str.strip()
    df['分类'] = df['分类'].fillna('未分类')
    print(df.columns)
    print(df.head())
    
    # Remove '序号' processing
    records = [
        Record(
            name=row['名字'],
            category=row['分类'],
            text=row['文案']
        )
        for index, row in df.iterrows()
    ]
    
    db = SessionLocal()
    db.add_all(records)
    db.commit()
    db.close()

    return {"message": "File uploaded and data added to database"}

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
