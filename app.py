from fastapi import FastAPI
from config import engine
import router
import models
import users
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
# Instrumentator().instrument(app).expose(app)

models.Base.metadata.create_all(bind=engine)

app.include_router(router.router)
app.include_router(users.router)