from SQLsession import SessionLocal, Person
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
import logging


# Создание объекта логирования
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s-%(name)s-%(levelname)s-%(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# API + описание 4-х действий
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
   

@app.get("/api")
async def read(data  = Body(), db: Session = Depends(get_db)):
    
    # Запрос к БД
    if(data["page"]): person = await db.query(Person).limit(10).offset((data["page"] - 1) * 10).all()
    if(data["id"]): person = await db.query(Person).filter(Person.id == data["id"]).first() 

    if person==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    # Если пользователь найден, отправляем его
    logger.info(f"Data requested for id: {person.id}")
    return person
  
  
@app.post("/api")
async def create(data  = Body(), db: Session = Depends(get_db)):

    # Запрос к БД
    # Если используется auto-increment, то не нужно отправлять id 
    person = Person(name=data["name"], surname=data["surname"], birthday=data["birthday"], status=data["status"])

    try:
        db.add(person)
        db.commit()
        db.refresh(person)
        logger.info(f"Data posted")
        return person
    except Exception as e:
        db.rollback()  # Откат на случай исключений
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api")
async def update(data  = Body(), db: Session = Depends(get_db)):
   
    person = await db.query(Person).filter(Person.id == data["id"]).first() # Запрос

    if person == None: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    # Если пользователь найден, обновляем его

    # Если поле заполнено, обновляем только его
    if(data["name"]): person.name = data["name"]
    if(data["surname"]): person.surname = data["surname"]
    if(data["birthday"]): person.surname = data["birthday"]
    if(data["status"]): person.status=data["status"]

    try:
        db.commit()
        db.refresh(person)
        logger.info(f"Data updated for id: {person.id}")
        return person
    except Exception as e:
        db.rollback()  # Откат на случай исключений
        raise HTTPException(status_code=500, detail=str(e))

  
@app.delete("/api")
async def delete(data  = Body(), db: Session = Depends(get_db)):

    if(data["id"]): person = await db.query(Person).filter(Person.id == data["id"]).first() # Запрос
    if(data["status"]): person = await db.query(Person).filter(Person.status == data["status"]) # Запрос

    if person == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
   
    # Если пользователь найден, удаляем его

    try:
        db.delete(person)
        db.commit()
        logger.info(f"Data deleted for id: {person.id}")
        return person
    except Exception as e:
        db.rollback()  # Откат на случай исключений
        raise HTTPException(status_code=500, detail=str(e))