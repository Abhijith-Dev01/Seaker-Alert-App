from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException
from starlette import status
from schemas import *
from models import *
from datetime import timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from db import db_dependency
from auth import authenticate_user,create_access_token,user_dependency

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


router = APIRouter(
    prefix='/api/user',
)
        


@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,user_request:UserSchema):
    
    if user_request.role not in ['Admin','User']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User role has only 2 choices - Admin and User')
    
            
    existing_user = db.query(User).filter(
                    (User.username==user_request.username)|
                    (User.email==user_request.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with same username or email already exists')
    
    db_user = User(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        username=user_request.username,
        password=bcrypt_context.hash(user_request.password),  # Assuming password is hashed already
        role=user_request.role)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Optionally, get the updated instance from the DB

    return {"message": "User created successfully", "user": db_user}
    




@router.post('/token/',response_model=Token)
def login_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                       db:db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    token = create_access_token(user.username,user.id,user.role,user.first_name,
                                timedelta(minutes=20))
    
    return {"access_token":token,'token_type':'bearer'}

    
@router.get('login/',status_code=status.HTTP_200_OK)
async def user(user:user_dependency):
    if user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "Authentication failed")
    return {'User':user}


@router.get('/',status_code=status.HTTP_200_OK)
async def user_list(db:db_dependency,skip:int=0,limit:int=100):
    user = db.query(User).offset(skip).limit(limit).all()    
    user_schema =[UserSchema.from_orm(info) for info in user]
    return user_schema