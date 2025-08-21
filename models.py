from sqlalchemy import (Column,String,Integer,CheckConstraint,
                        Float,JSON,DateTime,func,Interval)
from config import Base

class User(Base):
    __tablename__='user'
    role_choices = ('Admin','User')
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String,unique=True)
    email = Column(String,unique=True)
    password = Column(String)
    role = Column(String,nullable=False)
    
    __tableargs__ =(CheckConstraint(f"role in {role_choices}",
                                    name='valid_role_check'))
    
class Metrics(Base):
    __tablename__='metrics'
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    cpu_usuage = Column(Float)
    disk_percentage = Column(Float)
    disk_used = Column(Float)
    disk_total = Column(Float)
    memory_percentage = Column(Float)
    memory_used = Column(Float)
    memory_total = Column(Float)
    up_time = Column(Interval)
    temperature = Column(JSON)
    ts = Column(DateTime(timezone=True), server_default=func.now())

class thresholdSetting(Base):
    __tablename__ = 'threshold_settings'
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    metric_name = Column(String)
    threshold= Column(Float)
    
    
class Alerts(Base):
    __tablename__='alerts'
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    metric_name = Column(String)
    value = Column(String)
    threshold= Column(Float)
    ts= Column(DateTime(timezone=True), server_default=func.now())
    