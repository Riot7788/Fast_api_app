from fastapi import FastAPI
from src.database import Base, engine


app = FastAPI(title="Library")

# Импорт моделей здесь
from src import models

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Library start"}

