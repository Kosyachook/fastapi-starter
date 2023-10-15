from fastapi import FastAPI
from core.settings import settings
 
from data.base import Base
from apis.base import api_router


def include_router(app):
     app.include_router(api_router)
       

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    
    include_router(app)
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg":"Hello FastAPI🚀"}
