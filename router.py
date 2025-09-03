from fastapi import APIRouter,HTTPException,BackgroundTasks
from starlette import status
from models import * 
from schemas import * 
from db import db_dependency
from auth import user_dependency
import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from config import sessionLocal
import datetime
from utils import send_email

router = APIRouter(prefix='/api')
scheduler = BackgroundScheduler()

def alert_creation(metric_name:str,threshold:float,value:float):
    db = sessionLocal()
    db_alerts = Alerts(metric_name=metric_name, threshold=threshold, 
                       value=value)
    db.add(db_alerts)
    db.commit()
    db.close()
    
def metrics_insertion():
    print("check working or not")
    db = sessionLocal()
    boot_time = psutil.boot_time()
    disk_usage =  psutil.disk_usage('/')
    memory  = psutil.virtual_memory()
    temps = psutil.sensors_temperatures()
    if temps:
        temps_json = {}
        for name, entries in temps.items():
            for entry in entries:
                if entry.label:
                    temps_json.update({str(entry.label):str(entry.current)+"C"})
                else:
                      temps_json.update({str(name):str(entry.current)+"C"})
        
    metric_data ={
        "cpu_usuage" : psutil.cpu_percent(interval=1),
        "disk_percentage" : disk_usage.percent,
        "disk_used" : round(disk_usage.used/(1024**3),2),
        "disk_total" : round(disk_usage.total/(1024**3),2),
        "memory_percentage":memory.percent,
        "memory_used" : round(memory.used/(1024**3),2),
        "memory_total": round(memory.total/(1024**3),2),
        "temperature" :temps_json,
        "up_time" : datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    }
    db_metric = Metrics(**metric_data)
    db.add(db_metric)
    db.commit()
    db.close()
    
    #Logic for alerts
    threshold_query = db.query(thresholdSetting).all()
    threshold_data = [thresholdSettingSchema.from_orm(info) for info in threshold_query]
    emails = db.query(User.email).offset(0).limit(100).all()    
    email_list = [email[0] for email in emails]
    for info in threshold_data:
        info= info.dict()
        #cpu usuage
        if (info['metric_name'] == 'cpu_usuage' and 
         metric_data['cpu_usuage']>= info['threshold']):
            #alert post
            alert_creation('cpu_usuage',metric_data['cpu_usuage'],
                           info['threshold'])
            #email send
            send_email(recipient=email_list,
                       subject='CPU Usage Alert',
                    body=str(metric_data))
            
        #disk usuage
        if (info['metric_name'] == 'disk_percentage' and 
         metric_data['disk_percentage']>= info['threshold']):
            #alert post
            alert_creation('disk_percentage',metric_data['disk_percentage'],
                           info['threshold'])
            #email send
            send_email(recipient=email_list,
                       subject='Disk Usage Alert',
                    body=str(metric_data))
             
          
        if (info['metric_name'] == 'memory_percentage' and 
         metric_data['memory_percentage']>= info['threshold']):
            #alert post
            alert_creation('memory_percentage',metric_data['memory_percentage'],
                           info['threshold'])
            #email send
            send_email(recipient=email_list,
                       subject='M/Y Usage Alert',
                    body=str(metric_data))

def start_scheduler():
    if not scheduler.running: 
        scheduler.add_job(metrics_insertion,'interval',minutes=1)
        scheduler.start()


@router.on_event("startup")
def startup_event():
    start_scheduler()
    
    
@router.get('/metrics',status_code=status.HTTP_200_OK)
async def get_metrics(db:db_dependency):
    query = db.query(Metrics).all()
    metrics_schema = [metricsSchema.from_orm(info) for info in query]
    return metrics_schema


@router.post('/threshold_settings',status_code=status.HTTP_201_CREATED)
async def post_threshold(db:db_dependency,user:user_dependency,
                         threshold_request:thresholdSettingSchema):
    
    if user['role'] != 'Admin':
        raise HTTPException(status_code=400,
            detail =f"Only Admin can create threshold settings")
        
    metric_choices = ["cpu_usuage","disk_percentage","memory_percentage"]
    
    if threshold_request.metric_name not in metric_choices :
        raise HTTPException(status_code=400,
            detail =f"{threshold_request.metric_name} not in{metric_choices}")
        
    threshold_data = db.query(thresholdSetting).filter(
                    thresholdSetting.metric_name == threshold_request.metric_name).first()
    
    if threshold_data:
        raise HTTPException(status_code=400,
            detail =f"{threshold_request.metric_name} metric name is already there") 
        
        
    threshold = thresholdSetting(
            metric_name=threshold_request.metric_name,
            threshold = threshold_request.threshold)
    
    db.add(threshold)
    db.commit()
    db.refresh(threshold)
    
    return {"message": "Threshold Setting created successfully",
            "threshold":threshold }


@router.patch('/threshold_settings',status_code=status.HTTP_202_ACCEPTED)
async def patch_threshold (db:db_dependency,user:user_dependency,
                           threshold_id:int,
                           threshold_request:thresholdSettingSchema):
     
    if user['role'] != 'Admin':
        raise HTTPException(status_code=400,
            detail =f"Only Admin can edit threshold settings")
        
    threshold = db.query(thresholdSetting).filter(id==threshold_id).first()
    
    if not threshold:
        raise HTTPException(status_code=400,detail='Threshold not found')
    
    
    metric_choices = ["cpu_usuage","disk_percentage","memory_percentage"]
    
    
    if threshold_request.metric_name is not None:
        if threshold_request.metric_name not in metric_choices :
            raise HTTPException(status_code=400,
            detail =f"{threshold_request.metric_name} not in{metric_choices}")
        else:
            threshold.metric_name= threshold_request.metric_name
            
            
    if threshold_request.threshold is not None:
        threshold.threshold = threshold_request.threshold
    
    db.commit()
    db.refresh(threshold)
    
    return {"message":"Threshold setting updated successfully",
            "threshold":threshold}


@router.get('/threshold_settings',status_code=status.HTTP_200_OK)
async def get_thresholds(db:db_dependency):
    query = db.query(thresholdSetting).all()
    threshold_schema = [thresholdSettingSchema.from_orm(info) for info in query]
    return threshold_schema
