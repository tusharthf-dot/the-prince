from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models.user
from routers import analyze, socratic

Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Prince")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(socratic.router)

@app.get("/")
def root():
    return {"message": "The Prince is alive"}