# SQLAlchemy'den gerekli kolon ve veri türü sınıflarını içe aktar
from sqlalchemy import Column, Integer, String, Text

# Base sınıfını database.py dosyasından içe aktar
from .database import Base

# User sınıfı veritabanındaki "users" tablosunu temsil eder
class User(Base):
    __tablename__ = "users"  # Bu sınıfın karşılık geldiği tablo adı

    # Kolonlar (alanlar) tanımlanıyor
    id = Column(Integer, primary_key=True, index=True)  # Primary key, otomatik artan
    name = Column(Text, nullable=False)                 # Kullanıcının adı
    email = Column(Text, unique=True, nullable=False)   # E-posta adresi, benzersiz
    password_hash = Column(Text, nullable=False)        # Şifre (hashlenmiş şekilde tutulmalı)
    role = Column(String, nullable=False)               # Kullanıcı rolü: student, instructor, admin


from sqlalchemy import ForeignKey

# Course modeli, dersleri temsil eder
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)


from sqlalchemy import DateTime, func

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime
# En alta ekle:
class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    question = relationship("Question", backref="answers")
    user = relationship("User", backref="answers")
