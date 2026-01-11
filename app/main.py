from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routes.auth import router as auth_router
from app.routes.users import router as user_router

import os

app = FastAPI(
    title="Memosafe Gallery",
    description="A simple Social app for uploading profile pictures",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(user_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("Database tables created(or already exist).")


app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": "Memosafe Gallary"}

@app.get("/")
def root():
    return {"message": "Welcome to Memosafe Gallery API! Visit /docs for Swagger UI"}

