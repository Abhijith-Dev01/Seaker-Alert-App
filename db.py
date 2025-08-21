from config import sessionLocal
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import Depends

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)] 