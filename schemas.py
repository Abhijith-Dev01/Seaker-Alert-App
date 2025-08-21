from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Optional,List,TypeVar,Dict,Any
from datetime import datetime,timedelta

class UserSchema(BaseModel):
    id : Optional[int]=None
    first_name :str
    last_name :str
    username :str
    email :str
    password :str
    role :str
    
    class Config:
        orm_mode = True
        from_attributes = True

class metricsSchema(BaseModel):
    id : Optional[int]=None
    cpu_usuage :float
    disk_percentage :float
    disk_used :float
    disk_total :float
    memory_percentage :float
    memory_used :float
    memory_total :float
    up_time :timedelta
    temperature : Dict[str,Any]
    ts: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        

class thresholdSettingSchema(BaseModel):
    id : Optional[int]=None
    metric_name : str
    threshold : float
    
    class Config:
        orm_mode = True
        from_attributes = True
    
class alertsSchema(BaseModel):
    id : Optional[int]=None
    metric_name: str
    value: float
    threshold: float
    ts: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True
    
T = TypeVar('T')  
   
class Response(GenericModel):
    code : str
    status : int
    message : str
    result : List[T]
    

class  PostResponse(BaseModel):
    code : str
    status : int
    message : str

class Token(BaseModel):
    access_token:str
    token_type:str