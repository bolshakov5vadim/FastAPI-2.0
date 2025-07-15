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
    
    try:
        # Запрос к БД
        if(data["page"]): person = await db.query(Person).limit(10).offset((data["page"] - 1) * 10).all()
        if(data["status"]): person = await db.query(Person).filter(Person.status == data["status"])
    except Exception as e:  # Откат на случай исключений
        logger.info(f"ERROR in reading: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # Если пользователь найден, отправляем его
    if person==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    logger.info(f"Data requested for id: {person.id}")
    return person


@app.get(f"/api/{id}")
async def read(id: int, db: Session = Depends(get_db)):
    
    try:
        # Запрос к БД
        person = await db.query(Person).filter(Person.id == id).first() 
    except Exception as e:  # Откат на случай исключений
        logger.info(f"ERROR in reading: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # Если пользователь найден, отправляем его
    if person==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    logger.info(f"Data requested for id: {person.id}")
    return person
  
  
@app.post("/api")
async def create(data  = Body(), db: Session = Depends(get_db)):

    # Запрос к БД
    # Если используется auto-increment, не нужно отправлять id 
    person = Person(name=data["name"], surname=data["surname"], birthday=data["birthday"], status=data["status"])

    try:
        db.add(person)
        await db.commit()
        db.refresh(person)
        logger.info(f"Data posted")
        return person
    except Exception as e:  # Откат на случай исключений
        await db.rollback()
        logger.info(f"ERROR in creation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api")
async def update(data  = Body(), db: Session = Depends(get_db)):
   
    person = await db.query(Person).filter(Person.id == data["id"]).first() # Запрос

    # Если пользователь найден, обновляем его
    if person == None: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})

    # Если поле заполнено, обновляем только его
    if(data["name"]): person.name = data["name"]
    if(data["surname"]): person.surname = data["surname"]
    if(data["birthday"]): person.surname = data["birthday"]
    if(data["status"]): person.status=data["status"]

    try:
        await db.commit()
        db.refresh(person)
        logger.info(f"Data updated for id: {person.id}")
        return person
    except Exception as e:  # Откат на случай исключений
        await db.rollback()
        logger.info(f"ERROR in updating: {e}")
        raise HTTPException(status_code=500, detail=str(e))

  
@app.delete("/api")
async def delete(data  = Body(), db: Session = Depends(get_db)):

    if(data["status"]): person = await db.query(Person).filter(Person.status == data["status"]) # Запрос

    if person == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
   
    # Если пользователь найден, удаляем его

    try:
        db.delete(person)
        await db.commit()
        logger.info(f"Data deleted for id: {person.id}")
        return person
    except Exception as e:  # Откат на случай исключений
        await db.rollback()
        logger.info(f"ERROR in deletion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete(f"/api/{id}")
async def delete(id: int, db: Session = Depends(get_db)):

    person = await db.query(Person).filter(Person.id == id).first() # Запрос

    if person == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
   
    # Если пользователь найден, удаляем его

    try:
        db.delete(person)
        await db.commit()
        logger.info(f"Data deleted for id: {person.id}")
        return person
    except Exception as e:  # Откат на случай исключений
        await db.rollback()
        logger.info(f"ERROR in deletion: {e}")
        raise HTTPException(status_code=500, detail=str(e))