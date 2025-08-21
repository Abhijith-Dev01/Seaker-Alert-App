from models import *
from typing_extensions import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi import APIRouter,Depends,HTTPException
from starlette import status

SECRET_KEY = '1d1v4sa4SA4d5asdas54dds4a'
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def authenticate_user(username:str,password:str,db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=400,detail ='Username is incorrect')
    if not bcrypt_context.verify(password,user.password):
        raise HTTPException(status_code=400,detail ='Password is incorrect')
    return user

def create_access_token(username:str,id:int,role:str,first_name:str,expires_delta:timedelta):
    encode = {'sub':username,'id':id,'role':role,'first_name':first_name}
    expires = datetime.utcnow() + expires_delta
    encode.update({"expires":expires.isoformat()})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        role:str = payload.get('role')
        first_name:str = payload.get('first_name')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "could not validate user")
        
        return {'username':username,'user_id':user_id,'role':role,
                'first_name':first_name}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "could not validate user")

user_dependency = Annotated[dict,Depends(get_current_user)]