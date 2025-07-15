from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Kara API is live!"}

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit=limit)

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    result = crud.get_channel_activity(db, channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

@app.get("/api/search/messages", response_model=List[schemas.MessageSearch])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)
