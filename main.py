from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from database.database import DBServerWrites

from sqlalchemy.orm import Session
from schemas import room_schemas as schemas
from crud import crud

app = FastAPI()

try:
    DBServerWrites.Base.metadata.create_all(bind=DBServerWrites.engine)
except Exception as e:
    print(e)

#Dependency
def get_db():
    db = DBServerWrites.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/v1/facility", response_model=list[schemas.FasilitasLayananKesehatan])
async def get_fasilitas_layanan_kesehatan(skip: int = 0, limit: int = 100, db : Session= Depends(get_db)):
    facilities = crud.get_fasilitas_layanan_kesehatan_all(db, skip=skip, limit=limit)
    if facilities is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facilities

@app.get("/api/v1/facility/{facility_id}", response_model=schemas.FasilitasLayananKesehatan)
async def get_fasilitas_layanan_kesehatan(
    facility_id: str, 
    db: Session = Depends(get_db)
    ) -> schemas.FasilitasLayananKesehatan :
    facility = crud.get_fasilitas_layanan_kesehatan(db, facility_id)
    return facility

@app.post("/api/v1/facility", response_model=schemas.FasilitasLayananKesehatan)
async def create_fasilitas_layanan_kesehatan(
    facility: schemas.FasilitasLayananKesehatanCreate, 
    db: Session = Depends(get_db)
    ) -> schemas.FasilitasLayananKesehatan :
    return crud.create_fasilitas_layanan_kesehatan(db, facility)