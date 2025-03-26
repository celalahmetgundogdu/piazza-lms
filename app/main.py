from fastapi import FastAPI
from . import models
from .database import engine
from .routes import users, courses, questions
from .routes import users, courses, questions, answers

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

# Uygulamayı başlat
app = FastAPI()

# Tüm router'ları dahil et
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(questions.router)
app = FastAPI()
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(questions.router)
app.include_router(answers.router)
